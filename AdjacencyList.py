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


def convertToTuple(key):   
    coordList = key.split(",")
    tuplePair = (int(coordList[0]), int(coordList[1]))
    return tuplePair

def convertCoordsToKey(xCoord, yCoord):
    return (xCoord + "," + yCoord)

#returns true if key exists in given dict
def checkKey(dict, key):
    if key in dict.keys():
        return True
    return False
