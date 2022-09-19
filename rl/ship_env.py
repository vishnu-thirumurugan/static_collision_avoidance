# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:57:49 2022

@author: oe21s024
"""


# importing required dependencies

import os
import pickle 
import numpy as np
import gym
from gym import Env 
from gym import spaces, error, utils
from gym.utils import seeding 


# rendering colour specificaions - normalized 

colours = {0: [0,0,0], 1:[0.5,0.5,0.5], 2: [0,0,1], 3: [0,1,0], 4: [1,0,0], 5:[1,0,1], 6:[1,1,0], 8: [1,1,1]}


class Environment(Env):
    
    metadata = {'render.modes' : ['human', 'rgb_array'], 'video.frames_per_second' : 60}

    def __init__(self, wave = True, end = 0):
        
        # action_set
        self.actions = np.array([0,1,2,3,4]) # these will be rudder angles 
        self.rewards = np.ones((800,600))
        self.start   = np.array([400,30])    # ship starts from this coordinate
        self.goal    = np.array([400,570])   # 
        
        
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
        
        