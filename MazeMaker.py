import pygame
import sys
import math
from random import randint
WIDTH =800
HEIGHT=800
FPS = 30
done = False

#defines object of type box that contains its own coordinates and its visited status
class box :
    def __init__(self, startx, starty, endx, endy):
        self.startx=startx
        self.starty=starty
        self.endx=endx
        self.endy=endy
        self.visited=False
        self.dir=[]
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
w=WIDTH/n
h=HEIGHT/n
#initializes pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Grid (Space for maze, Enter to rst)")
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
            startx = i*w
            starty = j*h
            endx = (i+1)*w
            endy = (j+1)*h

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
   
#generates a random maze
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
                grid[x][y].dir.append("N")
                grid[x][y-1].dir.append("S")
                pygame.display.update()
                mazeMake(grid,x,y-1)
                track[0]=True
            elif not track[1] and rand == 2 and y+1<len(grid) and grid[x][y+1].visited==False:
                grid[x][y].drawB(white)
                grid[x][y].visited=True
                grid[x][y].dir.append("S")
                grid[x][y+1].dir.append("N")
                pygame.display.update()
                mazeMake(grid,x,y+1)
                track[1]=True
            elif not track[2] and rand == 3 and x-1>=0 and grid[x-1][y].visited==False:
                grid[x][y].drawL(white)
                grid[x][y].visited=True
                grid[x][y].dir.append("W")
                grid[x-1][y].dir.append("E")
                pygame.display.update()
                mazeMake(grid,x-1,y)
                track[2]=True
            elif not track[3] and rand == 4 and x+1<len(grid) and grid[x+1][y].visited==False:
                grid[x][y].drawR(white)
                grid[x][y].visited=True
                grid[x][y].dir.append("E")
                grid[x+1][y].dir.append("W")
                pygame.display.update()
                mazeMake(grid,x+1,y)
                track[3]=True
            track[rand-1]=True #set the tracker for the random option to true

#finds a solution for the current maze            
def mazeSolve (x,y,grid,currentPath,done):
    #adds current coordinates to the current path only if this position is not already in the path
    if ((x,y) in currentPath):
        return
    currentPath.append((x,y))
    #if the current box is the goal, save the current path because its the solution
    if (x,y) == (n-1,n-1):
        solution[:] = list(currentPath)
        currentPath.pop()
        done=True
        return done
    #based on information from the maze generation, decides next box, prioritizing E, S, N, W in that order
    while not done:
           
        if ("E" in grid[x][y].dir and (not ((x+1,y) in currentPath)) and (not done)):
            next_x = x + 1
            next_y = y 
            done = mazeSolve(next_x,next_y,grid,currentPath,done)
            
        if ("S" in grid[x][y].dir and (not ((x,y+1) in currentPath)) and (not done)):
            next_x = x 
            next_y = y + 1 
            done = mazeSolve(next_x,next_y,grid,currentPath,done)
            
        if ("N" in grid[x][y].dir and (not ((x,y-1) in currentPath)) and (not done)):
            next_x = x 
            next_y = y - 1 
            done = mazeSolve(next_x,next_y,grid,currentPath,done)

        if ("W" in grid[x][y].dir and (not ((x-1,y) in currentPath)) and (not done)):
            next_x = x - 1
            next_y = y 
            done = mazeSolve(next_x,next_y,grid,currentPath,done)
            
        currentPath.pop() 
        return done
    currentPath.pop()
    return          



   
grid=[]         #list of lists of start and end coords of boxes
solution=[]     #list of coords for the solution
gridMake(n)
running = True
counter = 0
#starts running the game
while running:
        clock.tick(FPS)
        #checks what has happened in the game window
        for event in pygame.event.get():
            #if user exits, stop 
            if event.type==pygame.QUIT:
                running =False
            #if they click the mouse reset back to grid
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    grid=[] 
                    gridMake(n)
            #if they press SPACE generate a new maze
            
                elif event.key == pygame.K_SPACE:
                    startingx, startingy = randint(0,len(grid)-1), randint(0,len(grid)-1) #randomly chooses starting coordinates for maze
                    mazeMake(grid,startingx,startingy)
                    solution=[]
                    done =False
                    mazeSolve(0,0,grid,[],done)
                    print(solution)
                    for i in solution:
                        pygame.draw.circle(screen, [255,0,0], [i[0]*w+w/2,i[1]*w+w/2],5)
                        pygame.display.update()
                    counter=counter+1
                    print(counter)              
        
#on closing window, program stops                
pygame.quit()

