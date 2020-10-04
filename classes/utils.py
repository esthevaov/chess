import numpy as np

def in_board(pos):
    return (pos[0] >= 0) & (pos[0] < 8) & (pos[1] >= 0) & (pos[1] < 8)

def inside_moves(moves, move):
    for m in moves:
        if (move[0] == m[0]) & (move[1] == m[1]):
            return True
    return False