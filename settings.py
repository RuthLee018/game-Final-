import pygame
class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,51,102)
        self.bg_image = pygame.image.load("images/dream.bmp")

        #飞船设置
        self.ship_speed = 4.0
        self.ship_limit = 2
               
        self.bullet_speed = 5.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255,255,153)

        self.bool = True

        #self.alien_speed = 1.5
        self.fleet_drop_speed = 8.0
        #1代表向右，-1表示向左
        self.fleet_direction = 1
        self.score_scale = 100
        
        #以何速度加快游戏节奏
        self.speed_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_speed = 3.0
        #计分设置
        self.alien_score = 10

    def increase_speed(self):
        self.alien_speed *= self.speed_scale 
        #self.ship_speed *= self.speed_scale 
        self.alien_score = int(self.alien_score * self.score_scale)
      




