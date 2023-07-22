import pygame
import os
import random
import math
import time
pygame.init(); pygame.mixer.init()
mel = pygame.mixer.music.load(os.path.join("balloon melody.mp3"))
width = 640
height = 480
dist_from_mid = 0
mid_aim = 0
direction = 1
dir_queue = 6
narrow = 0
bcgrx = 0
bcgr = pygame.image.load(os.path.join("balloon background.png"))
screen = pygame.display.set_mode((width, height))
widoczność = "start"
obstacles = []
testtime = time.time() + 0.1
speedtest = 0
while time.time() < testtime:
    speedtest +=1
def my_text(txt, location_x, location_y, size):
    font = pygame.font.SysFont("Monotype Corsiva", size)
    ren = font.render(txt, 1, (220, 30, 30))
    location_x = 0.5 * ( width - ren.get_rect().width)
    screen.blit(ren, (location_x, location_y))
class obstacle():
    def __init__(self, o_loc_x, o_width, dfm, nrw):
        self.o_loc_x = o_loc_x
        self.o_width = o_width
        self.y_up = 0
        self.direction = 0
        self.y_dist_from_mid = dfm
        self.narrow = nrw
        self.spread = 200 - random.randint(0, 20) - self.narrow / 2
        self.hgh_up = 240 - self.spread / 2 - self.y_dist_from_mid
        self.y_down = self.hgh_up + self.spread
        self.hgh_down = height - self.y_down
        self.color = (40, 110, 150)
        self.shape_up = pygame.Rect(self.o_loc_x, self.y_up, self.o_width,self.hgh_up)
        self.shape_down = pygame.Rect(self.o_loc_x, self.y_down, self. o_width, self.hgh_down)
        self.o_img = pygame.image.load(os.path.join("obstacle.png"))
    def drawing(self):
        screen.blit(self.o_img, (self.o_loc_x, self.hgh_up - 318))
        screen.blit(self.o_img, (self.o_loc_x, self.y_down))
    def moving(self, obst_v):
        self.o_loc_x = self.o_loc_x - obst_v
        self.shape_up = pygame.Rect(self.o_loc_x, self.y_up, self.o_width,self.hgh_up)
        self.shape_down = pygame.Rect(self.o_loc_x, self.y_down, self. o_width, self.hgh_down)
    def touching(self, plr):
        if self.shape_down.colliderect(plr) or self.shape_up.colliderect(plr): return True
        else: return False
class balon():
    def __init__(self, b_x, b_y):
        self.b_x = b_x
        self.b_y = b_y
        self.b_wht = 35
        self.b_hgh = 50
        self.shape = pygame.Rect(self.b_x, self.b_y, self.b_wht, self.b_hgh)
        self.graph = pygame.image.load(os.path.join("balon.png"))
    def drawing(self):
        screen.blit(self.graph, (self.b_x, self.b_y))
    def b_move(self, v):
        self.b_y = self.b_y + v
for create_obs in range (21):
    obstacles.append(obstacle(create_obs * width/20, width /20, dist_from_mid, narrow))
player = balon(200, 225)
bmv = 0
pygame.mixer.music.play()
while True:
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            pygame.quit(); exit()
        if evnt.type == pygame.KEYDOWN:
            if evnt.key == pygame.K_SPACE:
                if widoczność != "runda_1":
                    player.b_x = 200; player.b_y = 225; bmv = 0; widoczność = "runda_1"
                    pts = 0; speed = 200000/speedtest; bcgrx = 0
                else:
                    widoczność = "start"
                    player.b_x = 200; player.b_y = 225
            if evnt.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if evnt.key == pygame.K_LCTRL :widoczność = "game over"
    screen.fill((160, 180, 240))
    if widoczność == "start":
        my_text("Balloooon", 242, 128, 50)
        my_text("press Space to start or Esc to exit", 0, 340, 18)
        my_text("use up and down arrows to move", 1, 380, 15)
        my_text("engine speedtest: {}".format(speedtest), 1, 450, 12)
        screen.blit(player.graph, ((width - player.b_wht) / 2 , 232))
    elif widoczność == "runda_1":
        screen.blit(bcgr, (bcgrx, 0))
        for draw_obst in obstacles:
            draw_obst.moving(speed)
            draw_obst.drawing()
            if draw_obst.touching(pygame.Rect(player.b_x + 6, player.b_y + 6, player.b_wht - 12, player.b_hgh - 15)):
                draw_obst.hgh_up = 100; draw_obst.y_down = draw_obst.y_down + 100
                widoczność = "game over"
            if draw_obst.o_loc_x < - draw_obst.o_width:
                obstacles.remove(draw_obst);  obstacles.append(obstacle(width, width /20, dist_from_mid, narrow))
                pts = pts + 1
                narrow = narrow + 1
                if dir_queue < -1: dir_queue = -1
                dist_from_mid = dist_from_mid + random.randint(10, 40) / (dir_queue + 2) * direction
                if dir_queue <=0:
                    if mid_aim - dist_from_mid <= 16: dir_queue = 4; mid_aim = random.randint(0, 360) - 180
                else: dir_queue = dir_queue - 1
                if dist_from_mid > mid_aim: direction = -1
                else: direction = 1
        if evnt.type == pygame.KEYDOWN:
            if evnt.key == pygame.K_DOWN: bmv = bmv + (7000/speedtest)
            if evnt.key == pygame.K_UP: bmv = bmv - (20000/speedtest) 
        player.drawing();player.b_move(bmv); my_text("distance passed: "+str(pts) + " m",10, 5, 21)
        bmv = bmv + 5000/speedtest
        speed = speed + 200/speedtest
        bcgrx = bcgrx - speed * 0.1
    elif widoczność == "game over":
        for obst_rmv in obstacles:
            obst_rmv.hgh_up = 140
            obst_rmv.y_down = 340
        dist_from_mid = 0
        mid_aim = 0
        narrow = 0
        my_text("game over", 242, 166, 36)
        my_text("the balloon has moved " + str(pts)+" m", 274, 266, 21)
    pygame.display.update()
