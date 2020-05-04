#-*-coding:utf-8-*-
'''
func:我方飞机
'''
import pygame

class MyPlane(pygame.sprite.Sprite):
    energy = 3
    def __init__(self,bg_size,path,path2,left):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(str(path)).convert_alpha()
        self.image2 = pygame.image.load(str(path2)).convert_alpha()
        self.rect = self.image1.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = left,self.height-self.rect.height-60
        self.speed = 10  # 初始化玩家飞机速度
        self.active = True  # 生命状态
        # destory图片组
        self.destory_images=[]
        self.destory_images.extend([
            pygame.image.load("resources/image/player_distory1.png").convert_alpha(),
            pygame.image.load("resources/image/player_distory2.png").convert_alpha(),
            pygame.image.load("resources/image/player_distory3.png").convert_alpha(),
            pygame.image.load("resources/image/player_distory4.png").convert_alpha()
        ])
        self.mask=pygame.mask.from_surface(self.image1)
        self.energy = MyPlane.energy
        self.invincible = False
        self.bullet1 = []
        self.bullet2 = []
        self.bullets = []
        self.bullet1_index = 0
        self.bullet2_index = 0
        # self.is_double_bullet = False

    def reset(self):
        self.rect.left,self.rect.top = (self.width - self.rect.width)//2,self.height - self.rect.height-60
        self.active = True
        self.invincible = True

    # 向上移动
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # 向下移动
    def moveDown(self):
        if self.rect.bottom < self.height -60 :
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    # 向左移动
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width







