import numpy as np
from enum import Enum

def in_board(pos):
    return (pos[0] >= 0) & (pos[0] < 8) & (pos[1] >= 0) & (pos[1] < 8)

def inside_moves(moves, move):
    for m in moves:
        if (move[0] == m[0]) & (move[1] == m[1]):
            return True
    return False

class State(Enum):
    NONE = 0
    SELECTING = 1
    SELECTED = 2
    MOVING = 3
    MOVED = 4

class MoveType(Enum):
    NONE = 0
    MOVE = 1
    EAT = 2

class Side(Enum):
    WHITE = -1
    BLACK = 1