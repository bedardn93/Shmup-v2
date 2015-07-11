__author__ = 'Nick'
#This class is for all moving objects on the screen (players, enemies, objects, scrolling backgrounds, etc.)
#When creating new moving objects import this class using 'from actors import Actor' (minus quotes)
import os,sys,pygame


class Actor(pygame.sprite.Sprite):

    def __init__(self,x=None,y=None,img=None):
        super().__init__()
        if img is None:
            self.image = pygame.image.load(os.path.join('images',"spaceship.png")).convert()
        else:
            self.image = pygame.image.load(os.path.join('images',img)).convert_alpha()
        self.rect = self.image.get_rect()
        if x is None and y is None:
            self.rect.x = 0
            self.rect.y = 0
        else:
            self.rect.x = x
            self.rect.y = y
        self.x_speed = 0
        self.y_speed = 0

        self.image.set_colorkey((255,255,255))

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def getPos(self):
        return [self.rect.x,self.rect.y]
    def getXSpeed(self):
        return self.x_speed

    def getYSpeed(self):
        return self.y_speed

    def getImage(self):
        return self.image

    def getHeight(self):
        self.rect.height

    def getWidth(self):
        self.rect.width