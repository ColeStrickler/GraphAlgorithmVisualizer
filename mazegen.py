import random

class DisjointSet:
    def __init__(self, nodes):
        self.node_mapping = {}
        for i,val in enumerate(nodes):
            n = self.DSNode(val, i)
            self.node_mapping[val] = n

    def find(self, node):
        return self.find_node(node).parent

    def find_node(self, node):
        if type(self.node_mapping[node].parent) is int:
            return self.node_mapping[node]
        else:
            parent_node = self.find_node(self.node_mapping[node].parent.val)
            self.node_mapping[node].parent = parent_node
            return parent_node

    def union(self, node1, node2):
        parent1 = self.find_node(node1)
        parent2 = self.find_node(node2)
        if parent1.parent != parent2.parent:
            parent1.parent = parent2

    class DSNode:
        def __init__(self, val, parent):
            self.val = val
            self.parent = parent



class MazeGenerator():
    delete = False
    def __init__(self, Grid):
        for i in range(Grid.m):
            for j in range(Grid.n):
                Grid.grid[i][j] = -1
        self.grid = Grid
        self.visited = [[0 for i in range(self.grid.n)] for j in range(self.grid.m)]
        self.plan = []
        self.type = "mazegen"
    def planMaze(self, screen):
        row = int(random.random() * (self.grid.m - 2)) + 1
        col = int(random.random() * (self.grid.n - 2)) + 1

        if self.grid.current_genMaze == 5:
            self.dfs_mazegen(row, col, [(row, col)])
        elif self.grid.current_genMaze == 6:
            self.prims_mazegen(row, col, [(row, col)])
        elif self.grid.current_genMaze == 7:
            self.kruskals_mazegen()

    def move(self):
        if len(self.plan) == 0:
            self.delete = True
            return
        else:
            if 3 in self.grid.current_AnimationSettings: # instant animation
                for i in range(len(self.plan)):
                    move = self.plan.pop(0)
                    self.grid.grid[move[0]][move[1]] = 0
            else:
                move = self.plan.pop(0)
                self.grid.grid[move[0]][move[1]] = 0

    def dfs_mazegen(self, i, j, path):
        if i == 0 or i == self.grid.m - 1 or j == 0 or j == self.grid.n - 1:
            return
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(moves)

        for m in moves:
            if self.visited[i + m[0]][j + m[1]] != 1:
                self.visited[i + m[0]][j + m[1]] = 1
                if m[0] == 0:
                    self.visited[i + 1][j] = 1
                    self.visited[i - 1][j] = 1
                else:
                    self.visited[i][j + 1] = 1
                    self.visited[i][j - 1] = int(random.random() + .35)
                path.append((i + m[0], j + m[1]))
                self.plan = path
                self.dfs_mazegen(i + m[0], j + m[1], path)

    def prims_mazegen(self, i, j, path):
        q = [(i,j, i, j)]
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        while(len(q)):
            random.shuffle(q)
            i, j, prev_i, prev_j = q.pop()
            if i < 0 or i >= self.grid.m - 1 or j < 0 or j >= self.grid.n - 1:
                continue
            if self.visited[i][j] == 1:
                continue
            random.shuffle(directions)
            # appending moves
            i_shift = 0
            j_shift = 0
            while i + i_shift != prev_i:
                if i > prev_i:
                    path.append((i - i_shift, j))
                    i_shift -= 1
                else:
                    path.append((i + i_shift, j))
                    i_shift += 1
                self.visited[i+i_shift][j] = 1

            while j + j_shift != prev_j:
                if j > prev_j:
                    path.append((i, j - j_shift))
                    j_shift -= 1
                else:
                    path.append((i, j + j_shift))
                    j_shift += 1
                self.visited[i][j+j_shift] = 1
            path.append((prev_i, prev_j))

            for id, jd in directions:
                q.append((i+id, j+jd, i, j))
        self.plan = path

    def kruskals_mazegen(self):
        nodes = [(i, j) for j in range(0,self.grid.n,2) for i in range(0,self.grid.m,2)]
        neighbors = lambda n: [(n[0] + dx, n[1] + dy) for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2))
                               if
                               n[0] + dx >= 0 and n[0] + dx < self.grid.n and n[1] + dy >= 0 and n[1] + dy < self.grid.m]

        edges = [(node, nbor) for node in nodes for nbor in neighbors(node)]
        ds = DisjointSet(nodes)
        maze = []
        path = []
        while len(path) < len(nodes) - 1 and len(edges) > 0:
            edge = edges.pop(random.randint(0, len(edges) - 1))
            if ds.find(edge[0]) != ds.find(edge[1]):
                ds.union(edge[0], edge[1])
                maze.append(edge)
        for c in maze:
            i1, j1 = c[0]
            i2, j2 = c[1]
            path.append((i1, j1))
            path.append((i2, j2))
            if i1 != i2:
                path.append((int((i1+i2)/2), j1))
            else:
                path.append((i1, int((j1+j2)/2)))
        self.plan = path








