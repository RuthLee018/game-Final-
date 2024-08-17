import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        #初始化飞船位置
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #加载飞船图像，获取rect
        self.image = pygame.image.load("images/craft.bmp")
        self.rect = self.image.get_rect()

        #设置飞船位置
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        #新增移动标志位
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.rect.x += 1
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        #绘制飞船
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


