import pygame
import math
import random

pygame.init()

pygame.display.set_caption("Snake")

size = 600
rows = 20
black = pygame.Color(0, 0, 0)
grey = pygame.Color(178, 178, 178)


class Head:
    rows = 20
    size = 600
    def __init__(self, start, dx = 1, dy = 0, color= (255, 0, 0)):
        self.position = start
        self.dx = 1
        self.dy = 0
        self.color = color

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)

    def draw(self, background):
        distance = self.size // self.rows
        x1 = self.position[0]
        y1 = self.position[1]

        pygame.draw.rect(background, self.color, (x1*distance+1, y1*distance+1, distance-2, distance - 2))


class Snake:
    body = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.initial = Head(position)
        self.body.append(self.initial)
        self.dx = 0
        self.dy = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dx = -1
                    self.dy = 0
                    self.turns[self.initial.position[:]] = [self.dx, self.dy]
                    
                if keys[pygame.K_RIGHT]:
                    self.dx = 1
                    self.dy = 0
                    self.turns[self.initial.position[:]] = [self.dx, self.dy]
                    

                if keys[pygame.K_UP]:
                    self.dx = 0
                    self.dy = -1
                    self.turns[self.initial.position[:]] = [self.dx, self.dy]
                    

                if keys[pygame.K_DOWN]:
                    self.dx = 0
                    self.dy = 1
                    self.turns[self.initial.position[:]] = [self.dx, self.dy]

        for i, j in enumerate(self.body):
            pos = j.position[:]
            if pos in self.turns:
                turn = self.turns[pos] 
                j.move(turn[0], turn[1]) 
                if i == len(self.body) - 1:
                    self.turns.pop(pos) 
            else:
                if j.dx == -1 and j.position[0] <= 0:
                    j.position = (j.rows -1, j.position[1])

                elif j.dx == 1 and j.position[0] >= j.rows - 1:
                    j.position = (0, j.position[1])
                elif j.dy == 1 and j.position[1] >= j.rows - 1:
                    j.position = (j.position[0], 0)
                elif j.dy == -1 and j.position[1] <= 0:
                    j.position = (j.position[0], j.rows - 1)
                else:
                    j.move(j.dx, j.dy)    
                   
    def reset(self, position):
        self.initial = Head(position)
        self.body = []
        self.body.append(self.initial)
        self.turns = {}
        self.dx = 0
        self.dy = 1

    def addToBody(self):
        fin = self.body[-1]
        lastdx, lastdy = fin.dx, fin.dy

        if lastdx == 1 and lastdy == 0:
            self.body.append(Head((fin.position[0]-1,fin.position[1])))
        elif lastdx == -1 and lastdy == 0:
            self.body.append(Head((fin.position[0]+1,fin.position[1])))
        elif lastdx == 0 and lastdy == 1:
            self.body.append(Head((fin.position[0],fin.position[1]-1)))
        elif lastdx == 0 and lastdy == -1:
            self.body.append(Head((fin.position[0],fin.position[1]+1)))
        
        self.body[-1].dx = lastdx
        self.body[-1].dy = lastdy
    

    def draw(self, background):
        for i, c in enumerate(self.body):
            if i >= 0:
                c.draw(background)
            


def newScreen(background):
    global rows, size, mysnake, food
    background.fill((0, 0, 0))
    mysnake.draw(background)
    food.draw(background)
    pygame.display.update()

def randomFood(rows, snack):
 
    poses = snack.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda a: a.position == (x,y), poses))) > 0:
            continue
        else:
            break
    return (x,y)    


running = True

window = pygame.display.set_mode((size, size))

mysnake = Snake((178, 178, 178), (20, 20))

food = Head(randomFood(rows, mysnake), color= (178, 178, 178))

fps_controller = pygame.time.Clock()

while running:
    pygame.time.delay(50)
    fps_controller.tick(10)
    mysnake.move()
    if mysnake.body[0].position == food.position:
        mysnake.addToBody()
        food = Head(randomFood(rows, mysnake), color= (178, 178, 178))
    
    for i in range(len(mysnake.body)):
            if mysnake.body[i].position in list(map(lambda a:a.position,mysnake.body[i+1:])):
                ans = "Score {}"
                print(ans.format(len(mysnake.body)))
                mysnake.reset((10,10))
                break
 
    newScreen(window)
        
pass