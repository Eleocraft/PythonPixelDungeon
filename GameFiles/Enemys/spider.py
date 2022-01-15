import pygame as pg
import Enemys.enemy as en
import Core.saveAndLoad as SAL

class Spider(en.enemy):
    spiderLifes = 5
    spiderDamage = 1
    def __init__(self, main, display, X, Y, tileMap, player):
        self.main = main
        Sprites = SAL.loadSprites("gameObjects")
        SpiderSprites = [Sprites[2], Sprites[8], Sprites[7], Sprites[9]]
        en.enemy.__init__(self, main, display, X, Y, SpiderSprites, self.spiderLifes, tileMap, player, self.spiderDamage)
