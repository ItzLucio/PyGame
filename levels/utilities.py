import os

def __loadMapLayout(lines, startingLine) -> list:
    mapLayout = []

    for lineNumber in range(len(lines)-1):
        if lineNumber <= startingLine:
            continue

        if not lines[lineNumber].startswith("MAP_END"):
            mapLayout.append(lines[lineNumber])

    return mapLayout

def loadLevelFromPath(filePath) -> dict:
    levelData = {}

    file = open(filePath, "r")
    lines = file.readlines()

    currentLine = 0

    for line in lines:
        if line.startswith("#"):
            continue
        
        args = line.split(" : ")

        key = args[0]
        
        if key == "LEVELNAME":
            levelData["LEVEL_NAME"] = args[1]
        elif key == "STARTING_SCORE":
            levelData["STARTING_SCORE"] = float(args[1])
        elif key == "MAP_LAYOUT":
            levelData["MAP_LAYOUT"] = __loadMapLayout(lines, currentLine)
        
        currentLine += 1
    
    return levelData