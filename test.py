import pygame as pg
import numpy as np
from classes.pieces import *


board_list = [[Tower('tower_1', 'black'), Horse('horse_1', 'black'), Bishop('bishop_1', 'black'), Queen('queen_1', 'black'), King('king_1', 'black'), Bishop('bishop_2', 'black'), Horse('horse_2', 'black'), Tower('tower_2', 'black')],
                      [Pawn('pawn_1', 'black'), Pawn('pawn_2', 'black'), Pawn('pawn_3', 'black'), Pawn('pawn_4', 'black'), Pawn('pawn_5', 'black'), Pawn('pawn_6', 'black'), Pawn('pawn_7', 'black'), Pawn('pawn_8', 'black')],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn('pawn_9', 'white'), Pawn('pawn_10', 'white'), Pawn('pawn_11', 'white'), Pawn('pawn_12', 'white'), Pawn('pawn_13', 'white'), Pawn('pawn_14', 'white'), Pawn('pawn_15', 'white'), Pawn('pawn_16', 'white')],
                      [Tower('tower_3', 'white'), Horse('horse_3', 'white'), Bishop('bishop_3', 'white'), Queen('queen_2', 'white'), King('king_2', 'white'), Bishop('bishop_4', 'white'), Horse('horse_4', 'white'), Tower('tower_4', 'white')]]
board = np.array(board_list)

print(board[0,0])
print(board[0,1])
print(board[1,0])

print(board_list[0][0])
print(board_list[0][1])
print(board_list[1][0])