__author__ = 'Nick'

import os,pygame
from actors import Actor

class Bullet(Actor):

    bullets = ()
    def __init__(self,x=None,y=None,img=None):
        super().__init__(x,y,img)
        self.shot = True
        self.y_speed = -15

    def update(self):
        if self.shot is True:
            self.rect.y += self.y_speed
            if self.rect.y < 0:
                print()

    '''def shoot(self, actor):
        self.__init__(actor.rect.centerx, actor.rect.y, "bulletUp.png")
        self.shot = True
'''