#Import der benötigten Bibliotheken/Libraries
import pygame
import pygame.freetype
#import turtle
#import numpy

def gridConstruct():
    with open("grid.txt", 'rt') as gridFile:
        grid = gridFile.read().splitlines()
    return grid

#Importieren der Datei, die das Spielfeld aufbaut und einlesen der "Wände"
def waendeLesen():
    with open("spielfeld.txt", 'rt') as file:   #Datei wird importiert und mit 'rt' gelesen
        # X Werte des Labyrinths
        x_dimension = int(file.readline())
        # Y Werte des Labyrinths
        y_dimension = int(file.readline())
        # Reihen lesen und immer einen neuen Array erstellen bis zum Zeilenumbruch
        rows = file.read().splitlines()
        cols = []
        for line in rows:
            # splitlines() erzeugt string arrays
            # konvertiert die Array-Werte als "string" in einen integer-Wert (Zahlenwert)
            lineToInt = list(map(int, line.split()))
            cols.append(lineToInt)
        waende = cols
        print(waende)

    return [waende, x_dimension, y_dimension]


def buildwalls(screen, blockSize):
    [spielFeldWaende, xD, yD] = waendeLesen()
    white = (255, 255, 255)
    black = (0, 0, 0)
    cornflower = (77, 166, 255)

    for rIdx, rVal in enumerate(spielFeldWaende):
        for cIdx, cVal in enumerate(rVal):
            if spielFeldWaende[rIdx][cIdx] == 1:
                pygame.draw.rect(screen, cornflower, [cIdx * blockSize, rIdx * blockSize, blockSize, blockSize], 0)

            # Möglichkeit überall auf dem Spielfeld Punkte erscheinen zu lasen
            #elif spielFeldWaende[rIdx][cIdx] == 0:
                #pygame.draw.circle(screen, white, [cIdx * blockSize + 15, rIdx * blockSize + 15], 5, 0)

    return spielFeldWaende

def baueDasSpielfeldAuf(captionString):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption(captionString)
    # hier kommen dann die ganzen Waende
    waende = buildwalls(screen, 30)
    return [screen, waende]

def eventChecker(eSpeed):
    lspielaktiv = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lspielaktiv = False
            print("Spieler hat das Spiel beendet!")
    return lspielaktiv

def set_startpoint(screen, x, y):
    pygame.draw.circle(screen, (0, 128, 0), [x * 30 + 15, y * 30 + 15], 5, 0)

def set_endpoint(screen, x, y):
    pygame.draw.circle(screen, (255, 0, 0), [x * 30 + 15, y * 30 + 15], 5, 0)

def paint_Robot(screen, x, y):
    pygame.draw.circle(screen, (0, 0, 255), [x * 30 + 15, y * 30 + 15], 5, 0)

def paint_Robot_black(screen, x, y):
    pygame.draw.circle(screen, (255, 255, 0), [x * 30 + 15, y * 30 + 15], 5, 0)

def outputVisited(x, y):
    output_Field = str.format("X-Wert: " + str(x) + " Y-Wert: " + str(y))
    pygame.draw.rect(screenMain, (0, 0, 0), (580, 770, 300, 20))
    GAME_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 20)
    GAME_FONT.render_to(screenMain, (580, 770), output_Field, (255, 255, 255))

def shortestPath():
    FINISH_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 20)
    FINISH_FONT.render_to(screenMain, (20, 770), "Ziel erreicht!", (0, 255, 0))

def _depthSearch(visited, x, y):
    visited[y][x] = True
    if x == xEnd and y == yEnd:
        shortestPath()
        pygame.display.update()
        pygame.time.wait(3000)  # Zeit die verstreicht, wenn der Weg gefunden wurde, bis sich das Fenster wieder schließt
        exit()

    paint_Robot(screenMain, x, y)
    pygame.display.update()
    paint_Robot_black(screenMain, x, y)
    outputVisited(x, y)
    #print("Visited " + str(x) + ", " + str(y) + ".") # Ausgabe welche Punkte des Labyrinths gescannt wurden
    pygame.time.wait(setSpeed)
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


if __name__ == '__main__':  # Main-Methode: hier werden die Methoden aufgerufen und allgemeine Variablen definiert

    setSpeed = 80 # Geschwindigkeit anpassen: 500 = Langsam, 50 = schnell

    xstart = 2
    ystart = 17
    xEnd = 1
    yEnd = 1

    loadGrid = []
    loadGrid = gridConstruct()
    print(loadGrid)

    # hier kommt das  Spielfeld
    screenMain, waende = baueDasSpielfeldAuf("Pathfinder")  # Spielfeld aufbauen
    #print(waende[ystart][xstart])
    #res = self.WALLS[self.y_start][self.x_start]
    #if res == 1:
    set_startpoint(screenMain, xstart, ystart)
    set_endpoint(screenMain, xEnd, yEnd)

    # print(waende[ystart][xstart])
    # exit()

    # solange die Variable "aktiv" True ist, soll das Spiel laufen
    aktiv = True
    speed = 30
    clock = pygame.time.Clock()

    while aktiv:

        aktiv = eventChecker(speed)

        pygame.display.update()  # ohne update wartet er, löscht es dann und macht erst am Ende ein update
        if aktiv:
            clock.tick(10)
        else:
            pygame.time.wait(1000)

        depthSearch()
        pygame.display.update()

    pygame.quit()