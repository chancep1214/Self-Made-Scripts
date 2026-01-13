import random
import tkinter as tk
import math
import time

'''
Purpose: Tracks the click event pertaining to Left-Click
Param:
event - Contains the data corresponding to the recent event
'''
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
                changeConnectingRectangles(rectID, bombCounter)
    
    if len(guessedRectangles) == totalPossibleCorrectGuesses:
        winner()
    
'''
Purpose: Allow for dynamic generation of bombs after first click.
'''
def firstClick(event):
    global firstClickValue
    # Coords of click
    x, y = event.x, event.y
    # Stores the id's of all rectangles near click. Index 0 always contains the one that was clicked.
    nearestTiles = event.widget.find_closest(x, y)

    if (nearestTiles):
        rectID = nearestTiles[0]
        center = getCenterOfRectangle(rectID)
        bombCounter = 0
        changeRectangle(rectID,center,bombCounter)

        # Get IDs of rectangles in vicinity to prevent bombs from spawning there
        idRectangleVicinityList = getRectangleIDInVicinity(rectID)
        idRectangleVicinityList.append(rectID)
        generateBombs(idRectangleVicinityList)

        # Changes the rest of the rectangles near it
        changeConnectingRectangles(rectID, bombCounter)
        # Allows program to proceed
        firstClickValue.set(value=1)            

'''
Purpose: Tracks the flag event pertaining to Right-Click
Param:
event - Contains the data corresponding to the recent event
'''
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

            
'''
Purpose: Updates the rectangle to appear as flagged (Yellow)
Param:
rectID - The ID assigned to the given rectangle that was chosen
'''
def addFlagToRectangle(rectID):
    canvas.itemconfig(rectID, fill = "yellow")
    canvas.dtag(rectID, "Unflagged")
    canvas.addtag("Flagged", "withtag",rectID)

'''
Purpose: Updates the rectangle to appear as unflagged (White)
Param:
rectID - The ID assigned to the given rectangle that was chosen
'''
def removeFlagToRectangle(rectID):
    canvas.itemconfig(rectID, fill = "white")
    canvas.dtag(rectID, "Flagged")
    canvas.addtag("Unflagged", "withtag", rectID)

'''
Purpose: Returns the number of bombs in the selected rectangles vicinity (3x3)
Param:
clickedCenter - The center (x,y) of the clicked rectangle
'''
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

'''
Purpose: Returns the center of the chosen rectangle
Param:
rectID - The ID assigned to the given rectangle that was chosen
'''
def getCenterOfRectangle(rectID):
    index = rectID - 1
    return centerCoordsList[index]

'''
Purpose: Checks if the chosen rectangle is a bomb
Param:
rectID - The ID assigned to the given rectangle that was chosen
'''
def checkRectangleBomb(rectID):
    if (rectID in bombLocations):
        return True
    else:
        return False

'''
Purpose: Updates the chosen rectangle with a specific number correlating to (bombCounter)
Params:
rectID - The ID assigned to the given rectangle that was chosen
center - The X and Y coordinates of the center of the rectangle
bombCounter - The number of bombs in a 3x3 grid around (and including) the rectangle
'''
def changeRectangle(rectID, center, bombCounter):
    # Gives the rectangle the guessed attribute
    canvas.addtag("Guessed", "withtag", rectID)
    # Tracks the rectangle has been guessed now
    canvas.dtag(rectID, "Not Guessed")
    canvas.itemconfig(rectID, fill="grey")
    canvas.create_text(center[0], center[1], text=str(bombCounter), fill="white", font=("Arial", 30))
    
'''
Purpose: Describes what happens when a bomb is clicked and this function is ran.
Params:
rectID - The ID assigned to the given rectangle that was chosen
'''
def clickedBomb(rectID):
    canvas.itemconfig(rectID, fill="red")
    endText = "Oh no, you clicked a bomb. Game Over!"
    canvas.create_text(960,540, text=endText, font=("Arial", 40))
    # Prevents using buttons after loss
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-3>")

    '''
Purpose: Describes what happens when a bomb is clicked and this function is ran.
Params:
rectID - The ID assigned to the given rectangle that was chosen
'''
def winner():
    for rectID in range(1,rows*columns + 1):
        canvas.itemconfig(rectID, fill="green")
    for location in bombLocations:
        canvas.itemconfig(location, fill="red")
    endText = "You have won the game!"
    canvas.create_text(900,500, text=endText, font=("Arial", 40), fill="Yellow")
    # Prevents using buttons after loss
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-3>")

'''
Purpose: Returns a list containing the IDs of the rectangles in a 3x3 vicinity to a rectangle
Param:
rectID - The ID assigned to the given rectangle that was chosen
'''
def getRectangleIDInVicinity(rectID):
    # Stores IDs of connecting rectangles
    idList = []
   
    # Accounts for all rectangles one block in from the outside
    if (rectID > columns and (rectID <= rows*columns - columns)
        and rectID % columns != 1 and rectID % columns != 0):
        # Gets IDs of all blocks around chosen rectangle
        topLeft, topMiddle, topRight = (rectID - columns) - 1, (rectID - columns), (rectID - columns) + 1
        middleLeft, middleRight = rectID - 1, rectID + 1
        bottomLeft, bottomMiddle, bottomRight = (rectID + columns) - 1, (rectID + columns), (rectID + columns) + 1

        idList.append(topLeft); idList.append(topMiddle); idList.append(topRight)
        idList.append(middleLeft); idList.append(middleRight)
        idList.append(bottomLeft); idList.append(bottomMiddle); idList.append(bottomRight)
    # Left side rectangles not including corners
    elif (rectID != 1 and rectID % columns == 1 and (rectID != rows*columns + 1 - columns) ):
        topMiddle, topRight = (rectID - columns), (rectID - columns) + 1
        middleRight = rectID + 1
        bottomMiddle, bottomRight = (rectID + columns), (rectID + columns) + 1

        idList.append(topMiddle); idList.append(topRight)
        idList.append(middleRight)
        idList.append(bottomMiddle); idList.append(bottomRight)
    # Top side rectangles not including corners
    elif (rectID > 1 and rectID < columns):
        middleLeft, middleRight = rectID - 1, rectID + 1
        bottomLeft, bottomMiddle, bottomRight = (rectID + columns) - 1, (rectID + columns), (rectID + columns) + 1

        idList.append(middleLeft); idList.append(middleRight)
        idList.append(bottomLeft); idList.append(bottomMiddle); idList.append(bottomRight)
    # Right side rectangles not including corners
    elif (rectID % columns == 0 and rectID != columns and (rectID != rows*columns) ):
        topLeft, topMiddle = (rectID - columns) - 1, (rectID - columns)
        middleLeft = rectID - 1
        bottomLeft, bottomMiddle = (rectID + columns) - 1, (rectID + columns)

        idList.append(topLeft); idList.append(topMiddle)
        idList.append(middleLeft)
        idList.append(bottomLeft); idList.append(bottomMiddle)
    # Bottom side rectangles not including corners
    elif ( (rectID > rows * columns + 1 - columns) and (rectID < rows * columns) ):
        topLeft, topMiddle, topRight = (rectID - columns) - 1, (rectID - columns), (rectID - columns) + 1
        middleLeft, middleRight = rectID - 1, rectID + 1

        idList.append(topLeft); idList.append(topMiddle); idList.append(topRight)
        idList.append(middleLeft); idList.append(middleRight)
    # Top left corner
    elif rectID == 1:
        middleRight = rectID + 1
        bottomMiddle, bottomRight = (rectID + columns), (rectID + columns) + 1

        idList.append(middleRight)
        idList.append(bottomMiddle); idList.append(bottomRight)
    # Top right corner
    elif rectID == columns:
        middleLeft = rectID - 1
        bottomLeft, bottomMiddle = (rectID + columns) - 1, (rectID + columns)

        idList.append(middleLeft)
        idList.append(bottomLeft); idList.append(bottomMiddle)
    # Bottom left corner
    elif rectID == (rows*columns + 1) - columns:
        topMiddle, topRight = (rectID - columns), (rectID - columns) + 1
        middleRight = rectID + 1

        idList.append(topMiddle); idList.append(topRight)
        idList.append(middleRight)
    # Bottom right corner
    elif rectID == rows*columns:
        topLeft, topMiddle = (rectID - columns)-1, (rectID - columns)
        middleLeft = rectID - 1

        idList.append(topLeft); idList.append(topMiddle)
        idList.append(middleLeft)    

    for i in idList:
        if i in guessedRectangles or i in bombLocations:
            idList.remove(i)
    
    return idList

# Leverage Guessed tag on rectangles
# For each rectangle that has bombCounter = 0, run distance formula to get IDs of Rectangles
# in 3x3 vicinity.
# Check for Guessed tag, if rectangle doesn't have Guessed tag recursively call the function.
# If bombCounter = 0 for a rectangle just display that square, don't recursively search.
def changeConnectingRectangles(rectID, bombCounter):
    center = getCenterOfRectangle(rectID)

    # Check to see if the current rectangle has 0 bombs in vicinity or has been evaluated before
    if rectID not in guessedRectangles and bombCounter == 0:
        changeRectangle(rectID, center, bombCounter)
        guessedRectangles.append(rectID)
        connectingRectangleIDS = getRectangleIDInVicinity(rectID)

        for adjacentRectID in connectingRectangleIDS:
            adjacentCenter = getCenterOfRectangle(adjacentRectID)
            bombCounter = getNumBombVicinity(adjacentCenter)
            changeConnectingRectangles(adjacentRectID, bombCounter)
    # Base Case - Rectangle has bombs in vicinity
    elif rectID not in guessedRectangles and bombCounter > 0:
        guessedRectangles.append(rectID)
        changeRectangle(rectID, center, bombCounter)

# Might not need param
def generateBombs(idList):
    global bombLocations

    # Generates bomb locations
    for i in range(bombCount):
        location = random.randint(1, rows*columns)

        while (location in bombLocations or location in idList):
            location = random.randint(1, rows*columns)

        bombLocations.append(location)



        
root = tk.Tk()
root.title("Minesweeper")
root.geometry("1920x1080")

canvas = tk.Canvas(root, width=1920, height=1080, background="grey")
canvas.pack(fill="both", expand=True)

# Rectangle Coordinate Start
# (top-left x, top-left y, bottom-right x, bottom-right y)
topX, topY, botX, botY = 50, 50, 100, 100
xOffset, yOffset = 50, 50

rows = 17
columns = 30
bombCount = 100

coordsList = []
centerCoordsList = []
guessedRectangles = []

# Stores the number of rectangles that can be guessed
totalPossibleCorrectGuesses = (rows*columns) - bombCount

# Outer for loop creates 12 rows while inner loop creates 24 columns of boxes
for i in range(rows):
    for j in range(columns):
        # Creates rectangles
        id = canvas.create_rectangle(topX,topY,botX,botY,outline="black", fill="white", tags=("Unflagged","Not Guessed"))
        #unguessedIDS.append(id)
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

spinbox = tk.Spinbox(canvas, from_=0, to=100)
spinbox.pack(pady=10)

def getValue():
    value = int(spinbox.get())
    print(f"Value {value}")

button = tk.Button(canvas, text="Number of Bombs", command=getValue)
button.pack(pady=5)

# Works for the first click only and then resumes.
firstClickValue = tk.IntVar()
canvas.bind("<Button-1>",firstClick)
root.wait_variable(firstClickValue)
canvas.unbind("<Button-1>")

# Test Bombs (SHOW BOMBS)
# for i in bombLocations:
#     canvas.itemconfig(i, fill="red")

# Bind Left Click to Choose
canvas.bind("<Button-1>", rectangleClick)
# Bind Right Click to Flag
canvas.bind("<Button-3>", rectangleFlag)

root.mainloop()
