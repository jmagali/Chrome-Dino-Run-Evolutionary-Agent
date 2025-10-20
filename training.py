from game_files.game import Game
from game_files.dino import Dino
import time
import pygame
import os
import pickle
import neat

game  = Game(velocity=500)

def eval_genomes(genomes_tuple, config):
    genomes = []
    networks = []
    
    # Do stuff to each genome
    for _, genome in genomes_tuple:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genomes.append(genome)
    
    # Creates a list of n dinos, and resets other assets in the game
    game.reset_game(n=len(genomes))
        
    # EDIT THE TRAINING LOOP
    
           
    time.sleep(0.05)
    
def run_evolution(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file) 
    algorithm = neat.Population(config) # Initialize the NEAT algorithm with the parameters specified in the configuration file
    
    # Optional loggers
    algorithm.add_reporter(neat.StdOutReporter(True))
    algorithm.add_reporter(neat.StatisticsReporter())
    
    winner = algorithm.run(eval_genomes, 50) # Evaluating populations of 50 generations of dinos
    print('\nWinner\n\n', winner)
    
    #save the weights and bias of the perfect bird/neural network to a file so it can be used in the future
    with open('winning_genome.pkl', 'wb') as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    pygame.init()
    config_path = os.path.join(os.getcwd(), "config.txt")
    run_evolution(config_path)
