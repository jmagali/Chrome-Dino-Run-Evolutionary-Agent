from game_files.game import Game
from game_files.dino import Dino
import time
import pygame
import os
import pickle
import neat

def loadNeuralNetwork():
    local_dir = os.path.dirname(__file__) #gets the directory that we are currently in
    config_file = os.path.join(local_dir, "config.txt") #find the path to the config.txt file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    with open('winning_genome.pkl', 'rb') as f:
        perfect_genome = pickle.load(f)
    neural_network = neat.nn.FeedForwardNetwork.create(perfect_genome, config)
    return neural_network

pygame.init()
game = Game(velocity=500)
network = loadNeuralNetwork()
game.reset_game(n=1)

run = True
while run:
    dino = game.dinos[0]
    
    output = network.activate(game.get_observations(dino))
    if output[0] > 0.5 and dino.jumps_used < 2:
        dino.jump()
    
    game.step()
    if not dino.alive:
        break