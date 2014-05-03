#-------------------------------------------------------------------------------
# Name:        Python Project
# Purpose:      To load files for the space game so they do not need to be reloaded every use
#
# Author:      Dreded
#
# Created:     5/2/14
# Program:     PyCharm Community Edition
# Copyright:   (c) Dreded 2014
#-------------------------------------------------------------------------------

import pygame
import pyganim


class Loader(object):

    def __init__(self):
        #Initalize music track

        self.PLAYER_IMAGE = pygame.image.load("starship.png").convert_alpha()

        self.BULLET_IMAGE = pygame.image.load("projectile.png").convert_alpha()

        self.PLANET_IMAGE = pygame.image.load("planets.png").convert_alpha()

        self.UFO_ANI = pyganim.PygAnimation([('Asteroid/Asteroid 01-.%d.png' % (i+1), .06) for i in range(60)])
        self.UFO_ANI.smoothscale((64,64))
        #self.UFO_ANI.rotate(45)  # rotate 45 degrees so surface is large enough when we rotate later
        self.UFO_ANI.makeTransformsPermanent()  # this makes it so our animation surface is actually the new scaled size
        self.UFO_ANI.convert_alpha()

        #Open Sounds
        #self.sound_start = pygame.mixer.Sound("music/start.ogg")
        #self.sound_start.set_volume(.5)

        self.sound_engine_hum = pygame.mixer.Sound("enginehum.ogg")
        self.sound_engine_hum.set_volume(1)

        self.sound_bullet_fire = pygame.mixer.Sound("laser5.ogg")

        self.sound_engine = pygame.mixer.Sound("engine_takeoff.wav")
        self.sound_engine.set_volume(.5)

        #play sounds that will always play or only play once at beginning of game
        self.sound_engine_hum.play(-1)
        #self.sound_start.play()

    def music(self,track):
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)