# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:05:53 2019

@author: Gemmy George
"""

import pygame 
from sys import exit
from src.Config import Config 
from src.Snake import Snake, Obstacle
import random
import neat

class Game:
    def __init__(self, snake_array, config):
        self.display = pygame.display.set_mode((Config['game']['width'], Config['game']['width']))
        pygame.font.init() # you have to call this at the start,if you want to use this module.
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.score = 0
        self.snakes = snake_array
        for snakeId, snake in self.snakes:
            snake.net = neat.nn.FeedForwardNetwork.create(snake, config)
            

    def loop(self):
        obstacle = Obstacle(self.display, random.randint(50,451))
        x_change = 0
        y_change = 0
        
        clock = pygame.time.Clock()
        
        obstacle.draw()
        while True:
            self.display.fill(Config['colors']['white'])

            self.score+=1
            textsurface_score = self.myfont.render(str(self.score), False, (0, 0, 0))
            self.display.blit(textsurface_score,(0,0))

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -Config['snake']['speed']
                        y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x_change = Config['snake']['speed']
                        y_change = 0
                        
                    #self.display.fill(Config['colors']['white'])
                    #snake.move(x_change)
            obstacle.draw()
            
            is_anyone_alive = False
            for snakeId, snake in self.snakes: 
                if snake.is_alive()==True:
                    snake.predict(obstacle)
                    snake.draw(obstacle, self.display)
                    is_anyone_alive = True
            
            #self.display_info(snake, obstacle)
            obstacle.reincarnation_check(self.snakes)
            
            if is_anyone_alive == False:
                break

                #snake.kill(self.score)

            pygame.display.update()
            clock.tick(Config['game']['fps'])
        
    def get_width_change(self, snake, obstacle):
        return abs(snake.get_width_coord() - obstacle.get_width_coord())/200*1
    
    def get_height_change(self, snake, obstacle):
        return round(abs(snake.get_height_coord() - obstacle.get_height_coord())/550*1,2)
    
    def get_position(self, snake):
        return round((snake.get_width_coord()-50)/400,2)
    
    def get_obstacle_direction(self, snake, obstacle):
        if (snake.get_width_coord() - obstacle.get_width_coord()) > 0:
            return 1;
        if (snake.get_width_coord() - obstacle.get_width_coord()) < 0:
            return 0;
        else:
            return 0.5
            
    
    def display_info(self, snake, obstacle):
        textsurface_parameter1 = self.myfont.render(str(self.get_width_change(snake, obstacle)), False, (0, 0, 0))
        textsurface_parameter2 = self.myfont.render(str(self.get_height_change(snake, obstacle)), False, (0, 0, 0))
        textsurface_parameter3 = self.myfont.render(str(self.get_obstacle_direction(snake, obstacle)), False, (0, 0, 0))
        self.display.blit(textsurface_parameter1,(0,30))
        self.display.blit(textsurface_parameter2,(0,60))
        self.display.blit(textsurface_parameter3,(0,90))