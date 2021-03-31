from PIL import Image
import copy
import sys

sys.setrecursionlimit(3000)

IMAGE_PATH = 'huger.png'

# 1 = white
# 0 = black

class Maze():
    def __init__(self, width, height, pixels):
        self.grid = []
        self.width = width
        self.height = height
        for x in range(0, width):
            self.grid.append([])
            for y in range(0, height):
                self.grid[x].append(Coordinate(x, y, pixels[x,y]))

    def setStart(self, x, y):
        self.grid[x][y].isStart = True
        self.start = self.grid[x][y]

    def setEnd(self, x, y):
        self.grid[x][y].isEnd = True
        self.end = self.grid[x][y]

    def safeGetCoord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        try:
            return self.grid[x][y]
        except:
            return False


class Coordinate():
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.isStart = False
        self.isEnd = False

    def isWhite(self):
        return (self.colour == (255,255,255))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Path():
    def __init__(self):
        self.history = []

    def addToHistory(self, coord):
        self.history.append(coord)

def openImage():
    print(f'Loading image {IMAGE_PATH}.')
    img = Image.open(IMAGE_PATH).convert('RGB')
    print(f'Image loaded.')
    print(f'Image size: {img.size}')
    return img

def findStart(maze):
    for x in range(0,maze.width):
        if maze.grid[x][0].isWhite():
            print(maze.grid[x][0].colour)
            print(f"Start found at ({x},0)")
            maze.setStart(x, 0)
            return True
    return False

def findEnd(maze):
    for x in range(0,maze.width):
        if maze.grid[x][maze.height-1].isWhite():
            print(f"End found at ({x},{maze.height-1})")
            maze.setEnd(x, maze.height-1)
            return True
    return False

def move(maze, path, current_coord):
    global winning_path
    print(f"Assessing ({current_coord.x}, {current_coord.y})")
    new_path = Path()
    new_path.history = copy.copy(path.history)


    # check if end
    if (current_coord.isEnd):
        print("all done")
        new_path.addToHistory(current_coord)
        winning_path = new_path.history
        return True


    skippable = True
    while skippable:
        new_path.addToHistory(current_coord)
        neighbours = getNeighbours(maze, current_coord)
        if len(neighbours) == 2:
            for neighbour in neighbours:
                # print(neighbour)
                if neighbour not in new_path.history:
                    new_path.history.append(current_coord)
                    current_coord = neighbour
        else:
            skippable = False

    for neighbour in neighbours:
        if neighbour.isWhite() and neighbour not in new_path.history:

            print(f"Moving to {neighbour.x}, {neighbour.y}")
            if move(maze, new_path, neighbour):
                return True

    # else
    print("Dead end!")
    return False

def getNeighbours(maze, current_coord):
    up = maze.safeGetCoord(current_coord.x,current_coord.y-1)
    down = maze.safeGetCoord(current_coord.x,current_coord.y+1)
    left = maze.safeGetCoord(current_coord.x-1,current_coord.y)
    right = maze.safeGetCoord(current_coord.x+1,current_coord.y)
    neighbours = [up,down,left,right]
    
    valid_neighbours = []
    for direction in neighbours:
        if direction and direction.isWhite():
            valid_neighbours.append(direction)
    return valid_neighbours

def drawWinningPath(image, path, file_name):
    pixels = image.load()
    for coords in path:
        pixels[coords.x,coords.y] = (255,0,0) #red
    image.save(f'solved-{file_name}')

winning_path = []
image = openImage()
pixels = image.load()
maze = Maze(image.width, image.height, pixels)
if (not findStart(maze) or not findEnd(maze)):
    print("Error, invalid maze image.")
    exit()
move(maze, Path(), maze.start)
drawWinningPath(image, winning_path, IMAGE_PATH)
