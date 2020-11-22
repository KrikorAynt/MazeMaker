import pygame
import sys
import math
from random import randint
WIDTH =800
HEIGHT=800
FPS = 30

#defines object of type box that contains its own coordinates and its visited status
class box :
    def __init__(self, startx, starty, endx, endy):
        self.startx=startx
        self.starty=starty
        self.endx=endx
        self.endy=endy
        self.visited=False
#functions to draw the top, botton, left, and right of each box with any color sent
    def drawT(self, color):
        pygame.draw.line(screen, color,[self.startx,self.starty],[self.endx,self.starty],1)
    def drawB(self, color):
        pygame.draw.line(screen, color,[self.startx,self.endy],[self.endx,self.endy],1)
    def drawL(self, color):
        pygame.draw.line(screen, color,[self.startx,self.starty],[self.startx,self.endy],1)
    def drawR(self, color):
        pygame.draw.line(screen, color,[self.endx,self.starty],[self.endx,self.endy],1)

#calculates and displays the maximum size of the grid, based on the systems recursion maximum
max = math.sqrt(sys.getrecursionlimit())
print("Maximum: ", max)
#prompts user for size of grid
n=max+1
while(n>max):
    n = int(input("Size?: "))

#initializes pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Grid (Space for maze, Click to rst)")
clock = pygame.time.Clock()
#defines colors
white = [255,255,255]
black = [0,0,0]
screen.fill(white)
pygame.display.update()


#creates new box objects and draws a grid
def gridMake(n) -> list:
    screen.fill(white)
    for i in range(n):
        grid.append([])
        for j in range(n):

            #calculates where the box is
            startx = i*WIDTH/n
            starty = j*HEIGHT/n
            endx = (i+1)*WIDTH/n
            endy = (j+1)*HEIGHT/n

            #makes the box
            b=box(startx,starty,endx,endy)

            #uses box to draw the top and left of each box
            b.drawT(black)
            b.drawL(black)

            #adds box to list of boxes
            grid[i].append(b)
            grid[i][j].visited=False

            #updates to include new drawn lines
            pygame.display.update()

    #draws unnessesary lines on right and bottom of window, just because it was bothering me that the grid is technically not complete
    pygame.draw.line(screen,black,(0,800),(800,800),1)
    pygame.draw.line(screen,black,(800,0),(800,800),1)
    pygame.display.update()
   

def mazeMake(grid: list,x, y):
    track=[False,False,False,False] #this keeps track of which random options have been tried
    if grid[x][y].visited == False: #if the current box has not been visited...
        while True:
            rand = randint(1,4) #pick a number from 1 to 4...
            if track[0] and track[1] and track[2] and track[3]: #then check if all options have been tried. If no...
                return
            #...based on random number pick a side of the box and color over it with white, mark it visited, then run same method on the box on that side
            #but only if that box has also not been visited and if that side isn't off the grid
            #if the random option tried doesn't work, loops again and gets another random number until all options are tried
            #if none of the options work then go back to previous box and try a different direction
            if not track[0] and rand == 1 and y-1>=0 and grid[x][y-1].visited==False:
                grid[x][y].drawT(white)
                grid[x][y].visited=True
                pygame.display.update()
                mazeMake(grid,x,y-1)
                track[0]=True
            elif not track[1] and rand == 2 and y+1<len(grid) and grid[x][y+1].visited==False:
                grid[x][y].drawB(white)
                grid[x][y].visited=True
                pygame.display.update()
                mazeMake(grid,x,y+1)
                track[1]=True
            elif not track[2] and rand == 3 and x-1>=0 and grid[x-1][y].visited==False:
                grid[x][y].drawL(white)
                grid[x][y].visited=True
                pygame.display.update()
                mazeMake(grid,x-1,y)
                track[2]=True
            elif not track[3] and rand == 4 and x+1<len(grid) and grid[x+1][y].visited==False:
                grid[x][y].drawR(white)
                grid[x][y].visited=True
                pygame.display.update()
                mazeMake(grid,x+1,y)
                track[3]=True
            track[rand-1]=True #set the tracker for the random option to true
            



   
grid=[]         #list of lists of start and end coords of boxes
gridMake(n)
running = True
#starts running the game
while running:
        clock.tick(FPS)
        #checks what has happened in the game window
        for event in pygame.event.get():
            #if user exits, stop 
            if event.type==pygame.QUIT:
                running =False
            #if they click the mouse reset back to grid
            elif event.type == pygame.MOUSEBUTTONUP:
                grid=[] 
                gridMake(n)
            #if they press SPACE generate a new maze
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startingx, startingy = randint(0,len(grid)-1), randint(0,len(grid)-1) #randomly chooses starting coordinates for maze
                    mazeMake(grid,startingx,startingy)
              
        
#on closing window, program stops                
pygame.quit()

