# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:57:49 2022
@author: oe21s024
I have explained each and every line of the code to make it clean and elegant for the user
"""


# importing required dependencies

import os
import pickle 
import numpy as np
import gym
from gym import Env 
from gym import spaces, error, utils
from gym.utils import seeding 


# rendering colour specificaions - normalized rgb colours 

colours = {0: [0,0,0], 1:[0.5,0.5,0.5], 2: [0,0,1], 3: [0,1,0], 4: [1,0,0], 5:[1,0,1], 6:[1,1,0], 8: [1,1,1]}


class Environment(Env):

    ''' The state space and action space both are discrete
    So we define obstcales and goal point in terms of rewards'''


    metadata = {'render.modes' : ['human', 'rgb_array'], 'video.frames_per_second' : 60}

    def __init__(self, wave = True, end = 0):

        ''' This function initializes 
            1. the set of actions
            2. start and goal coordinate 
            3. obstacle coordinates for n obstacles 
            4. left and right shore boundaries 
            5. ship navigation area (water surface)
        '''

        # action_set
        self.actions = np.array([0,1,2,3,4]) # these will be rudder angles 

        # start and end points 
        self.start   = np.array([400,30])    # ship starts from this coordinate
        self.goal    = np.array([400,570])   # ship should reach this coordinate

        # reward function
        self.rewards = np.ones((800,600)) # reward function is defined as a grid

        # rendering
        self.viewer = None 

        # individual actions 
        self.act0 = self.actions[0]
        self.act1 = self.actions[1]
        self.act2 = self.actions[2]
        self.act3 = self.actions[3]
        self.act4 = self.actions[4]

        # other initializations
        self.wave = wave 
        self.end  = end 



        # creating list to store the coordinates of obstacles 
        obstacle1 = []
        obstacle2 = []
        obstacle3 = []
        obstacle4 = []


        # obstacles definition in terms of rewards 
        # obstacle 1
        for i in range(1,101):
            for j in range(1, 51):
                self.rewards[300 + i][200 + j] = -1000
                obstacle1.append((300 + i, 200 + j))


        # obstacle 2 
        for i in range(1,101):
            for j in range(1,51):
                self.rewards[400 + i][450 + j] = -1000
                obstacle2.append((400 + i, 450 + j))

        # obstacle 3
        for i in range(1,101):
            for j in range(1,51):
                self.rewards[350 + i][325 + j] = -1000
                obstacle3.append((350 + i, 325 + j))

        # obstacle 4 
        for i in range(1,101):
            for j in range(1,51):
                self.rewards[400 + i][100 + j] = -1000
                obstacle4.append((400 + i, 100 + j))

        # converting list of obstacle coordinates to array
        self.obstacle1 = np.array((obstacle1))
        self.obstacle2 = np.array((obstacle2))
        self.obstacle3 = np.array((obstacle3))
        self.obstacle4 = np.array((obstacle4))


        # creating list to store the coordinates of left and right land 
        left_shore  = []
        right_shore = []

        # left shore collision reward 
        for i in range(0,201):
            for j in range(0,601):
                self.rewards[0 + i][0 + j] = -1000
                left_shore.append((0 + i, 0 + j))


        # right shore collision reward
        for i in range(600, 801):
            for j in range(0, 601):
                self.rewards[600 + i][0 + j] = -1000
                right_shore.append((600 + i, 0 + j))

        # converting list of land coordinates into array of land coordinates
        self.left_shore  = np.array((left_shore))
        self.right_shore = np.array((right_shore))


        # defining goal points with reward
        self.Goal = self.goal
        self.rewards[400][570] = 1000


        def seed(self, seed = None):
            self.np_random, seed = seeding.np_random(seed)
            return [seed]

        def reset(self):
            ''' This function resets the ship's position to the coordinate (400,30).
                It happens when the learning is terminated or completed.
                This function returns current state of ship, after resetting its position
            '''
            self.current_state = [400,30]
            self.done          = False
            return self.current_state
        
        
        def step(self, action):
            self.next_state = np.copy(self.current_state)
            self.done       = False 
            self._          = 'in water'
            
            if np.random.randint > 0.9 :
                temp = np.random.randint(0, 5)
                if temp >= action:
                    action = temp + 1
                 
            if action == 0 :
                self.next_state[0] = max(self.current_state[0] - 2, 200)
                self.next_state[1] = min(self.current_state[1] + 1, 570)
                
            if action == 1 :
                self.next_state[0] = max(self.current_state[0] - 1, 200)
                self.next_state[1] = min(self.current_state[1] + 1, 570)
                
            if action == 2 :
                self.next_state[0] = max(self.current_state[0] + 0, 200)    # no movement of ship in x direction
                self.next_state[1] = min(self.current_state[1] + 1, 570)
                
            if action == 3 :
                self.next_state[0] = min(self.current_state[0] + 1, 200)
                self.next_state[1] = min(self.current_state[1] + 1, 570)
                
            if action == 4 :
                self.next_state[0] = min(self.current_state[0] + 2, 200)
                self.next_state[1] = min(self.current_state[1] + 1, 570)
                
        pass
                    
        def action_space_sampling(self):
            ''' This function does random sampling between integers 0 and 5.
                The output of this function is used to take actions defined in the step function.
                In real world, it denotes the rudder angle of the ship.
            '''
            rand = np.random.randint(0,5)
            return rand

        def render(self, mode = 'human'):

            ''' This function generates a screen with width size 800 and height 600. 
                It shows obstacles, ship position, shore on the left and right environments along with navigating water surface. 
                It uses OpenAI gym for rendering.
                It is optional function. 
                If you dont want to see the rendering, you can switch it off at the main file, by commenting the line env.render().
                This function returns the viewer, when the mode is 'rgb_array'
            '''
            screen_width  = 800
            screen_height = 600

            if self.viewer is None:

                # importing screen
                from gym.envs.classic_control import rendering
                self.viewer = rendering.Viewer(screen_width, screen_height)


                # water surface where ship can navigate
                water_area        = rendering.FilledPolygon([(200,0), (600,0), (600,600), (200, 600)])
                self.wa_transform = rendering.Transform()
                water_area.set_color(0.6, 0.9, 0.93)
                water_area.add_attr(self.wa_transform)
                self.viewer.add_geom(water_area)


                # left shore where ship cannot navigate
                left_shore        = rendering.FilledPolygon([(0,0),(200,0),(200,600),(0,600)])
                self.ls_transform = rendering.Transform()
                left_shore.set_color(0.77, 0.38, 0.06)
                left_shore.add_attr(self.ls_transform)
                self.viewer.add_geom(left_shore)

                # right shore, where ship cannot navigate 
                right_shore       = rendering.FilledPolygon([(600,0), (800,0), (800,600), (600,600)])
                self.rs_transform = rendering.Transform()
                right_shore.set_color(0.77,0.38, 0.06)
                right_shore.add_attr(self.rs_transform)
                self.viewer.add_geom(right_shore)

                # obstacle number 1 where ship should not go 
                first_obstacle    = rendering.FilledPolygon([(300,200), (400,200), (400,250), (300,250)])
                self.fo_transform = rendering.Transform()
                first_obstacle.set_color(0.84,0.04,0.33)
                first_obstacle.add_attr(self.fo_transform)
                self.viewer.add_geom(first_obstacle)

                # obstacle number 2 where ship should not go
                second_obstacle   = rendering.FilledPolygon([(400,450), (500,450), (500,500), (400,500)])
                self.so_transform = rendering.Transform()
                second_obstacle.set_color(0.84, 0.04, 0.33)
                second_obstacle.add_attr(self.so_transform)
                self.viewer.add_geom(second_obstacle)

                # obstacle number 3 where ship should not go 
                third_obstacle    = rendering.FilledPolygon([(350,325), (450,325), (450,375), (350,375)])
                self.to_transform = rendering.Transform()
                third_obstacle.set_color(0.84, 0.04,0.33)
                third_obstacle.add_attr(self.to_transform)
                self.viewer.add_geom(third_obstacle)

                # obstcle number 4 where ship should not go
                fourth_obstacle   = rendering.FilledPolygon([(400,100), (500,100), (500,150), (400,150)])
                self.fo_transform = rendering.Transform() 
                fourth_obstacle.set_color(0.84, 0.04, 0.33)
                fourth_obstacle.add_attr(self.fo_transform)
                self.viewer.add_geom(fourth_obstacle)


                # ship rendering 
                ship             = rendering.FilledPolygon([(-4,-7),(0,-3),(4,-7),(4,5),(0,8),(-4,4)])
                self.s_transform = rendering.Transform(translation = (0,15), rotation = 0.0 )
                ship.set_color(0.333, 0.333, 0.333)
                ship.add_attr(self.s_transform)
                self.viewer.add_geom(ship)

                # ship_axle rendering
                ship_axle = rendering.make_circle(2)
                sa = ship_axle 
                sa.set_color(1, 0.75, 0)
                sa.add_attr(self.s_transform)
                self.viewer.add_geom(sa)


                # storing ship_geometry
                self.ship_geometry = ship

                # making the ship to move  in the environment created
                ship_x, ship_y = self.current_state
                ship           = self.ship_geometry
                cart_x, cart_y = 400,15
                self.s_transform.set_translation(ship_x, ship_y)

                return self.viewer.render(return_rgb_array = mode == 'rgb_array')



            def close(self):

                ''' This function closes the rendering screen. 
                    It also sets the viewer to None 
                '''
                if self.viewer:
                    self.viewer.close()
                    self.viewer = None 
