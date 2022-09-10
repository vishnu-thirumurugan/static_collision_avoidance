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
        self.nodeRad         = 0
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
            
    
    def add_node(self):
        pass
    
    def remove_node(self):
        pass
    
    def add_edge(self):
        pass
    
    def remove_edge(self):
        pass
    
    def number_of_nodes(self):
        pass
    
    def distance(self):
        pass
    
    def nearest(self):
        pass
    
    def isFree(self):
        pass
    
    def CrossObstacle(self):
        pass
    
    def connect(self):
        pass
    
    def step(self):
        pass
    
    def path_to_goal(self):
        pass
    
    def getPathCoords(self):
        pass
    
    def bias(self):
        pass
    
    def expand(self):
        pass
    
    def cost(self):
        pass