import pygame as pg
import Enemys.enemy as en
import Core.saveAndLoad as SAL

class Zombie(en.enemy):
    zombieLifes = 4
    zombieDamage = 2
    def __init__(self, main, display, X, Y, tileMap, player):
        self.main = main
        Sprites = SAL.loadSprites("gameObjects")
        ZombieSprites = [Sprites[10], Sprites[5], Sprites[5], Sprites[10]]
        en.enemy.__init__(self, main, display, X, Y, ZombieSprites, self.zombieLifes, tileMap, player, self.zombieDamage)