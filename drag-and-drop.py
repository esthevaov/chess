import pygame as pg

# --- constants --- (UPPER_CASE names)

SPRITES_FOLDER_NAME = 'sprites'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

BLACK = (  0,   0,   0)
GREY  = (100, 100, 100)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 30

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# - Initialize board

def redraw_board():
    board_length = 8

    #Size of squares
    board_width = SCREEN_WIDTH / board_length
    board_height = SCREEN_HEIGHT / board_length

    #board length, must be even

    cnt = 0
    for i in range(0,board_length):
        for z in range(0,board_length):
            #check if current loop value is even
            if cnt % 2 == 0:
                pg.draw.rect(screen, WHITE, [board_width*z,board_height*i,board_width,board_height])
            else:
                pg.draw.rect(screen, GREY, [board_width*z,board_height*i,board_width,board_height])
            cnt +=1
        #since theres an even number of squares go back one value
        cnt-=1
    #Add a nice boarder
    pg.draw.rect(screen, BLACK, [board_width,board_height,board_length*board_width,board_length*board_height], 1)

    pg.display.update()


def main():

    pg.display.set_caption("Tracking System")

    # - objects -

    rectangle = pg.rect.Rect(176, 134, 17, 17)
    rectangle_draging = False

    # - mainloop -

    clock = pg.time.Clock()

    running = True
    should_redraw = False
    redraw_board()

    while running:

        # - events -

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                should_redraw = True
                if event.button == 1:            
                    if rectangle.collidepoint(event.pos):
                        rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = rectangle.x - mouse_x
                        offset_y = rectangle.y - mouse_y

            elif event.type == pg.MOUSEBUTTONUP:
                should_redraw = True
                if event.button == 1:            
                    rectangle_draging = False

            elif event.type == pg.MOUSEMOTION:
                if rectangle_draging:
                    should_redraw = True
                    mouse_x, mouse_y = event.pos
                    rectangle.x = mouse_x + offset_x
                    rectangle.y = mouse_y + offset_y
                else:
                    should_redraw = False

            else:
                should_redraw = False

        # - updates (without draws) -

        # empty

        # - draws (without updates) -
        if should_redraw:

            redraw_board()
            
            pg.draw.rect(screen, RED, rectangle)

        pg.display.flip()

        # - constant game speed / FPS -

        clock.tick(FPS)

    # - end -

    pg.quit()

main()