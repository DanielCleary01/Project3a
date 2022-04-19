from audioop import add
from collections import deque
from random import randint, choice

class AdjacencyList:
    mainDictionary = {}

    def __init__(self):#constructor
        pass

    def getVertex(self, xCoord, yCoord):#returns dictionary of data
        coordinates = convertCoordsToKey(xCoord, yCoord) #convert to string form
        return self.mainDictionary[coordinates]

    def addEntry(self, xCoord, yCoord):#creates entry and links adjacent entries
        coordinates = convertCoordsToKey(xCoord, yCoord) #convert to string form
        adjacencyDict = {}#stores adjacent verticies

        #check right, down, left, up for adjacency here (set up adjacency dict and preemtively link adjacent verticies)
        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord+1, yCoord)):#right
            adjacencyDict["Right"] = convertCoordsToKey(xCoord+1, yCoord)
            self.mainDictionary[convertCoordsToKey(xCoord+1, yCoord)]["Left"] = coordinates

        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord, yCoord+1)):#down
            adjacencyDict["Down"] = convertCoordsToKey(xCoord, yCoord+1)
            self.mainDictionary[convertCoordsToKey(xCoord, yCoord+1)]["Up"] = coordinates

        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord-1, yCoord)):#left
            adjacencyDict["Left"] = convertCoordsToKey(xCoord-1, yCoord)
            self.mainDictionary[convertCoordsToKey(xCoord-1, yCoord)]["Right"] = coordinates

        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord, yCoord-1)):#up
            adjacencyDict["Up"] = convertCoordsToKey(xCoord, yCoord-1)
            self.mainDictionary[convertCoordsToKey(xCoord, yCoord-1)]["Down"] = coordinates

        self.mainDictionary[coordinates] = adjacencyDict

    def addStartEntry(self, xCoord, yCoord):
        self.addEntry(xCoord, yCoord)
        self.mainDictionary[convertCoordsToKey(xCoord, yCoord)]["IsStart"] = True

    def addEndEntry(self, xCoord, yCoord):
        self.addEntry(xCoord, yCoord)
        self.mainDictionary[convertCoordsToKey(xCoord, yCoord)]["IsEnd"] = True

    def getRenderData(self):
        dataList = [] #Tuples in a list
        for key in self.mainDictionary.keys():
            dataList.append(convertToTuple(key))
        return dataList

    def bfs(self, startKey):
        queue = deque([startKey])
        visited = set((startKey))#mark start as visited
        parent = {startKey : None}#map node to parent to trace back shortest path

        while queue:#... is not empty
            u = queue.popleft()

            if "IsEnd" in self.mainDictionary[u]:#exit has been found
                path = [u]
                while path[-1] != startKey:#trace back path
                    path.append(parent[path[-1]])
                path.reverse()
                return path

            if "Left" in self.mainDictionary[u]:#left is not a wall
                if self.mainDictionary[u]["Left"] not in visited:
                    queue.append(self.mainDictionary[u]["Left"])#add adjacent node to queue
                    parent[self.mainDictionary[u]["Left"]] = u#add parent information to trace back shortest path
                    visited.add(self.mainDictionary[u]["Left"])#mark node as visited

            if "Up" in self.mainDictionary[u]:
                if self.mainDictionary[u]["Up"] not in visited:
                    queue.append(self.mainDictionary[u]["Up"])
                    parent[self.mainDictionary[u]["Up"]] = u
                    visited.add(self.mainDictionary[u]["Up"])

            if "Right" in self.mainDictionary[u]:
                if self.mainDictionary[u]["Right"] not in visited:
                    queue.append(self.mainDictionary[u]["Right"])
                    parent[self.mainDictionary[u]["Right"]] = u
                    visited.add(self.mainDictionary[u]["Right"])

            if "Down" in self.mainDictionary[u]:
                if self.mainDictionary[u]["Down"] not in visited:
                    queue.append(self.mainDictionary[u]["Down"])
                    parent[self.mainDictionary[u]["Down"]] = u
                    visited.add(self.mainDictionary[u]["Down"])

    def dfs(self, startKey):
        stack = deque([startKey])
        visited = set((startKey))
        parent = {startKey : None}

        while stack:#... is not empty
            u = stack.pop()

            if "IsEnd" in self.mainDictionary[u]:#exit has been found
                path = [u]
                while path[-1] != startKey:#trace back path
                    path.append(parent[path[-1]])
                path.reverse()
                return path

            if u not in visited:
                visited.add(u)

                if "Left" in self.mainDictionary[u]:#left is not a wall
                    if self.mainDictionary[u]["Left"] not in visited:
                        stack.append(self.mainDictionary[u]["Left"])#add adjacent node to queue
                        parent[self.mainDictionary[u]["Left"]] = u#add parent information to trace back shortest path

                if "Up" in self.mainDictionary[u]:
                    if self.mainDictionary[u]["Up"] not in visited:
                        stack.append(self.mainDictionary[u]["Up"])
                        parent[self.mainDictionary[u]["Up"]] = u

                if "Right" in self.mainDictionary[u]:
                    if self.mainDictionary[u]["Right"] not in visited:
                        stack.append(self.mainDictionary[u]["Right"])
                        parent[self.mainDictionary[u]["Right"]] = u

                if "Down" in self.mainDictionary[u]:
                    if self.mainDictionary[u]["Down"] not in visited:
                        stack.append(self.mainDictionary[u]["Down"])
                        parent[self.mainDictionary[u]["Down"]] = u

    def deleteMaze(self):
        self.mainDictionary = {}

    def returnValidDirections(self, key):#returns a set of valid directions that the carver can hop to
        coords = convertToTuple(key)#x and y
        validDirs = ("Right", "Down", "Left", "Up") #filled tuple, pop as needed
        minRange = 0
        maxRange = 999
        
        Checkers = ((1, 1), (1, 0), (1, -1), (2, 1), (2, 0), (2, -1)) #swap X and Y for Right(or left) vs Down(or up); swap signs to go from (right/up) to (left/down)
     
        for i in Checkers:
            #Right Check
            if convertCoordsToKey(coords[0]+Checkers[i][0], coords[1]+Checkers[i][1]) in self.mainDictionary.keys() or coords[0] > maxRange:
                validDirs.pop("Right")#right is invalid

            #Left Check
            if convertCoordsToKey(coords[0]-Checkers[i][0], coords[1]-Checkers[i][1]) in self.mainDictionary.keys() or coords[0] < minRange:
                validDirs.pop("Left")#left is invalid

            #Down check
            if convertCoordsToKey(coords[0]-Checkers[i][1], coords[1]-Checkers[i][0]) in self.mainDictionary.keys() or coords[1] > maxRange:
                validDirs.pop("Up")#up is invalid

            #Up Check
            if convertCoordsToKey(coords[0]+Checkers[i][1], coords[1]+Checkers[i][0]) in self.mainDictionary.keys() or coords[1] < minRange:
                validDirs.pop("Down")#down is invalid

        return validDirs

    def generateMaze(self, seed):

        if seed != 0: #If we set the seed to 0, then it'll just be random
            seed(seed) #sets rng seed

        startingX = randint(0, 699, 1)
        startingY = randint(0, 699, 1)
        startingKey = convertCoordsToKey(startingX, startingY)

        carverStack = deque([startingKey]) #initial carver point
        self.addEntry(startingX, startingY) #initial carver point

        #MAIN GENERATION ALGORITHM FOR CARVING MAZE
        while carverStack: #has elements
            
            stackTop = carverStack[0] #gets top element(where the carver is right now)
            topCoords = convertToTuple(stackTop) #gets numerical form of the coords
            validDirs = self.returnValidDirections(stackTop) #gets set of valid directions
            
            if not validDirs and carverStack: #If there are no valid directions and carver stack has elements left
                carverStack.pop() #pop off the stack and attempt a previous point
                continue

            randomDirection = choice(validDirs) #choses random direction for carver to move in if valid direction exists


            if randomDirection == "Right":
                self.addEntry(topCoords[0]+1, topCoords[1])
                carverStack.append(convertCoordsToKey(topCoords[0]+1, topCoords[1]))

            if randomDirection == "Left":
                self.addEntry(topCoords[0]-1, topCoords[1])
                carverStack.append(convertCoordsToKey(topCoords[0]-1, topCoords[1]))

            if randomDirection == "Up":
                self.addEntry(topCoords[0], topCoords[1]-1)
                carverStack.append(convertCoordsToKey(topCoords[0], topCoords[1]-1))

            if randomDirection == "Down":
                self.addEntry(topCoords[0], topCoords[1]+1)
                carverStack.append(convertCoordsToKey(topCoords[0], topCoords[1]+1))

        #add start and end elements
        while True:#keeps running until we finally add the start entry
            randCoords = generateRandCoordTup()
            if convertCoordsToKey(randCoords[0], randCoords[1]) in self.mainDictionary.keys():
                self.addStartEntry(randCoords[0], randCoords[1])
                startCoords = randCoords
                break

        while True:#keeps running until we finally add the end entry
            randCoords = generateRandCoordTup()
            if convertCoordsToKey(randCoords[0], randCoords[1]) in self.mainDictionary.keys() and randCoords != startCoords:
                self.EndEntry(randCoords[0], randCoords[1])
                break


def generateRandCoordTup():
    X = randint(0, 699, 1)
    Y = randint(0, 699, 1)
    return (X,Y)


def convertToTuple(key):   
    coordList = key.split(",")
    tuplePair = (int(coordList[0]), int(coordList[1]))
    return tuplePair

def convertCoordsToKey(xCoord, yCoord):
    return (str(xCoord) + "," + str(yCoord))

#returns true if key exists in given dict
def checkKey(dict, key):
    if key in dict.keys():
        return True
    return False