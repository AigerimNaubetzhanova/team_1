import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
block_size = 75
white = (255, 255, 255)
red = (200, 0, 0)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
you_lost_font = pygame.font.SysFont('Comic Sans MS', 40)

# Load images
spaceship = pygame.image.load("spaceship.png")
blue_laser = pygame.image.load("blue_laser.png")
greenlaser = pygame.image.load("greenlaser.png")
red_laser = pygame.image.load("redlaser.png")
blue_enemy_ship = pygame.image.load("blue_enemy.png")
grey_enemy_ship = pygame.image.load("grey_enemy.png")
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # to match the size of our window
spaceship = pygame.transform.scale(spaceship, (100, 100))
blue_laser = pygame.transform.scale(blue_laser, (20, 50))
greenlaser = pygame.transform.scale(greenlaser, (20, 50))
red_laser = pygame.transform.scale(red_laser, (block_size, block_size))
blue_enemy_ship = pygame.transform.scale(blue_enemy_ship, (block_size, block_size))
grey_enemy_ship = pygame.transform.scale(grey_enemy_ship, (100, 100))
cosmos = pygame.image.load("cosmos.jpg")
cosmos = pygame.transform.scale(cosmos, (WIDTH, HEIGHT))
back = pygame.image.load("back!.png")
back = pygame.transform.scale(back, (160, 100))
back.set_colorkey((0, 0, 0))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        # those we need to make boundaries for spaceship's movements, so it wouldn't get outside of the screen
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = spaceship
        self.laser_img = red_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):  # remove if  laser collide
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):  # implement draw method of the player shifts
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):  # hunam takes self
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            10))
        # 1st RED-length of the player, 2nd GREEN-on tip of the red (be only the length of the health)
        # ex. (255,0,0)-red color; (self.x, self.y + self.ship_img.get_height() + 10- we want to be sure tha health bar is below our player(so we want to get y value of the player add height of the shipp and ten pixels and then start drawing)
        # self.ship_img.get_width() * (self.health/self.max_health - what % of the width we should draw


class Enemy(Ship):
    # those we will need when we add our own pictures
    COLOR_MAP = {
        "blue": (blue_enemy_ship, blue_laser),
        "grey": (grey_enemy_ship, greenlaser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move_enemy(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 35, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x  # distance from obj1 to obj2 returns vector
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # is obj1 overlapping obj2( given two masks


def main(menu):
    run = True
    fps = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def update_window():  # in order to update the screen
        screen.blit(background, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))  # f takes the value of the brackets
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if lost:
            you_lost_label = you_lost_font.render("Game over", 1, (255, 255, 255))
            screen.blit(you_lost_label, (WIDTH / 2 - you_lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(fps)
        update_window()
        # if you lost then FREEZE
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            enemy_vel += 1
            # this is for the enemies fall down at random positions positions
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["grey", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            game.menu()

        for enemy in enemies[:]:
            # everytime they are on the screen move them down with their velocities
            enemy.move_enemy(enemy_vel)
            # everytime we don't kill the enemies we get lesser number of lives
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                if player.health == 10:
                    if lives <= 0:
                        lost = True
                    else:
                        player.health = player.max_health
                        lives -= 1
                        enemies.remove(enemy)
                else:
                    player.health -= 10
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                if lives <= 0:
                    lost = True
                else:
                    lives -= 1
                    enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)  # strelyat' vverh a ne vniz
    pygame.quit()


fps = 60


def help(menu):
    screen.blit(cosmos, (0, 0))
    screen.blit(back, (0, 600))
    text = you_lost_font.render("helpdkjanckjjd", True, white)
    screen.blit(text, (170, 100))
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rect = back.get_rect()
            if rect.collidepoint(pos):
                game.menu()
    pygame.display.flip()
    clock.tick(fps)


def tool(menu):
    screen.blit(cosmos, (0, 0))
    screen.blit(back, (0, 600))
    text = you_lost_font.render("tool", True, white)
    screen.blit(text, (170, 100))
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rect = back.get_rect()
            if rect.collidepoint(pos):
                menu.state = "menu"
                print("Tried to return to menu")
    pygame.display.flip()
    clock.tick(fps)


class Menu:
    state = "menu"

    def __init__(self, punkts=[200, 300, 'Punkts', white, red, 2]):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):  # отрисовка
        for i in self.punkts:
            if num_punkt == i[5]:  # если курсор и текущий эелемент совпадает окрашивается в красный
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))  # если нет то не окрашивается

    def menu(self):
        global state
        fps = 60
        done = True
        font_menu = pygame.font.SysFont("comicsans", 120)
        punkt = 0
        pygame.key.set_repeat(0, 0)  # отключили залипание курсора
        pygame.mouse.set_visible(True)  # сделали видимым курсор
        while done:
            if self.state == "menu":
                mp = pygame.mouse.get_pos()
                for i in self.punkts:
                    if mp[0] > i[0] and mp[0] < i[0] + 300 and mp[1] > i[1] and mp[1] < i[
                        1] + 100:  # checking пересекается курсор в пунктом меню или нет
                        punkt = i[5]
                screen.blit(cosmos, (0, 0))
                self.render(screen, font_menu, punkt)

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            sys.exit()
                        if e.key == pygame.K_UP:
                            if punkt > 0:
                                punkt -= 1
                        if e.key == pygame.K_DOWN:
                            if punkt > len(self.punkts) - 1:
                                punkt += 1
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        if punkt == 0:  # если нажать гейм то играет
                            self.state = "play"
                        if punkt == 1:  # если нажать хелп выводит текст
                            self.state = "tool"
                        if punkt == 2:
                            self.state = "help"

                pygame.display.flip()
                clock.tick(fps)

            if self.state == "play":
                main(self)

            if self.state == "help":
                help(self)

            if self.state == "tool":
                tool(self)


punkts = [(240, 220, 'Game', white, red, 0),
          (260, 340, 'Tools', white, red, 1),
          (280, 460, 'Help', white, red, 2)]
game = Menu(punkts)
game.menu()