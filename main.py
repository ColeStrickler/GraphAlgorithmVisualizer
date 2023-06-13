import math
import time
import random
from pacman import Pac
import pygame as p
from checkbox import Checkbox
from mazegen import MazeGenerator


class Grid():
    grid = None
    width = None
    height = None
    m = None
    n = None
    pacman_drawn = False
    pacman_pos = ()
    pacman = None
    color = (124,252,175)
    pyg = None
    block_size = 50
    screen = None
    settings_width = 300
    mode = 1
    food_coords = []
    entities = []
    genMaze_Button = None
    resetGrid_Button = None
    show_exploration = True

    def __init__(self, m, n, pyg):
        self.pyg = pyg
        self.m = m
        self.n = n
        self.grid = [[0 for i in range(n)] for j in range(m)]
        self.width = (self.block_size * n) + self.settings_width
        self.height = self.block_size * m
        self.pyg.font.init()
        self.label_font = self.pyg.font.SysFont('Comic Sans MS', 25)
        self.setting_font = self.pyg.font.SysFont('Comic Sans MS', 15)
        self.settings_buttons_coords = self.getCheckboxCoords()
        self.current_searchAlgorithm = 0
        self.current_AnimationSettings = [3,4]
        self.current_genMaze = 5

    def set_color(self, c1, c2, c3):
        self.color = (c1, c2, c3)

    def getDimensions(self):
        return self.width, self.height

    def drawBoard(self, screen):
        self.drawSettings(screen)
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    p.draw.rect(screen, self.color, p.Rect(i*self.block_size,j*self.block_size,self.block_size,self.block_size))
                elif self.grid[i][j] == 1:
                    p.draw.rect(screen, p.Color("yellow"), p.Rect(i*self.block_size, j*self.block_size, self.block_size, self.block_size))
                elif self.grid[i][j] == 2:
                    p.draw.rect(screen, p.Color("orange"), p.Rect(i*self.block_size, j*self.block_size, self.block_size, self.block_size))
                elif self.grid[i][j] == -1:
                    p.draw.rect(screen, p.Color("black"), p.Rect(i * self.block_size, j * self.block_size, self.block_size, self.block_size))
                elif self.grid[i][j] == 3:
                    p.draw.rect(screen, p.Color("red"), p.Rect(i * self.block_size, j * self.block_size, self.block_size, self.block_size))


    def checkButtonClicks(self, location, screen):
        x, y = location
        px1, py1, w1, h1 = self.genMaze_Button
        px2, py2, w2, h2 = self.resetGrid_Button
        if px1 < x < px1 + w1 and py1 < y < py1 + h1:
            m = MazeGenerator(self)
            m.planMaze(screen)
            self.entities.clear()
            self.entities.append(m)
        elif px2 < x < px2 + w2 and py2 < y < py2 + h2:
            self.entities.clear()
            self.grid = [[0 for i in range(self.n)] for j in range(self.m)]



    def drawSettings(self, screen):
        offset_x = self.m * self.block_size
        p.draw.rect(screen, p.Color("gray"), p.Rect(offset_x, 0, self.settings_width, self.height))
        genmaze_text = self.label_font.render('Generate Maze', False, (0, 0, 0))
        reset_text = self.label_font.render('Reset Grid', False, (0, 0, 0))
        if not self.genMaze_Button:
            self.genMaze_Button = p.Rect(offset_x + 55, (self.height/4) * 3, genmaze_text.get_width() + 10, genmaze_text.get_height() + 20)
        if not self.resetGrid_Button:
            self.resetGrid_Button = p.Rect(offset_x + 55, (self.height / 4) * 3 + 100, genmaze_text.get_width() + 10, genmaze_text.get_height() + 20)
        p.draw.rect(screen, p.Color("DodgerBlue2"), self.genMaze_Button)
        p.draw.rect(screen, p.Color("DodgerBlue2"), self.resetGrid_Button)
        screen.blit(genmaze_text, (offset_x + 60, (self.height/4) * 3 + 5))
        screen.blit(reset_text, (offset_x + 85, (self.height/4) * 3 + 110))
        text_objects = self.getSettingsObjects()
        offset_y = 0
        buttons = {}
        for t in text_objects:
            screen.blit(t[0], (offset_x + 20, offset_y))
            s_offset_y = offset_y + (self.height/4) / (len(t[1]) + 1)
            for s in t[1]:
                screen.blit(s, (offset_x + 20, s_offset_y))
                s_offset_y += (self.height/4) / (len(t[1]) + 1)
            offset_y += self.height/4

    def getCheckboxCoords(self):
        offset_x = self.m * self.block_size
        text_objects = self.getSettingsObjects()
        offset_y = 0
        buttons = {}
        for t in text_objects:
            s_offset_y = offset_y + (self.height / 4) / (len(t[1]) + 1)
            buttons[t[2]] = []
            for s in t[1]:
                buttons[t[2]].append((offset_x + self.settings_width - 40, s_offset_y + 5))
                s_offset_y += (self.height / 4) / (len(t[1]) + 1)
            offset_y += self.height / 4
        return buttons

    def getSettingsObjects(self):
        maze_gen_text = self.label_font.render('Generate Maze:', False, (0, 0, 0))
        randomized_dfs = self.setting_font.render('Randomized DFS', False, (0, 0, 0))
        randomized_kruskals = self.setting_font.render("Randomized Kruskal's", False, (0, 0, 0))
        randomized_prims = self.setting_font.render("Randomized Prim's", False, (0, 0, 0))
        search_algorithm_text = self.label_font.render('Search Algorithm:', False, (0, 0, 0))
        bfs_text = self.setting_font.render('BFS', False, (0, 0, 0))
        astar_text = self.setting_font.render('A*', False, (0, 0, 0))
        dfs_text = self.setting_font.render('DFS', False, (0, 0, 0))
        animation_setting_text = self.label_font.render('Animation Settings:', False, (0, 0, 0))
        instant_text = self.setting_font.render('Instant:', False, (0, 0, 0))
        show_exploration = self.setting_font.render('Show Exploration:', False, (0, 0, 0))
        return [(search_algorithm_text, [bfs_text, astar_text, dfs_text], 'SearchAlgorithm'),
                (animation_setting_text, [instant_text, show_exploration], 'AnimationSettings'),
                (maze_gen_text, [randomized_dfs, randomized_prims, randomized_kruskals], 'MazeGen')]



    def draw_pacman(self, xy):
        y = (xy[0] - (xy[0] % self.block_size)) / self.block_size
        x = (xy[1] - (xy[1] % self.block_size)) / self.block_size
        x = int(x)
        y = int(y)
        if x > (self.n * self.block_size): # this is glue code, we need to set up better control flow for this
            return
        if not self.pacman_drawn:
            self.pacman_pos = (x,y)
            self.grid[y][x] = 1
            self.pacman_drawn = True
        else:
            self.pacman.delete = True
            old_x,old_y = self.pacman_pos
            self.grid[old_y][old_x] = 0
            self.pacman_pos = (x, y)
            self.grid[y][x] = 1
        p = Pac((x,y), self, self.current_searchAlgorithm)
        self.pacman = p
        self.entities.append(p)


    def draw_food(self, xy):
        if len(self.food_coords):
            self.grid[self.food_coords[1]][self.food_coords[0]] = 0
        y = (xy[0] - (xy[0] % self.block_size)) / self.block_size
        x = (xy[1] - (xy[1] % self.block_size)) / self.block_size
        x = int(x)
        y = int(y)
        self.grid[y][x] = 2
        self.food_coords = [x, y]


    def update_mode(self):
        modes = {1: "Place Source", 2: "Place Target", 3: "Place Obstacle"}


        if self.mode % 3 == 0:
            self.mode = 1
        else:
            self.mode += 1
        print(f"Mode: {modes[self.mode]}")


    def draw_boundary(self, xy):
        y = (xy[0] - (xy[0] % self.block_size)) / self.block_size
        x = (xy[1] - (xy[1] % self.block_size)) / self.block_size
        x = int(x)
        y = int(y)
        self.grid[y][x] = -1
    def draw(self, xy,):
        if self.mode == 1:
            self.draw_pacman(xy)
        elif self.mode == 2:
            self.draw_food(xy)
        elif self.mode == 3:
            self.draw_boundary(xy)




def init_checkboxes(pygame, screen, coord_dict, grid):
    ret = []
    id = 0
    for key in coord_dict.keys():
        for coord in coord_dict[key]:
            c = Checkbox(screen, coord[0], coord[1], id, caption='', pygame=pygame)
            ret.append(c)
            if grid.current_searchAlgorithm == id or grid.current_genMaze == id or grid.current_AnimationSettings == id or id == 3 or id == 4:
                c.checked = True
            id += 1
    return ret


def draw_rect_alpha(surface, color, rect):
    shape_surf = p.Surface(p.Rect(rect).size, p.SRCALPHA)
    p.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def displayPathing(grid, screen, pac):
    block_size = grid.block_size
    if 4 in grid.current_AnimationSettings:         # display exploration checkbox is marked
        for c in pac.exploration:
            draw_rect_alpha(screen, (245, 243, 39, 175), (c[1] * block_size, c[0] * block_size, block_size, block_size))
    for c in pac.action_plan:
        draw_rect_alpha(screen, (255, 0, 0, 175), (c[1] * block_size, c[0] * block_size, block_size, block_size))


def displayAnimation(grid, screen, pac):
    block_size = grid.block_size
    if 4 in grid.current_AnimationSettings:         # display exploration checkbox is marked
        for c in pac.shown_exploration:
            draw_rect_alpha(screen, (245, 243, 39, 175), (c[1] * block_size, c[0] * block_size, block_size, block_size))
    for c in pac.shown_actionplan:
        draw_rect_alpha(screen, (255, 0, 0, 175), (c[1] * block_size, c[0] * block_size, block_size, block_size))



g = Grid(20, 20, p)
def main():
    p.init()
    screen = p.display.set_mode(g.getDimensions())
    p.display.set_caption('Graph Algorithm Visualizer')
    running = True
    clock = p.time.Clock()
    checkboxes = init_checkboxes(p, screen, g.settings_buttons_coords, g)


    """
    m = MazeGenerator(g)
    m.planMaze(screen)
    while not m.delete:
        g.drawBoard(screen)
        m.move()
        clock.tick(15)
        p.display.flip()
    """

    while running:
        g.drawBoard(screen)
        for c in checkboxes:
            c.render_checkbox()



        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()

                if location[0] < (g.block_size * g.n):
                    g.draw(location)
                else:
                    for c in checkboxes:
                       c._update(g, checkboxes, location)
                    g.checkButtonClicks(location, screen)


            elif e.type == p.KEYDOWN:
                g.update_mode()

        i = 0
        for e in g.entities:
            if e.delete:
                g.entities.remove(e)
            else:
                e.move()
                if e.type == "pacman":
                    if 3 in g.current_AnimationSettings:
                        if len(e.action_plan):
                            displayPathing(g, screen, e)
                    else:
                        e.animate()
                        displayAnimation(g, screen, e)



        clock.tick(15)
        p.display.flip()
main()