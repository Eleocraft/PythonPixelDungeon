import pygame as pg
import Core.levelGenerator as lg
import Core.saveAndLoad as SAL
import Interactable.Objects as Interactables
import json
import random as prng

class TileMap():
    mapSizeX = 150
    mapSizeY = 150
    offsetX = 0
    offsetY = 0
    tileSizePx = 40
    DoorTile = 5
    WallTile = 4
    ChestTile = 4
    OpenChestTile = 5
    StairsTile = 6
    SpiderSpawnPoint = 9
    ZombieSpawnPoint = 10
    SkelettSpawnPoint = 11
    BossSpawnPoint = 12
    Level = 0
    def __init__(self, display, main):
        # Initializing all variables for the tilemap
        self.displayWidth = int(display.get_width() / self.tileSizePx)
        self.displayHeight = int(display.get_height() / self.tileSizePx)
        self.display = display

        # Initializing arrays with Sprite references
        self.bgSprites = SAL.loadSprites("bgTiles")
        self.objSprites = SAL.loadSprites("objTiles")

        # Initializing arrays with Colision references
        self.bgColisions = SAL.loadProperties("bgColisions", "TileProperties", False)
        self.objColisions = SAL.loadProperties("objColisions", "TileProperties", False)

        # Initializing Arrays to hold the status of the tilemap
        self.bgTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
        self.objTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]

        # Initializing Item Array
        self.items = []
        
        # If the tilemap is in gameMode, the first level should be generated
        if main != False:
            self.main = main
            self.initPhase = True
            returnValue = lg.generateLevel(self, 20)
            main.playerSpawnPos = returnValue
            self.initPhase = False
            
        else:
            self.displayHeight = 10

    def Draw(self):
        for x in range(self.mapSizeX):
            for y in range(self.mapSizeY):
                if self.Visible(x, y):
                    bgSprite = self.bgSprites[self.bgTileMap[x][y]]
                    objSprite = self.objSprites[self.objTileMap[x][y]]
                    posX = round(self.tileSizePx * (x - self.offsetX))
                    posY = round(self.tileSizePx * (y - self.offsetY))
                    if (bgSprite != 0):
                        self.display.blit(bgSprite, (posX, posY))
                    if (objSprite != 0):
                        self.display.blit(objSprite, (posX, posY))

        for i in self.items:
            i.Draw()

    def ChangeSize(self, newSizeX, newSizeY):
        oldMapSizeX = self.mapSizeX
        oldMapSizeY = self.mapSizeY
        self.mapSizeX = newSizeX
        self.mapSizeY = newSizeY
        oldBgTileMap = self.bgTileMap
        oldObjTileMap = self.objTileMap
        self.bgTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
        self.objTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
        self.Insert(oldMapSizeX, oldMapSizeY, oldBgTileMap, oldObjTileMap, 0, 0)

    def SetRoom(self, Room, tileX, tileY):
        RoomData = SAL.load("Rooms", Room)
        bgTileMap = RoomData["bgTileMap"]
        mapSizeX = RoomData["mapSizeX"]
        mapSizeY = RoomData["mapSizeY"]
        for x in range(mapSizeX):
            for y in range(mapSizeY):
                if bgTileMap[x][y] == self.DoorTile:
                    bgTileMap[x][y] = self.WallTile
        self.Insert(mapSizeX, mapSizeY, bgTileMap, RoomData["objTileMap"], tileX, tileY)
        self.AddSpawnPoints(RoomData, tileX, tileY)

    def AddSpawnPoints(self, data, tileX, tileY):
        EnemySpawnPoints = data["EnemySpawnPoints"]
        EnemyTypes = data["EnemyTypes"]
        for i in range(len(EnemySpawnPoints)):
            EnemySpawnPoints[i][0] = int(EnemySpawnPoints[i][0] + tileX)
            EnemySpawnPoints[i][1] = int(EnemySpawnPoints[i][1] + tileY)
            self.objTileMap[EnemySpawnPoints[i][0]][EnemySpawnPoints[i][1]] = 0
        self.main.spawn(EnemySpawnPoints, EnemyTypes, self.initPhase)

    def Insert(self, sizeX, sizeY, bgTileMap, objTileMap, tileX, tileY):
        for x in range(sizeX):
            for y in range(sizeY):
                posX = int(x + tileX)
                posY = int(y + tileY)
                if (self.InBound(posX, posY)):
                    if bgTileMap[x][y] != 0:
                        self.bgTileMap[posX][posY] = bgTileMap[x][y]
                    self.objTileMap[posX][posY] = objTileMap[x][y]
    
    def MoveMap(self, X, Y):
        oldBgTileMap = self.bgTileMap
        oldObjTileMap = self.objTileMap
        self.bgTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
        self.objTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
        self.Insert(self.mapSizeX, self.mapSizeY, oldBgTileMap, oldObjTileMap, X, Y)
    
    def Interact(self, tileX, tileY):
        if self.InBound(tileX, tileY):
            if self.objTileMap[tileX][tileY] == self.ChestTile:
                self.objTileMap[tileX][tileY] = self.OpenChestTile
                itemType, itemID = Interactables.OpenChest()
                self.items.append(Interactables.Item(tileX, tileY, self, itemType, itemID))
            elif self.objTileMap[tileX][tileY] == self.StairsTile:
                self.Level += 1
                self.bgTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
                self.objTileMap = [[0]*(self.mapSizeY) for i in range(self.mapSizeX)]
                self.items.clear()
                self.main.enemys.clear()
                if self.Level < 5:
                    playerPos = lg.generateLevel(self, 20)
                    self.main.player.setPos(playerPos.x, playerPos.y)
                else:
                    self.LoadLevel("bossLevel")
                    self.main.player.setPos(2, 2)

    def pickup(self, tileX, tileY):
        for i in range(len(self.items)):
            if self.items[i].x == tileX and self.items[i].y == tileY:
                item = self.items.pop(i)
                return item.pickup()

    def InBound(self, tileX, tileY):
        return 0 <= tileX < self.mapSizeX and 0 <= tileY < self.mapSizeY

    def Visible(self, tileX, tileY):
        return -self.tileSizePx <= tileX - self.offsetX < self.displayWidth and -self.tileSizePx <= tileY - self.offsetY < self.displayHeight

    def Move(self, x, y):
        self.offsetX += x
        self.offsetY += y

    def SetPos(self, x, y):
        self.offsetX = x
        self.offsetY = y

    def CheckColision(self, tileX, tileY):
        if self.InBound(tileX, tileY):
            return self.bgColisions[self.bgTileMap[tileX][tileY]] or self.objColisions[self.objTileMap[tileX][tileY]]
        return True

    def GetTile(self, x, y):
        tileX = int(x / self.tileSizePx + self.offsetX)
        tileY = int(y / self.tileSizePx + self.offsetY)
        return tileX, tileY

    def SetBgTile(self, tileX, tileY, sprite):
        x = round(tileX + self.offsetX)
        y = round(tileY + self.offsetY)
        if self.InBound(x, y) and self.Visible(x, y):
            self.bgTileMap[x][y] = sprite

    def SetObjTile(self, tileX, tileY, sprite):
        x = round(tileX + self.offsetX)
        y = round(tileY + self.offsetY)
        if self.InBound(x, y) and self.Visible(x, y):
            self.objTileMap[x][y] = sprite
        
    def SetBgTileRaw(self, tileX, tileY, sprite):
        x = int(tileX)
        y = int(tileY)
        if self.InBound(x, y):
            self.bgTileMap[x][y] = sprite

    def SetObjTileRaw(self, tileX, tileY, sprite):
        x = int(tileX)
        y = int(tileY)
        if self.InBound(x, y):
            self.objTileMap[x][y] = sprite
    
    def Save(self, name):
        DoorSpawnPoints = []
        EnemySpawnPoints = []
        EnemyTypes = []
        for x in range(self.mapSizeX):
            for y in range(self.mapSizeY):
                if self.bgTileMap[x][y] == self.DoorTile:
                    DoorSpawnPoints.append([x,y])
                if self.objTileMap[x][y] == self.SpiderSpawnPoint:
                    EnemySpawnPoints.append([x,y])
                    EnemyTypes.append("Spider")
                elif self.objTileMap[x][y] == self.ZombieSpawnPoint:
                    EnemySpawnPoints.append([x,y])
                    EnemyTypes.append("Zombie")
                elif self.objTileMap[x][y] == self.SkelettSpawnPoint:
                    EnemySpawnPoints.append([x,y])
                    EnemyTypes.append("Skelett")
                elif self.objTileMap[x][y] == self.BossSpawnPoint:
                    EnemySpawnPoints.append([x,y])
                    EnemyTypes.append("Boss")

        data = TileMapData(self.bgTileMap, self.objTileMap, self.mapSizeX, self.mapSizeY, DoorSpawnPoints, EnemySpawnPoints, EnemyTypes)
        SAL.saveRaw(data.toJSON(), "Rooms", name)

    def Load(self, name):
        data = SAL.load("Rooms", name)
        self.bgTileMap = data["bgTileMap"]
        self.objTileMap = data["objTileMap"]
        self.mapSizeX = data["mapSizeX"]
        self.mapSizeY = data["mapSizeY"]
    
    def LoadLevel(self, name):
        data = SAL.load("Rooms", name)
        self.bgTileMap = data["bgTileMap"]
        self.objTileMap = data["objTileMap"]
        self.mapSizeX = data["mapSizeX"]
        self.mapSizeY = data["mapSizeY"]
        EnemySpawnPoints = data["EnemySpawnPoints"]
        EnemyTypes = data["EnemyTypes"]
        for x in range(self.mapSizeX):
            for y in range(self.mapSizeY):
                if [x,y] in EnemySpawnPoints:
                    self.objTileMap[x][y] = 0
        self.main.spawn(EnemySpawnPoints, EnemyTypes, False)

class TileMapData():
    def __init__(self, bgTileMap, objTileMap, mapSizeX, mapSizeY, DoorSpawnPoints, EnemySpawnPoints, EnemyTypes):
        self.bgTileMap = bgTileMap
        self.objTileMap = objTileMap
        self.mapSizeX = mapSizeX
        self.mapSizeY = mapSizeY
        self.DoorSpawnPoints = DoorSpawnPoints
        self.EnemySpawnPoints = EnemySpawnPoints
        self.EnemyTypes = EnemyTypes
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)