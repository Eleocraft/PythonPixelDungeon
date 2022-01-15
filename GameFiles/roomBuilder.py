import pygame as pg
import Core.tileSystem as ts
import Core.saveAndLoad as SAL

class roomBuilderMain():
    def __init__(self):
        pg.init()

        # Initializing variables
        displayResolutionX = 1500
        displayResolutionY = 800
        self.text_Color = (255, 50, 50)
        self.button_Color = (170,170,170)
        self.button_pressed_Color = (50, 255, 70)
        background_Color = (0, 0, 0)
        self.bgSprites = SAL.loadSprites("bgTiles")
        self.objSprites = SAL.loadSprites("objTiles")
        self.font = pg.font.SysFont('Helvetica',25)
        selectedButtonID = 0
        selectedButtonType = "bg"
        self.entryActive = False
        self.saveName = ''

        # Initializing Pygame display
        self.display = pg.display.set_mode((displayResolutionX, displayResolutionY))
        pg.display.set_caption("Pixel Dungeon Roombuilder")

        # Initializing Clock
        self.clock = pg.time.Clock()
        self.clock.tick(60)

        # Initializing TileMap
        self.tileMap = ts.TileMap(self.display, False)

        # Initializing toolButtons
        self.Create_Buttons()

        # Main programLoop
        while True:
            # hitergrund zurücksetzen
            self.display.fill(background_Color)

            # Initializing toolButtons
            self.Create_Buttons()
            if (selectedButtonType == "bg"):
                for i in range(4):
                    pg.draw.rect(self.display, self.button_pressed_Color, (self.bgButtons[selectedButtonID].x-i,self.bgButtons[selectedButtonID].y-i,self.bgButtons[selectedButtonID].width,self.bgButtons[selectedButtonID].height), 1)
            else:
                for i in range(4):
                    pg.draw.rect(self.display, self.button_pressed_Color, (self.objButtons[selectedButtonID].x-i,self.objButtons[selectedButtonID].y-i,self.objButtons[selectedButtonID].width,self.objButtons[selectedButtonID].height), 1)

            # events abrufen
            for event in pg.event.get():
                # quit befehl
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if self.entryActive:
                        if event.key == pg.K_BACKSPACE:
                            self.saveName = self.saveName[:-1]
                        else:
                            self.saveName += event.unicode
                    elif event.key == pg.K_UP:
                        self.tileMap.Move(0, -1)
                    elif event.key == pg.K_DOWN:
                        self.tileMap.Move(0, 1)
                    elif event.key == pg.K_LEFT:
                        self.tileMap.Move(-1, 0)
                    elif event.key == pg.K_RIGHT:
                        self.tileMap.Move(1, 0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.entryActive = False
                    for i in range(len(self.bgButtons)):
                        buttonX = self.bgButtons[i].x
                        buttonY = self.bgButtons[i].y
                        buttonW = self.bgButtons[i].width
                        buttonH = self.bgButtons[i].height
                        if self.bgButtons[i].collidepoint(event.pos):
                            for t in range(4):
                                pg.draw.rect(self.display, self.button_pressed_Color, (buttonX-i,buttonY-i,buttonW,buttonH), 1)
                            selectedButtonType = "bg"
                            selectedButtonID = i
                    
                    for i in range(len(self.objButtons)):
                        buttonX = self.objButtons[i].x
                        buttonY = self.objButtons[i].y
                        buttonW = self.objButtons[i].width
                        buttonH = self.objButtons[i].height
                        if self.objButtons[i].collidepoint(event.pos):
                            for t in range(4):
                                pg.draw.rect(self.display, self.button_pressed_Color, (buttonX-i,buttonY-i,buttonW,buttonH), 1)
                            selectedButtonType = "obj"
                            selectedButtonID = i

                    for i in range(len(self.additionalButtons)):
                        buttonX = self.additionalButtons[i].x
                        buttonY = self.additionalButtons[i].y
                        buttonW = self.additionalButtons[i].width
                        buttonH = self.additionalButtons[i].height
                        if self.additionalButtons[i].collidepoint(event.pos):
                            if i==0:
                                self.tileMap.Save(self.saveName)
                                self.saveName = ""
                            elif i==1:
                                self.tileMap.Load(self.saveName)
                                self.saveName = ""
                            elif i==2:
                                newSize = self.saveName.split(",")
                                self.tileMap.ChangeSize(int(newSize[0]), int(newSize[1]))
                                self.saveName = ""
                            elif i==3:
                                self.entryActive = True
                            elif i==4:
                                self.tileMap.MoveMap(0, -1)
                            elif i==5:
                                self.tileMap.MoveMap(0, 1)
                            elif i==6:
                                self.tileMap.MoveMap(1, 0)
                            elif i==7:
                                self.tileMap.MoveMap(-1, 0)

            if (pg.mouse.get_pressed(num_buttons=3)[0]):
                if selectedButtonType == "bg":
                    self.tileMap.SetBgTile(int(pg.Vector2(pg.mouse.get_pos()).x / self.tileMap.tileSizePx), int(pg.Vector2(pg.mouse.get_pos()).y / self.tileMap.tileSizePx), selectedButtonID)
                else:
                    self.tileMap.SetObjTile(int(pg.Vector2(pg.mouse.get_pos()).x / self.tileMap.tileSizePx), int(pg.Vector2(pg.mouse.get_pos()).y / self.tileMap.tileSizePx), selectedButtonID)
            
            # aktualisieren
            self.tileMap.Draw()
            pg.display.update()

            # clock für FixedUpdate
            self.clock.tick(60)

    def Create_Buttons(self):
        # ButtonSettings
        buttonWidth = 80
        buttonHeight = 60
        arrowButtonWidth = 40
        arrowButtonHeight = 40
        self.bgButtons = []
        self.objButtons = []
        self.additionalButtons = []
        buttonSpace = 20
        posY = 490
        posYY = 560
        halfTileSize = self.tileMap.tileSizePx/2
        self.display.blit(self.font.render('Background' , True , self.text_Color), (10,posY))
        self.display.blit(self.font.render('Objects' , True , self.text_Color), (10,posYY))
        textEmpty = self.font.render('Empty' , True , self.text_Color)
        textSave = self.font.render('Save' , True , self.text_Color)
        textLoad = self.font.render('Load' , True , self.text_Color)
        textResize = self.font.render('Resize' , True , self.text_Color)
        textSaveName = self.font.render(self.saveName, True, self.text_Color)
        textUp = self.font.render("^^", True , self.text_Color)
        textDown = self.font.render('\/' , True , self.text_Color)
        textLeft = self.font.render('<' , True , self.text_Color)
        textRight = self.font.render('>' , True , self.text_Color)
        # bgTileButtons
        for i in range(len(self.bgSprites)):
            posX = 150 + (buttonSpace + buttonWidth) * i
            self.bgButtons.append(pg.draw.rect(self.display,self.button_Color,[posX,posY,buttonWidth,buttonHeight]))
            if self.bgSprites[i] != 0:
                self.display.blit(self.bgSprites[i] , (posX + buttonWidth/2 - halfTileSize, posY + buttonHeight/2 - halfTileSize))
            else:
                self.display.blit(textEmpty, (posX,posY))
        # objTileButtons
        for i in range(len(self.objSprites)):
            posX = 100 + (buttonSpace + buttonWidth) * i
            self.objButtons.append(pg.draw.rect(self.display,self.button_Color,[posX,posYY,buttonWidth,buttonHeight]))
            if self.objSprites[i] != 0:
                self.display.blit(self.objSprites[i] , (posX + buttonWidth/2 - halfTileSize, posYY + buttonHeight/2 - halfTileSize))
            else:
                self.display.blit(textEmpty, (posX,posYY))
        # SaveButton
        savePosX = 300
        savePosY = 700
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[savePosX,savePosY,buttonWidth,buttonHeight]))
        self.display.blit(textSave, (savePosX,savePosY))

        # LoadButton
        loadPosX = 400
        loadPosY = 700
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[loadPosX,loadPosY,buttonWidth,buttonHeight]))
        self.display.blit(textLoad, (loadPosX,loadPosY))

        # ResizeButton
        ResizePosX = 200
        ResizePosY = 700
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[ResizePosX,ResizePosY,buttonWidth,buttonHeight]))
        self.display.blit(textResize, (ResizePosX,ResizePosY))

        # EntryField
        entryPosX = 500
        entryPosY = 700
        highlightedColor = (200, 200, 100)
        defaultColor = (100, 100, 255)
        if (self.entryActive):
            self.additionalButtons.append(pg.draw.rect(self.display, highlightedColor,[entryPosX,entryPosY,200,30]))
        else:
            self.additionalButtons.append(pg.draw.rect(self.display, defaultColor,[entryPosX,entryPosY,200,30]))
        self.display.blit(textSaveName, (entryPosX,entryPosY))

        # MoveUpButton
        arrowPosX = 90
        arrowPosY = 650
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[arrowPosX,arrowPosY,arrowButtonWidth,arrowButtonHeight]))
        self.display.blit(textUp, (arrowPosX,arrowPosY))

        # MoveDownButton
        arrowPosX = 90
        arrowPosY = 700
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[arrowPosX,arrowPosY,arrowButtonWidth,arrowButtonHeight]))
        self.display.blit(textDown, (arrowPosX,arrowPosY))

        # MoveRightButton
        arrowPosX = 140
        arrowPosY = 700
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[arrowPosX,arrowPosY,arrowButtonWidth,arrowButtonHeight]))
        self.display.blit(textRight, (arrowPosX,arrowPosY))

        # MoveLeftButton
        arrowPosX = 40
        arrowPosY = 700
        self.additionalButtons.append(pg.draw.rect(self.display,self.button_Color,[arrowPosX,arrowPosY,arrowButtonWidth,arrowButtonHeight]))
        self.display.blit(textLeft, (arrowPosX,arrowPosY))
                
    def __del__(self):
        print("roombuilder closed")

if __name__ == "__main__":
    roomBuilderMain()