import pygame

#普通子弹
class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("resources/image/playerbullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.rect.left -= self.rect.width/2
        self.speed=15
        self.active=False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top + self.rect.height < 0:
            self.active = False

    def reset(self,position):
        self.rect.left,self.rect.top = position
        self.rect.left -= self.rect.width / 2
        self.active=True

#加能量子弹
class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("resources/image/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.rect.left -= self.rect.width/2
        self.speed=15
        self.active=False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top + self.rect.height < 0:
            self.active = False

    def reset(self,position):
        self.rect.left,self.rect.top = position
        self.rect.left -= self.rect.width / 2
        self.active=True

