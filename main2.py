#Import der benötigten Bibliotheken/Libraries
import pygame
import pygame.freetype
from tkinter import *
from tkinter import messagebox

def dimensionChecker(dim):

    if dim != 30:   #Abfrage, ob der übergebene Wert (Dimension des Labyrints) dem Wert 30 entspricht
        #print("Bitte Dimension 30 in Textdokument eingeben!")
        Tk().wm_withdraw()  #Fenster verstecken, welches sich beim Aufruf der Funktion öffnet
        messagebox.showerror('Dimension Error!', 'Bitte Dimension 30 in Textdokument eingeben!\n(Erste Zeile)') #Pop-Up Errorfenster
        pygame.quit()  #Programm beenden

#Importieren der Datei, die das Spielfeld aufbaut und einlesen der Wände
def waendeLesen():
    with open("maze.txt", 'rt') as file:   #Datei wird importiert und mit 'rt' gelesen
        dimension = int(file.readline()) #Hier wird die Dimension des Spielfeldes aus Zeile 1 eingelesen
        rows = file.read().splitlines() #Reihen lesen und immer einen neuen Array erstellen bis zum Zeilenumbruch
        cols = []   #Definieren eines neuen Arrays, in welches später die Werte geschrieben werden
        for line in rows:
            #splitlines() erzeugt string arrays
            #konvertiert die Array-Werte als "string" in einen integer-Wert (Zahlenwert)
            lineToStr = list(map(str, line.split()))
            cols.append(lineToStr)
        waende = cols #Übergabe der Werte an eine neue Variable
    return [waende, dimension]

def buildwalls(screen):
    cornflower = (77, 166, 255) #Definieren der Wandfarbe
    [labyrinthWaende, dim] = waendeLesen() #Einlesen der Dimension und der Wände
    dimensionChecker(dim) #Übergabe der Dimension und Prüfung auf Korrektheit durch Funktion

    for rIdx, rVal in enumerate(labyrinthWaende): #Zeichnen der Wände durch Blöcke in Abhängigkeit zur Dimension
        for cIdx, cVal in enumerate(rVal):
            if labyrinthWaende[rIdx][cIdx] == "1":
                pygame.draw.rect(screen, cornflower, [cIdx * dim, rIdx * dim, dim, dim], 0)

    return labyrinthWaende

def gridConstruct():
    with open("maze.txt", 'rt') as gridFile:

        placeholder = int(gridFile.readline()) #Wird benötigt um Dimension beim Einlesen zu überspringen
        grid = gridFile.read().splitlines() #Einlesen des gesamten Spielfeldes
        gridFinish = []     #Definieren eines neuen Arrays, welches als Output der for-Schleife genutzt wird
        for i in grid:      #Leerzeichen aus Spielfeld entfernen
            j = i.replace(' ', '')
            gridFinish.append(j)

    return gridFinish

def buildMaze(captionString):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption(captionString)
    #hier werden die Wände aufgebaut
    waende = buildwalls(screen)
    return [screen, waende]

def programRunning(x_start, y_start, speed):
    screenMain, waende = buildMaze("Minotaurus")  # Spielfeld aufbauen
    set_startpoint(screenMain, startpoint_X, startpoint_Y)  # Startpunkt zeichnen (Funktion aufrufen)
    activeProgram = True  #Variable, welche aussagt, ob das Programm läuft
    clock = pygame.time.Clock()  #Definieren einer neuen Zeitrechnungsvariable

    while activeProgram:  #Schleife, welche das Programm ausführt, solange activeProgram auf True steht
        active = activeChecker()  #Prüft mit dem activeChecker, ob Programm noch aktiv ist und übergibt den Wert
        pygame.display.update()  #Aktualisieren der optischen Ausgabe

        if active:
            clock.tick(10)  #Stellt die Zeit auf den Wert 10, falls Programm aktiv ist
        else:
            pygame.time.wait(1000)  #Wartezeit von einer spezifischen Anazhl an Millisekunden

        depthSearch(x_start, y_start, speed, screenMain)  #Ausführen der Tiefensuchefunktion

        pygame.display.update()  #Aktualisieren der optischen Ausgabe

def activeChecker():   #Prüft, ob das Spiel am Laufen ist, oder beendet wird
    active = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            print("Das Spiel wurde beendet!")
    return active

def set_startpoint(screen, x, y):   #Startpunkt setzen
    pygame.draw.circle(screen, (0, 128, 0), [x * 30 + 15, y * 30 + 15], 5, 0)

def paint_Robot(screen, x, y):  #Roboter zeichnen
    #Körper
    pygame.draw.circle(screen, (0, 0, 255), [x * 30 + 15, y * 30 + 15], 10, 0)
    #Augen
    pygame.draw.circle(screen, (255, 255, 255), [x * 30 + 11, y * 30 + 13], 1, 0)
    pygame.draw.circle(screen, (255, 255, 255), [x * 30 + 19, y * 30 + 13], 1, 0)
    #Mund
    pygame.draw.circle(screen, (255, 255, 255), [x * 30 + 12, y * 30 + 18], 1, 0)
    pygame.draw.circle(screen, (255, 255, 255), [x * 30 + 15, y * 30 + 18], 1, 0)
    pygame.draw.circle(screen, (255, 255, 255), [x * 30 + 18, y * 30 + 18], 1, 0)

def robot_Path(screen, x, y): #Roboter Pfad anzeigen
    pygame.draw.circle(screen, (0, 0, 0), [x * 30 + 15, y * 30 + 15], 10, 0)
    pygame.draw.circle(screen, (255, 255, 0), [x * 30 + 15, y * 30 + 15], 3, 0)

def outputVisited(screen, x, y):    #Anzeige für das besuchte Feld
    output_Field = str.format("Besuche X-Wert: " + str(x) + " und Y-Wert: " + str(y)) #Festlegen eines Strings mit übergebenen x- und y-Werten
    pygame.draw.rect(screen, (0, 0, 0), (450, 770, 400, 20)) #Übermalen des zu beschreibenden Feldes mit schwarzem Rechteck
    GAME_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 20) #Neue Schrift initialisieren
    GAME_FONT.render_to(screen, (450, 770), output_Field, (255, 255, 255)) #Schrift auf Spielfeld rendern

def printShortestPath(screen): # Anzeigen der Schrift nach erfolgreichem Finden des Ausgangs
    FINISH_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 20) #Neue Schrift initialisieren
    FINISH_FONT.render_to(screen, (20, 770), "Ziel erreicht!", (0, 255, 0)) #Schrift auf Spielfeld rendern

def shortestPath(deepArray, screenMain):
        #Bedingung, falls der Algorithmus den Endpunkt findet
        #print(deepArray)
        count = 1
        for y1 in range(len(deepArray)):
            for x1 in range(len(deepArray[0])):
                value = deepArray[y1][x1]
                if value == count:
                    pygame.draw.circle(screenMain, (0, 0, 0), [x1 * 30 + 15, y1 * 30 + 15], 10, 0)
                    pygame.draw.circle(screenMain, (255, 0, 0), [x1 * 30 + 15, y1 * 30 + 15], 6, 0)
                    pygame.time.wait(50)
                    pygame.display.update()
                    count += 1

        printShortestPath(screenMain)  #Ausführen der Funktion, welche die abschließende Ausgabe zur Folge hat
        pygame.display.update() #Aktualisieren der optischen Ausgabe
        pygame.time.wait(10000)  # Zeit die verstreicht, wenn der Weg gefunden wurde, bis sich das Fenster wieder schließt
        exit()  #Beendet das Programm an dieser Stelle (Ziel wurde erreicht)


def _depthSearch(visited, x, y, grid, speed, screenMain, deepArray, deepCounter): #Rekursives Aufrufen der Funktion
    outputVisited(screenMain, x, y)  # Funktionsaufruf um besuchten Ort anzuzeigen
    visited[y][x] = True    #Setzt das Feld auf bereits besucht
    deepArray[y][x] = deepCounter
    deepCounter += 1

    paint_Robot(screenMain, x, y) #Funktionsaufruf um Roboter zu zeichnen
    pygame.display.update() #Aktualisieren der optischen Ausgabe
    robot_Path(screenMain, x, y) #Funktionsaufruf um Roboter Laufweg zu zeichnen
    pygame.time.wait(speed) #Übergabe der in Main definierten Geschwindigkeit für Algorithmus
    if y - 1 >= 0 and grid[y - 1][x] != "1" and not visited[y - 1][x]:      #Nach oben
        if grid[y - 1][x] == "X":
            shortestPath(deepArray, screenMain)
        _depthSearch(visited, x, y - 1, grid, speed, screenMain, deepArray, deepCounter)
    if x + 1 < 35 and grid[y][x + 1] != "1" and not visited[y][x + 1]:      #Nach rechts
        if grid[y][x + 1] == "X":
            shortestPath(deepArray, screenMain)
        _depthSearch(visited, x + 1, y, grid, speed, screenMain, deepArray, deepCounter)
    if x - 1 >= 0 and grid[y][x - 1] != "1" and not visited[y][x - 1]:      #Nach links
        if grid[y][x - 1] == "X":
            shortestPath(deepArray, screenMain)
        _depthSearch(visited, x - 1, y, grid, speed, screenMain, deepArray, deepCounter)
    if y + 1 < 35 and grid[y + 1][x] != "1" and not visited[y + 1][x]:      #Nach unten
        if grid[y + 1][x] == "X":
            shortestPath(deepArray, screenMain)
        _depthSearch(visited, x, y + 1, grid, speed, screenMain, deepArray, deepCounter)

    paint_Robot(screenMain, x, y)  # Funktionsaufruf um Roboter zu zeichnen
    pygame.display.update()  # Aktualisieren der optischen Ausgabe
    robot_Path(screenMain, x, y)  # Funktionsaufruf um Roboter Laufweg zu zeichnen
    pygame.time.wait(speed)  # Übergabe der in Main definierten Geschwindigkeit für Algorithmus

    deepCounter -= 1
    deepArray[y][x] = deepCounter

def depthSearch(start_X, start_Y, speed, screenMain):
    loadGrid = []  # Definieren eines neuen Arrays, in welches das Labyrint für den Algorithmus übertragen wird
    loadGrid = gridConstruct()  # Übertragen des Labyrinths in zuvor definiertes Array
    visited = []    #Erzeugt eine Liste für spätere Verwendung
    deepArray = []
    deepCounter = 1
    for i in range(len(loadGrid)):  #Schleife geht das Array der Länge nach durch
        l = []  #Erstellen einer leeren Liste
        d = []  #Erstellen einer leeren Liste
        for j in range(len(loadGrid[0])): #In Liste "l" wird für jedes Feld des Labyrints nun der Wert False gesetzt
            l.append(False)
            d.append(0)
        visited.append(l) #Übergabe der Werte an die zuvor erstellte Liste visited
        deepArray.append(d)
    _depthSearch(visited, start_X, start_Y, loadGrid, speed, screenMain, deepArray, deepCounter) #Aufruf des rekursiven Funktionteils der Tiefensuche mit übergabe der Liste visited

if __name__ == '__main__':

    #!!! Globale Variablen werden nur für leichtere Konfiguration verwendet, es erfolgt kein Zugriff aus Funktionen !!!

    set_Speed = 30     #Geschwindigkeit anpassen: 500 = Langsam, 50 = schnell
    startpoint_X = 1    #Start und Endpunkte für das Labyrinth
    startpoint_Y = 0

    programRunning(startpoint_X, startpoint_Y, set_Speed) #Eigentliches Programm starten

    pygame.quit() #Programm beenden