import sys, os, re
import pygame as pg
import numpy as np
from enum import Enum
from classes.board import Board
from classes.inputbox import InputBox
from classes.utils import *

SCREEN_HEIGHT = 675
SCREEN_LENGTH = 625

FPS = 30

MOVE_COMMAND_REGEX = r".*move\s*(?P<from>[A-Ha-h]{1}[1-8]{1})\s*(?P<to>[A-Ha-h]{1}[1-8]{1})\s*"
SELECT_COMMAND_REGEX = r".*select\s*(?P<index>[A-Ha-h]{1}[1-8]{1})\s*"

screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))

# - Initialize board

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

def check_command(board, command):
    from_index, to_index = check_move_command(command)
    if (from_index != None) and (to_index != None):
        board.move_piece(from_index, to_index)
    index = check_select_command(command)
    if index:
        board.select_piece(index)

def main():
    print('Starting chess game')
    pg.display.set_caption("Tracking System")
    clock = pg.time.Clock()
    input_box = InputBox(0, SCREEN_HEIGHT - 50, SCREEN_LENGTH, 50)
    running = True
    board = Board(screen)
    board.redraw_board()

    while running:
        state = State.NONE
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            command = input_box.handle_event(event)
            if command:
                check_command(board, command)
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