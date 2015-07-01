__author__ = 'Nick'

from actors import Actor

class Enemy(Actor):

    def __init__(self,x=None,y=None,img=None):
        super().__init__(x,y,img)

    def update(self):
        self.rect.y += self.y_speed