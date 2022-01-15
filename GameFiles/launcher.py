import pygame as pg
from pathlib import Path
import subprocess

class launcher():
    def __init__(self):
        pg.init()

        # Initializing variables
        background_Color = (0, 0, 0)
        displayResolutionX = 560
        displayResolutionY = 560

        # Initializing Pygame display
        self.display = pg.display.set_mode((displayResolutionX, displayResolutionY))
        pg.display.set_caption("Pixel Dungeon Launcher")

        # Title Screen
        title = pg.image.load(Path("Sprites/Title.png"))
        startButton = pg.image.load(Path("Sprites/StartButton.png"))
        buildMenuButton = pg.image.load(Path("Sprites/buildMenuButton.png"))

        # Button
        self.font = pg.font.SysFont('Helvetica',40)
        buttonPosX = 125
        buttonPosY = 400
        buildMenuButtonOffset = 225

        # Initializing Clock
        self.clock = pg.time.Clock()
        self.clock.tick(60) 

        # Main loop
        while True:
            # hitergrund zurücksetzen
            self.display.fill(background_Color)

            # events abrufen
            for event in pg.event.get():
                # quit befehl
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if StartButton.collidepoint(event.pos):
                        subprocess.call(["python", "main.py"])
                    elif BuildMenuButton.collidepoint(event.pos):
                        subprocess.call(["python", "roomBuilder.py"])

            # aktualisieren
            self.display.blit(title, (0, 0))
            StartButton = self.display.blit(startButton, (buttonPosX,buttonPosY))
            BuildMenuButton = self.display.blit(buildMenuButton, (buttonPosX + buildMenuButtonOffset ,buttonPosY))
            pg.display.update()

            # clock für FixedUpdate
            self.clock.tick(60)

    def __del__(self):
        print("pixel dungeon launcher Closed")

if __name__ == "__main__":
    launcher()