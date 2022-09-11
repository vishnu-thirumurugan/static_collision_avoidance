# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 13:15:27 2022
@author: oe21s024
"""

import pygame 
import math 
import random


class RRTMap:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        
        # start, goal point and map definition 
        self.start           = start
        self.goal            = goal
        self.MapDimensions   = MapDimensions
        self.Maph, self.Mapw = self.MapDimensions
        
        # pygame display settings initialization
        self.MapWindowName   = ' RRT Path Planning '
        pygame.display.set_caption(self.MapWindowName)
        self.map             = pygame.display.set_mode((self.Mapw, self.Maph))
        self.map.fill((255,255,255))
        self.nodeRad         = 2
        self.nodeThickness   = 0
        self.edgeThickness   = 1
        
        # obstacle defenition
        self.obstacles       = []
        self.obsdim          = obsdim 
        self.obsNumber       = obsnum
        
        # colors definition
        self.grey            = (70,70,70)
        self.Blue            = (0, 0, 255)
        self.Green           = (0, 255, 0)
        self.Red             = (255, 0, 0)
        self.white           = (255, 255, 255)
        
    
    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.Green, self.start, self.nodeRad + 5, 0)
        pygame.draw.circle(self.map, self.Red, self.goal, self.nodeRad + 20, 1)
        self.drawObs(obstacles)
   
    def drawPath(self):
        pass
    
    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while(len(obstaclesList)>0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)
            
            
            
    
class RRTGraph:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        (x,y)                = start 
        self.start           = start 
        self.goal            = goal 
        self.goalFlag        = False
        self.maph, self.mapw = MapDimensions
        self.x               = []
        self.y               = []
        self.parent          = []
        
        # initializing the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        
        # obstacle intialization using previous definitions
        self.obstacles       = []
        self.obsDim          = obsdim
        self.obsNum          = obsnum
        
        # storing the path in the memory 
        self.goalstate       = None
        self.path            = []
    
    
    def makeRandomRect(self):
        uppercornerx         = int(random.uniform(0, self.mapw - self.obsDim))
        uppercornery         = int(random.uniform(0, self.maph - self.obsDim))
        return (uppercornerx, uppercornery)
    
    def makeobs(self):
        obs = []
        
        for i in range(0, self.obsNum):
            rectang = None 
            startgoalcol = True 
            while startgoalcol:
                upper = self.makeRandomRect()
                rectang = pygame.Rect(upper, (self.obsDim, self.obsDim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol = True
                else:
                    startgoalcol = False
            obs.append(rectang)
            
        self.obstacles = obs.copy()
        return obs
            
    
    def add_node(self, n, x, y):
        self.x.insert(n, x)
        self.y.append(y)
    
    def remove_node(self, n):
        self.x.pop(n)
        self.y.pop(n)
    
    def add_edge(self, parent, child):
        self.parent.insert(child, parent)
    
    def remove_edge(self, n):
        self.parent.pop(n)
    
    def number_of_nodes(self):
        return len(self.x)
    
    def distance(self,n1,n2): # distance between two nodes 
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        px       = (float(x1) - float(x2))**2
        py       = (float(y1) - float(y2))**2
        return (px + py)**0.5
    
    def sample_envir(self):   # choosing a sample randomly from the envrironment and checking whether it comes under the obstacle area
        x = int(random.uniform(0, self.mapw))
        y = int(random.uniform(0, self.maph))
        return x,y
    
    def nearest(self, n):
        dmin = self.distance(0,n)
        nnear = 0
        for i in range(0,n):
            if self.distance(i,n) < dmin:
                dmin = self.distance(i,n)
                nnear = i
        return nnear
    
    def isFree(self):                        # to check whether randomly generated point collides with obstacle
        n = self.number_of_nodes() - 1
        (x,y) = (self.x[n], self.y[n])
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rectang = obs.pop(0)
            if rectang.collidepoint(x,y):
                self.remove_node(n)
                return False                 # false means the random point is colliding with the obstacle 
        return True                          # true means the randomly generated node is free from obstacle
    
    
    def CrossObstacle(self, x1, x2, y1, y2):
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rectang = obs.pop(0)
            for i in range(0,101):
                u = i/100  # splitting the line between two nodes by 100
                x = x1*u + x2*(1-u)
                y = y1*u + x2*(1-u)
                if rectang.collidepoint(x,y):
                    return True 
        return False
    
    def connect(self, n1, n2):        #connecting two nodes
        (x1, y1)  = (self.x[n1], self.y[n1])
        (x2, y2)  = (self.x[n2], self.y[n2])
        if self.crossObstacle(x1,y1,x2,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1, n2)
            return True
    
    def step(self, nnear, nrand, dmax = 35):     # create a node between 2 nodes 
        d = self.distance(nnear, nrand)
        if d > dmax:
            u = dmax/d
            (xnear, ynear) = (self.x[nnear], self.y[nnear])
            (xrand, yrand) = (self.x[nrand], self.y[nrand])
            (px,py)        = (xrand-xnear, yrand-ynear)
            theta          = math.atan2(py, px)
            
            (x,y)          = (int(xnear + dmax*math.cos(theta) ), int(ynear + dmax*math.sin(theta)))
            self.remove_node(nrand)  # finding a point between two points and then removing nrand, if distance is greater than 35
            
            if  abs(x - self.goal[0]) < 35 and abs(y - self.goal[1]) < 35:
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate = nrand
                self.goalFlag  = True 
            else : 
                self.add_node(nrand, x, y)
                
                
    def path_to_goal(self):
        pass
    
    def getPathCoords(self):
        pass
    
    def bias(self, ngoal):
        n = self.number_of_nodes()
        self.add_node(n, ngoal[0], ngoal[1])
        nnear = self.nearest(n)
        self.step(nnear,n)
        self.connect(nnear, n)
        return self.x, self.y, self.parent
        
    
    def expand(self):
        n = self.number_of_nodes()
        x, y  = self.sample_envir()
        self.add_node(n,x,y)
        if self.isFree():
            xnearest = self.nearest(n)
            self.step(xnearest, n)
            self.connect(xnearest, n)
        return self.x, self.y, self.parent 
    def cost(self):
        pass

