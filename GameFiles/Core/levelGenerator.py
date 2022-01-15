import pygame as pg
import random as prng
import math
import Core.saveAndLoad as SAL
import Core.Utility.MST as MST
import Core.Utility.Utils as Utils
import Core.pathfinding as pf

InitCircleRadius = 20
ConnectionPercent = 10
spawnPointOffset = pg.Vector2(2, 2)

def generateLevel(tileMap, roomcount):
    RoomData = SAL.load("", "Rooms")
    RoomDoors = []
    for i in range(len(RoomData["Rooms"])):
        RoomDoors.append(SAL.load("Rooms", RoomData["Rooms"][i])["DoorSpawnPoints"])
    RoomNames = RoomData["Rooms"]
    RoomSizes = RoomData["BigRoom"]

    Rooms = []
    MainRooms = []

    # creating spawnRoom
    RoomObject = SAL.load("Rooms", "spawnRoom")
    size = pg.Vector2(RoomObject["mapSizeX"], RoomObject["mapSizeY"])
    room = Room(pg.Vector2(0,0), len(RoomNames) - 1, size)
    Rooms.append(room)
    MainRooms.append(room)

    # creating endRoom
    RoomObject = SAL.load("Rooms", "endRoom")
    size = pg.Vector2(RoomObject["mapSizeX"], RoomObject["mapSizeY"])
    room = Room(getRandomPointInCircle(InitCircleRadius), len(RoomNames) - 2, size)
    Rooms.append(room)
    MainRooms.append(room)

    # Initial Room-Spawning inside a circle with the radius InitCircleRadius
    for i in range(roomcount):
        pos = getRandomPointInCircle(InitCircleRadius)
        roomId = prng.randint(0, len(RoomNames) - 2)
        RoomObject = SAL.load("Rooms", RoomNames[roomId])
        size = pg.Vector2(RoomObject["mapSizeX"], RoomObject["mapSizeY"])
        room = Room(pos, roomId, size)
        Rooms.append(room)
        if RoomSizes[roomId] == True:
            MainRooms.append(room)

    # All Rooms are oved out until there are no colisions left
    noColisions = False
    while not noColisions:
        noColisions = True
        for i in range(roomcount):
            for t in range(roomcount):
                if i != t and Rooms[i].rect.colliderect(Rooms[t].rect):
                    if (Rooms[i].pos != Rooms[t].pos):
                        direction = Rooms[i].pos - Rooms[t].pos
                        direction = direction.normalize()
                    else:
                        direction = pg.Vector2(0, 1)
                    Rooms[i].move(direction)
                    noColisions = False
    
    for i in Rooms:
        i.actualize()

    # Delunay Diagramm between Main Rooms
    g = MST.Graph(len(MainRooms))
    DelaunayEdges = []
    for i in range(len(MainRooms)):
        for t in range(i + 1, len(MainRooms)):
            pos1 = MainRooms[i].pos
            pos2 = MainRooms[t].pos
            length = Utils.distance(pos1, pos2)
            g.addEdge(i, t, length)
            DelaunayEdges.append([i, t, length])
    
    # Minimum spanning tree to detect the connections between rooms
    MinimumSpanningTree = g.KruskalMST()
    ConnectionsReuse = math.floor(len(DelaunayEdges) / ConnectionPercent)
    DelaunayEdges = [x for x in DelaunayEdges if x not in MinimumSpanningTree]

    # Adding back ConnectionPercent amount of edges
    for i in range(ConnectionsReuse):
        EdgeToAdd = prng.choice(DelaunayEdges)
        MinimumSpanningTree.append(EdgeToAdd)
        DelaunayEdges.remove(EdgeToAdd)

    # and converting the conection tree from MainRoom indexes to Room indexes
    for i in range(len(MinimumSpanningTree)):
        MinimumSpanningTree[i][0] = Rooms.index(MainRooms[MinimumSpanningTree[i][0]])
        MinimumSpanningTree[i][1] = Rooms.index(MainRooms[MinimumSpanningTree[i][1]])
    
    # Based on the Edges, now other Rooms are spawned back in
    FinalRoomList = []
    for i in MainRooms:
        FinalRoomList.append(Rooms.index(i))
    
    EdgeRooms = [[] for i in range(len(MinimumSpanningTree))]

    for i in range(len(MinimumSpanningTree)):
        EdgeRooms[i].append([MinimumSpanningTree[i][0], 0])
        EdgeRooms[i].append([MinimumSpanningTree[i][1], MinimumSpanningTree[i][2]])
    
    for i in range(roomcount):
        if Rooms[i] not in MainRooms:
            for t in range(len(MinimumSpanningTree)):
                IntersectionData = Rooms[i].intersectWithEdge(MinimumSpanningTree[t], Rooms)
                if IntersectionData != False:
                    EdgeRooms[t].append([i, IntersectionData])
                    if i not in FinalRoomList:
                        FinalRoomList.append(i)

    RoomConnections = []

    # Creating all connections between Rooms
    for i in range(len(EdgeRooms)):
        t = 0
        while t < len(EdgeRooms[i]):
            if t != 0 and EdgeRooms[i][t][1] < EdgeRooms[i][t-1][1]:
                EdgeRooms[i][t], EdgeRooms[i][t-1] = EdgeRooms[i][t-1], EdgeRooms[i][t]
                t -= 1
            else:
                t += 1
        
        for t in range(len(EdgeRooms[i])):
            if t != 0:
                RoomConnections.append([EdgeRooms[i][t-1][0], EdgeRooms[i][t][0]])

    # The Roomdata is passed to the tilemap, where the rooms are actually placed
    for i in range(len(FinalRoomList)):
        tileMap.SetRoom(RoomNames[Rooms[FinalRoomList[i]].id], Rooms[FinalRoomList[i]].pos.x + tileMap.mapSizeX / 2, Rooms[FinalRoomList[i]].pos.y + tileMap.mapSizeY / 2)

    # Creating the actual pathways using the pathfinding class
    for i in RoomConnections:
        path, Door1, Door2 = getConnection(Rooms[i[0]], Rooms[i[1]], RoomDoors, tileMap)
        if isinstance(path, list) and path != []:
            path.insert(0, Door1)
            path.append(Door2)
            for n in path:
                tileMap.SetBgTileRaw(n.x, n.y, 1)
                adjacentTilePositionsX = [n.x, n.x, n.x+1, n.x-1]
                adjacentTilePositionsY = [n.y+1, n.y-1, n.y, n.y]
                for i in range(4):
                    X, Y = int(adjacentTilePositionsX[i]), int(adjacentTilePositionsY[i])
                    if tileMap.bgTileMap[X][Y] == 0 or tileMap.bgTileMap[X][Y] == 5:
                        tileMap.SetBgTileRaw(X, Y, 4)
    
    spawnPoint = pg.Vector2(int(Rooms[0].pos.x + spawnPointOffset.x + tileMap.mapSizeX / 2), (Rooms[0].pos.y + spawnPointOffset.y + tileMap.mapSizeY / 2))
    return spawnPoint

def getRandomPointInCircle(radius):
    t = 2*math.pi*prng.random()
    u = prng.random()+prng.random()
    if u > 1:
        r = 2-u
    else: 
        r = u
    return pg.Vector2(radius*r*math.cos(t), radius*r*math.sin(t))

def getConnection(Room1, Room2, RoomDoors, tileMap):
    blockedDoors = []
    trys = 0
    while True:
        trys += 1
        if trys > 10:
            return 0, 0, 0
        smallestDist = 1000
        for i in RoomDoors[Room1.id]:
            for t in RoomDoors[Room2.id]:
                DoorPos1 = pg.Vector2(i[0] + Room1.pos.x + tileMap.mapSizeX / 2, i[1] + Room1.pos.y + tileMap.mapSizeY / 2)
                DoorPos2 = pg.Vector2(t[0] + Room2.pos.x + tileMap.mapSizeX / 2, t[1] + Room2.pos.y + tileMap.mapSizeY / 2)
                dist = Utils.distance(DoorPos1, DoorPos2)
                if dist < smallestDist and (DoorPos1 not in blockedDoors or DoorPos2 not in blockedDoors):
                    smallestDist = dist
                    Door1 = DoorPos1
                    Door2 = DoorPos2
        try:
            Door1
        except NameError:
            return 0, 0, 0

        tileMap.SetBgTileRaw(Door1.x, Door1.y, 5)
        tileMap.SetBgTileRaw(Door2.x, Door2.y, 5)
        path = pf.calculatePath(tileMap, Door1.x, Door1.y, Door2.x, Door2.y, 100)
        if not isinstance(path, list) or path == []:
            path = []
            blockedDoors.extend([Door1, Door2])
            tileMap.SetBgTileRaw(Door1.x, Door1.y, 4)
            tileMap.SetBgTileRaw(Door2.x, Door2.y, 4)
        else:
            break
    return path, Door1, Door2

class Room():
    def __init__(self, pos, id, size):
        self.pos = pos
        self.id = id
        self.size = size + pg.Vector2(2, 2)
        self.rect = pg.Rect(pos, (self.size.x, self.size.y))
    def move(self, direction):
        self.pos += direction
        self.rect = pg.Rect(self.pos, (self.size.x, self.size.y))
    def actualize(self):
        self.pos = pg.Vector2(int(self.pos.x), int(self.pos.y))
        self.rect = pg.Rect(self.pos, (self.size.x, self.size.y))
    def intersectWithEdge(self, Edge, RootRooms):
        pos1 = RootRooms[Edge[0]].pos
        pos2 = RootRooms[Edge[1]].pos
        Intersection = self.rect.clipline(pos1, pos2)
        if not Intersection:
            return False
        start, end = Intersection
        x1, y1 = start
        x2, y2 = end
        DistToRoom1 = min(Utils.distance(pg.Vector2(x1, y1), pos1), Utils.distance(pg.Vector2(x2, y2), pos1))
        return DistToRoom1