__author__ = 'Nick'
import pygame

WHITE = (255, 255, 255)
class TextPrint(object):
    def __init__(self, x=None, y=None):
        self.reset()
        self.x_pos = x
        self.y_pos = y
        self.font = pygame.font.Font(None, 20)

    def print(self, my_screen, text_string):
        text_bitmap = self.font.render(text_string, True, WHITE)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])

    def reset(self):
        self.x_pos = 10
        self.y_pos = 10

    def indent(self):
        self.x_pos += 10

    def unindent(self):
        self.x_pos -= 10