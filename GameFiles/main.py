import pygame as pg
import Core.tileSystem as ts
import Player.player as pl
import Enemys.spider as sp
import Enemys.zombie as zo
import Enemys.skelett as sk
import Enemys.boss as bo


class main():
    playerSpawnPos = pg.Vector2(5, 5)
    def __init__(self):
        pg.init()

        # Initializing variables
        background_Color = (0, 0, 0)
        displayResolutionX = 1920
        displayResolutionY = 1080

        # Initializing Pygame display
        self.display = pg.display.set_mode((displayResolutionX, displayResolutionY))
        pg.display.set_caption("Pixel Dungeon by Eliseo Cailloux und Keanu Aras")

        # Initializing Clock
        self.clock = pg.time.Clock()
        self.clock.tick(60)

        # Initializing Enemys
        self.enemys = []
        self.enemySpawnPoints = []
        self.enemyTypes = []

        # Initializing TileMap
        self.tileMap = ts.TileMap(self.display, self)

        # Initializing Player
        self.player = pl.Player(self, self.display, self.playerSpawnPos.x, self.playerSpawnPos.y, self.tileMap)

        # Spawning Enemys
        for i in range(len(self.enemySpawnPoints)):
            if (self.enemyTypes[i] == "Spider"):
                self.enemys.append(sp.Spider(self, self.display, self.enemySpawnPoints[i][0], self.enemySpawnPoints[i][1], self.tileMap, self.player))
            elif (self.enemyTypes[i] == "Zombie"):
                self.enemys.append(zo.Zombie(self, self.display, self.enemySpawnPoints[i][0], self.enemySpawnPoints[i][1], self.tileMap, self.player))
            elif (self.enemyTypes[i] == "Skelett"):
                self.enemys.append(sk.Skelett(self, self.display, self.enemySpawnPoints[i][0], self.enemySpawnPoints[i][1], self.tileMap, self.player))
            elif (self.enemyTypes[i] == "Boss"):
                self.enemys.append(bo.Boss(self, self.display, self.enemySpawnPoints[i][0], self.enemySpawnPoints[i][1], self.tileMap, self.player))

    
        # Main gameloop
        while True:
            # hitergrund zurücksetzen
            self.display.fill(background_Color)

            # events abrufen
            for event in pg.event.get():
                # quit befehl
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.player.usePotion(0)
                        self.action()
                    elif event.key == pg.K_2:
                        self.player.usePotion(1)
                        self.action()
                    elif event.key == pg.K_3:
                        self.player.usePotion(2)
                        self.action()
                    elif event.key == pg.K_4:
                        self.player.usePotion(3)
                        self.action()
                    elif event.key == pg.K_5:
                        self.player.usePotion(4)
                        self.action()
                    elif event.key == pg.K_0:
                        print(self.player.Lifes)
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.Vector2(event.pos).x, pg.Vector2(event.pos).y
                    self.player.Move(x, y, self.enemys)

            # aktualisieren
            self.tileMap.Draw()
            self.player.Draw()
            for i in self.enemys:
                i.Draw()
            self.player.inventory.Draw()
            pg.display.update()

            # clock für FixedUpdate
            self.clock.tick(60)

    def spawn(self, points, types, uninit):
        if uninit == True:
            self.enemySpawnPoints.extend(points)
            self.enemyTypes.extend(types)
        else:
            self.enemySpawnPoints.extend(points)
            self.enemyTypes.extend(types)
            # Spawning Enemys
            for i in range(len(points)):
                if (types[i] == "Spider"):
                    self.enemys.append(sp.Spider(self, self.display, points[i][0], points[i][1], self.tileMap, self.player))
                elif (types[i] == "Zombie"):
                    self.enemys.append(zo.Zombie(self, self.display, points[i][0], points[i][1], self.tileMap, self.player))
                elif (types[i] == "Skelett"):
                    self.enemys.append(sk.Skelett(self, self.display, points[i][0], points[i][1], self.tileMap, self.player))
                elif (types[i] == "Boss"):
                    self.enemys.append(bo.Boss(self, self.display, points[i][0], points[i][1], self.tileMap, self.player))

    def delEnemy(self, enemy):
        self.enemys.remove(enemy)

    def gameOver(self):
        pg.quit()
        quit()
    
    def action(self):
        for i in self.enemys:
            i.Move()
    
    def __del__(self):
        print("pixel dungeon closed")

if __name__ == "__main__":
    main()