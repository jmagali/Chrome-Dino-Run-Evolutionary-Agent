from game_files.game import Game
from game_files.dino import Dino
import time
import pygame
import os
import pickle
import neat

pygame.init()
game = Game(velocity=500)
game.reset_game(n=1)

run = True
play = True
while play:
    while run:
        dino = game.dinos[0]
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or pygame.K_UP and dino.jumps_used < 2: 
                    dino.jump()
        
        game.step()
        if not dino.alive:
            run = False
            break
    
    time.sleep(0.5)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
            play = False
        if event.type == pygame.KEYDOWN:
            game.reset_game(n=1)
            if event.key == pygame.K_SPACE or pygame.K_UP: 
                run = True