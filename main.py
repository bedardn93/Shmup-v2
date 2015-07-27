import pygame,sys,os,player,backdrop,textprint,bullet,enemy,asteroid,random
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)

SCREEN_WIDTH,SCREEN_HEIGHT = 1920,1080

SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

SOUND_VOLUME = 0.1

class Game (object):

    def __init__(self, screen=pygame.display.set_mode(SIZE,pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF), menu_items=('Start','Quit'), bg_color=(0,0,0), font=None,
                 font_size=30, font_color=(255,255,255)):
        self.score = 0
        self.pause = True
        self.game_over = False

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color

        self.items = menu_items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []

        for index, item in enumerate(menu_items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(menu_items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

        self.background_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.asteroid_list = pygame.sprite.Group()
        self.debris_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        for i in range(2):
            background = backdrop.Backdrop(None, None, "Space_Deep.jpg")

            if i == 0:
                background.rect.x = 0
                background.rect.y = 0
            else:
                background.rect.x = 0
                background.rect.y = -background.rect.height

            self.background_list.add(background)

        self.player = player.Player(int(SCREEN_HEIGHT/4),int(SCREEN_WIDTH/0.5))
        self.bullets = []
        self.shoot_sound = pygame.mixer.Sound(os.path.join('sounds', 'laser.wav'))
        self.explode_sound = pygame.mixer.Sound(os.path.join('sounds','enemylaser.wav'))
        self.shoot_sound.set_volume(SOUND_VOLUME)
        self.explode_sound.set_volume(SOUND_VOLUME)
        self.last_fps = pygame.time.get_ticks()
        self.last_fps2 = pygame.time.get_ticks()

        self.debris_xspeed = 4
        self.debris_yspeed = 2

        self.hud = textprint.TextPrint(20,20)
        self.hud2 = textprint.TextPrint(500,20)

        self.all_sprites_list.add(self.bullets)
        self.all_sprites_list.add(self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if not self.game_over and not self.pause:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN and (event.mod&(KMOD_LALT|KMOD_RALT)) != 0:
                        toggle_fullscreen()
                    if event.key == pygame.K_a:
                        self.player.x_speed += -self.player.player_speed
                    if event.key == pygame.K_d:
                        self.player.x_speed += self.player.player_speed
                    if event.key == pygame.K_w:
                        self.player.y_speed += -self.player.player_speed
                    if event.key == pygame.K_s:
                        self.player.y_speed += self.player.player_speed
                    if event.key == pygame.K_z:
                        print()
                    if event.key == pygame.K_SPACE:
                        self.shoot_sound.play()
                        temp = bullet.Bullet(self.player.rect.centerx, self.player.rect.y, "bulletUp.png")
                        self.bullet_list.add(temp)
                        self.all_sprites_list.add(temp)
                    if event.key == pygame.K_ESCAPE:
                        return True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.x_speed += self.player.player_speed
                    if event.key == pygame.K_d:
                        self.player.x_speed += -self.player.player_speed
                    if event.key == pygame.K_w:
                        self.player.y_speed += self.player.player_speed
                    if event.key == pygame.K_s:
                        self.player.y_speed += -self.player.player_speed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over is True:
                    self.__init__()
                if self.pause is True:
                    self.pause = False
            elif event.type == pygame.MOUSEBUTTONUP:
                    x=x
        return False

    def run_logic(self):

        if not self.game_over and not self.pause:
            self.background_list.update()
            self.all_sprites_list.update()

            #if player and enemy collide then add value to list
            astenm_col_list = pygame.sprite.groupcollide(self.asteroid_list, self.enemy_list, True, True)
            debast_col_list = pygame.sprite.groupcollide(self.debris_list, self.asteroid_list, True, True)
            debenm_col_list = pygame.sprite.groupcollide(self.debris_list, self.enemy_list, True, True)
            playenm_col_list = pygame.sprite.spritecollide(self.player, self.enemy_list, True)
            playast_col_list = pygame.sprite.spritecollide(self.player, self.asteroid_list, True)
            playdeb_col_list = pygame.sprite.spritecollide(self.player, self.debris_list, True)
            buldeb_col_list = pygame.sprite.groupcollide(self.bullet_list, self.debris_list, True, True)

            bulenm_col_list = pygame.sprite.groupcollide(self.bullet_list, self.enemy_list, True, True)
            bulast_col_list = pygame.sprite.groupcollide(self.bullet_list, self.asteroid_list, True, True)

            #destroy bullets offscreen
            for bul in self.bullet_list:
                if bul.rect.y < 0:
                    self.bullet_list.remove(bul)

            #destroy enemies offscreen
            for en in self.enemy_list:
                if en.rect.y > SCREEN_HEIGHT:
                    self.enemy_list.remove(en)

            #destroy asteroids offscreen
            for ast in self.asteroid_list:
                if ast.rect.y > SCREEN_HEIGHT:
                    self.asteroid_list.remove(ast)

            #create debris if a bullet hits an asteroid
            for ast in bulast_col_list:
                debris1 = asteroid.Asteroid(None,None,"asteroid.png")
                debris2 = asteroid.Asteroid(None,None,"asteroid.png")

                debris1.rect.x = ast.rect.x
                debris1.rect.y = ast.rect.y
                debris2.rect.x = ast.rect.x
                debris2.rect.y = ast.rect.y

                debris1.y_speed = self.debris_yspeed
                debris1.x_speed = self.debris_xspeed
                debris2.y_speed = self.debris_yspeed
                debris2.x_speed = -self.debris_xspeed

                self.debris_list.add(debris1)
                self.debris_list.add(debris2)
                self.all_sprites_list.add(debris1)
                self.all_sprites_list.add(debris2)

            #destroy enemies hit by bullets
            for bul in bulenm_col_list:
                self.score += 50
                self.explode_sound.play()
                print("enemy hit")

            #if enemies hit player, lower health
            for en in playenm_col_list:
                self.player.health -= 1

            #if asteroids hit player, lower health
            for ast in playast_col_list:
                self.player.health -= 1

            #if debris hit player, lower health
            for deb in playdeb_col_list:
                self.player.health -= 1

            #destroy enemies hit by asteroid
            for ast in astenm_col_list:
                self.explode_sound.play()

            #destroy enemies hit by debris
            for deb in debenm_col_list:
                self.score += 50
                self.explode_sound.play()

            #if debris hits asteroid, make more debris
            for ast in debast_col_list:
                debris1 = asteroid.Asteroid(None,None,"asteroid.png")
                debris2 = asteroid.Asteroid(None,None,"asteroid.png")

                debris1.rect.x = ast.rect.x
                debris1.rect.y = ast.rect.y
                debris2.rect.x = ast.rect.x
                debris2.rect.y = ast.rect.y

                debris1.y_speed = self.debris_yspeed
                debris1.x_speed = self.debris_xspeed
                debris2.y_speed = self.debris_yspeed
                debris2.x_speed = -self.debris_xspeed

                self.debris_list.add(debris1)
                self.debris_list.add(debris2)
                self.all_sprites_list.add(debris1)
                self.all_sprites_list.add(debris2)

            for deb in buldeb_col_list:
                self.explode_sound.play()


            if self.player.health <= 0:
                self.game_over = True

            if pygame.time.get_ticks() - self.last_fps > 500 and self.score < 1000:
                enemies = enemy.Enemy(None,None,"ghost.png")

                enemies.rect.x = random.randrange(SCREEN_WIDTH)
                enemies.rect.y = -random.randint(300, SCREEN_HEIGHT)

                self.enemy_list.add(enemies)
                self.all_sprites_list.add(enemies)

                self.last_fps = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.last_fps2 > 1000 and self.score < 1000:
                asteroids = asteroid.Asteroid(None,None,"asteroid.png")

                asteroids.rect.x = random.randrange(SCREEN_WIDTH)
                asteroids.rect.y = -random.randint(0, SCREEN_HEIGHT)

                self.asteroid_list.add(asteroids)
                self.all_sprites_list.add(asteroids)

                self.last_fps2 = pygame.time.get_ticks()

    def display_frame(self, screen):

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over and not self.pause:
            self.background_list.draw(screen)
            self.asteroid_list.draw(screen)
            self.all_sprites_list.draw(screen)
            self.hud.print(self.screen,'Health: '+str(self.player.health))
            self.hud2.print(self.screen,'Score: '+str(self.score))

        if self.pause is True:
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

        pygame.display.flip()


def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()

    pygame.display.quit()
    pygame.display.init()

    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

    return screen

def main():
    #pygame functionality
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    FPS = 60
    screen = pygame.display.set_mode(SIZE,pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Kill Aliens, Become God...")
    clock = pygame.time.Clock()
    done = False
    pygame.init()
    pygame.mouse.set_visible(False)
    menu_items = ('Start','Quit')
    #game = Game(screen, menu_items)
    game = Game()
    while not done:

        #player input
        done = game.process_events()

        #update game objects
        game.run_logic()

        #draw to screen
        game.display_frame(screen)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()