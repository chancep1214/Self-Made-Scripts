import random
import tkinter as tk
import math

def rectangleClick(event):
    # Coords of click
    x, y = event.x, event.y

    # Stores the id's of all rectangles near click. Index 0 always contains the one that was clicked.
    nearestTiles = event.widget.find_closest(x, y)

    if (nearestTiles):
        rectID = nearestTiles[0]
        # Checks to see if the clicked rectangle has been guessed already
        if ("Not Guessed" in canvas.gettags(rectID)):
            # Checks if the rectangle is a bomb
            if (checkRectangleBomb(rectID)):
                clickedBomb(rectID)
            else:
                # Retrieves center coordinates from clicked rectangle
                center = getCenterOfRectangle(rectID)
                #centerX1, centerY1 = center[0], center[1]
                # Stores the number of bombs in tiles vicinity
                bombCounter = getNumBombVicinity(center)
                changeRectangle(rectID, center, bombCounter)

def rectangleFlag(event):
    # Coords of click
    x, y = event.x, event.y

    # Stores the id's of all rectangles near click. Index 0 always contains the one that was clicked.
    nearestTiles = event.widget.find_closest(x, y)

    if (nearestTiles):
        rectID = nearestTiles[0]
        if ("Not Guessed" in canvas.gettags(rectID)):
            # Check if rectangle has been flagged
            if ("Unflagged" in canvas.gettags(rectID)):
                addFlagToRectangle(rectID)
            else:
                removeFlagToRectangle(rectID)
            

def addFlagToRectangle(rectID):
    canvas.itemconfig(rectID, fill = "yellow")
    canvas.dtag(rectID, "Unflagged")
    canvas.addtag("Flagged", "withtag",rectID)

def removeFlagToRectangle(rectID):
    canvas.itemconfig(rectID, fill = "white")
    canvas.dtag(rectID, "Flagged")
    canvas.addtag("Unflagged", "withtag", rectID)

def getNumBombVicinity(clickedCenter):
    numBombVicinity = 0
    # Can edit this for loop eventually to clear all connected blocks with no bombs
    for bomb in bombLocations:
        bombCoords = centerCoordsList[bomb - 1]
        # Calculates distance between clicked rectangle center and bombs centers
        distance = math.dist(clickedCenter, bombCoords)
        if (distance <= xOffset*math.sqrt(2)):
            numBombVicinity += 1
    return numBombVicinity

def getCenterOfRectangle(rectID):
    index = rectID - 1
    return centerCoordsList[index]
    
def checkRectangleBomb(rectID):
    if (rectID in bombLocations):
        return True
    else:
        return False

def changeRectangle(rectID, center, bombCounter):
    # Gives the rectangle the guessed attribute
    canvas.addtag("Guessed", "withtag", rectID)
    # Tracks the rectangle has been guessed now
    canvas.dtag(rectID, "Not Guessed")
    canvas.itemconfig(rectID, fill="grey")
    canvas.create_text(center[0], center[1], text=str(bombCounter), fill="white", font=("Arial", 30))
    # Increment the number of correct guesses that have been made
    global correctGuesses
    correctGuesses += 1

def clickedBomb(rectID):
    canvas.itemconfig(rectID, fill="red")
    endText = "Oh no, you clicked a bomb. Game Over!"
    canvas.create_text(690,360, text=endText, font=("Arial", 40))
    # Prevents using buttons after loss
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-3>")

def startButtonClicked():
    global startGame
    startGame = True
    return startGame


root = tk.Tk()
root.title("Minesweeper")
root.geometry("1280x720")

canvas = tk.Canvas(root, width=1280, height=720, background="grey")
canvas.pack(fill="both", expand=True)


root.mainloop()

print("TEST")
# Creates a start button

#buttonID = canvas.create_window(10,10, anchor="center", window=startButton)

# Rectangle Coordinate Start
# (top-left x, top-left y, bottom-right x, bottom-right y)
topX, topY, botX, botY = 50, 50, 100, 100
xOffset, yOffset = 50, 50

rows = 12
columns = 24
bombCount = 25

# Creates empty board that store 0's
board = [[0 for row in range(columns)] for col in range(rows)]

coordsList = []
centerCoordsList = []

# Stores the number of rectangles correctly guessed (or given)
global correctGuesses
correctGuesses = 0
totalPossibleCorrectGuesses = (rows*columns) - bombCount

# Outer for loop creates 12 rows while inner loop creates 24 columns of boxes
for i in range(rows):
    for j in range(columns):
        # Creates rectangles
        id = canvas.create_rectangle(topX,topY,botX,botY,outline="black", fill="white", tags=("Unflagged","Not Guessed"))
        # Stores id in the board
        board[i][j] = id
        # Store Coords in List
        coordsList.append(canvas.coords(id))
        centerCoordsList.append(((botX+topX) / 2, (botY+topY) / 2))
        # Changes x coordinates
        topX += xOffset; botX += xOffset
    # Changes y coordinates
    topY += yOffset; botY += yOffset
    # Resets x coordinates back to normal 
    topX = 50; botX = 100

# Creates empty list to store locations (rectangle id) of bombs
bombLocations = []
# Generates bomb locations
for i in range(bombCount):
    location = random.randint(1, rows*columns)
    
    while (location in bombLocations):
        location = random.randint(1, rows*columns)

    bombLocations.append(location)

# Bind Left Click to Choose
canvas.bind("<Button-1>", rectangleClick)
# Bind Right Click to Flag
canvas.bind("<Button-3>", rectangleFlag)

root.mainloop()
