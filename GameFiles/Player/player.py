import pygame as pg
import Core.gameObject as go
import Core.saveAndLoad as SAL
import Player.inventory as inv
import Interactable.Objects as Interactables
import Core.Utility.Utils as U

class Player(go.gameObject):
    Lifes = 10
    MaxLifes = 10
    Damageeffect = 1
    Armoreffect = 1
    DamageEffectClock = 0
    ArmorEffectClock = 0
    def __init__(self, main, display, X, Y, tileMap):
        self.main = main
        self.tileMap = tileMap
        sprites = [SAL.loadSprites("gameObjects")[6], SAL.loadSprites("gameObjects")[1], SAL.loadSprites("gameObjects")[1], SAL.loadSprites("gameObjects")[6]]
        go.gameObject.__init__(self, display, X, Y, sprites, tileMap)
        self.inventory = inv.inventory(display)
    
    def CreateImage(self, dir):
        displayX = self.tileMap.displayWidth / 2 * self.tileMap.tileSizePx
        displayY = self.tileMap.displayHeight / 2 * self.tileMap.tileSizePx
        self.tileMap.SetPos(self.X - self.tileMap.displayWidth / 2, self.Y - self.tileMap.displayHeight / 2)
        self.display.blit(self.sprites[dir], (displayX, displayY))

    def Move(self, x, y, enemys):
        tileX, tileY = self.tileMap.GetTile(x, y)
        if int(tileX) == int(self.X) and int(tileY) == int(self.Y):
            item = self.tileMap.pickup(tileX, tileY)
            if not item is None:
                oldItem = self.inventory.addItem(item[0], item[1])
                self.MaxLifes = self.inventory.getMaxLifes()
                if self.Lifes > self.MaxLifes:
                    self.Lifes = self.MaxLifes
                if oldItem and oldItem[1] != 0:
                    self.tileMap.items.append(Interactables.Item(tileX, tileY, self.tileMap, oldItem[0], oldItem[1]))
        blocked = False
        hitEnemy = False
        for i in enemys:
            if i.targetX == tileX and i.targetY == tileY:
                if U.distance(pg.Vector2(i.targetX, i.targetY), pg.Vector2(self.targetX, self.targetY)) < 2:
                    self.direction = pg.Vector2(i.targetX - self.X, i.targetY - self.Y).normalize()
                    Damage = self.Damageeffect * self.inventory.getDamage()
                    print("attack")
                    i.getHit(Damage)
                    self.main.action()
                    self.potionClock()
                    blocked = True
                else:
                    hitEnemy = True
        if not blocked:
            super(Player, self).Move(tileX, tileY)
            if hitEnemy:
                self.path.pop(len(self.path) - 1)
        
    def Moved(self):
        self.main.action()
        self.potionClock()

    def SetTarget(self):
        for i in self.main.enemys:
            if i.targetX == self.path[self.pathPos].x and i.targetY == self.path[self.pathPos].y:
                self.path = []
                return
        super(Player, self).SetTarget()

    def OnArrival(self, X, Y):
        self.tileMap.Interact(int(X), int(Y))
    
    def getHit(self, damage):
        Armor = self.Armoreffect * self.inventory.getArmor()
        self.Lifes -= damage / Armor
        if self.Lifes <= 0:
            self.main.gameOver()
        
    def potionClock(self):
        if self.ArmorEffectClock > 0:
            self.ArmorEffectClock -= 1
        elif self.Armoreffect != 1:
            self.Armoreffect = 1
        
        if self.DamageEffectClock > 0:
            self.DamageEffectClock -= 1
        elif self.Damageeffect != 1:
            self.Damageeffect = 1

    def usePotion(self, slotID):
        potion = self.inventory.usePotion(slotID)
        if potion == 1:
            self.Damageeffect = 2
            self.DamageEffectClock = 10
        elif potion == 2:
            self.Lifes = self.MaxLifes
        elif potion == 3:
            self.Armoreffect = 2
            self.ArmorEffectClock = 10