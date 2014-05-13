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
import pyganim
import random
from constants import *

class Asteroid(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    speed = 0
    points = 0

    def __init__(self, speed, points, image):
        pygame.sprite.Sprite.__init__(self)
        self.animation = pyganim.PygAnimation.getCopy(image)
        self.animation.rotate(random.randint(-90, 90))
        self.speed = speed
        self.points = points
        if not random.randint(0, 4):
            self.animation.reverse()
        self.animation.play()
        self.animation.rate = random.uniform(.5, 2.5)
        self.image = self.animation.getCurrentFrame()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.radius = self.rect.height/3.5

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = random.randrange(-300, -100)
        self.rect.x = random.randrange(100, SCREEN_WIDTH-100)

    def update(self, events, game):
        """ Automatically called when we need to move the block. """
        self.rect.y += self.speed
        self.image = self.animation.getCurrentFrame()
        hit_list = pygame.sprite.spritecollide(game.player, game.enemy_list, True, collided=pygame.sprite.collide_mask)

        for hit in hit_list:
                game.player.life -= 1
                # You can do something with "block" here.)

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    bullet_list = None
    life = 5

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_list = pygame.sprite.Group()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.radius = self.rect.height//2

    def shoot(self, game):
        if len(self.bullet_list) < 3:
            bullet = Bullet(game.loader.BULLET_IMAGE)
            # Set the bullet so it is where the player is(and centered)
            bullet.rect.center = self.rect.center
            # Add the bullet to the lists
            #pygame.Surface.fill(self.bullet.image,RED)
            game.all_sprites_list.add(bullet)
            self.bullet_list.add(bullet)
            #Play Bullet sound
            game.loader.SOUND_BULLET_FIRE.play()

    def update(self, events, game):
        """ Update the player location. """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                self.shoot(game)

        for bullet in self.bullet_list:
                # check if the lasers(bullet) hit anything in the block list(enemies)
                bullet_hit_list = pygame.sprite.spritecollide(bullet, game.enemy_list, True, collided=pygame.sprite.collide_mask)

                for enemy in bullet_hit_list:
                    bullet.kill()
                    game.score += enemy.points

        self.rect.center = pygame.mouse.get_pos()           # center player to mouse
        self.rect.y = SCREEN_HEIGHT-130                     # lock player to bottom of screen


class Bullet(pygame.sprite.Sprite):
    speed = 0

    """ This Class Represents a Bullet"""
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.radius = 5
        self.speed = 8

    def update(self, events, game):
        """Move Bullet"""
        self.rect.y -= self.speed
        if self.rect.y < -60:
            self.kill()

if __name__ == "__main__":
    pass