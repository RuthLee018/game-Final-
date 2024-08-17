import sys
from time import sleep
import pygame 
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_states import GameState
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()#创建Settings类实例

        #游戏启动后处于活动状态
        self.active = False

        
        
        self.screen = pygame.display.set_mode((1200,800))
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #创建用于存储游戏统计信息的实例,并创建计分牌
        self.states = GameState(self)
        self.score_board = ScoreBoard(self)

        #创建Ship类实例
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_star()        
        #self.bg_color = (100,140,150)#设置背景色

        #创建按钮
        self.play_button = Button(self,"Play")


    def _create_fleet(self):
        alien = Alien(self)
        self.aliens.add(alien)
    
    def _create_star(self):
        new_star = Star(self)
        self.stars.add(new_star)

    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.active:
            self.states.reset_states()
            self.score_board.prep_score()

            self.score_board.prep_ships()
            
            self.active = True

            #清空外星人列表、子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #elf.stars.empty()

            #创建一个新的外星人舰队，将飞船放在屏幕底部中间（x,y轴）
            self.ship.center_ship()
            #还原初始设置
            self.settings.initialize_dynamic_settings()
    

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_left = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_right = True
        #elif event.key == pygame.K_UP:
         #   self.ship.moving_up = True
        #elif event.key == pygame.K_DOWN:
         #   self.ship.moving_down = True

        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            """file = r"shot.mp3"
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()"""




    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_left = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_right = False
        #elif event.key == pygame.K_UP:
         #   self.ship.moving_up = False
        #elif event.key == pygame.K_DOWN:
         #   self.ship.moving_down = False

    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x,current_y = alien_width,alien_height
        while current_y < (self.settings.screen_height -6 * alien_height):
            while current_x < (self.settings.screen_width -3 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        

    def _check_bullet_alien_collisions(self):
        #检查是否有子弹击中外星人
        collision = pygame.sprite.groupcollide(self.bullets,self.aliens,self.settings.bool,True)
        if collision:
            self.states.score += self.settings.alien_score 
            self.score_board.prep_score()
            self.score_board.check_high_score()
            file = r"collision.mp3"
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
             if bullet.rect.bottom <= 0:
                  self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _update_star(self):
        if pygame.sprite.spritecollideany(self.ship,self.stars):
            #print("s")
            self.stars.empty()
            self.settings.bool = False


              
    def _update_screen(self):
        #self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.bg_image,(0,0))#绘制图片
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)

        #显示得分
        self.score_board.show_score()

        if not self.active:
            self.play_button.draw_button()

        pygame.display.flip()#让最近绘制的屏幕可见

   

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        self.settings.bool = True
        file = r"Game_over.mp3"
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        if self.states.ship_left > 0:
            #ship_left减1
            self.states.ship_left -= 1
            self.score_board.prep_ships()  ####
            
            #清空外星人列表(子弹、星星list)
            self.aliens.empty()
            self.bullets.empty()
            self.stars.empty()
            
            #将飞船放在屏幕底部中央
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.active = False
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #检测外星人与飞船是否发生碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
           # print("w")
            self._ship_hit()
        #检测是否有外星人到达屏幕下边缘
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():      
            if alien.rect.bottom >= self.settings.screen_height:
                #如飞船撞到外星人一样处理
                self._ship_hit()
                break

    def run_game(self):
        while True:
            self._check_events()
            if self.active:   
                self.ship.update()
                self._update_bullets()                    
                self._update_aliens()        
                self._update_star()        
            self._update_screen()        
            #控制帧率
            self.clock.tick(60)

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()


    

     