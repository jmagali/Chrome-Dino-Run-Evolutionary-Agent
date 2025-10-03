from game_files.game import Game
import time
import pygame

if __name__ == "__main__":
    pygame.init()

    game = Game(velocity=500)
    round_over = False
    game_over = False

    while not game_over:
        while not round_over:
            jump = False
            
            # Check for key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    round_over = True
                    game_over = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP and game.get_can_jump():
                        jump = True
                        
            # Run an iteration in the game loop
            alive = game.step(jump)
            obs = game.get_observations()
            if not alive:
                round_over = True
        
        time.sleep(0.25)
        # Start a new game by pressing space
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                game.reset_game()
                round_over = False
                
    pygame.quit()
