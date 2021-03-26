# This is a sample Python script.

import pygame
import turtle
import numpy

# Game = Labyrinth(25, 1, 1)

def gridConstruct():
    with open("grid.txt", 'rt') as gridFile:
        #platzhalter1 = int(gridFile.readline())
        #platzhalter2 = int(gridFile.readline())
        grid = []
        grid = gridFile.read().splitlines()
    return grid

def waendeLesen():
    with open("spielfeld.txt", 'rt') as file:
        # X dimension of field
        x_dimension = int(file.readline())
        # Y dimension of field
        y_dimension = int(file.readline())
        # Read rows and create always a new array until \n/line breaks come in
        rows = file.read().splitlines()
        cols = []
        for line in rows:
            # splitlines() creates string arrays
            # convert array values from type string to int
            lineToInt = list(map(int, line.split()))
            cols.append(lineToInt)
        waende = cols
        print(waende)

    return [waende, x_dimension, y_dimension]


def waendeAufbauen(screen, blockSize):
    [spielFeldWaende, xD, yD] = waendeLesen()
    WEISS = (255, 255, 255)

    for rIdx, rVal in enumerate(spielFeldWaende):
        for cIdx, cVal in enumerate(rVal):
            if spielFeldWaende[rIdx][cIdx] == 1:
                pygame.draw.rect(screen, CYAN, [cIdx * blockSize, rIdx * blockSize, blockSize, blockSize], 0)
            elif spielFeldWaende[rIdx][cIdx] == 0:
                pygame.draw.circle(screen, WEISS, [cIdx * blockSize + 15, rIdx * blockSize + 15], 5, 0)

    return spielFeldWaende


def baueDasSpielfeldAuf(captionString):
    pygame.init()
    screen = pygame.display.set_mode((800, 1000))
    pygame.display.set_caption(captionString)
    # hier kommen dann die ganzen Waende
    waende = waendeAufbauen(screen, 30)
    return [screen, waende]


def eventChecker(eSpeed):
    lspielaktiv = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lspielaktiv = False
            print("Spieler hat Quit-Button angeklickt")
    return lspielaktiv


def setstartpoint(screen, x, y):
    pygame.draw.circle(screen, (0, 128, 0), [x * 30 + 15, y * 30 + 15], 5, 0)

def setendpoint(screen, x, y):
    pygame.draw.circle(screen, (255, 0, 0), [x * 30 + 15, y * 30 + 15], 5, 0)

def paint_Robot(screen, x, y):
    pygame.draw.circle(screen, (0, 0, 255), [x * 30 + 15, y * 30 + 15], 5, 0)


xstart = 2
ystart = 17
xEnd = 1
yEnd = 1

def _depthSearch(visited, x, y):
    visited[y][x] = True
    if x == xEnd and y == yEnd:
        print("YEEEEEEEEEEEEEEEEEEEEEEES")
        pygame.time.wait(5000)
        exit()
        #screenMain.exitonclick()
    #paint_blob(x, y, red)
    paint_Robot(screenMain, x, y)
    print("Visited " + str(x) + ", " + str(y) + ".")
    pygame.time.wait(100)
    if y - 1 >= 1 and loadGrid[y - 1][x] != "1" and not visited[y - 1][x]:
        _depthSearch(visited, x, y - 1)
    if x + 1 < 25 and loadGrid[y][x + 1] != "1" and not visited[y][x + 1]:
        _depthSearch(visited, x + 1, y)
    if x - 1 >= 1 and loadGrid[y][x - 1] != "1" and not visited[y][x - 1]:
        _depthSearch(visited, x - 1, y)
    if y + 1 < 25 and loadGrid[y + 1][x] != "1" and not visited[y + 1][x]:
        _depthSearch(visited, x, y + 1)


def depthSearch():
    visited = []
    for i in range(len(loadGrid)):
        l = []
        for j in range(len(loadGrid[0])):
            l.append(False)
        visited.append(l)
    _depthSearch(visited, xstart, ystart)


if __name__ == '__main__':

    # hier kommen alle meine Definitionen
    ROT = (255, 0, 0)
    SCHWARZ = (0, 0, 0)
    CYAN = (0, 255, 255)
    loadGrid = []
    loadGrid = gridConstruct()
    print(loadGrid)

    # hier kommt das erste Spielfeld
    screenMain, waende = baueDasSpielfeldAuf("Pathfinder")

    #print(waende[ystart][xstart])
    #res = self.WALLS[self.y_start][self.x_start]
    #if res == 1:

    setstartpoint(screenMain, xstart, ystart)
    setendpoint(screenMain, xEnd, yEnd)

    # print(waende[ystart][xstart])
    # exit()
    # solange die Variable True ist, soll das Spiel laufen
    spielaktiv = True
    speed = 30
    clock = pygame.time.Clock()

    while spielaktiv:

        spielaktiv = eventChecker(speed)

        pygame.display.update()  # ohne update wartet er, loescht es dann und macht erst am Ende ein update
        if spielaktiv:
            clock.tick(10)
        else:
            pygame.time.wait(100)
        depthSearch()
        pygame.display.update()

    pygame.quit()