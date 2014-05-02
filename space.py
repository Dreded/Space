"""
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/4YqIKncMJNs
 Explanation video: http://youtu.be/ONAK8VZIcI4
 Explanation video: http://youtu.be/_6c4o41BIms
"""
 
import pygame
import random

window_size=[1280,720]
full_size=[1920,1200]
screen_size = window_size

def toggle_fullscreen(screen_size):
    screen = pygame.display.get_surface()
    caption = pygame.display.get_caption()

    flags = screen.get_flags()
    bits = screen.get_bitsize()

    screen = pygame.display.set_mode(screen_size,flags^pygame.FULLSCREEN,bits)
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??


    return screen

def firelaser(x, y):
    laserPosition.append([x, y])

MAX_STARS  = 350
STAR_SPEED = 2
stars = []
def init_stars(screen):
  """ Create the starfield """
  for i in range(MAX_STARS):
    # A star is represented as a list with this format: [X,Y,speed]
    star = [random.randrange(0,screen.get_width() - 1),
            random.randrange(0,screen.get_height() - 1),
            random.choice([1,2,3])]
    stars.append(star)

def move_and_draw_stars(screen):
  """ Move and draw the stars in the given screen """
  for star in stars:
    star[1] += star[2]
    # If the star hit the bottom border then we reposition
    # it in the top of the screen with a random X coordinate.
    if star[1] >= screen.get_height():
      star[1] = 0
      star[0] = random.randrange(0,screen.get_width() - 1)
      star[2] = random.choice([1,2,3])

    # Adjust the star color acording to the speed.
    # The slower the star, the darker should be its color.
    if star[2] == 1:
      color = (100,100,100)
    elif star[2] == 2:
      color = (190,190,190)
    elif star[2] == 3:
      color = (255,255,255)

    # Draw the star as a rectangle.
    # The star size is proportional to its speed.
    screen.fill(color,(star[0],star[1],star[2],star[2]))

def printscore(screen,score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score:  %d" % (score), 1, WHITE)
    textpos = text.get_rect(left=screen.get_width()-180,y=10)
    screen.blit(text, textpos)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF)
 
# This sets the name of the window
pygame.display.set_caption('Space Ace')
 
clock = pygame.time.Clock()
 
# Before the loop, load the sounds:
click_sound = pygame.mixer.Sound("laser5.ogg")
music_sound = pygame.mixer.Sound("music/level3.ogg")
music_sound.play(loops=-1)

# Set positions of graphics
background_position = [0, 0]

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# Load and set up graphics.
background_image = pygame.image.load("saturn_family1.jpg").convert()
planets_image = pygame.image.load("planets.png").convert()
planets_image.set_colorkey(BLACK)

player_image = pygame.image.load("starship.png").convert()
player_image.set_colorkey(BLACK)

projectile_image = pygame.image.load("projectile.png").convert()
projectile_image.set_colorkey(BLACK)

laserSpeed = 8
laserPosition = []
done = False
init_stars(screen)
score = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                click_sound.play()
                firelaser(x-64,y-128)
                score += 100
            elif pygame.mouse.get_pressed()[2]:
                score += 10

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            elif event.key == pygame.K_RETURN and (event.mod&(pygame.KMOD_LALT|pygame.KMOD_RALT) != 0) or pygame.K_f:
                if screen.get_width() == 1920:
                    toggle_fullscreen(window_size)

                elif screen.get_width() < 1920:
                    window_size = [screen.get_width(),screen.get_height()]
                    toggle_fullscreen(full_size)

        elif event.type==pygame.VIDEORESIZE:
            flags = screen.get_flags()
            bits = screen.get_bitsize()
            pygame.display.init()
            screen = pygame.display.set_mode(event.dict['size'],flags|pygame.RESIZABLE,bits)
            stars = []
            init_stars(screen)
            pygame.display.flip()
             
    # Copy image to screen:
    #screen.blit(background_image, background_position)
    screen.fill(BLACK)

    move_and_draw_stars(screen)

    #screen.blit(planets_image, background_position)
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    player_position = pygame.mouse.get_pos()
    x = player_position[0]
    y = player_position[1]
    for i in range(len(laserPosition)-1,-1,-1):
        laserPosition[i][1] -= laserSpeed
        screen.blit(projectile_image,laserPosition[i])
        if laserPosition[i][1] < -100:
            del laserPosition[i]
    # Copy image to screen:
    screen.blit(player_image, [x-64, y-64])
    printscore(screen,score)
    pygame.display.flip()
 
    clock.tick(20)
     
 
pygame.quit ()