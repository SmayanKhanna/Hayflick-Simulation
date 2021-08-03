import itertools
import pygame
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation

pygame.init()

#Clock
clock = pygame.time.Clock()

#Sprites
Male_Cell = pygame.image.load('Male.png')
Female_Cell = pygame.image.load('Female.png')
Viral_Cell = pygame.image.load('Virus.png')

#Variables:
run = True
screen_width = 1280
screen_height = 720

#Colours
gray = (125,125,125)
white = (255,255,255)
black = (0,0,0)

#fonts
title_font = pygame.font.SysFont('Helvetica',40)
button_font = pygame.font.SysFont('Helvetica',20)

#Graphing
xVal = []
yVal = []

index = count()

def animate(i):
    xVal.append(next(index))
    yVal.append(pygame.time.get_ticks())
    plt.plot(xVal,yVal)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Hayflick Simulation')

class Virus(object):

    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.vel = 10
        self.angle = angle
        self.visible = True
        self.seen = pygame.draw.circle(screen, white, (self.x + 15, self.y + 15), 80, 3)
        self.hitbox = pygame.Rect(self.x, self.y, 30, 30)
        self.velocity = 10
        self.Is_Collide = False

    def move(self):
        if self.Is_Collide == False:
            self.x += self.vel

    def draw(self,screen):
        self.move()
        # pygame.draw.circle(screen, white, (self.x + 15, self.y + 15), 80, 3)
        # pygame.draw.rect(screen, black, self.hitbox, 2)

        if self.visible:
            Viral = pygame.transform.scale(Viral_Cell, (30, 30))
            screen.blit(Viral,(self.x,self.y))

class Male_Fibroblasts(object):

    def __init__(self, x, y, age, ID):
        self.color = (0,0,125)
        self.x = x
        self.y =y
        self.age = age + random.choice(np.arange(0.0, 2.0, 0.1))
        self.ID = ID
        self.visible = True
        self.count = 0
        self.hitbox = pygame.Rect(self.x, self.y, 30, 30)
        self.seen = pygame.draw.circle(screen, white, (self.x + 15, self.y + 15), 50, 3)

    def draw(self,screen):
        # pygame.draw.circle(screen, white, (self.x + 15, self.y + 15), 50, 3)

        # pygame.draw.rect(screen,white, self.seen, 2)
        # pygame.draw.rect(screen, white, self.hitbox, 2)
        if self.visible:
            Male = pygame.transform.scale(Male_Cell, (30, 30))
            screen.blit(Male,(self.x,self.y))

    def tick(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.age * 1000:
            self.visible = False

class Female_Fibroblasts(object):
    def __init__(self, x, y,age,ID):
        self.x = x
        self.y =y
        self.ID = ID
        self.color = (255, 105, 180)
        self.age = age + random.choice(np.arange(0.0, 2.0, 0.1))
        self.visible = True
        self.count = 0
        self.hitbox = pygame.Rect(self.x, self.y, 30, 30)
        self.seen = pygame.draw.circle(screen, white, (self.x + 15, self.y + 15), 50, 3)

    def draw(self,screen):
        # pygame.draw.circle(screen, white, (self.x + 15, self.y + 15), 50, 3)
        # pygame.draw.rect(screen, white, self.hitbox, 2)
        if self.visible:
            Female = pygame.transform.scale(Female_Cell, (30, 30))
            screen.blit(Female, (self.x, self.y))

    def tick(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.age * 1000:
            self.visible = False
            self.count += 1


def draw(screen):
    screen.fill(white)

    pygame.draw.circle(screen, gray, (640, 360), 300)

    Title = title_font.render('Hayflick Simulation',1, black)
    Female_Option = button_font.render('Female Cells',1,black)
    Male_Option = button_font.render('Male Cells', 1, black)

    all_cells = Male_Cells + Female_Cells
    for cell1, cell2 in itertools.combinations(all_cells, 2):

        hitbox1 = pygame.Rect(cell1.x,cell1.y,30,30)
        hitbox2 = pygame.Rect(cell2.x,cell2.y,30,30)
        cell1.draw(screen)
        cell2.draw(screen)
        is_collide = hitbox1.colliderect(hitbox2)
        cell1.tick()
        cell2.tick()
        if is_collide:
            cell1.x += 10
            cell2.x -= 10
        # game_time = pygame.time.get_ticks()
        # if game_time > cell1.age * 1000:
        #     all_cells.pop(2)

    for virus in ViralCells:
        virus.draw(screen)

    screen.blit(Title, (500, 20))
    virus1.draw(screen)
    pygame.display.update()

#drawing multiple

Male_Cells = []
Female_Cells = []
position_male = []
position_female = []
ID_Male = 0
ID_Female = 20
lag_delay = 3

for count in range(20):
    ID_Male += 1
    ID_Female += 1
    position_male = [random.randint(440,840),random.randint(160,560)]
    position_female = [random.randint(440,840),random.randint(160,560)]

    Male_Cells.append(Male_Fibroblasts(position_male[0],position_male[1],10+lag_delay,ID_Male))
    Female_Cells.append(Female_Fibroblasts(position_female[0], position_female[1], 12+lag_delay, ID_Female))

#important variables
male_count = len(Male_Cells)
female_count = len(Female_Cells)
virus1 = Virus(300,300,30)
ViralCells = []
all_cells = Male_Cells + Female_Cells
cell_proximity = []
collide_count = 0


# for cell in all_cells:
#     hitbox_Cell_Viral = pygame.Rect(cell.x, cell.y, 30, 30)
#     hitbox_Viral_Cell = pygame.Rect(virus1.x, virus1.y, 30, 30)
#     collision = hitbox_Viral_Cell.colliderect(hitbox_Cell_Viral)
#     dist = math.sqrt((cell.x - virus1.x) ** 2 + (cell.y - virus1.y) ** 2)
#     cell_proximity.append(dist)
#     if collision:
#         virus1.Is_Collide = True
#         collide_count+= 1
#         print(collide_count)
#         virus1.x += (cell.x - virus1.x)/2
#         virus1.y += (cell.y - virus1.y)/2

        # virus_displacement_x = random.randint(1, 100)
        # virus_displacement_y = random.randint(1, 100)
        # ViralCells.append(Virus(virus1.x + virus_displacement_x, virus1.y, 50))
    # else:
    #     virus1.x += 10

#game loop
while run:

    clock.tick(27)

    draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for cell in all_cells:
        hitbox_Cell_Viral = pygame.Rect(cell.x, cell.y, 30, 30)
        hitbox_Viral_Cell = pygame.Rect(virus1.x, virus1.y, 30, 30)
        collision = hitbox_Viral_Cell.colliderect(hitbox_Cell_Viral)
        dist = math.sqrt((cell.x - virus1.x) ** 2 + (cell.y - virus1.y) ** 2)
        cell_proximity.append(dist)
        if collision:
            virus1.Is_Collide = True
            virus1.x += (cell.x - virus1.x) / 2
            virus1.y += (cell.y - virus1.y) / 2
            all_cells.pop(cell.ID)
            if virus1.x == cell.x:
                virus1.Is_Collide = False

        # if collision == True:
        #     print("collide")
        #     virus1.x += (cell.x - virus1.x)/10
        #     virus1.y += (cell.y - virus1.y)/10
            # virus_displacement_x = random.randint(1,100)
            # virus_displacement_y = random.randint(1,100)
            #
            # ViralCells.append(Virus(virus1.x + virus_displacement_x, virus1.y, 50))
        # else:
        #     virus1.x += 1

pygame.quit()