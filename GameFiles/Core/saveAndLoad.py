import json
from pathlib import Path
import pygame as pg



def saveRaw(data, directoryName, fileName):
    # Opening file
    f = open(Path("Objects/" + directoryName + "/" + fileName + ".json"),"w")

    # writing file
    f.write(data)

    # Closing file
    f.close()

def loadRaw(directoryName, fileName):
    # Opening file
    f = open(Path("Objects/" + directoryName + "/" + fileName + ".json"),"r")

    # Reading file
    data = f.read()

    # Closing file
    f.close()

    return data

def load(directoryName, fileName):
    # Opening file
    if directoryName != "":
        f = open(Path("Objects/" + directoryName + "/" + fileName + ".json"),"r")
    else:
        f = open(Path("Objects/" + fileName + ".json"),"r")

    # Reading file
    data = json.load(f)

    # Closing file
    f.close()

    return data

def loadProperties(Name, File, Empty): # load Properties with empty value
    # Opening JSON file
    f = open(Path("Objects/" + File + ".json"),"r")

    # Reading JSON fils
    data = json.load(f)
    outData = []
    outData.append(Empty) # First place on the list is empty

    for i in data[Name]:
        outData.append(i)
    
    # Closing file
    f.close()

    return outData

def loadPropertiesWithoutEmpty(Name, File): # load Properties without empty value
    # Opening JSON file
    f = open(Path("Objects/" + File + ".json"),"r")

    # Reading JSON fils
    data = json.load(f)
    outData = []

    for i in data[Name]:
        outData.append(i)
    
    # Closing file
    f.close()

    return outData

def loadSprites(Name):
    # Opening JSON file
    f = open(Path("Objects/Sprites.json"),"r")

    # Reading JSON fils
    data = json.load(f)
    sprites = []
    sprites.append(0) # First place on the list is empty
    for i in data[Name]:
        sprites.append(pg.image.load(Path("Sprites/"+ i)))
    
    # Closing file
    f.close()

    return sprites