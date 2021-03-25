#Importieren der Libaries turtle & pygame mit den jeweiligen Funktionen
import turtle
import pygame

def waendeLesen():
    grid = open("maze.txt", "r")
    xDim = int(f.readline())  # 15
    yDim = int(f.readline())  # 10
    mSpielfeld = [[0 for i in range(xDim)] for j in range(yDim)]
    mSpielfeld [2][1] = 99
    for row in range(yDim):
        for col in range(xDim):
            mSpielfeld[row][col] = int(f.read(1))
        f.read(1)   # das NL fressen

    f.close()
    return [xDim, yDim, mSpielfeld]

def waendeAufbauen(screen, blockSize):

    [xD, yD, spielFeldWaende] = waendeLesen()
    WEISS = (255, 255, 255)

    #spielFeldWaende = [
    #    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #    [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
    #    [1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
    #    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    #    [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    #    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #]

    # zaehlen, wie viele Punkte man maximal finden kann
    maxPuntos = 0

    for rIdx, rVal in enumerate(spielFeldWaende):
        for cIdx, cVal in enumerate(rVal):
            if spielFeldWaende[rIdx][cIdx] == 1:
                pygame.draw.rect(screen, CYAN, [cIdx*blockSize, rIdx*blockSize, blockSize, blockSize], 0)
            elif spielFeldWaende[rIdx][cIdx] == 0:
                pygame.draw.circle(screen, WEISS, [cIdx*blockSize + 15, rIdx*blockSize + 15], 5, 0)
                maxPuntos += 1
    return [spielFeldWaende, maxPuntos]

def baueDasSpielfeldAuf(captionString):
    pygame.init()
    screen = pygame.display.set_mode((450, 500))
    pygame.display.set_caption(captionString)
    # hier kommen dann die ganzen Waende
    [spf, maxPuntos] = waendeAufbauen(screen, 30)
    return [screen, spf, maxPuntos]

window = turtle.Screen()
window.bgcolor("black")
window.title("Tiefensuche im Labyrinth")
window.setup(1600,900)
start_x = 15
start_y = 10
end_x = 15
end_y = 10

class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

class Green(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)

class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)

def paint_blob(x, y, blob):
    screen_x = -700 + (x * 24)
    screen_y = 400 - (y * 24)
    blob.goto(screen_x, screen_y)
    blob.stamp()

def paint_maze(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            char = grid[y][x]
            if char == "s":
                print("start x = " + str(x) )
                print("start y = " + str(y) )
            if char == "e":
                print("end x = " + str(x) )
                print("end y = " + str(y) )

            if char == "0":
                paint_blob(x, y, wall)
            if char == "e":
                paint_blob(x, y, green)
            if char == "s":
                paint_blob(x, y, red)

def _tiefensuche(visited, x, y):
    visited[y][x] = True
    if x == end_x and y == end_y:
        window.exitonclick()
    paint_blob(x, y, red)
    print("Visited " + str(x) + ", " + str(y) + ".")
    if y - 1 >= 0 and grid[y-1][x] != "0" and not visited[y-1][x]:
        _tiefensuche(visited, x, y-1)
    if x + 1 < 35 and grid[y][x+1] != "0" and not visited[y][x+1]:
        _tiefensuche(visited, x+1, y)
    if x - 1 >= 0 and grid[y][x-1] != "0" and not visited[y][x-1]:
        _tiefensuche(visited, x - 1 , y)
    if y + 1 < 35 and grid[y + 1][x] != "0" and not visited[y+1][x]:
        _tiefensuche(visited, x, y + 1)

def tiefensuche(grid):
    visited = []
    for i in range(len(grid)):
        l = []
        for j in range(len(grid[0])):
            l.append(False)
        visited.append(l)
    _tiefensuche(visited, start_x, start_y)

if __name__ == "__main__":
    wall = Wall()
    red = Red()
    green = Green()
    paint_maze(grid)
    tiefensuche()
    window.exitonclick()