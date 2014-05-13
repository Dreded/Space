#-------------------------------------------------------------------------------
# Name:        Loader for Space Ace
# Purpose:      Make easy access to loaded files
#
# Author:      Dreded
#
# Created:     5/11/14
# Program:     PyCharm Community Edition
# Copyright:   (c) Dreded 2014
#-------------------------------------------------------------------------------
import pygame


class Loader(object):
    def __init__(self):
        self.PLAYER_IMAGE = pygame.image.load("sprites/starship.png").convert_alpha()

        self.BULLET_IMAGE = pygame.image.load("sprites/projectile.png").convert_alpha()

        self.PLANET_IMAGE = pygame.image.load("sprites/planets.png").convert_alpha()

        self.ASTEROID_ANIMATION = [(pygame.image.load('sprites/Asteroid/Asteroid 01-.%d.png' % (i+1)).convert_alpha()) for i in range(60)]
        #UFO_ANIMATION.smoothscale((64,64))
        #self.UFO_ANI.rotate(45)  # rotate 45 degrees so surface is large enough when we rotate later
        #UFO_ANI.makeTransformsPermanent()  # this makes it so our animation surface is actually the new scaled size
        #UFO_ANI.convert_alpha()

        #Open Sounds
        self.SOUND_START = pygame.mixer.Sound("music/start.ogg")
        self.SOUND_START.set_volume(.5)

        self.SOUND_ENGINE_HUM = pygame.mixer.Sound("sounds/enginehum.ogg")
        self.SOUND_ENGINE_HUM.set_volume(1)

        self.SOUND_BULLET_FIRE = pygame.mixer.Sound("sounds/laser5.ogg")

        self.SOUND_ENGINE = pygame.mixer.Sound("sounds/engine_takeoff.wav")
        self.SOUND_ENGINE.set_volume(.5)

        #play sounds that will always play or only play once at beginning of game
        self.SOUND_ENGINE_HUM.play(-1)
        #self.sound_start.play()

        # #Load High Scores
        # try:
        #     with open('highscore.txt', 'r') as file:
        #         for line in file:
        #             line = line.strip()
        #             line = list(filter(None, line.split(':')))
        #             self.highscore.append(line)
        #         self.highscore.sort(key=lambda x: int(x[1]),reverse=True)
        # except:
        #     pass


    def music(track):
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)


def main():
    pass

if __name__ == "__main__":
  main()