import math
import random
from copy import deepcopy


class Pac():
    x = None
    y = None
    m = None
    n = None
    delete = False
    grid = None
    action_plan = []
    exploration = []
    shown_actionplan = []
    shown_exploration = []
    bfs_nums = []

    def __init__(self, xy, Grid, strategy):
        self.grid = Grid
        self.m = Grid.m
        self.n = Grid.n
        self.x = xy[0]
        self.y = xy[1]
        self.strategy = strategy
        self.type = "pacman"
        self.shown_actionplan = []

    def move(self):
        """
        This is the actual movement animation

            x,y = self.action_plan.pop(0)
            self.grid.grid[self.y][self.x] = 0
            self.grid.grid[y][x] = 1
            self.x = x
            self.y = y
            if self.x == self.grid.food_coords[0] and self.y == self.grid.food_coords[1]:
                self.grid.food_coords = []
        """

        if len(self.action_plan):
            return
        else:
            self.shown_actionplan = []
            self.shown_exploration = []
            if self.grid.food_coords:
                if self.strategy == 0:
                    res = self.find_foodBFS()
                    self.action_plan = res[0]
                    self.exploration = res[1]
                elif self.strategy == 1:
                    res = self.find_foodAStar(self.grid.food_coords)
                    self.action_plan = res[0]
                    self.exploration = res[1]
                elif self.strategy == 2:
                    visited = [[0 for i in range(self.n)] for j in range(self.m)]
                    v = []
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    random.shuffle(directions)
                    if self.find_foodDFS(self.x, self.y, v, visited, directions):
                        self.action_plan = v
                        self.exploration = deepcopy(v)



    def animate(self):
        if self.strategy == 0:
            if len(self.bfs_nums):
                num = self.bfs_nums.pop(0)
                for i in range(num):
                    self.shown_exploration.append(self.exploration.pop(0))
            else:
                self.shown_actionplan = self.action_plan

        elif self.strategy == 1:
            if len(self.exploration):
                self.shown_exploration.append(self.exploration.pop(0))
            else:
                self.shown_actionplan = self.action_plan
        elif self.strategy == 2:
            if len(self.exploration):
                self.shown_exploration.append(self.exploration.pop(0))
            else:
                self.shown_actionplan = self.action_plan


    def setStrategy(self, selected):
        self.strategy = selected
        self.action_plan = []
        self.shown_actionplan = []
        self.shown_exploration = []
        self.bfs_nums = []


    def find_foodBFS(self):
        visited = [[0 for i in range(self.n)] for j in range(self.m)]
        q = []
        v = []
        bfs_nums = []
        q.append((self.x+1, self.y, []))
        q.append((self.x-1, self.y, []))
        q.append((self.x, self.y+1, []))
        q.append((self.x, self.y-1, []))
        while len(q):
            size = len(q)
            num = 0
            for i in range(size):
                item = q.pop(0)
                x = item[0]
                y = item[1]
                path = item[2]
                if y >= self.m or y < 0 or x >= self.n or x < 0:
                    continue
                if visited[y][x] == 1 or self.grid.grid[y][x] == -1:
                    continue
                num += 1
                if self.grid.grid[y][x] == 2:
                    self.bfs_nums = bfs_nums
                    return [path + [(x,y)], v]
                v.append((x,y))
                visited[y][x] = 1
                # first fix check x,y here
                q.append((x+1, y, path + [(x,y)]))
                q.append((x-1, y, path + [(x,y)]))
                q.append((x, y+1, path + [(x,y)]))
                q.append((x, y-1, path + [(x,y)]))
            bfs_nums.append(num)
        return [[],[]]

    def find_foodDFS(self, x, y, v, visited, directions):
        if x < 0 or y < 0 or x >= self.n or y >= self.m:
            return False
        if visited[y][x] == 1 or self.grid.grid[y][x] == -1:
            return False
        visited[y][x] = 1
        v.append((x,y))
        if self.grid.grid[y][x] == 2:
            return True
        x1, y1 = directions[0]
        x2, y2 = directions[1]
        x3, y3 = directions[2]
        x4, y4 = directions[3]
        return (self.find_foodDFS(x + x1, y + y1, v, visited, directions) or self.find_foodDFS(x + x2, y + y2, v, visited, directions)
                or self.find_foodDFS(x + x3, y + y3, v, visited, directions) or self.find_foodDFS(x + x4, y + y4, v, visited, directions))



    def euclidian_distance(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return 0
        euclidean = math.sqrt(((y2 - y1)**2) + ((x2 - x1)**2))
        return euclidean


    def find_foodAStar(self, food_coords):
        visited = [[0 for i in range(self.n)] for j in range(self.m)]
        food_x = food_coords[0]
        food_y = food_coords[1]
        if self.grid.grid[food_y][food_x] != 2:
            return [[],[]]
        q = []
        q.append((self.x, self.y, [], 9999))
        v = []
        while len(q):
            item = q.pop()
            x = item[0]
            y = item[1]
            path = item[2]
            if y >= self.m or y < 0 or x >= self.n or x < 0:
                continue
            if visited[y][x] == 1 or self.grid.grid[y][x] == -1:
                continue
            if x == food_x and y == food_y:
                return [path, v]
            v.append((x,y))
            visited[y][x] = 1
            neighbors = []
            neighbors.append((x + 1, y, path + [(x + 1,y)], self.euclidian_distance(x + 1, y, food_x, food_y)))
            neighbors.append((x - 1, y, path + [(x - 1, y)], self.euclidian_distance(x - 1, y, food_x, food_y)))
            neighbors.append((x, y + 1, path + [(x, y + 1)], self.euclidian_distance(x, y + 1, food_x, food_y)))
            neighbors.append((x, y - 1, path + [(x, y - 1)], self.euclidian_distance(x, y - 1, food_x, food_y)))
            q += neighbors
            q.sort(key=lambda a: len(a[2]) + a[3])
            q.reverse()
        return [[],[]]