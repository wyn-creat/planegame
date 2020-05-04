#-*-coding:utf-8-*-
'''
func:主函数
'''

import myplane
import enemy
import bullet
import supply

import os
import pygame
from sys import exit
from pygame.locals import *
from random import *
import sys
import traceback


#初始化pygame，使用pygame时首先加上这一句才可以用
pygame.init()
#音乐
pygame.mixer.init()
#设置游戏屏幕大小
bg_size = width,height = 480,700
#设置游戏界面大小、背景图片及标题
screen = pygame.display.set_mode((bg_size))
#标题及背景
pygame.display.set_caption("PLANE")
background = pygame.image.load('resources/image/background.png').convert()
startbg = pygame.image.load('resources/image/startpg.png').convert()

# 载入游戏音乐
fight_music_path="resources/sound/game_music.wav"
welcome_musice_path = "resources/sound/welcome.wav"


# pygame.mixer.music.load("resources/sound/game_music.wav")
# pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("resources/sound/bullet.wav")
bullet_sound.set_volume(0.1)
bomb_sound = pygame.mixer.Sound("resources/sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("resources/sound/achievement.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("resources/sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("resources/sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound("resources/sound/level_up.wav")
level_up_sound.set_volume(0.1)
enemy3_fly_sound = pygame.mixer.Sound("resources/sound/enemy3_fly.wav")
enemy3_fly_sound.set_volume(0.5)
enemy1_down_sound = pygame.mixer.Sound("resources/sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.15)
enemy2_down_sound = pygame.mixer.Sound("resources/sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.4)
enemy3_down_sound = pygame.mixer.Sound("resources/sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("resources/sound/game_over.wav")
me_down_sound.set_volume(0.2)
# welcome_sound = pygame.mixer.Sound("resources/sound/welcome.wav")
# welcome_sound.set_volume(0.5)

# 颜色
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE=(255,255,255)

# 生成敌方小飞机
def add_small_enemis(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

# 生成敌方中飞机
def add_mid_enemis(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

# 生成敌方大飞机
def add_big_enemis(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def add_myPlane(me2,group):
    group.add(me2)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc


def main():
    fight_music, welcome_music = True, True
    # pygame.mixer.music.load(welcome_musice_path)
    # pygame.mixer.music.play(-1)
    # pygame.mixer.music.play(-1)
    # welcome_sound.play(-1)

    # 游戏欢迎界面图标元素
    startGame_image = pygame.image.load("resources/image/startGame.png").convert_alpha()
    startGame_image_rect = startGame_image.get_rect()
    startGameChoose_image = pygame.image.load("resources/image/startGameChoose.png").convert_alpha()
    startGameChoose_image_rect = startGameChoose_image.get_rect()
    start_image = startGame_image
    start_image_rect = start_image.get_rect()
    start_image_rect.left, start_image_rect.top = (width - start_image_rect.width) // 2, height // 2 + 20
    double_image = pygame.image.load("resources/image/double.png").convert_alpha()
    double_image_rect = double_image.get_rect()
    doubleChoose_image = pygame.image.load("resources/image/doubleChoose.png").convert_alpha()
    doubleChoose_image_rect = doubleChoose_image.get_rect()
    d_image = double_image
    d_image_rect = d_image.get_rect()
    d_image_rect.left, d_image_rect.top = (width - d_image_rect.width) // 2, start_image_rect.bottom+10

    # 分数
    score = 0
    # 字体
    score_font = pygame.font.Font("resources/font/MarkerFelt.ttf", 36)

    # 控制暂停
    paused = False
    stop = False
    pause_nor_image = pygame.image.load("resources/image/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("resources/image/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("resources/image/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("resources/image/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width-paused_rect.width-10,10
    paused_image = pause_nor_image


    # 设置难度级别
    level = 1


    #生成我方飞机
    me1 = myplane.MyPlane(bg_size,"resources/image/player_blue.png","resources/image/player_blue1.png",width//4)
    me2 = myplane.MyPlane(bg_size,"resources/image/player_pink.png","resources/image/player_pink1.png",width//1.5)
    clock = pygame.time.Clock()

    # 生成我方飞机组，用于碰撞检测
    myplanes = pygame.sprite.Group()
    myplanes.add(me1)

    #我方飞机无敌计时器
    INVINCIBLE_TIME = USEREVENT + 2

    #生成总敌方飞机组，用于碰撞检测
    enemis = pygame.sprite.Group()
    #生成三种敌方飞机组，并新建各种敌机添加到组内
    small_enemis = pygame.sprite.Group()
    add_small_enemis(small_enemis,enemis, 25)
    mid_enemis = pygame.sprite.Group()
    add_mid_enemis(mid_enemis, enemis, 5)
    big_enemis = pygame.sprite.Group()
    add_big_enemis(big_enemis, enemis, 2)

    BULLET1_NUM = 4
    BULLET2_NUM = 8

    #生成子弹
    for i in range(BULLET1_NUM):
        me1.bullet1.append(bullet.Bullet1(me1.rect.midtop))
        me2.bullet1.append(bullet.Bullet1(me2.rect.midtop))
    #生成超级子弹
    for i in range(BULLET2_NUM//2):
        me1.bullet2.append(bullet.Bullet2((me1.rect.centerx-33,me1.rect.centery)))
        me2.bullet2.append(bullet.Bullet2((me2.rect.centerx-33,me2.rect.centery)))
        me1.bullet2.append(bullet.Bullet2((me1.rect.centerx+30,me1.rect.centery)))
        me2.bullet2.append(bullet.Bullet2((me2.rect.centerx+30,me2.rect.centery)))


    # 全屏炸弹
    bomb_image = pygame.image.load("resources/image/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left,bomb_rect.top  = 10,height-bomb_rect.height-10
    bomb_num = 1 # 初始一个炸弹
    bomb_font = pygame.font.Font("resources/font/MarkerFelt.ttf",48)

    # 每30秒发放一个随机补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,5*1000)

    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT+1

    #标志- 是否使用超级子弹
    is_double_bullet = False

    # 备用飞机图标-生命值
    life_image = pygame.image.load("resources/image/life.png").convert_alpha()
    life_image = pygame.transform.scale(life_image, (40, 40))
    life_rect = life_image.get_rect()
    life_font = pygame.font.Font("resources/font/MarkerFelt.ttf", 40)


    # 图片索引
    e1_destory_index=0
    e2_destory_index=0
    e3_destory_index=0
    me_destory_index=0


    #用于切换图片的flag
    switch_image = True

    #用于延迟
    delay = 100

    # 用于阻止重复打开记录文件
    recorded = False

    # 游戏结束界面图标
    gameover_img = pygame.image.load("resources/image/gameover1.png").convert_alpha()
    gameover_rect = gameover_img.get_rect()

    # 游戏结束界面
    gameover_font = pygame.font.Font("resources/font/MarkerFelt.ttf",48)
    again_image = pygame.image.load("resources/image/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    return_image = pygame.image.load("resources/image/return.png").convert_alpha()
    return_rect = return_image.get_rect()


    #游戏主体循环
    running = True
    gamestart = False
    doublePlayer = False
    addPlayer = False
    stop_index = 0

    while running:

        if not gamestart:
            if welcome_music :
                welcome_music = False
                fight_music = True
                pygame.mixer.init()
                pygame.mixer.music.load(welcome_musice_path)
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)

            # 绘制游戏欢迎界面
            screen.blit(startbg,(0,0))
            #单人或者双人选择
            screen.blit(start_image, start_image_rect)
            screen.blit(d_image,d_image_rect)
            # 绘制'开始游戏'
            for event in pygame.event.get():
                # 检测事件
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEMOTION:
                    if start_image_rect.collidepoint(event.pos):
                        start_image = startGameChoose_image
                    else:
                        start_image = startGame_image
                    if d_image_rect.collidepoint(event.pos):
                        d_image = doubleChoose_image
                    else:
                        d_image = double_image

                # 如果玩家按下左键
                elif pygame.mouse.get_pressed()[0]:
                    # 获取鼠标坐标
                    pos1 = pygame.mouse.get_pos()
                    # 如果鼠标在“重新开始”上
                    if start_image_rect.left < pos1[0] < start_image_rect.right and \
                            start_image_rect.top < pos1[1] < start_image_rect.bottom:
                        gamestart = True
                    # 如果鼠标在“双人游戏”上
                    if d_image_rect.left < pos1[0] <d_image_rect.right and \
                            d_image_rect.top < pos1[1] <d_image_rect.bottom:
                        doublePlayer = True
                        addPlayer = True
                        gamestart = True

        elif addPlayer:
            # 添加第二架我方飞机
            add_myPlane(me2,myplanes)
            addPlayer = False

        elif gamestart:
            if fight_music:
                fight_music = False
                welcome_music = True
                pygame.mixer.init()
                pygame.mixer.music.load(fight_music_path)
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)

            for event in pygame.event.get():
                # 检测事件
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    # 鼠标按下
                    if event.button == 1 and paused_rect.collidepoint(event.pos):
                        # 1代表左键，并且时间范围在paused_rect内
                        paused = not paused     #取反
                        if paused:
                            pygame.time.set_timer(SUPPLY_TIME,0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()

                elif event.type == MOUSEMOTION:
                    if paused_rect.collidepoint(event.pos):
                        if paused:
                            paused_image = resume_pressed_image
                        else :
                            paused_image = pause_pressed_image
                    else:
                        if paused:
                            paused_image = resume_nor_image
                        else:
                            paused_image = pause_nor_image

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if bomb_num >0:
                            bomb_num -=1
                            for each in enemis:
                                if each.rect.bottom > 0:
                                    # 屏幕内的所有敌机炸毁
                                    each.active = False

                elif event.type == SUPPLY_TIME:
                    if choice([True,False]):
                        bomb_supply.reset()
                    else:
                        bullet_supply.reset()

                elif event.type == DOUBLE_BULLET_TIME:
                    is_double_bullet = False
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

                elif event.type == INVINCIBLE_TIME:
                    for each in myplanes:
                        # 计时器时间结束
                        each.invincible = False
                        pygame.time.set_timer(INVINCIBLE_TIME,0)


            #绘制屏幕
            screen.blit(background,(0,0))


            # 根据用户得分增加难度
            if level == 1 and score > 50000:
                level_up_sound.play()
                level = 2
                # 增加3架小飞机，2架中型飞机，1架大型飞机
                add_small_enemis(small_enemis,enemis,3)
                add_mid_enemis(mid_enemis,enemis,2)
                add_big_enemis(big_enemis,enemis,1)
                # 提升敌机的速度
                inc_speed(small_enemis,1)
            elif level == 2 and score > 300000:
                level_up_sound.play()
                level = 3
                # 增加4架小飞机，增加3架中型飞机,增加2个大型敌机
                add_small_enemis(small_enemis,enemis,3)
                add_mid_enemis(mid_enemis,enemis,3)
                add_big_enemis(big_enemis,enemis,1)
                inc_speed(mid_enemis,1)
            elif level == 3 and score > 600000:
                level_up_sound.play()
                level = 4
                # 增加4架小飞机，增加4架中型飞机,增加1个大型敌机
                add_small_enemis(small_enemis, enemis, 3)
                add_mid_enemis(mid_enemis, enemis, 2)
                add_big_enemis(big_enemis, enemis, 1)
                inc_speed(mid_enemis, 1)
                inc_speed(big_enemis, 1)
            elif level == 4 and score > 1200000:
                level_up_sound.play()
                level = 5
                # 增加4架小飞机，增加5架中型飞机,增加1个大型敌机
                add_small_enemis(small_enemis, enemis, 3)
                add_mid_enemis(mid_enemis, enemis, 2)
                add_big_enemis(big_enemis, enemis, 1)
                inc_speed(mid_enemis, 1)
                inc_speed(big_enemis, 1)
            elif level == 5 and score > 2400000:
                level_up_sound.play()
                # 增加6架小飞机，增加6架中型飞机,增加5个大型敌机
                add_small_enemis(small_enemis, enemis, 6)
                add_mid_enemis(mid_enemis, enemis, 6)
                add_big_enemis(big_enemis, enemis, 1)
                inc_speed(small_enemis, 1)
                inc_speed(mid_enemis, 1)
                inc_speed(big_enemis, 1)



            if (not doublePlayer and me1.energy and not paused) or (doublePlayer and (me1.energy or me2.energy) and not paused):


                # 检测用户键盘操作
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_UP]:
                    me1.moveUp()
                if key_pressed[K_DOWN]:
                    me1.moveDown()
                if key_pressed[K_LEFT]:
                    me1.moveLeft()
                if key_pressed[K_RIGHT]:
                    me1.moveRight()

                if doublePlayer:
                    if key_pressed[K_w] :
                        me2.moveUp()
                    if key_pressed[K_s]:
                        me2.moveDown()
                    if key_pressed[K_a]:
                        me2.moveLeft()
                    if key_pressed[K_d]:
                        me2.moveRight()


                # 绘制全屏炸弹补给并检测能否获得
                if bomb_supply.active:
                    bomb_supply.move()
                    screen.blit(bomb_supply.image,bomb_supply.rect)
                    if pygame.sprite.spritecollide(bomb_supply,myplanes,False):
                        if bomb_num <3:
                            bomb_num +=1
                        bomb_supply.active = False


                # 绘制强化攻击补给并检测能否获得
                if bullet_supply.active:
                    bullet_supply.move()
                    screen.blit(bullet_supply.image, bullet_supply.rect)
                    if pygame.sprite.spritecollide(bullet_supply, myplanes,False):
                        # 发射超级子弹
                        is_double_bullet = True
                        pygame.time.set_timer(DOUBLE_BULLET_TIME,18*1000)
                        bullet_supply.active = False


                # 装填子弹
                if delay%10==0:
                    bullet_sound.play()
                    if is_double_bullet:
                        me1.bullets = me1.bullet2
                        me1.bullets[me1.bullet2_index].reset((me1.rect.centerx-33,me1.rect.centery))
                        me1.bullets[me1.bullet2_index+1].reset((me1.rect.centerx+30,me1.rect.centery))
                        me1.bullet2_index = (me1.bullet2_index + 2) % BULLET2_NUM
                        if doublePlayer:
                            me2.bullets = me2.bullet2
                            me2.bullets[me2.bullet2_index].reset((me2.rect.centerx - 33, me2.rect.centery))
                            me2.bullets[me2.bullet2_index + 1].reset((me2.rect.centerx + 30, me2.rect.centery))
                            me2.bullet2_index = (me2.bullet2_index + 2) % BULLET2_NUM
                    else:
                        me1.bullets = me1.bullet1
                        me1.bullets[me1.bullet1_index].reset(me1.rect.midtop)
                        me1.bullet1_index = (me1.bullet1_index +1)%BULLET1_NUM
                        if doublePlayer:
                            me2.bullets = me2.bullet1
                            me2.bullets[me2.bullet1_index].reset(me2.rect.midtop)
                            me2.bullet1_index = (me2.bullet1_index + 1) % BULLET1_NUM



                # 发射子弹+检测子弹是否击中敌机
                for each in myplanes:
                    for b in each.bullets:
                        if b.active:
                            b.move()
                            screen.blit(b.image,b.rect)
                            enemy_hit = pygame.sprite.spritecollide(b,enemis,False,pygame.sprite.collide_mask)
                            if enemy_hit:
                                b.active=False
                                for e in enemy_hit:
                                    if e in mid_enemis or e in big_enemis:
                                        e.hit=True
                                        e.energy-=1
                                        if e.energy == 0:
                                            e.active = False
                                    else:
                                        e.active = False


                # 检测我方飞机是否发生碰撞
                for each in myplanes:
                    enemis_down = pygame.sprite.spritecollide(each,enemis,False,pygame.sprite.collide_mask)
                    if enemis_down and not each.invincible :
                        each.active = False
                        for e in enemis_down:
                            e.active = False


                #绘制我方飞机
                for me in myplanes:
                    if me.active:
                        if switch_image:
                            screen.blit(me.image1,me.rect)
                        else:
                            screen.blit(me.image2,me.rect)
                    else:
                        # 毁灭
                        if delay%3==0:
                            if me_destory_index == 0:
                                me_down_sound.play()
                            screen.blit(me.destory_images[me_destory_index],me.rect)
                            me_destory_index = (me_destory_index+1)%4
                            if me_destory_index==0:
                                if me.energy > 0:
                                    me.energy -= 1
                                    me.reset()
                                    pygame.time.set_timer(INVINCIBLE_TIME,1*1000)
                                if me.energy <= 0:
                                    myplanes.remove(me)


                # 绘制全屏炸弹
                screen.blit(bomb_image,bomb_rect)
                bomb_text = bomb_font.render("x %d"%bomb_num,True,WHITE)
                text_rect = bomb_text.get_rect()
                screen.blit(bomb_text,(20+bomb_rect.width,height-5-text_rect.height))


                # 绘制生命值图标
                if me1.energy:
                    life_text = score_font.render("1P", True, WHITE)
                    screen.blit(life_text, (width-life_rect.width*4, height-life_rect.height-10))
                    for i in range(me1.energy):
                        screen.blit(life_image,(5+width-life_rect.width*(i+1),height-life_rect.height-10))
                if doublePlayer:
                    if me2.energy:
                        life2_text = score_font.render("2P", True, WHITE)
                        screen.blit(life2_text, (width - life_rect.width * 4, height - life_rect.height*2 - 10))
                        for i in range(me2.energy):
                            screen.blit(life_image,
                                        (5 + width - life_rect.width * (i + 1), height - life_rect.height*2 - 10))


                # 绘制大飞机
                for each in big_enemis:
                    if each.active:
                        each.move()
                        # 即将出现在画面中，给个牌面
                        if each.rect.bottom == -20:
                            enemy3_fly_sound.play(-1)
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else:
                            if switch_image:
                                screen.blit(each.image1,each.rect)
                            else:
                                screen.blit(each.image2,each.rect)

                        # 绘制血条
                        pygame.draw.line(screen,BLACK,
                                         (each.rect.left,each.rect.top - 5),
                                         (each.rect.right,each.rect.top - 5),
                                         2)
                        # 当生命值大于20%显示绿色，否则红色
                        energy_remain = each.energy / enemy.BigEnemy.energy
                        if energy_remain > 0.2:
                            energy_color = GREEN
                        else :
                            energy_color = RED
                        pygame.draw.line(screen,energy_color,
                                         (each.rect.left,each.rect.top - 5),
                                         (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),
                                         2)
                    else:
                        # 毁灭
                        if delay%3==0:
                            if e3_destory_index == 0:
                                enemy3_down_sound.play()
                            screen.blit(each.destory_images[e3_destory_index],each.rect)
                            e3_destory_index = (e3_destory_index+1)%6
                            if e3_destory_index == 0:
                                score +=10000
                                enemy3_fly_sound.stop()
                                each.reset()

                # 绘制中飞机
                for each in mid_enemis:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else:
                            screen.blit(each.image,each.rect)

                        # 绘制血条
                        pygame.draw.line(screen, BLACK,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5),
                                         2)
                        # 当生命值大于20%显示绿色，否则红色
                        energy_remain = each.energy / enemy.MidEnemy.energy
                        if energy_remain > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen, energy_color,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                         2)
                    else :
                        #毁灭
                        if delay%3==0:
                            if e2_destory_index == 0:
                                enemy2_down_sound.play()
                            screen.blit(each.destory_images[e2_destory_index],each.rect)
                            e2_destory_index = (e2_destory_index+1)%4
                            if e2_destory_index==0:
                                score += 6000
                                each.reset()

                # 绘制小飞机
                for each in small_enemis:
                    if each.active:
                        each.move()
                        screen.blit(each.image,each.rect)
                    else:
                        # 毁灭
                        if e1_destory_index == 0:
                            enemy1_down_sound.play()
                        if delay%3==0:
                            screen.blit(each.destory_images[e1_destory_index],each.rect)
                            e1_destory_index = (e1_destory_index+1)%4
                            if e1_destory_index==0:
                                score += 1000
                                each.reset()


                # 分数
                score_text = score_font.render("Score : {0}".format(str(score)), True, WHITE)
                screen.blit(score_text, (10, 5))


            # 玩家死亡
            elif (not doublePlayer and not me1.energy) or (not me1.energy and not me2.energy):
                # 背景音乐停止
                pygame.mixer.music.stop()
                # 停止全部音效
                pygame.mixer.stop()
                # 停止发放补给
                pygame.time.set_timer(SUPPLY_TIME,0)

                # 判断是否将分数记录在记录文件中
                if not recorded:
                    recorded = True
                    # 读取历史最高得分
                    with open("maxScore.txt","r") as f:
                        stream = f.read()
                        if stream=='':
                            stream = f.read()+'0'
                        record_score = int (stream)
                    # 如果玩家得分大于历史最高分，则存档
                    if score > record_score:
                        with open("maxScore.txt","w") as f:
                            f.write(str(score))

                # 绘制游戏结束界面
                screen.blit(gameover_img, (0, 0))
                record_score_text = score_font.render("Best Score : {0}".format(record_score),True,(0,0,255))
                screen.blit(record_score_text,(20,10))
                # 在屏幕中央绘制'你的分数'
                your_score_text = gameover_font.render("Your Score",True,WHITE)
                your_score_text_rect = your_score_text.get_rect()
                your_score_text_rect.left,your_score_text_rect.top = (width - your_score_text_rect.width)//2,\
                                                                   height//2-your_score_text_rect.height-40
                screen.blit(your_score_text,your_score_text_rect)
                # 在'你的分数'下方绘制本局分数
                gameover_text = gameover_font.render(str(score),True,WHITE)
                gameover_text_rect = gameover_text.get_rect()
                gameover_text_rect.left,gameover_text_rect.top = (width-gameover_text_rect.width)//2,\
                                                        your_score_text_rect.bottom + 50
                screen.blit(gameover_text,gameover_text_rect)
                # 绘制重新开始按钮图标
                again_rect.left,again_rect.top = (width-again_rect.width)//2,\
                                                    gameover_text_rect.bottom+50
                screen.blit(again_image,again_rect)
                # 绘制退出游戏按钮图标
                return_rect.left, return_rect.top = (width - return_rect.width) // 2, \
                                                  again_rect.bottom + 50
                screen.blit(return_image, return_rect)

                # 检测用户的鼠标操作
                # 如果按下左键
                if pygame.mouse.get_pressed()[0]:
                    # 获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    #如果鼠标在“重新开始”上
                    if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                        # 调用main函数重新开始游戏
                        main()
                    elif return_rect.left < pos[0] <return_rect.right and return_rect.top < pos[1] < return_rect.bottom:
                        # 退出游戏
                        pygame.quit()
                        sys.exit()

            if (not doublePlayer and me1.energy) or (doublePlayer and (me1.energy or me2.energy)):
                # 绘制暂停按钮
                screen.blit(paused_image, paused_rect)



            #设定延迟
            if delay%5==0:
                switch_image = not switch_image
            delay-=1
            if delay == 0:
                delay = 100

        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()



