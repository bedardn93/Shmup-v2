import pygame,sys,os,player,backdrop,textprint,bullet,enemy,random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 700


class Game (object):

    def __init__(self, screen, items, bg_color=(0,0,0), font=None,
                 font_size=30, font_color=(255,255,255)):
        self.score = 0
        self.pause = True
        self.game_over = False

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color

        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []

        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

        self.background_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        for i in range(20):
            enemies = enemy.Enemy(None,None,"ghost.png")

            enemies.rect.x = random.randrange(SCREEN_WIDTH)
            enemies.rect.y = -random.randint(300, SCREEN_HEIGHT)

            self.enemy_list.add(enemies)
            self.all_sprites_list.add(enemies)

        for i in range(2):
            background = backdrop.Backdrop(None, None, "Space_Deep.jpg")

            if i == 0:
                background.rect.x = 0
                background.rect.y = 0
            else:
                background.rect.x = 0
                background.rect.y = -background.rect.height

            self.background_list.add(background)

        self.player = player.Player(SCREEN_HEIGHT/2,SCREEN_WIDTH/2)
        self.bullets = []
        self.shoot_sound = pygame.mixer.Sound(os.path.join('sounds', 'laser.wav'))
        self.explode_sound = pygame.mixer.Sound(os.path.join('sounds','enemylaser.wav'))

        self.all_sprites_list.add(self.bullets)
        self.all_sprites_list.add(self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if not self.game_over and not self.pause:
                if event.type == pygame.KEYDOWN:
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
                    print("User pressed a key.")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.x_speed += self.player.player_speed
                    if event.key == pygame.K_d:
                        self.player.x_speed += -self.player.player_speed
                    if event.key == pygame.K_w:
                        self.player.y_speed += self.player.player_speed
                    if event.key == pygame.K_s:
                        self.player.y_speed += -self.player.player_speed
                    print("User let go of a key.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over is True:
                    self.__init__()
                if self.pause is True:
                    self.pause = False
            elif event.type == pygame.MOUSEBUTTONUP:
                print("User let go of a mouse button")

        return False

    def run_logic(self):

        if not self.game_over and not self.pause:
            self.background_list.update()
            self.all_sprites_list.update()

            #if player and enemy collide then add value to list
            enemy_col_list = pygame.sprite.spritecollide(self.player, self.enemy_list, True)
            bullet_col_list = pygame.sprite.groupcollide(self.bullet_list, self.enemy_list, True, True)

            for bul in bullet_col_list:
                self.score += 1
                self.explode_sound.play()
                print("enemy hit")


            for en in enemy_col_list:
                self.player.health -= 1
                print(self.score)

            if self.player.health <= 0:
                self.game_over = True




    def display_frame(self, screen):

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])


        if not self.game_over and not self.pause:
            self.background_list.draw(screen)
            self.all_sprites_list.draw(screen)

        if self.pause is True:
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

        pygame.display.flip()


def main():
    #pygame functionality
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    FPS = 60
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Kill Aliens, Become God...")
    clock = pygame.time.Clock()
    done = False
    pygame.init()
    pygame.mouse.set_visible(False)
    menu_items = ('Start','Quit')
    game = Game(screen, menu_items)
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