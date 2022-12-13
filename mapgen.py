import pygame

#Start up pygame modules
pygame.init()
#resources\
#          Diff\
#               Diff format difficulty1.png - difficulty7.png
#          Laps\
#               Laps format laps1.png - laps8.png
#          Maps\
#               Map format MAP01P.png - MAPZZP.png

#Token format:
#   [ID "XX", Diff "X", Laps "X", Notes "string"]

def openWindow(size):
    #setup display window surface
    surf = pygame.display.set_mode(size)

    #set the window name
    pygame.display.set_caption('Image')

    surf.fill((255, 255, 255))

    return surf

#NEEDS error checking!
def openConfig(path):
    file = open(path, "r")
    return file

def cleanUp():
    pygame.quit()
    quit()

DEBUG = False
name = "mapgen: "
loadedImages = []


def printd(inp):
    if DEBUG:
        print(inp)

config = openConfig("config.cfg")
surface = openWindow((160, 100))



def getSnippet(currentSnippet):
    #setup
    global config
    curString = ""
    char = config.read(1)

    #scroll through the whitespace
    if char == ' ' or char == '\n':
        printd("scrolling past whitespace")
        while char == ' ' or char == '\n':
            char = config.read(1)

    #check for notes to ignore whitespace until we hit a semicolon
    if currentSnippet == "Notes:":
        printd("Reading notes")
        while char != ';':
            curString = curString+char
            char = config.read(1)
    else:
        printd("getting data...")
        while char != ' ' and char != '\n' and char != ';':
            if DEBUG: print(char, end='')
            curString = curString+char
            char = config.read(1)
        printd("")

    snippet = curString
    return currentSnippet, snippet

def readConfig():
    #Layers:
    #1 "Maps{"
    #  "End"
    #2 "ID:"
    #  "Diff:"
    #  "Laps:"
    #  "Notes:"
    #  "}"
    #3 Data;
    Layer = 1

    #Controls when loop ends
    Run = True

    #A snippet is a chunk of the config file
    snippet = ""
    lastSnippet = ""

    token = []
    tokenIndex = 0
    tokens = []

    loadedImages = []

    while Run:
        printd("Getting snippet...")
        lastSnippet, snippet = getSnippet(snippet)
        printd("Got snippet "+snippet)
        if Layer == 1:
            if snippet == "Map{":
                Layer = 2
                printd("Found Map entering layer 2")
            elif snippet == "End":
                printd("Found End, breaking")
                Run = False
                break
            else:
                print(name+"unknown block data "+snippet)
                Run = False
                break

        elif Layer == 2:
            if snippet == "ID:":
                printd("Found ID:")
                Layer = 3
            elif snippet == "Diff:":
                printd("Found Diff:")
                Layer = 3
            elif snippet == "Laps:":
                printd("Found Laps:")
                Layer = 3
            elif snippet == "Notes:":
                printd("Found Notes:")
                Layer = 3
            elif snippet == "}":
                printd("Found } entering layer 1")
                Layer = 1
                tokens.append(token)
                token = []
                tokenIndex += 1
            else:
                print(name+"unknown atribute "+snippet)
                Run = False
                break

        elif Layer == 3:
            if lastSnippet == "ID:":
                token.append(snippet)
            elif lastSnippet == "Diff:":
                token.append(snippet)
            elif lastSnippet == "Laps:":
                token.append(snippet)
            elif lastSnippet == "Notes:":
                token.append(snippet)
            else:
                print(name+"unknown attribute from previous layer: "+lastSnippet)
                Run = False
                break
            Layer = 2

    return tokens

#NEEDS error detection!
def findImage(path):
    index = 0
    global loadedImages
    for img in loadedImages:
        if path == img:
            return index
        index += 1
    loadedImages.append(pygame.image.load(r''+path))
    #add error detection and return -1 when image fails to load
    return index

def drawImage(path):
    index = findImage(path)

    #throw error is image fails to load
    if index == -1:
        print(name+"could not find image at "+path)
        return -1

    #draw code
    surface.blit(loadedImages[index], (0, 0))
    return 0

def generateThumbnail(token):
    drawImage("resources/Maps/Map"+token[0]+"P.png")
    drawImage("resources/Diff/difficulty"+token[1]+".png")
    drawImage("resources/Laps/laps"+token[2]+".png")


def saveThumbnail(path):
    pygame.image.save(surface,path)

printd("Reading config")
tokens = readConfig()

printd("Entering main loop")
for tok in tokens:
    generateThumbnail(tok)
    saveThumbnail("output/Map"+tok[0]+"P.png")
    print(name+"Saved thumbnail "+"output/Map"+tok[0]+"P.png")

cleanUp()

"""
this is example code

#define window size
displayWidth = 160
displayHeight = 100

#setup display window surface
surface = pygame.display.set_mode((displayWidth, displayHeight))

#set the window name
pygame.display.set_caption('Image')

#load the image to draw
displayImage = pygame.image.load(r'ban.png')

while True:
    surface.fill((255, 255, 255))
    surface.blit(displayImage, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()
"""
