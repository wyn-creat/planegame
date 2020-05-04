#-*-coding:utf-8-*-
#小敌机 中敌机 大敌机
#敌机都有向下移动方法， 大敌机两个图切换
#main生成所有敌机组用于检测碰撞
#main为三种敌机设置三个组
#main新添加三个生成不同敌机的方法-加入到组中-生成的位置有讲究
import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("resources/image/eplane1.png").convert_alpha()
        self.rect = self.image.get_rect()
        #获得背景尺寸
        self.width,self.height = bg_size[0],bg_size[1]
        self.speed = 2
        self.rect.left,self.rect.top = randint(0,self.width-self.rect.width),randint(-2*self.height,0)#给个初始化位置。
        self.destory_images = []
        self.active = True  # 生命状态
        self.destory_images.extend([
            pygame.image.load("resources/image/small_break1.png").convert_alpha(),
            pygame.image.load("resources/image/small_break2.png").convert_alpha(),
            pygame.image.load("resources/image/small_break3.png").convert_alpha(),
            pygame.image.load("resources/image/small_break4.png").convert_alpha()
        ])
        self.mask = pygame.mask.from_surface(self.image)


    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        # 重新初始化
        self.rect.left,self.rect.top = randint(0,self.width-self.rect.width),randint(-3*self.height,0)
        self.active = True  # 生命状态


class MidEnemy(pygame.sprite.Sprite):
    energy = 10 # 声明值

    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("resources/image/midEnemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.speed = 1
        self.rect.left,self.rect.top = randint(0,self.width-self.rect.width),randint(-4*self.height,0)
        self.destory_images=[]
        self.active = True  # 生命状态
        self.destory_images.extend([
            pygame.image.load("resources/image/mid_break1.png").convert_alpha(),
            pygame.image.load("resources/image/mid_break2.png").convert_alpha(),
            pygame.image.load("resources/image/mid_break3.png").convert_alpha(),
            pygame.image.load("resources/image/mid_break4.png").convert_alpha(),
        ])
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.image_hit = pygame.image.load("resources/image/mid_hit.png")
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left,self.rect.top = randint(0,self.width-self.rect.width),randint(-4*self.height,0)
        self.active = True  # 生命状态
        self.energy = MidEnemy.energy


class BigEnemy(pygame.sprite.Sprite):
    energy = 40
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("resources/image/bigEnemy1.png").convert_alpha()
        self.image2 = pygame.image.load("resources/image/bigEnemy2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-7 * self.height, -2*self.height)
        self.destory_images=[]
        self.active = True # 生命状态
        self.destory_images.extend([
            pygame.image.load("resources/image/big_break1.png").convert_alpha(),
            pygame.image.load("resources/image/big_break2.png").convert_alpha(),
            pygame.image.load("resources/image/big_break3.png").convert_alpha(),
            pygame.image.load("resources/image/big_break4.png").convert_alpha(),
            pygame.image.load("resources/image/big_break5.png").convert_alpha(),
            pygame.image.load("resources/image/big_break6.png").convert_alpha()
        ])
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigEnemy.energy
        self.image_hit = pygame.image.load("resources/image/big_hit.png")
        self.hit = False


    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-8 * self.height, 0)
        self.active = True  # 生命状态
        self.energy = MidEnemy.energy


