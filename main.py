#-------------------------------------------------------------------------------
# Name:        Space Ace
# Purpose:     A Space Game
#
# Author:      Dreded
#
# Created:     5/11/14
# Program:     PyCharm Community Edition
# Copyright:   (c) Dreded 2014
#-------------------------------------------------------------------------------
import pygame
import kezmenu
import loader
from sprites import *
import starfield
import os
from constants import *
os.environ['SDL_VIDEO_CENTERED'] = '1'


class fsm(object):
    """ A simple to use finite state machine class.
        Allows definition of multiple states, condition functions from state to state and optional callbacks
    """
    def __init__(self, states=[]):
        self._states = states
        self.currentState = None

    def start(self,startState=None):
        """ Start the finite state machine
        """
        if not startState or not (startState in [x[0] for x in self._states]):
            raise ValueError("Not a valid start state")
        self.currentState = startState

    def stop(self):
        """ Stop the finite state machine
        """
        # Bug fix 15 Dec 2012 - self.currentState should be reset, not startState - Identified by Holger Waldmann
        self.currentState = None

    def addTransition(self,fromState, toState, condition, callback=None):
        """ Add a state transition to the list, order is irellevant, loops are undetected
            Can only add a transition if the state machine isn't started.
        """
        if not self.currentState:
            raise ValueError("StateMachine already Started - cannot add new transitions")

        # add a transition to the state table
        self._states.append( (fromState, toState,condition, callback))

    def event(self, value):
        """ Trigger a transition - return a tuple (<new_state>, <changed>)
            Raise an exception if no valid transition exists.
            Callee needs to determine if the value will be consumed or re-used
        """
        if not self.currentState:
            raise ValueError("StateMachine not Started - cannot process event")

        # get a list of transitions which are valid
        self.nextStates = [ x for x in self._states\
                            if x[0] == self.currentState \
                            and (x[2]==True or (callable(x[2]) and x[2](value))) ]

        if not self.nextStates:
            raise ValueError("No Transition defined from state {0} with value '{1}'".format(self.currentState, value))
        elif len(self.nextStates) > 1:
            raise ValueError("Ambiguous transitions from state {0} with value '{1}' ->  New states defined {2}".format(self.currentState, value, [x[0] for x in self.nextStates]))
        else:
            if len(self.nextStates[0]) == 4:
                current, next, condition, callback = self.nextStates[0]
            else:
                current, next, condition = self.nextStates[0]
                callback = None

            self.currentState, changed = (next,True) \
                    if self.currentState != next else (next, False)

            # Execute the callback if defined
            if callable(callback):
                callback(self, value)

            return self.currentState, changed

    def CurrentState(self):
        """ Return the current State of the finite State machine"""
        return self.currentState


class Game():
    menu = kezmenu.KezMenu()

    def __init__(self):

        self.gamemode = fsm([('Playing', 'GameOver', lambda x: x == 'GameOver'),
                             ('MainMenu', 'Playing', lambda x: x == 'NewGame', lambda x, y: self.newgame()),
                             ('MainMenu', 'Playing', lambda x: x == 'Resume'),
                             ('Playing', 'MainMenu', lambda x: x == 'MainMenu'),
                             ('GameOver', 'Playing', lambda x: x == 'GameOver')])
        self.gamemode.start('MainMenu')

        self.menu = kezmenu.KezMenu(['SPACE ACE!', lambda: True],
                                    ['New Game', lambda: self.gamemode.event('NewGame')],
                                    ['Exit', lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))])
        self.menu.center = True  # enable horizontal menu item centering
        self.menu.color = WHITE
        self.menu.focus_color = GREEN
        self.menu.options[0]['focus_color'] = RED
        self.menu.options[0]['color'] = RED
        self.menu.options[0]['font'] = pygame.font.Font("fonts/OverdriveInline.ttf", 75)
        self.menu._fixSize()
        self.menu.center_at(SCREEN_CENTER)  # center entire menu to screen

        self.asteroid_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        self.events = None

        # Create the player
        self.player = Player(LOADER.PLAYER_IMAGE)
        self.all_sprites_list.add(self.player)
        self.player_list.add(self.player)

    def newgame(self):
        LOADER.SOUND_START.play()
        self.menu.insert(2, ['Resume Game', lambda: self.gamemode.event('Resume')])

    def quit(self):
        """Run Stuff needed before exit"""
        print("We Quit!")

    def process_events(self):
        """ Process all of the events. Return a "True" if we need to close the window. """
        self.events = pygame.event.get()
        for e in self.events:
            if e.type == pygame.QUIT:
                self.quit()
                return True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                elif self.gamemode.currentState == 'Playing':
                    if e.key == pygame.K_RETURN:
                        print("Firing Weapons")
                    elif e.key == pygame.K_ESCAPE:
                        self.gamemode.event('MainMenu')

        return False  # not done

    def run_logic(self):
        if self.gamemode.currentState == 'MainMenu':
            self.menu.update(self.events)

        elif self.gamemode.currentState == 'Playing':
            self.all_sprites_list.update(self.events, self)

    def display_frame(self, screen):
        screen.fill(BLACK)
        starfield.move_and_draw_stars(screen)

        if self.gamemode.currentState == 'MainMenu':
            pygame.mouse.set_visible(True)
            self.menu.draw(screen)
        elif self.gamemode.currentState == 'Playing':
            self.all_sprites_list.draw(screen)

        pygame.display.update()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    global LOADER  # set as global to make reference within all class's simple.
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Space Ace")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class

    LOADER = loader.Loader()
    game = Game()

    #create Starfield(background)
    starfield.init_stars(screen)

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
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    main()