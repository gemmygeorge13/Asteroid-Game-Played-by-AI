# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 17:52:09 2019

@author: 91961
"""

import pygame
import random
import neat
from src.Config import Config

class Snake(neat.DefaultGenome):
    def __init__(self, key):
        super().__init__(key)
        
        self.x_pos = (Config['game']['width'])/2
        self.y_pos = (Config['game']['height'])-50
        self.state = True;
        self.fitness = 0;
        self.net = None
        self.rect = pygame.Rect(self.x_pos, self.y_pos, Config['snake']['height'], Config['snake']['width'])
        
    def draw(self, obstacle, display):
        if self.state == True:
            self.rect = pygame.Rect(self.x_pos, self.y_pos, Config['snake']['height'], Config['snake']['width'])
            pygame.draw.rect(
                display, 
                Config['colors']['green'],
                self.rect
            )
            if self.has_collided(obstacle):
                self.fitness += 1
                #print(self.fitness)

    def move(self, x_change):
        if self.state == True:
            if self.x_pos>50 and self.x_pos<450:
                self.x_pos += x_change
            elif self.x_pos == 50 and x_change > 0 :
                self.x_pos += x_change
            elif self.x_pos == 450 and x_change < 0 :    
                self.x_pos += x_change

            
    def get_width_coord(self):
        return self.x_pos
    
    def get_height_coord(self):
        return self.y_pos
    
    def has_collided(self, obstacle):
        return self.rect.colliderect(obstacle.rect)
            
    def kill(self):
        self.x_pos = None;
        self.y_pos = None;
        self.state = False;        
        print("Dead snake")
        
    def is_alive(self):
        return self.state;
    
    def is_not_fit(self, baseline):
        if self.state == True: 
            #print(str(baseline)+":"+str(self.fitness))
            if self.fitness<baseline:
                return True; 
        return False;
    
    def predict(self, obstacle):
        input = (float(self.get_obstacle_direction(obstacle)),float(self.get_width_change(obstacle)))
        output = self.net.activate(input)
        #print("O1:"+str(output[0])+" - O2:"+str(output[1]))
        if output[0]>0.7:
            self.move(Config['snake']['speed'])
        if output[1]<=0.3:
            self.move(-Config['snake']['speed'])
            
    def get_obstacle_direction(self, obstacle):
        if (self.get_width_coord() - obstacle.get_width_coord()) > 0:
            return 1;
        elif (self.get_width_coord() - obstacle.get_width_coord()) < 0:
            return 0;
        else:
            return 0.5
        
    def get_width_change(self, obstacle):
        return abs(self.get_width_coord() - obstacle.get_width_coord())/200*1
    
    def configure_new(self, config):
        super().configure_new(config)
    

    def configure_crossover(self, genome1, genome2, config):
        super().configure_crossover(genome1, genome2, config)
    

    def mutate(self, config):
        super().mutate(config)
    

    def distance(self, other, config):
        return super().distance(other, config)
        


class Obstacle:
    def __init__(self, display, random_x):
        self.x_pos = random_x
        self.y_pos = -300
        self.display = display
        self.i = 1
        self.baseline = 0
        self.rect = pygame.Rect(self.x_pos, self.y_pos, Config['snake']['height'], Config['snake']['width'])

    def draw(self):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, Config['snake']['height'], Config['snake']['width'])
        pygame.draw.rect(
            self.display, 
            Config['colors']['red'],
            self.rect
        )
        self.update()
        
    def update(self):
        self.y_pos = self.y_pos + Config['snake']['obstacle']
        
    def reincarnation_check(self, snakes):
        if self.y_pos >= ((Config['game']['height'])+50) :
            self.y_pos = 0
            self.baseline += 4
            self.x_pos = random.randint(50,451)
            for snakeId, snake in snakes:
                if snake.is_not_fit(self.baseline)==True:
                    snake.kill()
            

    def get_width_coord(self):
        return self.x_pos
    
    def get_height_coord(self):
        return self.y_pos

