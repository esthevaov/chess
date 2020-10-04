import pygame as pg

pg.font.init()
FONT = pg.font.Font(None, 32)

BLACK = (  0,   0,   0)
GREY  = (100, 100, 100)
WHITE = (255, 255, 255)

class InputBox:

    def __init__(self, x, y, w, h, text='> '):
        self.rect = pg.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = True
        self.pos = (x, y, w, h)

    def handle_event(self, event):
        command = ''
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                command = self.text
                self.text = '> '
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)
        return command

    def draw(self, screen):
        screen.fill(BLACK, self.pos)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)