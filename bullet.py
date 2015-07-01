__author__ = 'Nick'

import os,pygame
from actors import Actor

class Bullet(Actor):

    bullets = ()
    def __init__(self,x=None,y=None,img=None):
        if x is None and y is None and img is None:
            Actor.__init__(self)
        elif x is None and y is None:
            Actor.__init__(self,None,None,img)
        else:
            Actor.__init__(self,x,y,img)
        self.shot = True

    def update(self):
        if self.shot is True:
            self.rect.y += self.y_speed
            if self.rect.y < 0:
                print("destroy bullet")

    def shoot(self, actor):
        self.__init__(actor.rect.centerx, actor.rect.y, "bulletUp.png")
        self.shot = True
