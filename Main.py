# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:02:16 2019

@author: Gemmy George
"""

import pygame
import neat
import pickle
import os

from src.Game import Game
from src.Config import Config
from src.Snake import Snake

class Simulate(object):
    def __init__(self):
        self.GENERATION_NUMBER = 0
        
        #pygame.display.set_caption(Config['game']['caption'])

    def main(self):        
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config')
        config = neat.Config(Snake, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

        pop = neat.Population(config)
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
 
        winner = pop.run(self.eval_genomes, 50)

        # Save winner in a file
        with open('best_AI.pickle', 'wb') as handle:
            pickle.dump(winner, handle, protocol = pickle.HIGHEST_PROTOCOL)

    def eval_genomes(self, genomes, config):
        
        self.GENERATION_NUMBER += 1
        for _, snake in genomes:
            snake.alive = True
            snake.fitness = 0
    
        g = Game(genomes, config)
        g.loop()
        
        maxScore = 0
        for _, snake in genomes:
            if snake.fitness > maxScore:
                maxScore = snake.fitness
        
        print("Max score for generation : "+str(self.GENERATION_NUMBER)+ " is "+str(maxScore))

sim = Simulate()
sim.main()
