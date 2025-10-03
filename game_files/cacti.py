import pygame, os
import random

class Cacti:
    def __init__(self, y=410, vel_px_s = 300, screen_w: int = 800):  # velocity in pixels/second
        self.x, self.y = screen_w, y
        self.vel_px_s = vel_px_s
        self.interest = []
        self.screen_w = screen_w

        def make_entry(path):
            img = pygame.image.load(path).convert_alpha()
            bbox = img.get_bounding_rect()
            img = img.subsurface(bbox).copy()
            return {
                "img": img,
                "width": img.get_width(),
                "height": img.get_height(),
            }

        base = os.path.join("game_files", "assets")
        self.cacti_imgs = {
            "small1": make_entry(os.path.join(base, "small1.png")),
            "small2": make_entry(os.path.join(base, "small2.png")),
            "small3": make_entry(os.path.join(base, "small3.png")),
            "large1": make_entry(os.path.join(base, "large1.png")),
            "large2": make_entry(os.path.join(base, "large2.png")),
            "large3": make_entry(os.path.join(base, "large3.png")),
        }
        
        self.cacti_queue = [[random.choice(list(self.cacti_imgs.keys())), screen_w + 50]]
        self.generate_next_cacti() # Always has 5 cacti in line, (name, x_pos)
        self.interest = self.find_cactus_of_interest()

    def find_cactus_of_interest(self): # Only those in front of dino and within screen are of interest
        interest = []
        for cactus in self.cacti_queue:
            if self.screen_w / 2 - 100 < cactus[1] < self.screen_w:
                interest.append(cactus)
            if cactus[1] > self.screen_w:
                break
        return interest
    
    def generate_next_cacti(self):
        for _ in range(5 - len(self.cacti_queue)):
            self.cacti_queue.append([random.choice(list(self.cacti_imgs.keys())), self.cacti_queue[-1][1] + random.randrange(150, 500)])
        
    def move(self, dt):
        dx = self.vel_px_s * dt
        for i in range(len(self.cacti_queue)):
            self.cacti_queue[i][1] -= dx
        
        # Remove if rolled off screen
        if self.cacti_queue[0][1] < - 100:
            self.cacti_queue.pop(0)
            self.generate_next_cacti()
        
        self.interest = self.find_cactus_of_interest()
            
    def draw(self, window):
        for i, cactus in enumerate(self.cacti_queue):
            name, x_pos = cactus
            img = self.cacti_imgs[name]["img"]
            rect = img.get_rect()
            rect.left = int(x_pos)
            rect.bottom = int(self.y)

            if cactus in self.interest:
                # Make a tinted red copy of the cactus
                red_img = img.copy()
                red_surface = pygame.Surface(img.get_size(), flags=pygame.SRCALPHA)
                red_surface.fill((255, 0, 0, 100))  # RGBA, alpha=100 makes it translucent
                red_img.blit(red_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                window.blit(red_img, rect)
            else:
                window.blit(img, rect)