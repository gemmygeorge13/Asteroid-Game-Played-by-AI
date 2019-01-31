# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 08:36:04 2019

@author: 91961
"""

import pygame

from src.Config import Config

class Obstacle:
    def __init__(self, display, delta):
        self.x_pos = (Config['game']['width'])/2
        self.y_pos = 600
        self.display = display
        self.i = 1;

    def draw(self):
        pygame.draw.rect(
            self.display, 
            Config['colors']['red'],
            [
                self.x_pos,
                self.y_pos,
                Config['snake']['height'],
                Config['snake']['width']
            ]
        )
        self.y_pos -= self.y_pos
        if self.y_pos <= -50 :
            self.y_pos = 600

