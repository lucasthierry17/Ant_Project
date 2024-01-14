import pygame
from sys import exit
import time
import os

class Map:
    def __init__(self, width, height):
        """
        Hier wird die Größe der Karte festgelegt.
        """
        
        self.width = width
        self.height = height
        pygame.init # Initialisiere Pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Ants')
        self.clock = pygame.time.Clock() # Clock Object
        self.color = [255, 255, 255]
        # Creating a white background
        
        self.screen.fill(self.color)
    def ant_nest():
        """
        Nest wird zufällig auf der Karte platziert und enthält alle Ameisen.
        Die Anzahl an Ameisen können mittels eines Inputs festgelegt werden.
        """
        pass

    def food_source():
        """
        Die Nahrungsquellen werden ebenfalls zufällig auf der Karte platziert.
        Man kann ein int mitangeben um die Anzahl an Nahrungsquellen festzulegen.
        Außerdem wird die "Lebenszeit" der Nahrungsquelle bestimmt. Also wie viele Ameisen braucht es bis die Nahrungsquelle aufgebraucht ist.
        """
        pass

    def obstacle():
        """
        Die Nahrungsquellen werden ebenfalls zufällig auf der Karte platziert.
        Man kann ein int mitangeben um die Anzahl an Nahrungsquellen festzulegen.
        """
    
    def visualize(self):
        '''In tthis function, all the elements will be drawn on the map.'''
        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()
            # draw all elements
            # update everything
            pygame.display.update()
            self.clock.tick(60) # 60fps
        pass

if __name__ == '__main__':

    map = Map(400,400)
    map.visualize()