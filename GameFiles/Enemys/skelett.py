import pygame as pg
import Enemys.enemy as en
import Core.saveAndLoad as SAL

class Skelett(en.enemy):
    skelettLifes = 6
    skelettDamage = 3
    def __init__(self, main, display, X, Y, tileMap, player):
        self.main = main
        Sprites = SAL.loadSprites("gameObjects")
        SkelettSprites = [Sprites[4], Sprites[11], Sprites[11], Sprites[4]]
        en.enemy.__init__(self, main, display, X, Y, SkelettSprites, self.skelettLifes, tileMap, player, self.skelettDamage)