import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
from random import randint, choice


class AdjacencyList:
    mainDictionary = {}

    def __init__(self):  # constructor
        pass

    def getVertex(self, xCoord, yCoord):  # returns dictionary of data
        coordinates = convertCoordsToKey(xCoord, yCoord)  # convert to string form
        return self.mainDictionary[coordinates]

    def addEntry(self, xCoord, yCoord):  # creates entry and links adjacent entries
        coordinates = convertCoordsToKey(xCoord, yCoord)  # convert to string form
        adjacencyDict = {}  # stores adjacent verticies

        # check right, down, left, up for adjacency here (set up adjacency dict and preemtively link adjacent verticies)
        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord + 1, yCoord)):  # right
            adjacencyDict["Right"] = convertCoordsToKey(xCoord + 1, yCoord)
            self.mainDictionary[convertCoordsToKey(xCoord + 1, yCoord)]["Left"] = coordinates

        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord, yCoord + 1)):  # down
            adjacencyDict["Down"] = convertCoordsToKey(xCoord, yCoord + 1)
            self.mainDictionary[convertCoordsToKey(xCoord, yCoord + 1)]["Up"] = coordinates

        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord - 1, yCoord)):  # left
            adjacencyDict["Left"] = convertCoordsToKey(xCoord - 1, yCoord)
            self.mainDictionary[convertCoordsToKey(xCoord - 1, yCoord)]["Right"] = coordinates

        if checkKey(self.mainDictionary, convertCoordsToKey(xCoord, yCoord - 1)):  # up
            adjacencyDict["Up"] = convertCoordsToKey(xCoord, yCoord - 1)
            self.mainDictionary[convertCoordsToKey(xCoord, yCoord - 1)]["Down"] = coordinates

        self.mainDictionary[coordinates] = adjacencyDict

    def addStartEntry(self, xCoord, yCoord):
        self.addEntry(xCoord, yCoord)
        self.mainDictionary[convertCoordsToKey(xCoord, yCoord)]["IsStart"] = True

    def addEndEntry(self, xCoord, yCoord):
        self.addEntry(xCoord, yCoord)
        self.mainDictionary[convertCoordsToKey(xCoord, yCoord)]["IsEnd"] = True

    def getRenderData(self):
        dataList = []  # Tuples in a list
        for key in self.mainDictionary.keys():
            dataList.append(convertToTuple(key))
        return dataList

    def bfs(self, startKey):
        queue = deque([startKey])
        visited = set(startKey)  # mark start as visited
        parent = {startKey: None}  # map node to parent to trace back shortest path

        while queue:  # ... is not empty
            u = queue.popleft()

            if "IsEnd" in self.mainDictionary[u]:  # exit has been found
                path = [u]
                while path[-1] != startKey:  # trace back path
                    path.append(parent[path[-1]])
                path.reverse()
                return path

            if "Left" in self.mainDictionary[u]:  # left is not a wall
                if self.mainDictionary[u]["Left"] not in visited:
                    queue.append(self.mainDictionary[u]["Left"])  # add adjacent node to queue
                    parent[self.mainDictionary[u]["Left"]] = u  # add parent information to trace back shortest path
                    visited.add(self.mainDictionary[u]["Left"])  # mark node as visited

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
        visited = set(startKey)
        parent = {startKey: None}

        while stack:  # ... is not empty
            u = stack.pop()

            if "IsEnd" in self.mainDictionary[u]:  # exit has been found
                path = [u]
                while path[-1] != startKey:  # trace back path
                    path.append(parent[path[-1]])
                path.reverse()
                return path

            if u not in visited:
                visited.add(u)

                if "Left" in self.mainDictionary[u]:  # left is not a wall
                    if self.mainDictionary[u]["Left"] not in visited:
                        stack.append(self.mainDictionary[u]["Left"])  # add adjacent node to queue
                        parent[self.mainDictionary[u]["Left"]] = u  # add parent information to trace back shortest path

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

    def returnValidDirections(self, key):  # returns a set of valid directions that the carver can hop to
        coords = convertToTuple(key)  # x and y
        validDirs = ["Right", "Down", "Left", "Up"]  # filled list, remove as needed
        minRange = 0
        maxRange = 699

        Checkers = ((1, 1), (1, 0), (1, -1), (2, 1), (2, 0), (2, -1))  # swap X and Y for Right(or left) vs Down(or up); swap signs to go from (right/up) to (left/down)

        for i in Checkers:
            # Right Check
            if convertCoordsToKey(coords[0] + i[0], coords[1] + i[1]) in self.mainDictionary.keys() or coords[0] >= maxRange:
                if "Right" in validDirs:
                    validDirs.remove("Right")  # right is invalid

            # Left Check
            if convertCoordsToKey(coords[0] - i[0], coords[1] - i[1]) in self.mainDictionary.keys() or coords[0] <= minRange:
                if "Left" in validDirs:
                    validDirs.remove("Left")  # left is invalid

            # Up check
            if convertCoordsToKey(coords[0] - i[1], coords[1] - i[0]) in self.mainDictionary.keys() or coords[1] <= minRange:
                if "Up" in validDirs:
                    validDirs.remove("Up")  # up is invalid

            # Down Check
            if convertCoordsToKey(coords[0] + i[1], coords[1] + i[0]) in self.mainDictionary.keys() or coords[1] >= maxRange:
                if "Down" in validDirs:
                    validDirs.remove("Down")  # down is invalid

        return validDirs

    def generateMaze(self):
        self.mainDictionary = {}
        startingX = randint(0, 699)
        startingY = randint(0, 699)
        startingKey = convertCoordsToKey(startingX, startingY)

        carverStack = deque([startingKey])  # initial carver point
        self.addEntry(startingX, startingY)  # initial carver point

        # MAIN GENERATION ALGORITHM FOR CARVING MAZE
        while carverStack:  # has elements

            stackTop = carverStack[0]  # gets top element(where the carver is right now)
            topCoords = convertToTuple(stackTop)  # gets numerical form of the coords
            validDirs = self.returnValidDirections(stackTop)  # gets set of valid directions

            if not validDirs and carverStack:  # If there are no valid directions and carver stack has elements left
                carverStack.popleft()  # pop off the stack and attempt a previous point
                continue

            randomDirection = choice(validDirs)  # choses random direction for carver to move in if valid direction exists

            #uncomment this line to print out all of the data if you want
            #print(randomDirection + stackTop)

            if randomDirection == "Right":
                self.addEntry(topCoords[0] + 1, topCoords[1])
                carverStack.appendleft(convertCoordsToKey(topCoords[0] + 1, topCoords[1]))

            if randomDirection == "Left":
                self.addEntry(topCoords[0] - 1, topCoords[1])
                carverStack.appendleft(convertCoordsToKey(topCoords[0] - 1, topCoords[1]))

            if randomDirection == "Up":
                self.addEntry(topCoords[0], topCoords[1] - 1)
                carverStack.appendleft(convertCoordsToKey(topCoords[0], topCoords[1] - 1))

            if randomDirection == "Down":
                self.addEntry(topCoords[0], topCoords[1] + 1)
                carverStack.appendleft(convertCoordsToKey(topCoords[0], topCoords[1] + 1))

        # add start and end elements
        while True:  # keeps running until we finally add the start entry
            randCoords = generateRandCoordTup()
            if convertCoordsToKey(randCoords[0], randCoords[1]) in self.mainDictionary.keys():
                self.addStartEntry(randCoords[0], randCoords[1])
                startCoords = randCoords
                break

        while True:  # keeps running until we finally add the end entry
            randCoords = generateRandCoordTup()
            if convertCoordsToKey(randCoords[0], randCoords[1]) in self.mainDictionary.keys() and randCoords != startCoords:
                self.addEndEntry(randCoords[0], randCoords[1])
                break


def generateRandCoordTup():
    X = randint(0, 699)
    Y = randint(0, 699)
    return X, Y


def convertToTuple(key):
    coordList = key.split(",")
    tuplePair = (int(coordList[0]), int(coordList[1]))
    return tuplePair


def convertCoordsToKey(xCoord, yCoord):
    return str(xCoord) + "," + str(yCoord)


# returns true if key exists in given dict
def checkKey(dictionary, key):
    if key in dictionary.keys():
        return True
    return False


maze = AdjacencyList()

root = tk.Tk()
root.title("Project 3 Group 54")
root.geometry("1025x750")
root.resizable(False, False)

window_frame = tk.Frame(root, bg="#313131")
window_frame.place(relwidth=1, relheight=1)

maze_frame = tk.Frame(window_frame, bg="#545454")
maze_frame.place(x=25, y=25, width=700, height=700)

maze_canvas_image = [Image.new("RGB", (700, 700), "#212121")]
maze_canvas_image_tk = [ImageTk.PhotoImage(image=maze_canvas_image[0])]

maze_canvas = [tk.Canvas(maze_frame, bg="#545454")]
maze_canvas[0].place(relwidth=1, relheight=1)
maze_image_instance = [maze_canvas[0].create_image(0, 0, anchor="nw", image=maze_canvas_image_tk[0])]

solve_button = tk.Button(window_frame, text="Solve!", fg="white", bg="#424242", activebackground="#424242", activeforeground="white", font="Fixedsys", state="disabled")
solve_button.place(x=787, y=590, width=175, height=50)

generate_button = tk.Button(window_frame, text="Generate New Maze", fg="white", bg="#424242", activebackground="#424242", activeforeground="white", font="Fixedsys")
generate_button.place(x=750, y=665, width=250, height=50)

stats_list = ["Most Recent Times", "BFS: N/A", "DFS: N/A", "\nAverage Times", "BFS: N/A", "DFS: N/A", "\nRelative Performance", "BFS: N/A", "DFS: N/A"]
stats_label = tk.Label(window_frame, bg="#424242", fg="white", text="\n".join(stats_list), font="Fixedsys", relief="ridge")
stats_label.place(x=750, y=25, width=250, height=540)


def generate_button_function():
    solve_button.config(state="disabled")
    maze_canvas[0].delete(maze_image_instance[0])
    maze_canvas_image[0].close()
    maze_canvas_image[0] = Image.new("RGB", (700, 700), "#212121")
    maze.generateMaze()
    for path in maze.getRenderData():
        maze_canvas_image[0].putpixel(path, (255, 255, 255))
    maze_canvas_image_tk[0] = ImageTk.PhotoImage(image=maze_canvas_image[0])
    maze_image_instance[0] = maze_canvas[0].create_image(0, 0, anchor="nw", image=maze_canvas_image_tk[0])
    solve_button.config(state="active")


def solve_button_function():
    pass


solve_button.config(command=solve_button_function)
generate_button.config(command=generate_button_function)
root.mainloop()
