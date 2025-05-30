import pygame
import os
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH  / 2 , WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laset_shoot_time = 0
        self.cooldown_duration = 2000
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laset_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
            

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])    
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            print("Fire Laser")
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()    

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

        
        

# -------- Setup --------
# Initialize Pygame
pygame.init()
# Get the folder where the current script lives
base_path = os.path.dirname(__file__)
# Build absolute path to player.png
icon_path = os.path.join(base_path, "..", "images", "player.png")
icon_path = os.path.abspath(icon_path)
# print("Loading icon from:", icon_path) test the path
# Load and set the icon
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
# Set up display
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter Game")
# loop
running = True
clock = pygame.time.Clock()

# plain surface 
surf = pygame.Surface((100,200))
surf.fill("orange")
x = 100


all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(os.path.join(base_path, "..", "images", "star.png")).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)






meteor_surf = pygame.image.load(os.path.join(base_path, "..", "images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH  / 2 , WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(os.path.join(base_path, "..", "images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20,WINDOW_HEIGHT - 20))


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type ==  meteor_event:
        #     print("create meteor")

        

   
    all_sprites.update(dt)


    # draw the game 
    display_surface.fill("darkgray")
    all_sprites.draw(display_surface)


    pygame.display.update()

pygame.quit()
