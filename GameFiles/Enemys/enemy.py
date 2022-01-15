import pygame as pg
import Core.gameObject as go
import Core.Utility.Utils as Utils

class enemy(go.gameObject):
    def __init__(self, main, display, X, Y, sprites, Lifes, tileMap, player, Damage):
        self.Lifes = Lifes
        self.tileMap = tileMap
        self.player = player
        self.main = main
        self.Damage = Damage
        go.gameObject.__init__(self, display, X, Y, sprites, tileMap)

    def Draw(self):
        if Utils.distance(pg.Vector2(self.player.X, self.player.Y), pg.Vector2(self.X, self.Y)) <= 1.01:
            self.direction = pg.Vector2(self.player.X - self.X, self.player.Y - self.Y).normalize()
        super(enemy, self).Draw()
    
    def Move(self):
        x = self.player.X
        y = self.player.Y
        distance = Utils.distance(pg.Vector2(x, y), pg.Vector2(self.X, self.Y))
        if distance <= 1.01:
            print("hit")
            self.player.getHit(self.Damage)
        elif distance < 10:
            super(enemy, self).Move(x, y)

    def SetTarget(self):
        if self.pathPos == 0:
            if len(self.player.path) > 0:
                if not (self.player.targetX == self.path[0].x and self.player.targetY == self.path[0].y):
                    super(enemy, self).SetTarget()
            else:
                super(enemy, self).SetTarget()
            self.path = []

    def getHit(self, damage):
        self.Lifes -= damage
        if self.Lifes <= 0:
            self.main.delEnemy(self)