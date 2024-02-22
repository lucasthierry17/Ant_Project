import pygame
import numpy as np
import math
import random
from math import pi, sin, cos, atan2, radians, degrees

WIDTH, HEIGHT = 900, 600
NUM_ANTS = 10
PRATIO = 4  # Ratio between screen and phero_grid
NEST = (WIDTH // 5, HEIGHT // 4)
VSYNC = True
SHOWFPS = True
FOOD_RADIUS = 10
SPEED= 1
NEST_SIZE = 10
HOME_PHEROMONE = 200
FOOD_PHEROMONE = 100
SIZE_ANT = 3
max_distance = 0
food_sources = []


class Ants(pygame.sprite.Sprite):
    def __init__(self, drawSurf, nest, pheromones):
        super().__init__()
        self.x, self.y = nest  # Starting coordinates
        self.phero = pheromones
        self.drawSurf = drawSurf
        self.angle = random.randint(0, 360)
        self.image = pygame.Surface((12, 21), pygame.SRCALPHA)
        self.pgSize = (int(WIDTH/PRATIO), int(HEIGHT/PRATIO))

        pygame.draw.circle(self.image, (255, 0, 0), (6, 5), SIZE_ANT)  # Draw ants
        self.orig_image = pygame.transform.rotate(self.image.copy(), -90)
        self.rect = self.orig_image.get_rect(center=nest)
        self.pos = pygame.Vector2(self.rect.center)
        self.angle_range = (-8, 8)  # Range for random angle change
        self.desireDir = pygame.Vector2(np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle)))  # Direction 
        self.has_food = False # True if food, else False
        self.path_to_food = []  # List to store the path to the food source
        self.last_sdp = (NEST[0] / PRATIO, NEST[1] / PRATIO)
        self.isMyTrail = np.full(self.pgSize, False)
        self.vel = pygame.Vector2(0, 0)
        
    def update(self):
        global max_distance, SPEED
        angle = random.randint(0, 360)
        randDir = pygame.Vector2(np.cos(np.radians(angle)), np.sin(np.radians(angle)))
        random_scale = 0.11
        scaled_pos = (int(self.x / PRATIO), int(self.y / PRATIO))

        if self.has_food:
            self.update_with_food(randDir, random_scale, scaled_pos)
        else:
            #self.update_without_food(randDir, scaled_pos)
            self.trail_food(scaled_pos)
        self.move()
        self.check_boundaries()
        self.last_sdp = scaled_pos

    def trail_food(self, scaled_pos):
        mid_result = left_result = right_result = [0,0,0]
        mid_GA_result = left_GA_result = right_GA_result = [0,0,0]
        dt = 0.22
        randAng = random.randint(0, 360)
        foodColor = (0, 255, 0)
        mid_sens = Vec2.vint(self.pos + pygame.Vector2(20, 0).rotate(self.angle))
        left_sens = Vec2.vint(self.pos + pygame.Vector2(18, -8).rotate(self.angle)) # -9
        right_sens = Vec2.vint(self.pos + pygame.Vector2(18, 8).rotate(self.angle)) # 9
        wandrStr = 0.12
        maxSpeed = 12
        accel = pygame.Vector2(0,0)
        steerStr = 3
        distance = 1000
        if self.drawSurf.get_rect().collidepoint(mid_sens):
            mspos = (mid_sens[0]//PRATIO,mid_sens[1]//PRATIO)
            mid_result = self.phero.img_array[mspos]
            mid_isID = self.isMyTrail[mspos]
            mid_GA_result = self.drawSurf.get_at(mid_sens)[:3]
        if self.drawSurf.get_rect().collidepoint(left_sens):
            left_result, left_isID, left_GA_result = self.sensCheck(left_sens)
        if self.drawSurf.get_rect().collidepoint(right_sens):
            right_result, right_isID, right_GA_result = self.sensCheck(right_sens)

        setAcolor = (0,0,100)
        if scaled_pos != self.last_sdp and scaled_pos[0] in range(0,self.pgSize[0]) and scaled_pos[1] in range(0,self.pgSize[1]):
            self.phero.img_array[scaled_pos] += setAcolor
            self.isMyTrail[scaled_pos] = True
            self.last_sdp = scaled_pos
     
        if mid_result[1] > max(left_result[1], right_result[1]):
            self.desireDir += pygame.Vector2(1,0).rotate(self.angle).normalize()
            wandrStr = .1
        elif left_result[1] > right_result[1]:
            self.desireDir += pygame.Vector2(1,-2).rotate(self.angle).normalize() #left (0,-1)
            wandrStr = .1
        elif right_result[1] > left_result[1]:
            self.desireDir += pygame.Vector2(1,2).rotate(self.angle).normalize() #right (0, 1)
            wandrStr = .1
        if left_GA_result == foodColor and right_GA_result != foodColor :
            self.desireDir += pygame.Vector2(0,-1).rotate(self.angle).normalize() #left (0,-1)
            wandrStr = .1
        elif right_GA_result == foodColor and left_GA_result != foodColor:
            self.desireDir += pygame.Vector2(0,1).rotate(self.angle).normalize() #right (0, 1)
            wandrStr = .1
        for food in food_sources:
            distance = self.calculate_distance(scaled_pos, food)
        if distance < 8: # if food
            self.desireDir = pygame.Vector2(-1,0).rotate(self.angle).normalize() #pg.Vector2(self.nest - self.pos).normalize()
            #self.lastFood = self.pos + pg.Vector2(21, 0).rotate(self.ang)
            maxSpeed = 5
            wandrStr = .01
            steerStr = 5
            self.has_food = True

        randDir = pygame.Vector2(cos(radians(randAng)),sin(radians(randAng)))
        self.desireDir = pygame.Vector2(self.desireDir + randDir * wandrStr).normalize()
        dzVel = self.desireDir * maxSpeed
        dzStrFrc = (dzVel - self.vel) * steerStr
        accel = dzStrFrc if pygame.Vector2(dzStrFrc).magnitude() <= steerStr else pygame.Vector2(dzStrFrc.normalize() * steerStr)
        velo = self.vel + accel * dt
        self.vel = velo if pygame.Vector2(velo).magnitude() <= maxSpeed else pygame.Vector2(velo.normalize() * maxSpeed)
        self.pos += self.vel * dt
        self.ang = degrees(atan2(self.vel[1],self.vel[0]))
        # adjusts angle of img to match heading
        self.image = pygame.transform.rotate(self.orig_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # recentering fix
        # actually update position
        self.rect.center = self.pos

    def update_with_food(self, randDir, random_scale, scaled_pos):
        global max_distance
        distance = self.calculate_distance(scaled_pos, (NEST[0] / PRATIO, NEST[1] / PRATIO))
        if distance > max_distance:
            max_distance = distance
        if distance < (NEST_SIZE / PRATIO):
            self.has_food = False 
        elif distance > max_distance - 15:
            self.desireDir = pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize()
        else:
            self.desireDir += pygame.Vector2(NEST[0] - self.x, NEST[1] - self.y).normalize() * .08
            self.desireDir = pygame.Vector2(self.desireDir + randDir * random_scale).normalize()
            self.path_to_food.append(scaled_pos)  # Store current position in the path_to_food list
        pheromone_value = 200 * (distance / max_distance)
        if pheromone_value > 255:
            pheromone_value = 255  
        if scaled_pos != self.last_sdp:
            self.phero.img_array[scaled_pos] += (0, FOOD_PHEROMONE, 0)

    def update_without_food(self, randDir, scaled_pos):
        random_angle = random.uniform(-8, 8)
        self.desireDir = self.desireDir.rotate(random_angle)
        if food_sources:
            self.update_with_food_sources(randDir, scaled_pos)
        else:
            self.random_walk() 
            #self.adjust_direction(scaled_pos, 1)
            
        if self.last_sdp != scaled_pos:
            self.phero.img_array[scaled_pos] += (0, 0, HOME_PHEROMONE)
    
    def return_home(self):
        # Follow the reverse of the path_to_food list to return home
        while self.path_to_food:
            next_pos = self.path_to_food.pop()  # Get the next position from the path_to_food list
            self.desireDir = pygame.Vector2(next_pos[0] - self.x, next_pos[1] - self.y).normalize()  # Set direction towards next_pos
            self.move()

    def random_walk(self):
        self.desireDir = self.desireDir.rotate(random.uniform(*self.angle_range))


    def update_with_food_sources(self, randDir, scaled_pos):
        min_distance = float("inf")
        nearest_food = None
        for food in food_sources:
            distance = self.calculate_distance(scaled_pos, food)
            if distance < min_distance:
                min_distance = distance
                nearest_food = food
                if min_distance < (FOOD_RADIUS / PRATIO):
                    self.has_food = True
                elif min_distance < (FOOD_RADIUS / 2):
                    self.desireDir = pygame.Vector2(nearest_food[0] - scaled_pos[0], nearest_food[1] - scaled_pos[1]).normalize()
                else:
                    #self.adjust_direction(scaled_pos, 1)
                    self.follow_highest_pheromone(scaled_pos, 1)
    def move(self):
        self.x += self.desireDir[0] * SPEED 
        self.y += self.desireDir[1] * SPEED
        self.rect.center = (self.x, self.y)

    def check_boundaries(self):
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(self.x, self.y):
            self.turn_around()

    
    def calculate_distance(self, start, target):
        return math.sqrt((target[0] - start[0])**2 + (target[1] - start[1])**2)

    def turn_around(self):
        self.desireDir *= -1
        self.x += self.desireDir[0] * SPEED
        self.y += self.desireDir[1] * SPEED
        return self.x, self.y
    
    def follow_highest_pheromone(self, scaled_pos, channel):
        mid_sens = (self.pos + pygame.Vector2(20, 0).rotate(self.angle))
        left_sens = (self.pos + pygame.Vector2(18, -8).rotate(self.angle)) # -9
        right_sens = (self.pos + pygame.Vector2(18, 8).rotate(self.angle)) # 9
        
        mspos = (int(mid_sens[0] // PRATIO), int(mid_sens[1] // PRATIO))
        lspos = (int(left_sens[0] // PRATIO), int(left_sens[1] // PRATIO))
        rspos = (int(right_sens[0] // PRATIO), int(right_sens[1] // PRATIO))

        mid_result = self.phero.img_array[mspos]
        left_result = self.phero.img_array[lspos]
        right_result = self.phero.img_array[rspos]

        max_concentration = max(mid_result[channel], left_result[channel], right_result[channel])

        if max_concentration == mid_result[channel]:
            self.desireDir = pygame.Vector2(1,0).rotate(self.angle).normalize()
            print(self.desireDir)
            print("went middle")
        elif max_concentration == left_result[channel]:
            self.desireDir = pygame.Vector2(1,-2).rotate(self.angle).normalize() #left (0,-1)
            print("went left")
        elif max_concentration == right_result[channel]:
            self.desireDir = pygame.Vector2(1,2).rotate(self.angle).normalize() #right (0, 1)
            print("went right")


    def sensCheck(self, pos): #, pos2): # checks given points in Array, IDs, and pixels on screen.
        sdpos = (int(pos[0]/PRATIO),int(pos[1]/PRATIO))
        array_r = self.phero.img_array[sdpos]
        ga_r = self.drawSurf.get_at(pos)[:3]
        return array_r, self.isMyTrail[sdpos], ga_r


class Vec2():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def vint(self):
		return (int(self.x), int(self.y))
    
class Pheromones:
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0] / PRATIO), int(bigSize[1] / PRATIO))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)

    def update(self):
        self.img_array -= 0.3  # Evaporation rate
        self.img_array = self.img_array.clip(0, 255)  # Clip to color range
        pygame.surfarray.blit_array(self.image, self.img_array) 
        return self.image

        
def handle_mouse_input(event):
    global food_sources
    mousepos = pygame.mouse.get_pos()
    if event.button == 1:
        food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
    elif event.button == 3:
        for source in food_sources:
            if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < FOOD_RADIUS:
                food_sources.remove(source)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=VSYNC) 
    pheromones = Pheromones((WIDTH, HEIGHT))  # Creating phero grid
    ants = pygame.sprite.Group()
    global food_sources # Define food_sources locally

    for _ in range(NUM_ANTS):  # Adding num_ants
        ants.add(Ants(screen, NEST, pheromones))

    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_input(event)  # Pass event
        phero_grid = pheromones.update()
        ants.update()

        draw(screen, phero_grid, food_sources, ants)  # Pass ants as parameter
    pygame.quit()

def draw(screen, phero_grid, food_sources, ants):
    screen.fill(0)  # Fill black for the next step
    scaled_screen = pygame.transform.scale(phero_grid, (WIDTH, HEIGHT))  # Scale phero_grid back to normal screen size
    screen.blit(scaled_screen, (0, 0))  # Draw pheromone grid onto screen
    pygame.draw.circle(screen, [70, 50, 40], NEST, NEST_SIZE)  # Draw nest

    # Draw food sources
    for source in food_sources:
        pygame.draw.circle(screen, (0, 255, 0), (source[0] * PRATIO, source[1] * PRATIO), FOOD_RADIUS)  # Draw food

    ants.draw(screen)  # Draw ants directly onto the screen

    pygame.display.update()

if __name__ == "__main__":
    main()

