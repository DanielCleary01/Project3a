import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from collections import deque
from random import randint, choice
import time


class AdjacencyList:
    mainDictionary = {}
    startKey = ""
    endKey = ""

    def __init__(self, maze_size):  # constructor
        self.size = maze_size

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
        self.startKey = convertCoordsToKey(xCoord, yCoord)

    def addEndEntry(self, xCoord, yCoord):
        self.addEntry(xCoord, yCoord)
        self.mainDictionary[convertCoordsToKey(xCoord, yCoord)]["IsEnd"] = True
        self.endKey = convertCoordsToKey(xCoord, yCoord)

    def getRenderData(self):
        dataList = []  # Tuples in a list
        for key in self.mainDictionary.keys():
            dataList.append(convertToTuple(key))
        return dataList

    def bfs(self):
        startKey = self.startKey
        queue = deque([startKey])
        route = []
        visited = set(startKey)  # mark start as visited
        parent = {startKey: None}  # map node to parent to trace back shortest path

        while queue:  # ... is not empty
            u = queue.popleft()
            route.append(u)

            if "IsEnd" in self.mainDictionary[u]:  # exit has been found
                path = [u]
                while path[-1] != startKey:  # trace back path
                    path.append(parent[path[-1]])
                path.reverse()
                return route

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

    def dfs(self):
        startKey = self.startKey
        stack = deque([startKey])
        visited = set(startKey)
        route = []
        parent = {startKey: None}

        while stack:  # ... is not empty
            u = stack.pop()
            route.append(u)

            if "IsEnd" in self.mainDictionary[u]:  # exit has been found
                path = [u]
                while path[-1] != startKey:  # trace back path
                    path.append(parent[path[-1]])
                path.reverse()
                return route

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
        maxRange = self.size-1

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

    def generateMaze(self, window):
        #empties the maze
        self.mainDictionary = {}
        self.startKey = ""
        self.endKey = ""

        startingX = randint(0, self.size-1)
        startingY = randint(0, self.size-1)
        startingKey = convertCoordsToKey(startingX, startingY)

        carverStack = deque([startingKey])  # initial carver point
        self.addEntry(startingX, startingY)  # initial carver point

        loading_counter = 0
        loading_text = ["Loading", "Loading.", "Loading..", "Loading..."]
        loading_label = tk.Label(window, bg="#212121", fg="white", text="", font=("Fixedsys", 20), relief="ridge")
        loading_label.place(y=25, x=25, width=700, height=700)

        # MAIN GENERATION ALGORITHM FOR CARVING MAZE
        while carverStack:  # has elements
            if loading_counter % 10000 == 0:
                loading_label.config(text=loading_text[int(loading_counter/10000) % 4])
            window.update()
            loading_counter += 1

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
            randCoords = generateRandCoordTup(self.size)
            if convertCoordsToKey(randCoords[0], randCoords[1]) in self.mainDictionary.keys():
                self.addStartEntry(randCoords[0], randCoords[1])
                startCoords = randCoords
                break

        while True:  # keeps running until we finally add the end entry
            randCoords = generateRandCoordTup(self.size)
            if convertCoordsToKey(randCoords[0], randCoords[1]) in self.mainDictionary.keys() and randCoords != startCoords:
                self.addEndEntry(randCoords[0], randCoords[1])
                break

        loading_label.destroy()

    def returnStartKey(self):
        return convertToTuple(self.startKey)

    def returnEndKey(self):
        return convertToTuple(self.endKey)


def generateRandCoordTup(size):
    X = randint(0, size-1)
    Y = randint(0, size-1)
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


maze = AdjacencyList(700)

root = tk.Tk()
root.title("Project 3 Group 54")
root.geometry("1025x750")
root.resizable(False, False)

window_frame = tk.Frame(root, bg="#313131")
window_frame.place(relwidth=1, relheight=1)

maze_frame = tk.Frame(window_frame, bg="#545454")
maze_frame.place(x=22, y=22, width=706, height=706)

maze_canvas_image = [Image.new("RGB", (700, 700), "#212121")]
maze_canvas_image_tk = [ImageTk.PhotoImage(image=maze_canvas_image[0])]
maze_canvas_merge_image = [maze_canvas_image[0].copy()]
merging = [False]

maze_canvas = [tk.Canvas(maze_frame, bg="#212121")]
maze_canvas[0].place(relwidth=1, relheight=1)
maze_image_instance = [maze_canvas[0].create_image(3, 3, anchor="nw", image=maze_canvas_image_tk[0])]

toggle_merge_overlay = tk.Checkbutton(window_frame, text="Highlight Overlap", variable=merging[0], relief=tk.RIDGE, bg="#313131", fg="white", activeforeground="white", activebackground="#313131", selectcolor="#414141", font="Fixedsys")
toggle_merge_overlay.place(x=750, y=615, width=250, height=25)

generate_button = tk.Button(window_frame, text="New Maze", fg="black", bg="#424242", activebackground="#424242", activeforeground="black", font="Fixedsys")
generate_button.place(x=750, y=650, width=250, height=50)

title_frame = tk.Frame(window_frame, bg="#424242", highlightbackground="#767676", highlightthickness=2)
title_frame.place(x=750, y=25, width=249, height=100)

title_bfs_label = tk.Label(title_frame, bg="#424242", fg="#bd0d0d", text="BFS", font=("Fixedsys", 20), relief="ridge")
title_bfs_label.place(relwidth=1/3, relheight=1, relx=0)
title_vs_label = tk.Label(title_frame, bg="#424242", fg="white", text="VS", font=("Fixedsys", 20), relief="ridge")
title_vs_label.place(relwidth=1/3, relheight=1, relx=1/3)
title_dfs_label = tk.Label(title_frame, bg="#424242", fg="#1faabf", text="DFS", font=("Fixedsys", 20), relief="ridge")
title_dfs_label.place(relwidth=1/3, relheight=1, relx=2/3)

stats_list = ["Starting Point: N/A", "Goal Point: N/A", "\nMost Recent Times", "BFS: N/A", "DFS: N/A", "\nAverage Times", "BFS: N/A", "DFS: N/A", "\nRelative Performance", "BFS: N/A", "DFS: N/A"]
stats_label = tk.Label(window_frame, bg="#424242", fg="white", text="\n".join(stats_list), font=("Fixedsys", 16), relief="ridge")
stats_label.place(x=750, y=125, width=250, height=490)

dfs_total_time = [0]
bfs_total_time = [0]
maze_count = [0]


def update_maze_image():
    maze_canvas_image_tk[0] = ImageTk.PhotoImage(image=maze_canvas_image[0] if not merging[0] else maze_canvas_merge_image[0])
    maze_canvas[0].delete(maze_image_instance[0])
    maze_image_instance[0] = maze_canvas[0].create_image(3, 3, anchor="nw", image=maze_canvas_image_tk[0])
    root.update()


def generate_button_function():
    generate_button.config(state="disabled")
    if maze_count[0] > 0:
        for i in range(175):
            maze_canvas_image[0] = maze_canvas_image[0].crop((0, 4, maze_canvas_image[0].size[0], maze_canvas_image[0].size[1]))
            update_maze_image()
    maze.generateMaze(root)
    maze_canvas[0].delete(maze_image_instance[0])
    maze_canvas_image[0].close()
    maze_canvas_image[0] = Image.new("RGB", (700, 700), "#212121")
    renderData = maze.getRenderData()
    for i in range(len(renderData)):
        maze_canvas_image[0].putpixel(renderData[i], (0, 0, 0))
        if i % 1000 == 0:
            update_maze_image()
            time.sleep(0.02)
    update_maze_image()
    start_coord = maze.returnStartKey()
    end_coord = maze.returnEndKey()
    adjacent_start_coords = [(start_coord[0]+1, start_coord[1]+1), (start_coord[0]-1, start_coord[1]-1), (start_coord[0]+1, start_coord[1]), (start_coord[0]-1, start_coord[1]), (start_coord[0], start_coord[1]+1), (start_coord[0], start_coord[1]-1), (start_coord[0]+1, start_coord[1]-1), (start_coord[0]-1, start_coord[1]+1)]
    adjacent_end_coords = [(end_coord[0]+1, end_coord[1]+1), (end_coord[0]-1, end_coord[1]-1), (end_coord[0]+1, end_coord[1]), (end_coord[0]-1, end_coord[1]), (end_coord[0], end_coord[1]+1), (end_coord[0], end_coord[1]-1), (end_coord[0]+1, end_coord[1]-1), (end_coord[0]-1, end_coord[1]+1)]
    maze_canvas_merge_image[0] = maze_canvas_image[0].copy()
    for i in range(10):
        for f in range(len(adjacent_start_coords)):
            if 0 <= adjacent_start_coords[f][0] < 700 and 0 <= adjacent_start_coords[f][1] < 700:
                maze_canvas_image[0].putpixel(adjacent_start_coords[f], ((255, 0, 0) if i % 2 == 0 else maze_canvas_merge_image[0].getpixel(adjacent_start_coords[f])))
            if 0 <= adjacent_end_coords[f][0] < 700 and 0 <= adjacent_end_coords[f][1] < 700:
                maze_canvas_image[0].putpixel(adjacent_end_coords[f], ((0, 255, 0) if i % 2 == 0 else maze_canvas_merge_image[0].getpixel(adjacent_end_coords[f])))
        update_maze_image()
        time.sleep(0.1)
    maze_count[0] += 1
    start = time.time()
    dfs_path = maze.dfs()
    dfs_time = time.time()-start
    dfs_total_time[0] += dfs_time
    start_dfs_rgb = (29, 52, 97)
    end_dfs_rgb = (92, 200, 255)
    start = time.time()
    bfs_path = maze.bfs()
    bfs_time = time.time() - start
    bfs_total_time[0] += bfs_time
    start_merge_rgb = (117, 0, 117)
    end_merge_rgb = (255, 46, 255)
    start_bfs_rgb = (84, 11, 14)
    end_bfs_rgb = (196, 32, 33)
    max_length = max(len(bfs_path), len(dfs_path))
    time.sleep(0.5)
    for i in range(max_length):
        if i < len(bfs_path):
            bfs_coord = convertToTuple(bfs_path[i])
        else:
            bfs_coord = None
        if i < len(dfs_path):
            dfs_coord = convertToTuple(dfs_path[i])
        else:
            dfs_coord = None
        if bfs_coord is not None:
            bfs_color = maze_canvas_image[0].getpixel(bfs_coord)
            if bfs_color != (0, 0, 0):
                maze_canvas_image[0].putpixel(bfs_coord, (start_bfs_rgb[0] - round(i * (start_bfs_rgb[0] - end_bfs_rgb[0]) / len(bfs_path)), start_bfs_rgb[1] - round(i * (start_bfs_rgb[1] - end_bfs_rgb[1]) / len(bfs_path)), start_bfs_rgb[2] - round(i * (start_bfs_rgb[2] - end_bfs_rgb[2]) / len(bfs_path))))
                maze_canvas_merge_image[0].putpixel(bfs_coord, (start_merge_rgb[0] - round(i * (start_merge_rgb[0] - end_merge_rgb[0]) / len(bfs_path)), start_merge_rgb[1] - round(i * (start_merge_rgb[1] - end_merge_rgb[1]) / len(bfs_path)), start_merge_rgb[2] - round(i * (start_merge_rgb[2] - end_merge_rgb[2]) / len(bfs_path))))
            else:
                maze_canvas_image[0].putpixel(bfs_coord, (start_bfs_rgb[0] - round(i*(start_bfs_rgb[0]-end_bfs_rgb[0])/len(bfs_path)), start_bfs_rgb[1] - round(i*(start_bfs_rgb[1]-end_bfs_rgb[1])/len(bfs_path)), start_bfs_rgb[2] - round(i*(start_bfs_rgb[2]-end_bfs_rgb[2])/len(bfs_path))))
                maze_canvas_merge_image[0].putpixel(bfs_coord, (round((start_bfs_rgb[0] - round(i * (start_bfs_rgb[0] - end_bfs_rgb[0]) / len(bfs_path)))/2), round(start_bfs_rgb[1] - round(i * (start_bfs_rgb[1] - end_bfs_rgb[1]) / len(bfs_path))/2), round(start_bfs_rgb[2] - round(i * (start_bfs_rgb[2] - end_bfs_rgb[2]) / len(bfs_path))/2)))

        if dfs_coord is not None:
            dfs_color = maze_canvas_image[0].getpixel(dfs_coord)
            if dfs_color != (0, 0, 0):
                maze_canvas_image[0].putpixel(dfs_coord, (start_dfs_rgb[0] - round(i * (start_dfs_rgb[0] - end_dfs_rgb[0]) / len(dfs_path)), start_dfs_rgb[1] - round(i * (start_dfs_rgb[1] - end_dfs_rgb[1]) / len(dfs_path)), start_dfs_rgb[2] - round(i * (start_dfs_rgb[2] - end_dfs_rgb[2]) / len(dfs_path))))
                maze_canvas_merge_image[0].putpixel(dfs_coord, (start_merge_rgb[0] - round(i * (start_merge_rgb[0] - end_merge_rgb[0]) / len(dfs_path)), start_merge_rgb[1] - round(i * (start_merge_rgb[1] - end_merge_rgb[1]) / len(dfs_path)), start_merge_rgb[2] - round(i * (start_merge_rgb[2] - end_merge_rgb[2]) / len(dfs_path))))
            else:
                maze_canvas_image[0].putpixel(dfs_coord, (start_dfs_rgb[0] - round(i * (start_dfs_rgb[0] - end_dfs_rgb[0]) / len(dfs_path)), start_dfs_rgb[1] - round(i * (start_dfs_rgb[1] - end_dfs_rgb[1]) / len(dfs_path)), start_dfs_rgb[2] - round(i * (start_dfs_rgb[2] - end_dfs_rgb[2]) / len(dfs_path))))
                maze_canvas_merge_image[0].putpixel(dfs_coord, (round((start_dfs_rgb[0] - round(i * (start_dfs_rgb[0] - end_dfs_rgb[0]) / len(dfs_path)))/2), round(start_dfs_rgb[1] - round(i * (start_dfs_rgb[1] - end_dfs_rgb[1]) / len(dfs_path))/2), round(start_dfs_rgb[2] - round(i * (start_dfs_rgb[2] - end_dfs_rgb[2]) / len(dfs_path))/2)))
        if i % 50 == 0:
            update_maze_image()
            time.sleep(0.005)
    update_maze_image()
    stats_list[0] = f"Starting Point: {maze.returnStartKey()}"
    stats_list[1] = f"Goal Point: {maze.returnEndKey()}"
    stats_list[3] = f"BFS: {round(bfs_time, 3)}s"
    stats_list[4] = f"DFS: {round(dfs_time, 3)}s"
    try:
        stats_list[6] = f"BFS: {round(bfs_total_time[0]/maze_count[0], 3)}s"
        stats_list[7] = f"DFS: {round(dfs_total_time[0]/maze_count[0], 3)}s"
        stats_list[9] = f"BFS: {round((dfs_total_time[0]/maze_count[0])/(bfs_total_time[0]/maze_count[0]), 3)}x"
        stats_list[10] = f"DFS: {round((bfs_total_time[0]/maze_count[0])/(dfs_total_time[0]/maze_count[0]), 3)}x"
    except ZeroDivisionError:
        pass
    stats_label.config(text="\n".join(stats_list))
    generate_button.config(state="active")


def toggle_merging(event=None):
    merging[0] = not merging[0]
    update_maze_image()


toggle_merge_overlay.config(command=toggle_merging)
generate_button.config(command=generate_button_function)
root.mainloop()
