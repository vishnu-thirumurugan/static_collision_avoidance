# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 14:35:16 2022

@author: oe21s024
"""

import pygame
from base import RRTGraph
from base import RRTMap


def main():
    dimensions = (600, 1000)
    start = (50, 50)
    goal = (510, 510)
    obsdim = 30
    obsnum = 50
    
    # pygame initialization
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)
    
    obstacles = graph.makeobs()
    
    map.drawMap(obstacles)
    
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)
    

if __name__ == '__main__':
    main()
    