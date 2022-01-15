import pygame as pg
import Core.pathfinding as pf

class gameObject():
    speed = 0.1
    maxDist = 100
    def __init__(self, display, X, Y, sprites, tileMap):
        self.X = X
        self.Y = Y
        self.targetX = self.X
        self.targetY = self.Y
        self.tileMap = tileMap
        self.display = display
        self.sprites = sprites
        self.path = []
        self.pathPos = 0
        self.direction = pg.Vector2(0,0)

    def Draw(self):
        if self.targetX != self.X or self.targetY != self.Y:
            self.direction = pg.Vector2(self.targetX - self.X, self.targetY - self.Y).normalize()
            movement = self.direction * self.speed
            if abs(self.targetX - self.X) <= abs(movement.x) and abs(self.targetY - self.Y) <= abs(movement.y):
                self.X = self.targetX
                self.Y = self.targetY
                self.Moved()
            else:
                self.X += movement.x
                self.Y += movement.y
        elif self.pathPos < len(self.path):
            self.SetTarget()
        else:
            self.OnArrival(self.X, self.Y)
        
        self.CreateImage(self.setDirection(self.direction))
    
    def Moved(self):
        pass

    def setDirection(self, direction):
        dir = 0
        if direction.x == 1:
            dir = 0
        elif direction.x == -1:
            dir = 2
        elif direction.y == 1:
            dir = 3
        elif direction.y == -1:
            dir = 1
        
        return dir

    def CreateImage(self, dir):
        displayX = (self.X - self.tileMap.offsetX) * self.tileMap.tileSizePx
        displayY = (self.Y - self.tileMap.offsetY) * self.tileMap.tileSizePx
        self.display.blit(self.sprites[dir], (displayX, displayY))

    def OnArrival(self, X, Y):
        pass

    def SetTarget(self):
        self.targetX = self.path[self.pathPos].x
        self.targetY = self.path[self.pathPos].y
        self.pathPos += 1

    def Move(self, x, y):
        if (self.tileMap.InBound(x, y) and self.tileMap.Visible(x, y)):
            self.path = pf.calculatePath(self.tileMap, int(self.targetX), int(self.targetY), x, y, self.maxDist)
            if not isinstance(self.path, list):
                self.path = []
            self.pathPos = 0
    
    def setPos(self, x, y):
        self.X = int(x)
        self.Y = int(y)
        self.targetX = int(x)
        self.targetY = int(y)
        self.path.clear()