import Core.saveAndLoad as SAL
import Core.Utility.Utils as Utils

class Item():
    def __init__(self, x, y, tileMap, ItemType, ItemID):
        self.x = x
        self.y = y
        self.tileMap = tileMap
        self.ItemType = ItemType
        self.ItemID = ItemID
        self.sprite = SAL.loadSprites(ItemType)[ItemID]

    def Draw(self):
        displayX = (self.x - self.tileMap.offsetX) * self.tileMap.tileSizePx
        displayY = (self.y - self.tileMap.offsetY) * self.tileMap.tileSizePx
        self.tileMap.display.blit(self.sprite, (displayX, displayY))

    def pickup(self):
        return self.ItemType, self.ItemID

def OpenChest():
    typeProbabilities = SAL.loadPropertiesWithoutEmpty("Types", "ItemSpawnProbabilities")
    typeList = ["Swords", "Armors", "Potions", "Rings"]
    type = typeList[Utils.RandomFromList(typeProbabilities)]
    itemProbabilities = SAL.loadPropertiesWithoutEmpty(type, "ItemSpawnProbabilities")
    item = Utils.RandomFromList(itemProbabilities) + 1
    return type, item