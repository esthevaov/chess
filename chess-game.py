import sys, os
import pygame as pg
import numpy as np

# --- constants --- (UPPER_CASE names)

SPRITES_FOLDER_NAME = 'sprites'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_LENGTH = 8

BLACK = (  0,   0,   0)
GREY  = (100, 100, 100)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 30

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# - Initialize board

class Piece:
    def __init__(self, name, side, sprite_name):
        self.name = name
        self.side = side
        self.sprite_name = sprite_name
        self.sprite = pg.transform.scale( pg.image.load(os.path.join(SPRITES_FOLDER_NAME, sprite_name)), (100, 100) )
        self.obj = None
        self.is_active = True
        self.x = -1
        self.y = -1

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def check_movement(self):
        pass

    def move(self):
        pass


class Tower(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_tower.png'
        Piece.__init__(self, name, side, sprite_name)


class Horse(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_horse.png'
        Piece.__init__(self, name, side, sprite_name)


class Bishop(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_bishop.png'
        Piece.__init__(self, name, side, sprite_name)


class Queen(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_queen.png'
        Piece.__init__(self, name, side, sprite_name)


class King(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_king.png'
        Piece.__init__(self, name, side, sprite_name)


class Pawn(Piece):
    def __init__(self, name, side):
        sprite_name = 'sprite_pawn.png'
        Piece.__init__(self, name, side, sprite_name)


class Board:
    def __init__(self):
        self.size = 8

        board_list = [[Tower('tower_1', 'black'), Horse('horse_1', 'black'), Bishop('bishop_1', 'black'), Queen('queen_1', 'black'), King('king_1', 'black'), Bishop('bishop_2', 'black'), Horse('horse_2', 'black'), Tower('tower_2', 'black')],
                      [Pawn('pawn_1', 'black'), Pawn('pawn_2', 'black'), Pawn('pawn_3', 'black'), Pawn('pawn_4', 'black'), Pawn('pawn_5', 'black'), Pawn('pawn_6', 'black'), Pawn('pawn_7', 'black'), Pawn('pawn_8', 'black')],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn('pawn_9', 'white'), Pawn('pawn_10', 'white'), Pawn('pawn_11', 'white'), Pawn('pawn_12', 'white'), Pawn('pawn_13', 'white'), Pawn('pawn_14', 'white'), Pawn('pawn_15', 'white'), Pawn('pawn_16', 'white')],
                      [Tower('tower_3', 'white'), Horse('horse_3', 'white'), Bishop('bishop_3', 'white'), Queen('queen_2', 'white'), King('king_2', 'white'), Bishop('bishop_4', 'white'), Horse('horse_4', 'white'), Tower('tower_4', 'white')]]
        self.board = np.array(board_list)

        self.pieces = []
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if self.board[i, k] is not None:
                    self.board[i, k].set_pos(i, k)
                    self.pieces.append(self.board[i, k])

    def move(self):
        pass

    def check_piece_collision(self, pos):
        print('check pos: ' + str(pos))
        for i in range(len(self.pieces)):
            if self.pieces[i].obj.collidepoint(pos):
                return i
        return -1

    def set_piece_pos(self, index, pos):
        print('set pos: ' + str(pos))
        x, y = (np.floor(pos[1] * BOARD_LENGTH / SCREEN_WIDTH), np.floor(pos[0] * BOARD_LENGTH/ SCREEN_HEIGHT))
        print(x, y)
        self.pieces[index].set_pos(x, y)

    def redraw_board(self):
        self.redraw_background()

        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.obj = screen.blit(piece.sprite, (SCREEN_WIDTH/BOARD_LENGTH * piece.y, SCREEN_HEIGHT/BOARD_LENGTH * piece.x))                   

    def redraw_background(self):
        #Size of squares
        board_width = SCREEN_WIDTH / BOARD_LENGTH
        board_height = SCREEN_HEIGHT / BOARD_LENGTH

        #board length, must be even

        cnt = 0
        for i in range(0,BOARD_LENGTH):
            for z in range(0,BOARD_LENGTH):
                #check if current loop value is even
                if cnt % 2 == 0:
                    pg.draw.rect(screen, WHITE, [board_width*z,board_height*i,board_width,board_height])
                else:
                    pg.draw.rect(screen, GREY, [board_width*z,board_height*i,board_width,board_height])
                cnt +=1
            #since theres an even number of squares go back one value
            cnt-=1
        #Add a nice boarder
        pg.draw.rect(screen, BLACK, [board_width,board_height,BOARD_LENGTH*board_width,BOARD_LENGTH*board_height], 1)

        pg.display.update()


def main():

    board = Board()

    pg.display.set_caption("Tracking System")

    # - mainloop -

    clock = pg.time.Clock()

    running = True
    should_redraw = False
    piece_draging = False
    board.redraw_board()

    while running:

        # - events -

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                should_redraw = True
                if event.button == 1:            
                    piece_index = board.check_piece_collision(event.pos)
                    if piece_index >= 0:
                        piece_draging = True

            elif event.type == pg.MOUSEBUTTONUP:
                should_redraw = True
                if event.button == 1:            
                    piece_draging = False

            elif event.type == pg.MOUSEMOTION:
                if piece_draging:
                    should_redraw = True
                    mouse_x, mouse_y = event.pos
                    board.set_piece_pos(piece_index, (mouse_x , mouse_y))
                else:
                    should_redraw = False

            else:
                should_redraw = False

        # - updates (without draws) -

        # empty

        # - draws (without updates) -
        if should_redraw:

            board.redraw_board()

        pg.display.flip()

        # - constant game speed / FPS -

        clock.tick(FPS)

    # - end -

    pg.quit()

main()