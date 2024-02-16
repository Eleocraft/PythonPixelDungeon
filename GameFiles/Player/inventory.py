import pygame as pg
import Core.saveAndLoad as SAL

class inventory():
    invX = 50
    invY = 1000
    def __init__(self, display):
        self.display = display
        self.sword = 0
        self.armor = 0
        self.ring = 0

        self.potions = [0, 0, 0, 0, 0]

        self.itemFrames = SAL.loadSprites("ItemFrames")
        self.swordSprites = SAL.loadSprites("Swords")
        self.armorSprites = SAL.loadSprites("Armors")
        self.ringSprites = SAL.loadSprites("Rings")
        self.potionSprites = SAL.loadSprites("Potions")

        self.swordDamages = SAL.loadProperties("Swords", "ItemAttributes", 1)
        self.armorResistances = SAL.loadProperties("Armors", "ItemAttributes", 1)

    def Draw(self):
        # 3 itmemFrames for the sword, the armor and the ring
        self.display.blit(self.itemFrames[1], (self.invX, self.invY))
        if self.sword != 0:
            self.display.blit(self.swordSprites[self.sword], (self.invX, self.invY))

        self.display.blit(self.itemFrames[1], (self.invX + 50, self.invY))
        if self.armor != 0:
            self.display.blit(self.armorSprites[self.armor], (self.invX + 50, self.invY))

        self.display.blit(self.itemFrames[1], (self.invX + 100, self.invY))
        if self.ring != 0:
            self.display.blit(self.ringSprites[self.ring], (self.invX + 100, self.invY))

        # 5 itemFrames for the Potions
        for i in range(len(self.potions)):
            posX = self.invX + 200 + 50 * i
            self.display.blit(self.itemFrames[2], (posX, self.invY))
            if self.potions[i] != 0:
                self.display.blit(self.potionSprites[self.potions[i]], (posX, self.invY))

    def addPotion(self, potion):
        for i in range(len(self.potions)):
            if self.potions[i] == 0:
                self.potions[i] = potion
                return True
        return False

    def usePotion(self, slotID):
        potion = self.potions[slotID]
        self.potions[slotID] = 0
        return potion

    def changeSword(self, newSword):
        oldSword = self.sword
        self.sword = newSword
        return oldSword

    def changeArmor(self, newArmor):
        oldArmor = self.armor
        self.armor = newArmor
        return oldArmor

    def changeRing(self, newRing):
        oldRing = self.ring
        self.ring = newRing
        return oldRing

    def getDamage(self):
        if self.ring == 3:
            return 2 * self.swordDamages[self.sword]
        return self.swordDamages[self.sword]

    def getArmor(self):
        if self.ring == 2:
            return 2 * self.armorResistances[self.armor]
        return self.armorResistances[self.armor]

    def getMaxLifes(self):
        if self.ring == 1:
            return 20
        return 10

    def addItem(self, ItemType, ItemID):
        if ItemType == "Swords":
            return "Swords", self.changeSword(ItemID)
        elif ItemType == "Armors":
            return "Armors", self.changeArmor(ItemID)
        elif ItemType == "Rings":
            return "Rings", self.changeRing(ItemID)
        elif ItemType == "Potions":
            self.addPotion(ItemID)
            return False