import pygame as pg
import Enemys.enemy as en
import Core.saveAndLoad as SAL

class Boss(en.enemy):
    bossLifes = 20
    bossDamage = 10
    def __init__(self, main, display, X, Y, tileMap, player):
        self.main = main
        Sprites = SAL.loadSprites("gameObjects")
        BossSprites = [Sprites[3], Sprites[12], Sprites[12], Sprites[3]]
        en.enemy.__init__(self, main, display, X, Y, BossSprites, self.bossLifes, tileMap, player, self.bossDamage)