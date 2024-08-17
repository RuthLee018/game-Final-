import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard():
    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen #screen为ai_game的一个属性
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.states = ai_game.states

        #显示得分时的字体设置
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None,48)

        #显示初始化得分图像
        self.prep_score()
        
        #准备最高分图像
        self.prep_high_score()
        #准备绘制飞船图像
        self.prep_ships()

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.states.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 400 + ship_number * ship.rect.width ###
            ship.rect.y = 10
            self.ships.add(ship)

    
    def prep_high_score(self):
        high_score = round(self.states.high_score, -1)     
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,
                                            self.settings.bg_color)
        #将最高分显示在屏幕顶部左方
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left 
        self.high_score_rect.top = self.score_rect.top 

    def prep_score(self):
        round_score = round(self.states.score, -1)
        score_str = f"{round_score:,}"
        self.score_image = self.font.render(score_str,True,self.text_color,
                                            self.settings.bg_color)
        #将分数显示在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        #path = Path("highest.json")
        #contents = {"highest":self.states.high_score}
        #path.write_text(json.dumps(contents))

        self.ships.draw(self.screen)
        
    def check_high_score(self):
        if self.states.score > self.states.high_score:
            self.states.high_score = self.states.score
            self.prep_high_score()





