import pygame
from sys import exit
import time
import os
import random
import numpy as np

WIDTH = 800
HEIGHT = 800
FOOD_LIFE_SPAN = 100
NUM_OF_ANTS = 10


class Ant:
    def __init__(self,):
        self.food = Food(WIDTH, HEIGHT)
        self.DEFAULT_ANT_SIZE = (int(0.1*WIDTH), int(0.1*HEIGHT))
            

    def looks(self):
        """
        Hier wird das Aussehen der Ameisen definiert.
        """
        self.ant = pygame.image.load("graphics/ant.png").convert_alpha()
        self.scaled_ant = pygame.transform.scale(self.ant, (int(self.DEFAULT_ANT_SIZE[0]*0.5), int(self.DEFAULT_ANT_SIZE[1]*0.5)))
        self.ant_rect = self.scaled_ant.get_rect(center = (int(WIDTH*0.5), int(HEIGHT*0.5)))
        #self.ant_rect = self.scaled_ant.get_rect(center = (int(0.5*map.WIDTH), int(0.5*map.HEIGHT)))
        return self.scaled_ant
    
    def movement(self):
        """
        Hier wird die Bewegung der Ameise festgelegt. Sie kann in allen Richtungen unendlich weit laufen
        Die Bewegung geschieht zufällig und hat vor dem Entdecken der Nahrung keine Regeln.
        Bei jeder Bewgung werden Pheromone freigesetzt, die später näher definiert werden.
        Das Nest wird zufällig auf der Karte in map.py gesetzt. Wichtig ist, dass die Ameise ihren Startpunkt kennt und dass jener in einer Variabel gespeichert wird.
        Diese Info wird nämlich später in der memory-Funktion wichtig.
        """


        pass

    def spawn_ant(self):
        '''
        Places a Rectangle on the ant, which makes it easir to move the ant around
        '''
        self.ant_rect = self.scaled_ant.get_rect(center = (int(WIDTH*0.5), int(HEIGHT*0.5)))
        return self.ant_rect
    
    def memory():
        """
        In der Erinnerung werden die wichtigsten Datenpunkte auf der Karte gespeichert:
        Die Futterquellen, Das Nest, Hindernisse etc.
        Diese werden von der Ameise entweder angepeilt oder gemieden.
        Die Erinnerung der Ameise, wird natürlich immer wieder aktualisiert, sofern sie eine neue Futterquelle entdeckt oder die bereits bekannte
        Futterquelle verbraucht ist.
        """
        pass

    def perception():
        """
        Hier wird die Wahrnehmung der Ameise festegelegt. Die Ameise kann in einem gewissen Umkreis ihre Umgebeung wahrnehmen und
        mögliche Futterquellen oder Futterkanäle identifizieren.
        Diese könnten in der memory der Ameise gespeichert werden.
        """
        pass

    def pheromone():
        """
        Die Pheromone der Ameisen legen ihren "Status" fest. Die Pheromone werden auf ihrem Pfad entlang ausgelassen:
        Status: Nahrung gefunden.
        Status: Keine Nahrung und auf der Suche nach Nahrung.

        """
        pass

    def approach():
        """
        Für Hindernisse um sie zu identifizieren???
        """
        pass

    def gohome():
        """
        Ist sehr trivial. Wie der Name schon sagt sorgt diese Funktion dafür, dass die Ameise wieder zurück in ihr Nest gelangt.
        Am besten ist der kürzeste Weg dahin.
        """
        pass

    def die():
        """
        Ist sehr trivial. Sobald die Ameise ein Hindernis nicht erkennt stirbt sie. (Mögliche Hindernisse:
        Loch, Pfütze,....)
        """
        pass

    def take_food():
        """
        Sobald die Ameise die Nahrungsquelle gefunden hat soll die Ameise, die Nahrung aufnehmen.
        Damit ändert sich der pheromonen Status und die Ameise macht sich auf den Weg ins Nest.
        """
        pass

    def follow_pheromone():
        """
        follow_pheromone macht genau das was der Name sagt. Soabld die Ameise die Pheromonen der anderen Ameisen wahrnimmt
        und diese auf den Status "Nahrung gefunden gesetzt sind", dann beginnt die Ameise dieser Spur zu folgen bis sie eine Nahrungsquelle gefunden hat
        um ihren Pheromonen Status auch zu ändern.
        """ 


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
        self.DEFAULT_IMAGE_SIZE = (self.WIDTH*0.08, self.HEIGHT*0.08)
        

        # Importing fruits
        self.green_apple = pygame.image.load("graphics/green_apple.png").convert_alpha() # for better time results
        self.red_apple = pygame.image.load(f"graphics/red_apple.png").convert_alpha() # for better time results
        self.plum = pygame.image.load(f"graphics/plum.png").convert_alpha() # for better time results

        self.food = [self.green_apple, self.red_apple, self.plum]
        self.scaled_food = [pygame.transform.scale(food, self.DEFAULT_IMAGE_SIZE) for food in self.food]


    def food_sources(self, food_life_span = FOOD_LIFE_SPAN):

        # Food will be spawnd randomly on window, using different screens for each food_source
        self.x = random.randint(0, self.WIDTH - 100)
        self.y = random.randint(0, self.HEIGHT - 100)
        self.position = (self.x, self.y)
    
        #self.food_rects = [img.get_rect(center=self.DEFAULT_IMAGE_SIZE) for img in self.scaled_food]
        self.spawn = self.scaled_food[random.randint(0,len(self.food)-1)]
        self.spawn_rect = self.spawn.get_rect(center=self.position)
        return self.spawn_rect
        
        # Defining a method in which the zone is definded, which will be placed in the center of each image.


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
        self.spawns = Food()

        # Importing Ant
        """self.ant = pygame.image.load("graphics/ant.png").convert_alpha()
        self.scaled_ant = pygame.transform.scale(self.ant, (int(self.spawns.DEFAULT_IMAGE_SIZE[0]*0.5), int(self.spawns.DEFAULT_IMAGE_SIZE[1]*0.5)))
        self.ant_rect = self.scaled_ant.get_rect(center = (int(0.5*self.WIDTH), int(0.5*self.HEIGHT)))"""

        self.ant = Ant()

    def ant_nest(self, num_ants=NUM_OF_ANTS):
        """
        Nest wird zufällig auf der Karte platziert und enthält alle Ameisen.
        Die Anzahl an Ameisen können mittels eines Inputs festgelegt werden.
        """
        #spawning the Ants:
        for i in range(num_ants):
            self.screen.blit(self.ant.looks(), self.ant.ant_rect)
            print(f"{i}te Ameise wurde platzier")
        

    def obstacle():
        """
        Die Nahrungsquellen werden ebenfalls zufällig auf der Karte platziert.
        Man kann ein int mitangeben um die Anzahl an Nahrungsquellen festzulegen.
        """
        pass

    def spawn_food(self):
        """
        This function spawns the food in front of a circle that symbolizes the zone of the food. 
        In That way, if an ant approches the 
        """
      
        self.spawn_position = self.spawns.food_sources()
        print(self.spawn_position)
        pygame.draw.circle(self.screen, (230, 230, 230), self.spawn_position.center, 1.5*self.spawns.DEFAULT_IMAGE_SIZE[1]) #(r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
        self.screen.blit(self.spawns.spawn,self.spawn_position)

        
        
    
    def visualize(self):
        '''In this function, all the elements will be drawn on the map.'''

        while True:
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # Spawning random food sources with right click
                    self.spawn_food()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Spawning food sources at the position of the mouse courser
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.random_fruit = self.spawns.scaled_food[random.randint(0, len(self.spawns.scaled_food) - 1)]
                    self.random_fruit_rect = self.random_fruit.get_rect(center = self.mouse_pos)
                    pygame.draw.circle(self.screen, (230, 230, 230), self.mouse_pos, 1.5*self.spawns.DEFAULT_IMAGE_SIZE[1]) #(r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
                    self.screen.blit(self.random_fruit, self.random_fruit_rect)
                
            if self.spawn_counter == 0:
                self.spawn_food()
                self.ant_nest()
                self.spawn_counter += 1
                

            pygame.display.update()
            self.clock.tick(60) # 60fps
        

if __name__ == '__main__':

    map = Map(WIDTH, HEIGHT)
    map.visualize()