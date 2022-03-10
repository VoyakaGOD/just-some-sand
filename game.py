import pygame as pg
import numpy as np
from numba import jit
from random import random

GAME_WIDTH = 128
GAME_HEIGHT = 128
GAME_SCALE = 4
MAX_BRUSH_SIZE = 6

class Element:
    def __init__(self, name, color):
        self.name = name
        self.color = color

ELEMENTS = [
    Element("void", (0, 0, 0)),
    Element("sand", (255, 0, 0)),
    Element("stone", (127, 127, 127)),
    Element("water", (0, 20, 200)),
    Element("steam", (220, 220, 220))
    ];

EL_COLORS = np.zeros([len(ELEMENTS)],dtype=np.uint32)
for i in range(len(ELEMENTS)):
    color = ELEMENTS[i].color
    EL_COLORS[i] = color[2] + 256*(color[1] + 256*color[0])

ID_VOID = 0
ID_SAND = 1
ID_STONE = 2
ID_WATER = 3
ID_STEAM = 4


@jit
def InBounds(x, y):
    return (x >= 0 and x < GAME_WIDTH and y >= 0 and y < GAME_HEIGHT)

@jit
def Swap(matrix, x, y, dx, dy):
    tmp = matrix[x][y]
    matrix[x][y] = matrix[x+dx][y+dy]
    matrix[x+dx][y+dy] = tmp

@jit
def GetId(matrix, x, y):
    if InBounds(x, y):
        return matrix[x][y]
    return -1

@jit
def UpdateMoveableSolid(matrix, x, y):
    if (GetId(matrix, x, y+1) == ID_VOID) or (GetId(matrix, x, y+1) == ID_WATER):
        Swap(matrix, x, y, 0, 1)
    elif (GetId(matrix, x-1, y+1) == ID_VOID) or (GetId(matrix, x-1, y+1) == ID_WATER):
        Swap(matrix, x, y, -1, 1)
    elif (GetId(matrix, x+1, y+1) == ID_VOID) or (GetId(matrix, x+1, y+1) == ID_WATER):
        Swap(matrix, x, y, 1, 1)

@jit
def LiquidStep(matrix, x, y):
    if GetId(matrix, x, y+1) == 0:
        Swap(matrix, x, y, 0, 1)
        return (x, y+1)
    elif GetId(matrix, x-1, y) == 0:
        Swap(matrix, x, y, -1, 0)
        return (x-1, y)
    elif GetId(matrix, x+1, y) == 0:
        Swap(matrix, x, y, 1, 0)
        return (x+1, y)
    return (x, y)

@jit
def UpdateLiquid(matrix, x, y):
    p = (x, y)
    p = LiquidStep(matrix, p[0], p[1])
    p = LiquidStep(matrix, p[0], p[1])
    p = LiquidStep(matrix, p[0], p[1])

@jit
def UpdateGas(matrix, x, y):
    pass

@jit
def UpdateMatrix(matrix, xOrder):
    for y in range(GAME_HEIGHT-1, -1, -1):
        for x in xOrder:
            if matrix[x][y] == 1:
                UpdateMoveableSolid(matrix, x, y)
            elif matrix[x][y] == 3:
                UpdateLiquid(matrix, x, y)
            elif matrix[x][y] == 4:
                UpdateGas(matrix, x, y)

@jit
def Redraw(buffer, matrix, colors):
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            for t1 in range(GAME_SCALE):
                for t2 in range(GAME_SCALE):
                    buffer[GAME_SCALE*x+t1][GAME_SCALE*y+t2] = colors[matrix[x][y]]
    
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.matrix = np.zeros((GAME_WIDTH,GAME_HEIGHT),dtype=int)
        self.screen_buffer = np.zeros((GAME_SCALE*GAME_WIDTH, GAME_SCALE*GAME_HEIGHT),dtype=np.uint32)
        self.xOrder = np.arange(GAME_WIDTH)

    def UseBrush(self, x, y, elId, size):
        l = max(x-size, 0)
        r = min(x+size, GAME_WIDTH-1)
        u = max(y-size, 0)
        d = min(y+size, GAME_HEIGHT-1)
        for x in range(l, r+1):
            for y in range(u, d+1):
                self.matrix[x][y] = elId

    def Update(self):
        np.random.shuffle(self.xOrder)
        UpdateMatrix(self.matrix, self.xOrder)
        Redraw(self.screen_buffer, self.matrix, EL_COLORS)
        pg.pixelcopy.array_to_surface(self.screen, self.screen_buffer)
        pg.display.update()
