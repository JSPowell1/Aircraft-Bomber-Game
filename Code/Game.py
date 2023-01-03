# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
pygame.display.set_caption("Aircraft Bomber")
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

# Define constants for the screen width and height
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
# Define constants for colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (135, 206, 250)
#Acceleration due to gravity
ACCELERATION = 9.80665

# Define the Aircraft object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Aircraft(pygame.sprite.Sprite):
    def __init__(self):
        super(Aircraft, self).__init__()
        self.surf = pygame.image.load("aircraft.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            #move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            #move_down_sound.play()
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
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the bomb object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bomb(pygame.sprite.Sprite):
    def __init__(self, velocity = (0,0)):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("Bomb.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        self.velocity = velocity
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                (aircraft.rect.x + 20),
                (aircraft.rect.y + 20),
            )
        )
        self.on_ground = False

    def update(self):
        self.rect.x = self.rect.x + self.velocity[0]
        self.rect.y = self.rect.y + self.velocity[1]
        
        if not self.on_ground:
            # do gravity
            current_x_vel = self.velocity[0]
            current_y_vel = self.velocity[1]
            y_vel = current_y_vel + ACCELERATION
            self.velocity = (current_x_vel, y_vel)
        #self.speed = ACCELERATION

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    #def update(self):
    #    self.rect.move_ip(0,self.speed)
    #    if self.rect.bottomleft[1] >= SCREEN_HEIGHT:
    #        self.kill()
        #self.rect.x = self.rect.x + self.velocity[0]
        #self.rect.y = self.rect.y + self.velocity[1]

# Define the target object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super(Target, self).__init__()
        self.surf = pygame.image.load("Target1.png").convert()
        self.surf.set_colorkey((BLACK), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH + 20),
                random.randint(SCREEN_HEIGHT - 50, SCREEN_HEIGHT - 10),
            )
        )
        self.speed = 10

    # Move the target based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((BLACK), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Define the landscape object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Landscape(pygame.sprite.Sprite):
    def __init__(self):
        super(Landscape, self).__init__()
        self.surf = pygame.image.load("Landscape.png").convert()
        self.surf.set_colorkey((WHITE), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH-350),
                (SCREEN_HEIGHT-150),
            )
        )

    # Move the landscape based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            self.kill()
            
            

'''# Setup for sounds, defaults are good
pygame.mixer.init()'''

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDBOMB = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBOMB, 250)
ADDTARGET = pygame.USEREVENT + 3
pygame.time.set_timer(ADDTARGET, 1000)
'''ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
'''
# Create our 'aircraft'
aircraft = Aircraft()

landscape = Landscape()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
#enemies = pygame.sprite.Group()
targets = pygame.sprite.Group()
bombs = pygame.sprite.Group()
#clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(aircraft)
#all_sprites.add(landscape)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
'''pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)'''

# Variable to keep our main loop running
running = True

counter = 0

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                new_bomb = Bomb()
                bombs.add(new_bomb)
                all_sprites.add(new_bomb)

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        #elif event.type == ADDENEMY:
        #    # Create the new enemy, and add it to our sprite groups
        #    new_enemy = Enemy()
        #    enemies.add(new_enemy)
        #    all_sprites.add(new_enemy)
        
        # Should we add a new target?
        elif event.type == ADDTARGET:
            # Create the new target, and add it to our sprite groups
            pygame.time.set_timer(ADDTARGET, random.randint(100, 1000))
            new_target = Target()
            targets.add(new_target)
            all_sprites.add(new_target)

        '''# Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)'''
  
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    aircraft.update(pressed_keys)

    # Update the position of our enemies and clouds
    #enemies.update()
    targets.update()
    bombs.update()
    '''clouds.update()'''
    '''if pygame.sprite.Sprite.alive(landscape) == True:
         landscape.update()
    else: 
        landscape = Landscape()
        all_sprites.add(landscape)'''

    # Fill the screen with sky blue
    screen.fill(BLUE)
    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    ''' # Check if any enemies have collided with the aircraft
    if pygame.sprite.spritecollideany(aircraft, enemies):
        # If so, remove the aircraft
        aircraft.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # Stop the loop
        running = False'''
    
       counter += 1
    if counter %100 == 0:
        print(aircraft.rect.x)
        print(aircraft.rect.y)

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 60 frames per second rate
    clock.tick(60)

    # At this point, we're done, so we can stop and quit the mixer
    #pygame.mixer.music.stop()
    #pygame.mixer.quit()