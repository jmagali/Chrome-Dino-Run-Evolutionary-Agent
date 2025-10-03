import pygame, os

class Base:
    def __init__(self, y=600, vel_px_s=300):  # velocity in pixels/second
        self.y = y
        self.vel_px_s = vel_px_s

        img = pygame.image.load(os.path.join("game_files", "assets", "track.png")).convert_alpha()
        self.BASE_IMG = pygame.transform.scale2x(img)
        self.WIDTH = self.BASE_IMG.get_width()

        # floats for smooth subpixel motion
        self.x1 = 0.0
        self.x2 = float(self.WIDTH)

    def move(self, dt):
        dx = self.vel_px_s * dt
        self.x1 -= dx
        self.x2 -= dx

        # wrap-around
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.BASE_IMG, (int(self.x1), int(self.y)))
        window.blit(self.BASE_IMG, (int(self.x2), int(self.y)))
