import sys, os, re
import pygame as pg
import numpy as np
from enum import Enum
from classes.inputbox import InputBox
from classes.pieces import *
from classes.utils import *

SCREEN_HEIGHT = 675
SCREEN_LENGTH = 625
BOARD_LENGTH = 600
BOARD_NUM_TILES = 8
TILE_SIZE = BOARD_LENGTH / BOARD_NUM_TILES

BLACK = (  0,   0,   0)
GREY  = (100, 100, 100)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (0,   255,   0)

FPS = 30
FONT = pg.font.Font(None, 32)

MOVE_COMMAND_REGEX = r".*move\s*(?P<from>[A-Ha-h]{1}[1-8]{1})\s*(?P<to>[A-Ha-h]{1}[1-8]{1})\s*"
SELECT_COMMAND_REGEX = r".*select\s*(?P<index>[A-Ha-h]{1}[1-8]{1})\s*"

screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))

# - Initialize board

class Board:
    def __init__(self):
        self.size = 8

        board_list = [[Tower('tower_1', Side.BLACK), Horse('horse_1', Side.BLACK), Bishop('bishop_1', Side.BLACK), Queen('queen_1', Side.BLACK), King('king_1', Side.BLACK), Bishop('bishop_2', Side.BLACK), Horse('horse_2', Side.BLACK), Tower('tower_2', Side.BLACK)],
                      [Pawn('pawn_1', Side.BLACK), Pawn('pawn_2', Side.BLACK), Pawn('pawn_3', Side.BLACK), Pawn('pawn_4', Side.BLACK), Pawn('pawn_5', Side.BLACK), Pawn('pawn_6', Side.BLACK), Pawn('pawn_7', Side.BLACK), Pawn('pawn_8', Side.BLACK)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn('pawn_9', Side.WHITE), Pawn('pawn_10', Side.WHITE), Pawn('pawn_11', Side.WHITE), Pawn('pawn_12', Side.WHITE), Pawn('pawn_13', Side.WHITE), Pawn('pawn_14', Side.WHITE), Pawn('pawn_15', Side.WHITE), Pawn('pawn_16', Side.WHITE)],
                      [Tower('tower_3', Side.WHITE), Horse('horse_3', Side.WHITE), Bishop('bishop_3', Side.WHITE), Queen('queen_2', Side.WHITE), King('king_2', Side.WHITE), Bishop('bishop_4', Side.WHITE), Horse('horse_4', Side.WHITE), Tower('tower_4', Side.WHITE)]]
        self.board = np.array(board_list)
        self.white_dead_pieces = []
        self.black_dead_pieces = []
        self.pieces = []
        self.current_piece = -1
        self.state = State.MOVED
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                piece = self.board[i, k]
                if piece is not None:
                    piece.move_pos([i, k], self, True)
                    piece.calculate_moves(self)
                    self.pieces.append(piece)

    def check_enemy(self, pos, side):
        piece = self.board[pos[0], pos[1]]
        if (piece != None) and (piece.side != side):
            return True
        return False

    def check_piece(self, pos):
        if self.board[pos[0], pos[1]] != None:
            return True
        return False

    def get_board_index(self, pos):
        return (np.floor(pos[1] / TILE_SIZE), np.floor(pos[0] / TILE_SIZE))

    def select_piece(self, pos):
        piece = self.board[pos[0], pos[1]]
        if piece is not None:
            piece.calculate_moves(self)
            for move in piece.moves:
                self.select_move_space(move, RED)
            for move in piece.eat_moves:
                self.select_move_space(move, GREEN)
            pg.display.update()
            print('Selected piece at ({},{})'.format(pos[0], pos[1]))
        else:
            print('No piece found at ({},{})'.format(pos[0], pos[1]))

    def select_move_space(self, pos, color):
        screen_pos = (int(pos[1] * TILE_SIZE + TILE_SIZE/2), int(pos[0] * TILE_SIZE + TILE_SIZE/2))
        pg.draw.circle(screen, color, screen_pos, 8)

    def move_piece(self, pos1, pos2):
        piece = self.board[pos1[0], pos1[1]]
        movement = piece.check_movement(pos2, self)
        if movement == MoveType.EAT:
            eaten_piece = self.board[pos2[0], pos2[1]]
            if eaten_piece.side == Side.WHITE:
                self.white_dead_pieces.append(eaten_piece)
            else:
                self.black_dead_pieces.append(eaten_piece) 
            self.board[pos2[0], pos2[1]] = piece
            self.board[pos1[0], pos1[1]] = None
            piece.move_pos(pos2, self)
            self.redraw_board()
            print('Moved piece {} from ({},{}) to ({},{}) and eaten piece {}'.format(piece.name, pos1[0], pos1[1], pos2[0], pos2[1], eaten_piece.name))

        if movement == MoveType.MOVE:
            self.board[pos2[0], pos2[1]] = piece
            self.board[pos1[0], pos1[1]] = None
            piece.move_pos(pos2, self)
            self.redraw_board()
            print('Moved piece {} from ({},{}) to ({},{})'.format(piece.name, pos1[0], pos1[1], pos2[0], pos2[1]))

    def redraw_board(self):
        self.redraw_background()

        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.obj = screen.blit(piece.sprite, (TILE_SIZE * piece.y, TILE_SIZE * piece.x))

    def redraw_background(self):
        #Size of squares
        board_width = TILE_SIZE
        board_height = TILE_SIZE

        #board length, must be even

        cnt = 0
        for i in range(0,BOARD_NUM_TILES):
            for z in range(0,BOARD_NUM_TILES):
                #check if current loop value is even
                if cnt % 2 == 0:
                    pg.draw.rect(screen, WHITE, [board_width*z,board_height*i,board_width,board_height])
                else:
                    pg.draw.rect(screen, GREY, [board_width*z,board_height*i,board_width,board_height])
                cnt +=1
            #since theres an even number of squares go back one value
            cnt-=1
        #Add a nice boarder
        #pg.draw.rect(screen, BLACK, [board_width,board_height,BOARD_NUM_TILES*board_width,BOARD_NUM_TILES*board_height], 1)
        for i in range(0,BOARD_NUM_TILES):
            text_render = FONT.render(chr(97+i), True, WHITE, BLACK)
            screen.blit(text_render, (TILE_SIZE*i + TILE_SIZE/2, BOARD_LENGTH + 1))
        for i in range(0,BOARD_NUM_TILES):
            text_render = FONT.render(str(8-i), True, WHITE, BLACK)
            screen.blit(text_render, (BOARD_LENGTH + 7, TILE_SIZE*i + TILE_SIZE/2 - 10))

        pg.display.update()
    
def check_move_command(command):
    matches= re.search(MOVE_COMMAND_REGEX, command)
    if matches:
        return get_board_index_from_text(matches.group('from')), get_board_index_from_text(matches.group('to'))
    return None, None 

def check_select_command(command):
    matches = re.search(SELECT_COMMAND_REGEX, command)
    if matches:
        return get_board_index_from_text(matches.group('index'))
    return None 

def get_board_index_from_text(text):
    try:
        index1 = ord(text[0].lower()) - 97
        index1 = index1 if index1 < 8 else None
        index2 = int(text[1]) - 1
        index2 = 7 - index2 if (index2 >= 0) and (index2 < 8) else None
        return [index2, index1]
    except Exception as e:
        print(e)
        return None, None

def check_command(command):
    from_index, to_index = check_move_command(command)
    if (from_index != None) and (to_index != None):
        board.move_piece(from_index, to_index)
    index = check_select_command(command)
    if index:
        board.select_piece(index)

board = Board()

def main():
    pg.display.set_caption("Tracking System")
    clock = pg.time.Clock()
    input_box = InputBox(0, SCREEN_HEIGHT - 50, SCREEN_LENGTH, 50)
    running = True
    board.redraw_board()

    while running:
        state = State.NONE
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            #elif event.type == pg.MOUSEBUTTONUP:
            #    if event.button == 1:
            #        self.select_or_move(event.pos)

            command = input_box.handle_event(event)
            if command:
                check_command(command)
        input_box.draw(screen)

        if state == State.SELECTING:
            state = State.SELECTED
            board.redraw_board()
        elif state == State.MOVING:
            state = State.MOVED
            board.redraw_board()
        pg.display.flip()

        clock.tick(FPS)

    pg.quit()
    

main()