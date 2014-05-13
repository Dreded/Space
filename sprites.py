#-------------------------------------------------------------------------------
# Name:        Sprites handler for Space Ace
# Purpose:
#
# Author:      Dreded
#
# Created:     5/12/14
# Program:     PyCharm Community Edition
# Copyright:   (c) Dreded 2014
#-------------------------------------------------------------------------------
import pygame
import loader
import random
from constants import *

class Block(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    block_speed = 0
    points = 0

    def __init__(self, block_speed, points):
        """ Constructor, create the image of the block. """
        pygame.sprite.Sprite.__init__(self)
        self.ufo_ani = pyganim.PygAnimation.getCopy(loader.UFO_ANI)
        self.ufo_ani.rotate(random.randint(-90, 90))
        self.rect = self.ufo_ani.getRect()
        self.image = self.ufo_ani.getCurrentFrame()
        self.mask = pygame.mask.from_surface(self.image)
        #self.image.fill(RED)
        self.block_speed = block_speed
        self.points = points
        if not random.randint(0, 4):
            self.ufo_ani.reverse()
        self.ufo_ani.play()
        self.ufo_ani.rate = random.uniform(.5, 2.5)

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

    bullet_list = None

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_list = pygame.sprite.Group()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self, game):
        if len(self.bullet_list) < 3:
            bullet = Bullet(game.LOADER.BULLET_IMAGE)
            # Set the bullet so it is where the player is(and centered)
            bullet.rect.center = self.rect.center
            # Add the bullet to the lists
            #pygame.Surface.fill(self.bullet.image,RED)
            game.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
            #Play Bullet sound
            LOADER.SOUND_BULLET_FIRE.play()

    def update(self, events, game):
        """ Update the player location. """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                self.shoot(game)

        self.rect.center = pygame.mouse.get_pos()           # center player to mouse
        self.rect.y = SCREEN_HEIGHT-130                     # lock player to bottom of screen


class Bullet(pygame.sprite.Sprite):
    speed = 0

    """ This Class Represents a Bullet"""
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8

    def update(self):
        """Move Bullet"""
        self.rect.y -= self.speed

if __name__ == "__main__":
    pass