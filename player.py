__author__ = 'Nick'

import os,pygame
from actors import Actor
import main

class Player(Actor):

    def __init__(self,x=None,y=None,img=None):
        if x is None and y is None and img is None:
            Actor.__init__(self)
        elif x is None and y is None:
            Actor.__init__(self,None,None,img)
        else:
            Actor.__init__(self,x,y,img)
        self.player_speed = 5
        self.health = 5

    def update(self):
        if self.rect.x < 0:
            self.rect.x = 0
            print("left")
        elif self.rect.x+self.rect.width > main.SCREEN_WIDTH:
            self.rect.x = main.SCREEN_WIDTH-self.rect.width
            print("right")
        elif self.rect.y < 0:
            self.rect.y = 0
            print("top")
        elif self.rect.y+self.rect.height > main.SCREEN_HEIGHT:
            self.rect.y = main.SCREEN_HEIGHT-self.rect.height
            print(self.rect.y)

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
