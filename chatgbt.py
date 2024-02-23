#!/usr/bin/env python3
from math import pi, sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg
import numpy as np
import math

ANTS = 300              # Number of Ants to spawn
WIDTH = 1200            # default 1200
HEIGHT = 800            # default 800
FPS = 30                # 48-90
VSYNC = True            # limit frame rate to refresh rate
PRATIO = 5              # Pixel Size for Pheromone grid, 5 is best
SHOWFPS = True          # show framerate debug
nest = (WIDTH/3, HEIGHT/2)


class Ant(pg.sprite.Sprite):
    def __init__(self, drawSurf, nest, pheroLayer):
        super().__init__()
        self.drawSurf = drawSurf
        self.curW, self.curH = self.drawSurf.get_size()
        self.pgSize = (int(self.curW/PRATIO), int(self.curH/PRATIO))
        self.isMyTrail = np.full(self.pgSize, False)
        self.phero = pheroLayer
        self.nest = nest
        self.image = pg.Surface((12, 21)).convert()
        self.image.set_colorkey(0)
        cBrown = (100,42,42)
        # Draw Ant
        pg.draw.circle(self.image, cBrown, (6, 5), 5)
        # save drawing for later
        self.orig_img = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=self.nest)
        self.ang = randint(0, 360)
        self.desireDir = pg.Vector2(cos(radians(self.ang)),sin(radians(self.ang)))
        self.pos = pg.Vector2(self.rect.center)
        self.vel = pg.Vector2(0,0)
        self.last_sdp = (nest[0]/10/2,nest[1]/10/2)
        self.mode = 1

    def update(self, dt):  # behavior
        mid_result = left_result = right_result = [0,0,0]
        mid_GA_result = left_GA_result = right_GA_result = [0,0,0]
        randAng = randint(0,360)
        accel = pg.Vector2(0,0)
        foodColor = (0,200,0)  # color of food to look for
        wandrStr = .18  # how random they walk around
        maxSpeed = 12  # 10-12 seems ok
        steerStr = 3  # 3 or 4, dono
        # Converts ant's current screen coordinates, to smaller resolution of pherogrid.
        scaledown_pos = (int(self.pos.x/PRATIO), int(self.pos.y/PRATIO))
        # Get locations to check as sensor points, in pairs for better detection.
        mid_sens = Vec2.vint(self.pos + pg.Vector2(20, 0).rotate(self.ang))
        left_sens = Vec2.vint(self.pos + pg.Vector2(18, -8).rotate(self.ang)) # -9
        right_sens = Vec2.vint(self.pos + pg.Vector2(18, 8).rotate(self.ang)) # 9
        mid_sens = (self.pos + pg.Vector2(20, 0).rotate(self.ang))
        mid_sens = int(mid_sens[0]), int(mid_sens[1])
        left_sens = (self.pos + pg.Vector2(18, -8).rotate(self.ang))
        left_sens = int(mid_sens[0]), int(mid_sens[1])
        right_sens = (self.pos + pg.Vector2(18, 8).rotate(self.ang))
        right_sens = int(mid_sens[0]), int(mid_sens[1])

        if self.drawSurf.get_rect().collidepoint(mid_sens):
            mspos = (mid_sens[0]//PRATIO,mid_sens[1]//PRATIO)
            mid_result = self.phero.img_array[mspos]
            mid_GA_result = self.drawSurf.get_at(mid_sens)[:3]
        if self.drawSurf.get_rect().collidepoint(left_sens):
            left_result, left_isID, left_GA_result = self.sensCheck(left_sens)
        if self.drawSurf.get_rect().collidepoint(right_sens):
            right_result, right_isID, right_GA_result = self.sensCheck(right_sens)



        if self.mode == 1:  # Look for food, or trail to food.
            setAcolor = (0,0,100)
            if scaledown_pos != self.last_sdp and scaledown_pos[0] in range(0,self.pgSize[0]) and scaledown_pos[1] in range(0,self.pgSize[1]):
                self.phero.img_array[scaledown_pos] += setAcolor
                self.isMyTrail[scaledown_pos] = True
                self.last_sdp = scaledown_pos
            if mid_result[1] > max(left_result[1], right_result[1]):
                self.desireDir += pg.Vector2(1,0).rotate(self.ang).normalize()
                wandrStr = .1
            elif left_result[1] > right_result[1]:
                self.desireDir += pg.Vector2(1,-2).rotate(self.ang).normalize() #left (0,-1)
                wandrStr = .1
            elif right_result[1] > left_result[1]:
                self.desireDir += pg.Vector2(1,2).rotate(self.ang).normalize() #right (0, 1)
                wandrStr = .1
            if left_GA_result == foodColor and right_GA_result != foodColor :
                self.desireDir += pg.Vector2(0,-1).rotate(self.ang).normalize() #left (0,-1)
                wandrStr = .1
            elif right_GA_result == foodColor and left_GA_result != foodColor:
                self.desireDir += pg.Vector2(0,1).rotate(self.ang).normalize() #right (0, 1)
                wandrStr = .1
            elif mid_GA_result == foodColor: # if food
                self.desireDir = pg.Vector2(-1,0).rotate(self.ang).normalize() #pg.Vector2(self.nest - self.pos).normalize()
                #self.lastFood = self.pos + pg.Vector2(21, 0).rotate(self.ang)
                maxSpeed = 5
                wandrStr = .01
                steerStr = 5
                self.mode = 2

        elif self.mode == 2:  # Once found food, either follow own trail back to nest, or head in nest's general direction.
            setAcolor = (0,80,0)
            if scaledown_pos != self.last_sdp and scaledown_pos[0] in range(0,self.pgSize[0]) and scaledown_pos[1] in range(0,self.pgSize[1]):
                self.phero.img_array[scaledown_pos] += setAcolor
                self.last_sdp = scaledown_pos
            if self.pos.distance_to(self.nest) < 24:
                #self.desireDir = pg.Vector2(self.lastFood - self.pos).normalize()
                self.desireDir = pg.Vector2(-1,0).rotate(self.ang).normalize()
                self.isMyTrail[:] = False #np.full(self.pgSize, False)
                maxSpeed = 5
                wandrStr = .01
                steerStr = 5
                self.mode = 1
            else: 
                self.desireDir = pg.Vector2(self.nest - self.pos).normalize()

    

        # Avoid edges
        if not self.drawSurf.get_rect().collidepoint(left_sens) and self.drawSurf.get_rect().collidepoint(right_sens):
            self.desireDir += pg.Vector2(0,1).rotate(self.ang) #.normalize()
            wandrStr = .01
            steerStr = 5
        elif not self.drawSurf.get_rect().collidepoint(right_sens) and self.drawSurf.get_rect().collidepoint(left_sens):
            self.desireDir += pg.Vector2(0,-1).rotate(self.ang) #.normalize()
            wandrStr = .01
            steerStr = 5
        elif not self.drawSurf.get_rect().collidepoint(Vec2.vint(self.pos + pg.Vector2(21, 0).rotate(self.ang))):
            self.desireDir += pg.Vector2(-1,0).rotate(self.ang) #.normalize()
            maxSpeed = 5
            wandrStr = .01
            steerStr = 5

        randDir = pg.Vector2(cos(radians(randAng)),sin(radians(randAng)))
        self.desireDir = pg.Vector2(self.desireDir + randDir * wandrStr).normalize()
        dzVel = self.desireDir * maxSpeed
        dzStrFrc = (dzVel - self.vel) * steerStr

        self.vel = self.vel + dzStrFrc * dt
        self.pos += self.vel * dt
        # actually update position
        self.rect.center = self.pos

    def sensCheck(self, pos): #, pos2): # checks given points in Array, IDs, and pixels on screen.
        sdpos = (int(pos[0]/PRATIO),int(pos[1]/PRATIO))
        array_r = self.phero.img_array[sdpos]
        ga_r = self.drawSurf.get_at(pos)[:3]
        return array_r, self.isMyTrail[sdpos], ga_r
    
class PheroGrid():
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0]/PRATIO), int(bigSize[1]/PRATIO))
        self.image = pg.Surface(self.surfSize).convert()
        self.img_array = np.array(pg.surfarray.array3d(self.image),dtype=float)#.astype(np.float64)
    def update(self, dt):
        self.img_array -= .6 * (60/FPS) * ((dt/10) * FPS) #[self.img_array > 0] # dt might not need FPS parts
        self.img_array = self.img_array.clip(0,255)
        pg.surfarray.blit_array(self.image, self.img_array)
        return self.image
    
class Vec2():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def vint(self):
		return (int(self.x), int(self.y))

def main():
    pg.init()  # prepare window
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED, vsync=VSYNC)

    cur_w, cur_h = screen.get_size()
    screenSize = (cur_w, cur_h)
    nest = (cur_w/3, cur_h/2)
    food_sources = []
    workers = pg.sprite.Group()
    pheroLayer = PheroGrid(screenSize)

    for n in range(ANTS):
        workers.add(Ant(screen, nest, pheroLayer))

    foods = pg.sprite.Group()
    font = pg.font.Font(None, 30)
    clock = pg.time.Clock()
    # main loop
    go = True
    while go:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                go = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mousepos = pg.mouse.get_pos()
                if event.button == 1:
                    food_sources.append((mousepos[0] // PRATIO, mousepos[1] // PRATIO))
     
                if event.button == 3:
                    for source in food_sources:
                        if math.dist(mousepos, (source[0] * PRATIO, source[1] * PRATIO)) < 15:
                            food_sources.remove(source)

        dt = clock.tick(FPS) / 100
        pheroImg = pheroLayer.update(dt)
        workers.update(dt)
        screen.fill(0) # fill MUST be after sensors update, so previous draw is visible to them

        rescaled_img = pg.transform.scale(pheroImg, (cur_w, cur_h))
        pg.Surface.blit(screen, rescaled_img, (0,0))

        #workers.update(dt)  # enable here to see debug dots
        foods.draw(screen)

        pg.draw.circle(screen, [40,10,10], (nest[0],nest[1]+6), 6, 3)
        pg.draw.circle(screen, [50,20,20], (nest[0],nest[1]+4), 9, 4)
        pg.draw.circle(screen, [60,30,30], (nest[0],nest[1]+2), 12, 4)
        pg.draw.circle(screen, [70,40,40], nest, 16, 5)

        for food in food_sources:
            pg.draw.circle(screen, (0, 200, 0), (food[0] * PRATIO, food[1] * PRATIO), 40)
        workers.draw(screen)

        if SHOWFPS : screen.blit(font.render(str(int(clock.get_fps())), True, [0,200,24]), (8, 8))

        pg.display.update()

if __name__ == '__main__':
    main()  