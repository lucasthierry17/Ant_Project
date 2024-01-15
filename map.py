import pygame
from sys import exit
import time
import os
import random
import numpy as np

WIDTH = 1000
HEIGHT = 1000

class Food:
    """
    Die Nahrungsquellen werden ebenfalls zufällig auf der Karte platziert.
    Man kann ein int mitangeben um die Anzahl an Nahrungsquellen festzulegen.
    Außerdem wird die "Lebenszeit" der Nahrungsquelle bestimmt. Also wie viele Ameisen braucht es bis die Nahrungsquelle aufgebraucht ist.
    """

    def __init__(self, amnt_food = 1, life_span = 50, width = WIDTH, height = HEIGHT):

        self.amnt_food = amnt_food
        self.life_span = life_span
        self.WIDTH = width
        self.HEIGHT = height

        # Importing fruits
        self.green_apple = pygame.image.load("graphics/green_apple.png").convert_alpha() # for better time results
        self.red_apple = pygame.image.load(f"graphics/red_apple.png").convert_alpha() # for better time results
        self.plum = pygame.image.load(f"graphics/plum.png").convert_alpha() # for better time results
        self.food = [self.green_apple, self.red_apple, self.plum]
        self.DEFAULT_IMAGE_SIZE = (self.WIDTH*0.05, self.HEIGHT*0.05)

        # Importing Ant
        self.ant = pygame.image.load("graphics/ant.png").convert_alpha()
        self.scaled_ant = pygame.transform.scale(self.ant, self.DEFAULT_IMAGE_SIZE)

    def food_sources(self, food_life_span = 100):

        # Images need to be rescaled, acording to the size of the window
        self.scaled_food = [pygame.transform.scale(food, self.DEFAULT_IMAGE_SIZE) for food in self.food]

        # Food will be spawnd randomly on window, using different screens for each food_source
        # List that contain tuples for all the positions
        self.positions = {}
        for i in range(self.amnt_food):
            self.x = random.randint(0, self.WIDTH - 100)
            self.y = random.randint(0, self.HEIGHT - 100)
            self.position = (self.x, self.y)

            self.spawn = self.scaled_food[random.randint(0,len(self.food)-1)]
            self.positions[self.spawn] = self.position

        return self.positions


class Map:
    def __init__(self, width, height):
        """
        Hier wird die Größe der Karte festgelegt.
        """
        #Width and Height of the window
        self.WIDTH = width
        self.HEIGHT = height

        pygame.init # Initialisiere Pygame
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Ants')
        self.clock = pygame.time.Clock() # Clock Object
        
        # Creating a white background
        self.color = [255, 255, 255]
        self.screen.fill(self.color)

        #Spawned_Counter:
        self.spawn_counter = 0


    def ant_nest(self, num_ants = 100):
        """
        Nest wird zufällig auf der Karte platziert und enthält alle Ameisen.
        Die Anzahl an Ameisen können mittels eines Inputs festgelegt werden.
        """
        self.position

        pass

    def obstacle():
        """
        Die Nahrungsquellen werden ebenfalls zufällig auf der Karte platziert.
        Man kann ein int mitangeben um die Anzahl an Nahrungsquellen festzulegen.
        """
        pass

    def spawn_food(self):

        self.spawns = Food()
        self.spawn_positions = self.spawns.food_sources()
        print(self.spawn_positions)
        for fruit, position in self.spawn_positions.items():
            self.screen.blit(fruit, position)
    
    def visualize(self):
        '''In this function, all the elements will be drawn on the map.'''

        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.spawn_food()
                
            if self.spawn_counter == 0:
                self.spawn_food()
                self.spawn_counter += 1

            pygame.display.update()
            self.clock.tick(60) # 60fps
        

if __name__ == '__main__':

    map = Map(WIDTH, HEIGHT)
    map.visualize()