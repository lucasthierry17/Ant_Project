from math import pi, sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg
import numpy as np



FLLSCRN = False         # True for Fullscreen, or False for Window
ANTS = 50               # Number of Ants to spawn
WIDTH = 1200            # default 1200
HEIGHT = 800            # default 800
FPS = 60               # frames per second (48-90)
VSYNC = True            # limit frame rate to refresh rate
PRATIO = 5              # Pixel Size for Pheromone grid, 5 is best
SHOWFPS = True          # show framerate debug
nest = (WIDTH/3, HEIGHT/2)


class Ant(pg.sprite.Sprite):
    def __init__(self, drawSurf, nest, pheroLayer):
        super().__init__()
        self.drawSurf = drawSurf
        self.pgSize = (int(WIDTH / PRATIO), int(HEIGHT / PRATIO))
        self.isMyTrail = np.full(self.pgSize, False)
        self.phero = pheroLayer
        self.image = pg.Surface((12, 21)).convert_alpha()  # Use convert_alpha() to create a surface with transparency
        self.image.fill((0, 0, 0, 0))  # Fill the surface with transparent color
        cBrown = (100, 42, 42)
        pg.draw.circle(self.image, cBrown, (6, 5), 5)  # Draw the ant with respect to the new surface
        self.orig_img = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=nest)
        self.ang = randint(0, 360) # angle for starting
        self.next_step = pg.Vector2(cos(radians(self.ang)), sin(radians(self.ang)))
        self.pos = pg.Vector2(self.rect.center)
        self.vel = pg.Vector2(0, 0)
        self.last_sdp = (nest[0] / 10 / 2, nest[1] / 10 / 2)
        self.mode = 1
        self.desireDir = pg.Vector2(cos(radians(self.ang)), sin(radians(self.ang)))


    def update(self, dt):  # behavior
        mid_result = left_result = right_result = [0,0,0]
        mid_GA_result = left_GA_result = right_GA_result = [0,0,0]
        randAng = randint(0,360)
        accel = pg.Vector2(0,0)
        foodColor = (0,255,0)  # color of food to look for
        rand_dir = .12  # how random they walk around
        maxSpeed = 12  # 10-12 seems ok
        steerStr = 4  # 3 or 4, dono
        # Converts ant's current screen coordinates, to smaller resolution of pherogrid.
        scaledown_pos = (int(self.pos.x/PRATIO), int(self.pos.y/PRATIO))
        # Get locations to check as sensor points, in pairs for better detection.
        mid_sens = Vec2.vint(self.pos + pg.Vector2(20, 0).rotate(self.ang))
        left_sens = Vec2.vint(self.pos + pg.Vector2(18, -8).rotate(self.ang)) # -9
        right_sens = Vec2.vint(self.pos + pg.Vector2(18, 8).rotate(self.ang)) # 9

        if self.drawSurf.get_rect().collidepoint(mid_sens):
            mspos = (mid_sens[0]//PRATIO,mid_sens[1]//PRATIO)
            mid_result = self.phero.img_array[mspos]
            mid_isID = self.isMyTrail[mspos]
            mid_GA_result = self.drawSurf.get_at(mid_sens)[:3]
        if self.drawSurf.get_rect().collidepoint(left_sens):
            left_result, left_isID, left_GA_result = self.sensCheck(left_sens)
        if self.drawSurf.get_rect().collidepoint(right_sens):
            right_result, right_isID, right_GA_result = self.sensCheck(right_sens)


        if self.mode == 1:  # Look for food, or trail to food.
            home_phero = (0,0,50) # color for home_pheromones
            if scaledown_pos != self.last_sdp and scaledown_pos[0] in range(0,self.pgSize[0]) and scaledown_pos[1] in range(0,self.pgSize[1]):
                self.phero.img_array[scaledown_pos] += home_phero
                self.isMyTrail[scaledown_pos] = True
                self.last_sdp = scaledown_pos
            
            if mid_result[1] > max(left_result[1], right_result[1]):
                self.desireDir += pg.Vector2(1,0).rotate(self.ang).normalize()
                rand_dir = .1
            elif left_result[1] > right_result[1]:
                self.desireDir += pg.Vector2(1,-2).rotate(self.ang).normalize() #left (0,-1)
                rand_dir = .1
            elif right_result[1] > left_result[1]:
                self.desireDir += pg.Vector2(1,2).rotate(self.ang).normalize() #right (0, 1)
                rand_dir = .1
                
            
            if left_GA_result == foodColor and right_GA_result != foodColor :
                self.desireDir += pg.Vector2(0,-1).rotate(self.ang).normalize() #left (0,-1)
                rand_dir = .1
            elif right_GA_result == foodColor and left_GA_result != foodColor:
                self.desireDir += pg.Vector2(0,1).rotate(self.ang).normalize() #right (0, 1)
                rand_dir = .1
            elif mid_GA_result == foodColor: # if food
                self.desireDir = pg.Vector2(-1,0).rotate(self.ang).normalize() #pg.Vector2(self.nest - self.pos).normalize()
                #self.lastFood = self.pos + pg.Vector2(21, 0).rotate(self.ang)
                maxSpeed = 5
                rand_dir = .01
                steerStr = 5
                self.mode = 2


        elif self.mode == 2:  # Once found food, either follow own trail back to nest, or head in nest's general direction.
            food_phero = (0,50,0) # color for food_pheromones
            pass

        # Avoid edges
        if not self.drawSurf.get_rect().collidepoint(left_sens) and self.drawSurf.get_rect().collidepoint(right_sens):
            self.desireDir += pg.Vector2(0,1).rotate(self.ang) #.normalize()
            rand_dir = .01
            steerStr = 5
        elif not self.drawSurf.get_rect().collidepoint(right_sens) and self.drawSurf.get_rect().collidepoint(left_sens):
            self.desireDir += pg.Vector2(0,-1).rotate(self.ang) #.normalize()
            rand_dir = .01
            steerStr = 5
        elif not self.drawSurf.get_rect().collidepoint(Vec2.vint(self.pos + pg.Vector2(21, 0).rotate(self.ang))):
            self.desireDir += pg.Vector2(-1,0).rotate(self.ang) #.normalize()
            maxSpeed = 5
            rand_dir = .01
            steerStr = 5

        randDir = pg.Vector2(cos(radians(randAng)),sin(radians(randAng)))
        self.desireDir = pg.Vector2(self.desireDir + randDir * rand_dir).normalize()
        dzVel = self.desireDir * maxSpeed
        dzStrFrc = (dzVel - self.vel) * steerStr
        accel = dzStrFrc if pg.Vector2(dzStrFrc).magnitude() <= steerStr else pg.Vector2(dzStrFrc.normalize() * steerStr)
        velo = self.vel + accel * dt
        self.vel = velo if pg.Vector2(velo).magnitude() <= maxSpeed else pg.Vector2(velo.normalize() * maxSpeed)
        self.pos += self.vel * dt
        self.ang = degrees(atan2(self.vel[1],self.vel[0]))
        # adjusts angle of img to match heading
        self.image = pg.transform.rotate(self.orig_img, -self.ang)
        self.rect = self.image.get_rect(center=self.rect.center)  # recentering fix
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
        self.img_array -= .2 #[self.img_array > 0] # dt might not need FPS parts
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
    # setup fullscreen or window mode
    WIDTH = 1200
    HEIGHT = 800
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED, vsync=VSYNC)
    workers = pg.sprite.Group()
    pheroLayer = PheroGrid((WIDTH, HEIGHT))

    for n in range(ANTS):
        workers.add(Ant(screen, nest, pheroLayer))
    font = pg.font.Font(None, 30)
    clock = pg.time.Clock()
    # main loop
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                return
      
        dt = clock.tick(FPS) / 100
        pheroImg = pheroLayer.update(dt)
        workers.update(dt)
        screen.fill(0) # fill MUST be after sensors update, so previous draw is visible to them
        rescaled_img = pg.transform.scale(pheroImg, (WIDTH, HEIGHT))
        pg.Surface.blit(screen, rescaled_img, (0,0))
        #workers.update(dt)  # enable here to see debug dots
        pg.draw.circle(screen, [70,40,40], nest, 16, 5)
        workers.draw(screen)

        if SHOWFPS : screen.blit(font.render(str(int(clock.get_fps())), True, [0,200,0]), (8, 8))

        pg.display.update()

if __name__ == '__main__':
    main()  # by Nik
    pg.quit() 

    
        

    