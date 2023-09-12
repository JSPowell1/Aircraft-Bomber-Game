# Imports
# Import pygame to allow game to be played 
import pygame
# Import random for random numbers
import random
# Import math for maths functions
import math as maths
# Import pygame.locals for access to coordinates
from pygame.locals import *

# Initialize pygame
pygame.init()
# Setup sounds
pygame.mixer.init()
# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# Size is determined by the screen resolution
pygame.display.set_caption("Aircraft Bomber")
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# Get the screen width and height for use in the program
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

# Constants
# Fonts
FONT = pygame.font.SysFont("Comic Sans MS", 20)
BIG_FONT = pygame.font.SysFont("Comic Sans MS", 60)
# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (135, 206, 250)
# Acceleration due to gravity
ACCELERATION = 9.80665
# Wind
WIND = 1
# Maximum bomb count
MAXIMUM_BOMBS = 200

# Initialise variables
score = 0
target_count = 0
bomb_count = 0
targets_percentage_hit = 0
scroll = 0
# Allow game information to be shown once at the end
i = 0

# Variable to keep the game loop running
playing = True

# Create landscape
landscape = pygame.image.load("Landscape.png").convert()
# Get landscape width and height for use in the program
LANDSCAPE_WIDTH = landscape.get_width()
LANDSCAPE_HEIGHT = landscape.get_height()
# Tiles for landscape scrolling
tiles = maths.ceil(SCREEN_WIDTH / LANDSCAPE_WIDTH) + 1

# Aircraft object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Aircraft(pygame.sprite.Sprite):
    def __init__(self):
        super(Aircraft, self).__init__()
        self.surf = pygame.image.load("Aircraft.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep aircraft on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT - LANDSCAPE_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - LANDSCAPE_HEIGHT

# Bomb object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Bomb(pygame.sprite.Sprite):
    def __init__(self, velocity = (0,0)):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("Bomb.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        self.velocity = velocity
        # Starting position is set to the position of the aircraft
        self.rect = self.surf.get_rect(
            center=(
                (aircraft.rect.x + 20),
                (aircraft.rect.y + 20),
            )
        )

    # Gravity  
    def update(self):
        self.rect.x = self.rect.x + self.velocity[0]
        self.rect.y = self.rect.y + self.velocity[1]
        current_x_velocity = self.velocity[0]
        current_y_velocity = self.velocity[1]
        x_velocity = current_x_velocity - WIND
        y_velocity = current_y_velocity + ACCELERATION
        self.velocity = (x_velocity, y_velocity)
        # Remove bomb when it leaves the bottom side of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Target object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super(Target, self).__init__()
        self.surf = pygame.image.load("Target.png").convert()
        self.surf.set_colorkey((BLACK), RLEACCEL)
        # Starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( 
                (SCREEN_WIDTH + 20),
                random.randint(SCREEN_HEIGHT - 50, SCREEN_HEIGHT - 10),
            )
        )
        self.speed = 10
            
    def update(self):
        # Move target based on a constant speed
        self.rect.move_ip(-self.speed, 0)
        # Remove target when it leaves the left side of the screen
        if self.rect.right < 0:
            self.kill()
            # Respawn target to the right of the screen
            self.rect = self.surf.get_rect(
            center=( 
                (SCREEN_WIDTH + 20),
                random.randint(SCREEN_HEIGHT - 50, SCREEN_HEIGHT - 10),
            )
        )
    # Damaged target
    def damage(self):
        self.surf = pygame.image.load("Damaged_Target.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        
# Cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("Cloud.png").convert()
        self.surf.set_colorkey((BLACK), RLEACCEL)
        # Starting position and speed are randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT - LANDSCAPE_HEIGHT)
            )
        )
        self.speed = random.randint(8, 12)

    def update(self):
        # Move the cloud based on a random speed
        self.rect.move_ip(-self.speed, 0)
        # Remove cloud when it leaves the left side of the screen
        if self.rect.right < 0:
            self.kill()        

# Create custom events for adding a new bomb, target and cloud
ADDBOMB = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBOMB, 250)
ADDTARGET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDTARGET, 1000)
ADDCLOUD = pygame.USEREVENT + 3
pygame.time.set_timer(ADDCLOUD, 1000)

# Create the aircraft
aircraft = Aircraft()

# Create groups for bomb sprites, target sprites, cloud sprites, and all sprites
bombs = pygame.sprite.Group()
targets = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(aircraft)

# Aircraft sound is played throughout the game
aircraft_sound = pygame.mixer.Sound("Aircraft-engine.wav")
aircraft_sound.play(loops = -1)

# Load all sound files
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
bomb_release_sound = pygame.mixer.Sound("Bomb_release.mp3")
bomb_explosion_sound = pygame.mixer.Sound("Bomb_explosion.wav")

# Base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
bomb_release_sound.set_volume(0.5)
bomb_explosion_sound.set_volume(0.5)

# Functions to show messages on screen
def show_game_instructions(screen, font, message):
    label = font.render(message, 1, WHITE)
    label_rect = label.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(label, label_rect)

def show_bomb_count(screen, font, message):
    label = font.render(message, 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH - 180, 0))

def show_score(screen, font, message):
    label = font.render(message, 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH - 180, 25))

def show_game_over(screen, font, message):
    label = font.render(message, 1, WHITE)
    label_rect = label.get_rect(center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - 65))
    screen.blit(label, label_rect)

def show_final_score(screen, font, message):
    label = font.render(message, 1, WHITE)
    label_rect = label.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(label, label_rect)

def show_targets_percentage_hit(screen, font, message):
    label = font.render(message, 1, WHITE)
    label_rect = label.get_rect(center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) + 25))
    screen.blit(label, label_rect)

def show_exit_instructions(screen, font, message):
    label = font.render(message, 1, WHITE)
    label_rect = label.get_rect(center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) + 50))
    screen.blit(label, label_rect)

# The game loop
while playing:
    # Look at each event in the queue
    for event in pygame.event.get():
        # Did the player press a key?
        if event.type == KEYDOWN:
            # Is it the ESCAPE key? If so, stop the game.
            if event.key == K_ESCAPE:
                playing = False
            # If bombs used by player is less than maximum, allow a new bomb to be added
            elif bomb_count < MAXIMUM_BOMBS:
                # Is it the SPACEBAR? If so, add a new bomb.
                if event.key == K_SPACE:
                    new_bomb = Bomb()
                    bombs.add(new_bomb)
                    all_sprites.add(new_bomb)
                    bomb_release_sound.play()
                    bomb_count += 1
        # Did the player click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            playing = False

        # Add a new target?
        elif event.type == ADDTARGET:
            # Create a new target, and add it to the sprite groups
            pygame.time.set_timer(ADDTARGET, random.randint(100, 1000))
            new_target = Target()
            targets.add(new_target)
            all_sprites.add(new_target)
            if bomb_count < MAXIMUM_BOMBS:
                target_count += 1

        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create a new cloud, and add it to the sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    
    # Get the set of keys pressed and check for player input
    pressed_keys = pygame.key.get_pressed()
    aircraft.update(pressed_keys)

    # Update the position of targets, bombs and clouds
    bombs.update()
    targets.update()
    clouds.update()
    
    # Fill the screen with sky blue
    screen.fill(BLUE)
    # Scroll landscape
    counter = 0
    while (counter < tiles):
        screen.blit(landscape, (LANDSCAPE_WIDTH * counter + scroll, SCREEN_HEIGHT - LANDSCAPE_HEIGHT))
        counter += 1
    scroll -= 10
    if abs(scroll) > LANDSCAPE_WIDTH:
        scroll = 0
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # Show instrctions for player if bomb count equals 0
    if bomb_count == 0: 
        show_game_instructions(screen, FONT, "Use CURSOR KEYS to move Aircraft around and SPACEBAR to release bombs. Use ESC to quit.")
    # Show score and bombs used on screen if bombs used are less than maximum
    if bomb_count < MAXIMUM_BOMBS:
        show_score(screen, FONT, "Score: "+str(score) + "/" + str(target_count))
        show_bomb_count(screen, FONT, "Bombs: " + str(bomb_count) + "/" + str(MAXIMUM_BOMBS))
    # Update percentage of targets hit
    if target_count != 0: targets_percentage_hit = int((score/target_count)*100)

    # Check if bombs have hit targets
    collisions = pygame.sprite.groupcollide(bombs, targets, False, False)  
    for bomb, damaged_targets in collisions.items():
        for target in damaged_targets:
            target.damage()
            bomb_explosion_sound.play()
            score += 1
    
    # Show end screen if maximum bomb count is reached
    if bomb_count == MAXIMUM_BOMBS:
        show_game_over(screen, BIG_FONT, "Game Over!")
        show_final_score(screen, FONT, "Targets Hit: " + str(score) + "/" + str(target_count))
        show_targets_percentage_hit(screen, FONT, "You hit " + str(targets_percentage_hit) + "% of targets!")
        show_exit_instructions(screen, FONT, "Press ESC to exit")
        # Remove aircraft
        for entity in all_sprites:
            aircraft.kill()
        # Stop sounds
        aircraft_sound.stop()
        move_up_sound.stop()
        move_down_sound.stop()
        bomb_release_sound.stop()
        bomb_explosion_sound.stop()
        # Show game information on command window once at the end
        if i == 0: 
            print("Game Over!\nTargets Hit: " + str(score) + "/" + str(target_count) + "\nYou hit " + str(targets_percentage_hit) 
                  + "% of targets!")
            i += 1

    # Update everything on the display
    pygame.display.flip()

    # Maintain a 60 frames per second rate (probably less)
    clock.tick(60)