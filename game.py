import pygame as pg

GAME_WIDTH = 128
GAME_HEIGHT = 128
GAME_SCALE = 4
MAX_BRUSH_SIZE = 5

T_SOLID = 0
T_MSOLID = 1
T_LIQUID = 2
T_GAS = 3

class Element:
    def __init__(self, name, elType, color):
        self.name = name
        self.elType = elType
        self.color = color

ELEMENTS = [
    Element("void", T_SOLID, (0, 0, 0)),
    Element("sand", T_MSOLID, (255, 0, 0)),
    Element("stone", T_SOLID, (127, 127, 127)),
    Element("water", T_LIQUID, (0, 20, 200)),
    Element("steam", T_GAS, (220, 220, 220))
    ];

def UpdateMoveableSolid(game, x, y):
    if game.GetId(x, y+1) == 0:
        game.Swap(x, y, 0, 1)
    elif game.GetId(x-1, y+1) == 0:
        game.Swap(x, y, -1, 1)
    elif game.GetId(x+1, y+1) == 0:
        game.Swap(x, y, 1, 1)

def UpdateLiquid(game, x, y):
    pass

def UpdateGas(game, x, y):
    pass

def InBounds(x, y):
    return (x >= 0 and x < GAME_WIDTH and y >= 0 and y < GAME_HEIGHT)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.matrix = [[0 for y in range(GAME_HEIGHT)] for x in range(GAME_WIDTH)]
        pass

    def Repaint(self, x, y, color):
        pg.draw.rect(self.screen, color, (x*GAME_SCALE, y*GAME_SCALE, GAME_SCALE, GAME_SCALE))

    def Swap(self, x, y, dx, dy):
        tmp = self.matrix[x][y];
        self.matrix[x][y] = self.matrix[x+dx][y+dy];
        self.matrix[x+dx][y+dy] = tmp;

    def GetId(self, x, y):
        if InBounds(x, y):
            return self.matrix[x][y]
        return -1

    def UseBrush(self, x, y, elId, size):
        l = max(x-size, 0)
        r = min(x+size, GAME_WIDTH-1)
        u = max(y-size, 0)
        d = min(y+size, GAME_HEIGHT-1)
        for x in range(l, r+1):
            for y in range(u, d+1):
                self.matrix[x][y] = elId

    def Update(self):
        for sy in range(GAME_HEIGHT):
            y = GAME_HEIGHT - sy - 1
            for x in range(GAME_WIDTH):
                if ELEMENTS[self.matrix[x][y]].elType == T_MSOLID:
                    UpdateMoveableSolid(self, x, y)
                elif ELEMENTS[self.matrix[x][y]].elType == T_LIQUID:
                    UpdateLiquid(self, x, y)
                elif ELEMENTS[self.matrix[x][y]].elType == T_GAS:
                    UpdateGas(self, x, y)

        for y in range(GAME_HEIGHT):
            for x in range(GAME_WIDTH):
                self.Repaint(x, y, ELEMENTS[self.matrix[x][y]].color)

        pg.display.update()
