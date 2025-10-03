import pygame
from game_files.base import Base
from game_files.cacti import Cacti
from game_files.dino import Dino

class Game:
    WIN_WIDTH = 1000
    WIN_HEIGHT = 500
    FPS = 60
    
    def __init__(self, velocity: int):
        self.window = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.velocity = velocity # Velocity for all objects in game
        
        # Use pixels/second
        self.base = Base(y=400, vel_px_s=velocity)
        self.cacti = Cacti(y=(400 + self.base.BASE_IMG.get_height() - 20), vel_px_s=velocity, screen_w=self.WIN_WIDTH)
        self.dinos = []
        self.score = 0
        
    def draw_window(self):
        self.window.fill((255, 255, 255))

        self.base.draw(self.window)
        self.cacti.draw(self.window)
        for dino in self.dinos:
            dino.draw(self.window)
        
        # Score
        font = pygame.font.Font(None, 30)
        fontLabel = font.render(f"Score: {round(self.score / 10) * 10}", True, (0, 0, 0))
        labelRect = fontLabel.get_rect(center=(10 + fontLabel.get_size()[0] / 2, 10 + fontLabel.get_size()[1] / 2))
        self.window.blit(fontLabel, labelRect)
        
        pygame.display.update()
        
    def reset_game(self, n):
        self.clock = pygame.time.Clock()
        self.cacti = Cacti(y=(400 + self.base.BASE_IMG.get_height() - 20), vel_px_s=self.velocity, screen_w=self.WIN_WIDTH)
        self.score = 0
        
        self.dinos = []
        for i in range(n):
            self.dinos.append(Dino(self.WIN_WIDTH // 2, 400 + self.base.BASE_IMG.get_height() - 20))

    def step(self):
        for _ in pygame.event.get():
            pass
        
        self.score += 0.1
        dt = self.clock.tick(self.FPS) / 1000.0   
        self.base.move(dt)
        self.cacti.move(dt)
        cacti_to_check = [(self.cacti.cacti_imgs[str(self.cacti.interest[i][0])]["img"]) for i in range(len(self.cacti.interest))]
        cacti_to_check_x_poses = [self.cacti.interest[i][1] for i in range(len(self.cacti.interest))]
        
        for dino in self.dinos:
            dino.move(dt, cacti_to_check, cacti_to_check_x_poses)
        
        self.draw_window()
    
    def get_observations(self, dino):
        obs = []
        for i in range(0, 4):
            if i < len(self.cacti.interest):
                cactus = self.cacti.interest[i]
                obs.append(cactus[1] - self.WIN_WIDTH / 2) # From head of dino to start of cactus
                obs.append(self.cacti.cacti_imgs[cactus[0]]["width"]) # Width of cactus
                obs.append(self.cacti.cacti_imgs[cactus[0]]["height"]) # Width of cactus
            else:
                obs.extend([0, 0, 0])
        obs.append(dino.height - (400 + self.base.BASE_IMG.get_height() - 20)) # Get the current height of dino from ground
        obs.append(2 - dino.jumps_used)
        return obs