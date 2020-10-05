import os
import pygame as pg
import numpy as np

from classes.utils import *

SPRITES_FOLDER_NAME = 'sprites'
BOARD_LENGTH = 600
BOARD_NUM_TILES = 8
TILE_SIZE = BOARD_LENGTH / BOARD_NUM_TILES

V_MOVE = np.array([1,0])
H_MOVE = np.array([0,1])

class Piece:
    def __init__(self, name, side, sprite_name):
        self.name = name
        self.side = side
        self.sprite_name = sprite_name
        self.sprite = pg.transform.scale( pg.image.load(os.path.join(SPRITES_FOLDER_NAME, sprite_name)), (int(TILE_SIZE), int(TILE_SIZE)) )
        self.obj = None
        self.is_active = True
        self.x = -1
        self.y = -1
        self.pos = np.array([-1,-1])
        self.moves = []
        self.eat_moves = []
        self.has_moved = False

    def move_pos(self, pos, board, init=False):
        self.x = pos[0]
        self.y = pos[1]
        self.pos = np.array(pos)
        if (not self.has_moved) and (not init):
            self.has_moved = True

    def check_movement(self, new_pos, board):
        self.calculate_moves(board)
        if inside_moves(self.eat_moves, new_pos):
            return MoveType.EAT
        if inside_moves(self.moves, new_pos):
            return MoveType.MOVE
        else:
            return MoveType.NONE

    def add_to_moves(self, move, board):
        if in_board(move)  and (not board.check_piece(move)):
            self.moves.append(move)
            return True
        return False

    def add_to_eat_moves(self, move, board):
        if in_board(move):
            if board.check_enemy(move, self.side):
                self.eat_moves.append(move)
                return True
        return False

    def calculate_moves(self, board, options={}):
        pass

###########################################################################

class Tower(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_tower.png'
        Piece.__init__(self, name, side, sprite_name)

    def calculate_moves(self, board, options={}):
        self.moves = []
        self.eat_moves = []
        for i in range(1,8):
            move = self.pos + V_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos  - V_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos + H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos - H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break

###########################################################################

class Horse(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_horse.png'
        Piece.__init__(self, name, side, sprite_name)

    def calculate_moves(self, board, options={}):
        self.moves = []
        self.eat_moves = []
        move = self.pos + V_MOVE * 2 + H_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos + V_MOVE * 2 - H_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos - V_MOVE * 2 + H_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos - V_MOVE * 2 - H_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos + H_MOVE * 2 + V_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos + H_MOVE * 2 - V_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos - H_MOVE * 2 + V_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)
        move = self.pos - H_MOVE * 2 - V_MOVE 
        if not self.add_to_eat_moves(move, board):
            self.add_to_moves(move, board)

###########################################################################

class Bishop(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_bishop.png'
        Piece.__init__(self, name, side, sprite_name)

    def calculate_moves(self, board, options={}):
        self.moves = []
        self.eat_moves = []
        for i in range(1,8):
            move = self.pos + V_MOVE * i + H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos + V_MOVE * i - H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos - V_MOVE * i + H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos - V_MOVE * i - H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break

###########################################################################

class Queen(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_queen.png'
        Piece.__init__(self, name, side, sprite_name)

    def calculate_moves(self, board, options={}):
        self.moves = []
        self.eat_moves = []
        for i in range(1,8):
            move = self.pos + V_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos  - V_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos + H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos - H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos + V_MOVE * i + H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos + V_MOVE * i - H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos - V_MOVE * i + H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break
        for i in range(1,8):
            move = self.pos - V_MOVE * i - H_MOVE * i
            if self.add_to_eat_moves(move, board):
                break
            if not self.add_to_moves(move, board):
                break

###########################################################################

class King(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_king.png'
        Piece.__init__(self, name, side, sprite_name)

    def calculate_moves(self, board, options={}):
        self.moves = []
        self.eat_moves = []
        move = self.pos + V_MOVE
        self.add_to_moves(move, board)
        self.add_to_eat_moves(move, board)
        move = self.pos + V_MOVE * -1
        self.add_to_moves(move, board)
        self.add_to_eat_moves(move, board)
        move = self.pos + H_MOVE
        self.add_to_moves(move, board)
        self.add_to_eat_moves(move, board)
        move = self.pos + H_MOVE * -1
        self.add_to_moves(move, board)
        self.add_to_eat_moves(move, board)

###########################################################################

class Pawn(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_pawn.png'
        Piece.__init__(self, name, side, sprite_name)

    def calculate_moves(self, board, options={}):
        self.moves = []
        if not self.has_moved:
            self.add_to_moves(self.pos + V_MOVE * 2 * self.side.value, board)
        self.add_to_moves(self.pos + V_MOVE * self.side.value, board)
        self.eat_moves = []
        self.add_to_eat_moves((self.pos + V_MOVE * self.side.value + H_MOVE), board)
        self.add_to_eat_moves((self.pos + V_MOVE * self.side.value - H_MOVE), board)
        self.add_to_eat_moves((self.pos - V_MOVE * self.side.value + H_MOVE), board)
        self.add_to_eat_moves((self.pos - V_MOVE * self.side.value - H_MOVE), board)