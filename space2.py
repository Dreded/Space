#-------------------------------------------------------------------------------
# Name:        Python Project
# Purpose:
#
# Author:      Dreded
#
# Created:     4/26/14
# Program:     PyCharm Community Edition
# Copyright:   (c) Dreded 2014
#-------------------------------------------------------------------------------

import pygame
import random
import pyganim

#--- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Classes ---


class Block(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    block_speed = 0
    scorevalue= 0

    def __init__(self, caller, block_speed, scorevalue):
        """ Constructor, create the image of the block. """
        pygame.sprite.Sprite.__init__(self)
        self.ufo_ani = pyganim.PygAnimation.getCopy(caller.UFO_ANI)
        self.ufo_ani.rotate(random.randint(-90, 90))
        self.rect = self.ufo_ani.getRect()
        self.image = self.ufo_ani.getCurrentFrame()
        self.mask = pygame.mask.from_surface(self.image)
        #self.image.fill(RED)
        self.block_speed = block_speed
        self.scorevalue = scorevalue
        if not random.randint(0,4):
            self.ufo_ani.reverse()
        self.ufo_ani.play()
        self.ufo_ani.rate = random.uniform(.5,2.5)

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = random.randrange(-300, -100)
        self.rect.x = random.randrange(100, SCREEN_WIDTH-100)

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += self.block_speed
        self.image = self.ufo_ani.getCurrentFrame()

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    mouse = True
    bullet_list = None

    def __init__(self, caller):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_list = pygame.sprite.Group()
        self.image = caller.PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.BULLET_IMAGE = caller.BULLET_IMAGE
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self,caller):
        if len(self.bullet_list) < 3:
            bullet = Bullet(self)
            # Set the bullet so it is where the player is(and centered)
            bullet.rect.center = self.rect.center
            # Add the bullet to the lists
            #pygame.Surface.fill(self.bullet.image,RED)
            caller.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
            #Play Bullet sound
            caller.sound_bullet_fire.play()

    def update(self):
        """ Update the player location. """
        if self.mouse:
            self.rect.center = pygame.mouse.get_pos()           # center player to mouse
            self.rect.y = SCREEN_HEIGHT-130                     # lock player to bottom of screen


class Bullet(pygame.sprite.Sprite):
    speed = 0

    """ This Class Represents a Bullet"""
    def __init__(self, caller):

        #call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = caller.BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8

    def update(self):
        """Move Bullet"""
        self.rect.y -= self.speed


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    # --- Class attributes.
    # In this case, all the data we need
    # to run our game.

    # Sprite lists
    block_list = None
    all_sprites_list = None
    player = None
    player_list = None

    #Sounds
    sound_bullet_fire = None

    # Other data
    need_loader = True
    level_over = False
    level_start = False
    ticks_last = 0
    player_destination = []
    game_over = False
    start_block_speed = 2
    block_speed = start_block_speed
    start_block_count = 5
    block_count = start_block_count

    start_life = 5
    life = start_life

    level = 1
    highscore = 0
    try:
        with open('highscore.txt','r') as file:
            for line in file:
                highscore = int(line.strip())
    except:
        pass
    score = 0
    MAX_STARS = 350
    STAR_SPEED = 2
    stars = []
    currenttrack = ""
    music = None

    # --- Class methods
    # Set up the game
    def __init__(self):
        #load and inatialize level music
        self.currenttrack = "music/level%s.ogg" % (self.level % 5+1)
        pygame.mixer.music.load(self.currenttrack)
        pygame.mixer.music.play(-1)

        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()

        if self.need_loader:
            self.loader()

        # Create the block sprites
        for i in range(self.block_count):
            block = Block(self,self.block_speed,100*self.level)

            block.rect.x = random.randrange(100,SCREEN_WIDTH-100)
            block.rect.y = random.randrange(-300, SCREEN_HEIGHT//3)

            self.block_list.add(block)
            self.all_sprites_list.add(block)

        # Create the player
        self.player = Player(self)
        self.all_sprites_list.add(self.player)
        self.player_list.add(self.player)
        #pygame.mouse.set_pos([SCREEN_WIDTH/2,SCREEN_HEIGHT-130])

    def loader(self):
        self.need_loader = False

        self.PLAYER_IMAGE = pygame.image.load("starship.png").convert()
        self.PLAYER_IMAGE.set_colorkey(BLACK)

        self.BULLET_IMAGE = pygame.image.load("projectile.png").convert()
        self.BULLET_IMAGE.set_colorkey(BLACK)

        self.PLANET_IMAGE = pygame.image.load("planets.png").convert()
        self.PLANET_IMAGE.set_colorkey(BLACK)

        self.UFO_ANI = pyganim.PygAnimation([('Asteroid/Asteroid 01-.%d.png' % (i+1), .06) for i in range(60)])
        self.UFO_ANI.smoothscale((64,64))
        #self.UFO_ANI.rotate(45)  # rotate 45 degrees so surface is large enough when we rotate later
        self.UFO_ANI.makeTransformsPermanent()  # this makes it so our animation surface is actually the new scaled size
        self.UFO_ANI.convert()
        #self.UFO_ANI.set_colorkey(BLACK)  # removed because for some odd reason causes missing transparency issues

        #Open Sounds
        self.sound_engine_hum = pygame.mixer.Sound("enginehum.ogg")
        self.sound_engine_hum.set_volume(1)
        self.sound_bullet_fire = pygame.mixer.Sound("laser5.ogg")
        self.sound_engine = pygame.mixer.Sound("engine_takeoff.wav")
        self.sound_engine.set_volume(.5)

        self.sound_engine_hum.play(-1)

    def init_stars(self, screen):
      """ Create the starfield """
      for i in range(self.MAX_STARS):
        # A star is represented as a list with this format: [X,Y,speed]
        star = [random.randrange(0, screen.get_width() - 1),
                random.randrange(0, screen.get_height() - 1),
                random.choice([1, 2, 3])]
        self.stars.append(star)

    def move_and_draw_stars(self, screen):
      """ Move and draw the stars in the given screen """
      for star in self.stars:
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

    def printhud(self,screen):
        font = pygame.font.Font(None, 36)

        text = font.render("Score:  {:07}".format(self.score), 1, WHITE)
        textpos = text.get_rect(right=screen.get_width()-20,y=10)
        screen.blit(text, textpos)

        for life in range(self.life):
            image = pygame.transform.scale(self.player.image, (self.player.rect.width//3,self.player.rect.height//3))
            rect = image.get_rect(y=10,x=15)
            rect.x = rect.x+rect.width*life
            screen.blit(image,rect)

        text = font.render("Level: {:02}".format(self.level),1,WHITE)
        textpos = text.get_rect(left=SCREEN_WIDTH/2-text.get_rect()[0],y=10)
        screen.blit(text, textpos)

    def new_game(self):
        self.block_speed = self.start_block_speed
        self.block_count = self.start_block_count
        self.score = 0
        self.level = 1
        self.life = self.start_life
        self.game_over = False
        self.__init__()

        print(self.game_over)

    def next_level(self):
        self.player_destination = []
        self.level += 1
        if self.block_speed < 7:
            self.block_speed += 1
        self.block_count += 2
        self.level_over = False
        self.__init__()

    def level_transition(self,screen):
        if self.level_start:
            if not self.ticks_last:
                self.ticks_last = pygame.time.get_ticks()
            if not self.player.mouse:
                self.player.mouse = True
                pygame.mouse.set_pos([SCREEN_WIDTH/2,SCREEN_HEIGHT-130])

            font = pygame.font.Font("fonts/OverdriveInline.ttf", 75)
            text = font.render("GET READY!", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height())
            screen.blit(text, [center_x, center_y])

            if self.ticks_last + 1000 < pygame.time.get_ticks():
                self.level_start = False
                self.ticks_last = 0
                self.next_level()

        else:
            self.player.mouse = False
            font = pygame.font.Font("fonts/OverdriveInline.ttf", 50)
            text = font.render("LEVEL %d" % self.level, True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height())
            screen.blit(text, [center_x, center_y-40])

            text = font.render("COMPLETED!", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height())
            screen.blit(text, [center_x, center_y+30])

            center_speed = 10

            if self.player.rect.x > SCREEN_WIDTH/2-64:
                if SCREEN_WIDTH/2-64 - self.player.rect.x > center_speed:
                    self.player.rect.x -=1
                else:
                    self.player.rect.x -= center_speed
            elif self.player.rect.x < SCREEN_WIDTH // 2 - 64:
                if SCREEN_WIDTH // 2 - 64 - self.player.rect.x < center_speed:
                    self.player.rect.x +=1
                else:
                    self.player.rect.x +=center_speed
            else:
                if not self.ticks_last:  # delay moving the ship to make the sound line up better
                    self.ticks_last = pygame.time.get_ticks()
                fly_speed = 10
                if len(self.player_destination) == 0:
                    # can put stuff you only want to run once on level transition here

                    self.player_destination = [1, -200, SCREEN_HEIGHT + 200, SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 130]
                    self.sound_engine.play()
                if self.ticks_last + 400 < pygame.time.get_ticks():  # delay has happened let the ship fly
                    if self.player_destination[self.player_destination[0]] == self.player.rect.y and self.player_destination[0] != len(self.player_destination)-1:
                            self.player_destination[0] += 1
                    elif self.player_destination[self.player_destination[0]] > SCREEN_HEIGHT:
                        self.player.rect.y = self.player_destination[self.player_destination[0]]
                    elif self.player_destination[self.player_destination[0]-1] > self.player_destination[self.player_destination[0]]:
                        self.player.rect.y -= fly_speed
                    elif self.player_destination[0] == len(self.player_destination)-1 and self.player_destination[self.player_destination[0]] == self.player.rect.y:
                        self.level_start = True
                        self.ticks_last = 0
                    elif self.player_destination[self.player_destination[0]-1] < self.player_destination[self.player_destination[0]]:
                        self.player.rect.y += fly_speed//2
        self.player_list.draw(screen)

    def game_over_screen(self,screen):
        self.planet_scroll = -300
        screen.blit(self.PLANET_IMAGE, (0, self.planet_scroll))
        if self.score > self.highscore:
            self.highscore = self.score
        font = pygame.font.Font("fonts/OverdriveInline.ttf", 50)
        text = font.render("Game Over, 'Space' to restart", True, WHITE)
        x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        y = 100
        screen.blit(text, [x, y])

        text = font.render("HIGH SCORE: {:7}".format(self.highscore), True, WHITE)
        x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        y += 200
        screen.blit(text, [x, y])
        text = font.render("YOUR SCORE: {:7}".format(self.score), True, WHITE)
        x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        y += 200
        screen.blit(text, [x, y])

    def quit(self):
        with open('highscore.txt','w') as file:
            print(str(self.highscore), file=file)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over or self.level_over: # dont fir when in other screens
                    pass

                else:
                    # Fire a bullet if the user clicks the mouse button
                    self.player.shoot(self)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.new_game()

                    elif self.level_over:
                        self.next_level()
                elif event.key == pygame.K_q:
                    self.quit()
                    return True
                elif event.key == pygame.K_r:
                    self.level_over = False
                    self.game_over = False
                    self.new_game()
        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()

            # See if the player block has collided with any enemies
            blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True, collided=pygame.sprite.collide_mask)

            # Check the list of collisions.
            for block in blocks_hit_list:
                self.life -= 1
                # You can do something with "block" here.

            for bullet in self.player.bullet_list:
                # check if the lasers(bullet) hit anything in the block list(enemies)
                bullet_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True,collided=pygame.sprite.collide_mask)

                for block in bullet_hit_list:
                    self.player.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    self.score += block.scorevalue

                if bullet.rect.y < -10:  # remove bullet if it goes off screen
                    self.player.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

            if len(self.block_list) == 0 and self.life > 0:
                self.level_over = True
            elif self.life == 0:
                self.game_over = True

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BLACK)
        self.move_and_draw_stars(screen)

        if self.game_over:
            self.game_over_screen(screen)

        if self.level_over:
            self.level_transition(screen)

        if not self.game_over and not self.level_over:
            self.block_list.draw(screen)
            self.player.bullet_list.draw(screen)
            self.player_list.draw(screen)

        self.printhud(screen)

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Space Ace")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    #create Starfield(background)
    game.init_stars(screen)


    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()