import pygame as pg

def calculatePath(tileMap, startX, startY, targetX, targetY, maxDist):
    startX = int(startX)
    startY = int(startY)
    targetX = int(targetX)
    targetY = int(targetY)
    if tileMap.CheckColision(targetX, targetY):
        return
    distanceMap = manhattanDistance(tileMap, targetX, targetY, startX, startY, maxDist)
    if (distanceMap[startX][startY] == -1):
        return
    x = startX
    y = startY
    path = []
    while distanceMap[x][y] != 0:
        smallestDist = 1000
        adjacentTilePositionsX = [x, x, x+1, x-1]
        adjacentTilePositionsY = [y+1, y-1, y, y]
        for i in range(4):
            X, Y = int(adjacentTilePositionsX[i]), int(adjacentTilePositionsY[i])
            if (distanceMap[X][Y] < smallestDist and distanceMap[X][Y] != -1):
                smallestDist = distanceMap[X][Y]
                x, y = X, Y
        path.append(pg.Vector2(x, y))
    return path
        

def manhattanDistance(tileMap, startPosX, startPosY, endPosX, endPosY, maxDist):
    distanceMap = [[-1]*(tileMap.mapSizeY) for i in range(tileMap.mapSizeX)]
    distanceMap[startPosX][startPosY] = 0
    tileList = [pg.Vector2(startPosX, startPosY)]
    while len(tileList) != 0:
        if tileList[0].x == endPosX and tileList[0].y == endPosY:
            break
        elif distanceMap[int(tileList[0].x)][int(tileList[0].y)] == maxDist:
            break
        tileList.extend(findAdjacentTiles(tileMap, distanceMap, tileList[0].x, tileList[0].y))
        tileList.pop(0)
    return distanceMap
    

def findAdjacentTiles(tileMap, distanceMap, x, y): 
    adjacentTilePositionsX = [x, x, x+1, x-1]
    adjacentTilePositionsY = [y+1, y-1, y, y]
    adjacentTiles = []
    for i in range(4):
        X, Y = int(adjacentTilePositionsX[i]), int(adjacentTilePositionsY[i])
        if tileMap.InBound(X, Y) and not tileMap.CheckColision(X, Y) and distanceMap[X][Y] == -1:
            adjacentTiles.append(pg.Vector2(X, Y))
            distanceMap[X][Y] = distanceMap[int(x)][int(y)] + 1
    return adjacentTiles

