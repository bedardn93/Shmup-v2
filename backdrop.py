__author__ = 'Nick'

import os,pygame
import main
from actors import Actor


class Backdrop(Actor):

    def __init__(self,x=None,y=None,img=None):
        if x is None and y is None and img is None:
            Actor.__init__(self)
        elif x is None and y is None:
            Actor.__init__(self,None,None,img)
        else:
            Actor.__init__(self,x,y,img)
        self.y_speed = 4

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > main.SCREEN_HEIGHT:
            self.rect.y = -self.rect.height