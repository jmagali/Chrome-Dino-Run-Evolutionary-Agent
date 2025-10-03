import pygame
import os

class Dino:
    base = os.path.join("game_files", "assets")
    DINO_IMGS = [pygame.transform.scale_by(pygame.image.load(os.path.join(base, "run1.png")), 0.75), 
             pygame.transform.scale_by(pygame.image.load(os.path.join(base, "run2.png")), 0.75)] 
    ANIMATION_TIME = 10

    def __init__ (self, x, y): 
        self.x, self.y = x, y
        self.t = 0 # tick_count keeps track of how many frames went by since the bird last jumped
        self.vel = -55
        self.gravity = 9.8
        self.is_jumping = False
        self.y0 = self.y # Starting height for double jump
        self.height = self.y # Height of jumps
        self.img_count = 0
        self.img = self.DINO_IMGS[0]
        self.jumps_used = 0 # For double jumping
        self.alive = True
    
    def jump(self):
        self.is_jumping = True
        self.jumps_used += 1
        self.t = 0
        self.y0 = self.y if (self.jumps_used == 1) else self.height
    
    def move(self, dt, cacti, cacti_x_poses):
        # Jump
        self.t += dt * 20
        if self.is_jumping:
            self.height = self.y0 + self.vel * self.t + 0.5 * self.gravity * (self.t ** 2)
            if self.height >= self.y:
                self.height = self.y
                self.is_jumping = False
                self.jumps_used = 0

        # Dino mask
        dino_w = self.img.get_width()
        dino_h = self.img.get_height()
        dino_left = int(self.x - dino_w)
        dino_top  = int(self.height - dino_h)
        dino_rect = pygame.Rect(dino_left, dino_top, dino_w, dino_h)
        dino_mask = pygame.mask.from_surface(self.img)

        # Cacti mask
        for i, cactus in enumerate(cacti):
            c_w, c_h = cactus.get_width(), cactus.get_height()
            c_left = int(cacti_x_poses[i])
            c_top  = int(self.y - c_h)
            cactus_rect = pygame.Rect(c_left, c_top, c_w, c_h)
            cactus_mask = pygame.mask.from_surface(cactus)

            # Offset = cactus top-left relative to dino rect
            offset = (cactus_rect.left - dino_rect.left, cactus_rect.top - dino_rect.top)

            if dino_mask.overlap(cactus_mask, offset):
                self.alive = False
  
    def draw(self, window):
        self.img_count = (self.img_count + 1) % (self.ANIMATION_TIME * 2)
        img_index = self.img_count // self.ANIMATION_TIME
        self.img = self.DINO_IMGS[img_index]
        window.blit(self.img, (self.x - self.img.get_width(), int((self.height - self.img.get_height()))))