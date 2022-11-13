import sys, pygame
from pygame import sprite
pygame.init()
#--------------------------CONSTANTS-------------------------
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
BLUE  = (0, 0, 127)
GREEN = (31, 191, 31)
DEFAULT_FONT = pygame.font.SysFont("monospace", 15)
MAX_SPEED = 100
ACCELERATION_DUE_TO_GRAVITY = 11

#--------------------------VARIABLES----------------------------
# Usually you blit surface objects onto the screen surface.
# The following line needs an egg image in folder with this game. 
# Then can be blit onto the screen surface in the game loop
# If you have a variable for where you want to blit it (x and y) you can 
# change those values each frame if you want to animate!
#egg_surface = pygame.image.load("egg.png")
# Clock manages FPS but also gives you accurate time which can help with some animations.
clock = pygame.time.Clock()
#Sceen is a surface that you can draw (blit) on: https://www.pygame.org/docs/ref/surface.html
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#Pygame uses Rect objects. They need an x, y, width, height. See https://www.pygame.org/docs/ref/rect.html
temp_rect_x = 0
temp_rect_y = 9 * WINDOW_HEIGHT // 10
temp_rect_width = WINDOW_WIDTH
temp_rect_height = WINDOW_HEIGHT - temp_rect_y
foreground_rect = pygame.Rect(temp_rect_x, temp_rect_y, temp_rect_width, temp_rect_height)
#--------------------------CLASSES----------------------------
# Classes are when you want to do it OOP style. Extending sprite can be a good option as it already has
# loads of useful attribuites (like rect which stores x, y etc, and image) and methods like kill()




class Ball(pygame.sprite.Sprite):
    def __init__(self, group, image, size, bounciness, centre, velocity = (0,0)): # 'Constructor' makes a new object of class Ball
        super().__init__(group) # Call superclass constructor
         #rect is an object of class sprite
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.bounciness = bounciness
        self.rect.center = centre
        self.velocity = velocity
        self.on_ground = False

    def update(self, screen):
        self.rect.x = self.rect.x + self.velocity[0]
        self.rect.y = self.rect.y + self.velocity[1]
        
        if not self.on_ground:
            # do gravity
            current_x_vel = self.velocity[0]
            current_y_vel = self.velocity[1]
            y_vel = current_y_vel + ACCELERATION_DUE_TO_GRAVITY
            self.velocity = (current_x_vel, y_vel)
            # if bottom of screen, bounce
            if self.rect.bottomleft[1] >= screen.get_height():
                self.bounce()
    def bounce(self):
        current_x_vel = self.velocity[0]
        current_y_vel = self.velocity[1]
        print("Y vel before bounce", current_y_vel)
        if current_y_vel > 0.1: # if falling...
            current_y_vel = -1 * current_y_vel * self.bounciness #...then bounce
        else:
            current_y_vel = 0 # or settle at rest
            self.on_ground = True
            
        self.velocity = (current_x_vel, current_y_vel)
        print("Y vel after bounce", current_y_vel)
        


balls = pygame.sprite.Group()
ball1 = Ball(balls, "ball.png", (50,50), 0.8, (100,100))
balls.add(ball1)


#--------------------------FUNCTIONS/PROCEDURES---------------
# Write some functions you can call
def show_message(screen, font, message):
    label = font.render(message, 1, (255,255,0))
    screen.blit(label, (25, 25))
    

#--------------------------MAIN_GAME_LOOP---------------
#Often handy to keep tabls of frame number
frame_number = 0
running = True
# Game loop
while running:
    # deal with events like clicks, keydown, keyup. https://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():
        # OS says quit, i.e. clicking on the cross
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #find keys here: https://www.pygame.org/docs/ref/key.html#module-pygame.key
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                old_vel_x = ball.velocity[0]
                old_vel_y = ball.velocity[1]
                ball.velocity = (old_vel_x -MAX_SPEED, old_vel_y)
    
    # update stuff
    for ball in balls:
        ball.update(screen)
    
    # drawing stuff...
    # background
    screen.fill(BLUE)
    #draw rect on the screen in specified colour
    pygame.draw.rect(screen, GREEN, foreground_rect)
    
    #Use pygame.Surface.blit to blit images onto the screen: https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
    #Messages can be useful
    if frame_number < 50:
        show_message(screen, DEFAULT_FONT, "Let's go")
    balls.draw(screen)
    # keep track of time
    frame_number += 1
    pygame.display.flip()  # updates display
    clock.tick(10)  # 10 fps
# Leave tidily and return resources to OS.
pygame.display.quit()
pygame.quit()
sys.exit(0)