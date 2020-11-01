import random
import pygame

pygame.init()
WIDTH, HEIGHT = 750, 750
fps = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
block_size = 50
white = (255, 255, 255)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
you_lost_font = pygame.font.SysFont('Comic Sans MS', 40)

# Load images
spaceship = pygame.image.load("spaceship.png")
green_laser = pygame.image.load("green_laser.png")
red_laser = pygame.image.load("red_laser.png")
enemy_ship = pygame.image.load("enemy.png")
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # to match the size of our window
spaceship = pygame.transform.scale(spaceship, (100, 100))
green_laser = pygame.transform.scale(green_laser, (block_size, block_size))
red_laser = pygame.transform.scale(red_laser, (block_size, block_size))
enemy_ship = pygame.transform.scale(enemy_ship, (50, 50))


def update_window():  # in order to update the screen
    screen.blit(background, (0, 0))
    level_label = myfont.render(f"Level:{level}", 1, (white))  # f takes the value of the brackets
    lives_label = myfont.render(f"Lives:{lives}", 1, (white))
    screen.blit(lives_label, (10, 10))
    screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)
    if lost:
        you_lost_font_label = you_lost_font.render("You lost!!!", 1, (255, 255, 255))
        screen.blit(you_lost_font_label, (WIDTH/2 - you_lost_font_label.get_width()/2, 350))
    pygame.display.update()

class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw (self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not( self.y <= height and self.y>=0)

    def collision(self, obj):
        return collide(self , obj)



class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = spaceship
        self.lasers_img = red_laser
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
            laser.nove(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -=10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter >0 :
            self.cool_down_counter += 1
        
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.lasers_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = spaceship
        self.laser = red_laser
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
                    if laser.collision(obj): # remove if  laser collide
                        obj.remove(obj)
                        self.lasers.remove(laser)

class Enemy(Ship):
    # those we will need when we add our own pictures
    COLOR_MAP={
                "green" : (enemy_ship, green_laser)

    }
    def __init__(self, x, y, color,health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move_enemy(self, vel):
        self.y +=  vel


player = Player(300, 650)
level = 0
lives = 5
player_vel = 5
laser_vel = 5
# Game loop

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x  # distance from obj1 to obj2 returns vector
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None# is obj1 overlapping obj2( given two masks

run = True
lost = False
lost_count = 0
enemies = []
wave_length = 5
enemy_vel = 1
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
        wave_length +=5
        # this is for the enemies fall down at random positions positions 
        for i in range(wave_length):
            enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                          random.choice(["green"]))
            enemies.append(enemy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - player_vel > 0:
        player.x -= player_vel
    if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
        player.x += player_vel
    if keys[pygame.K_UP] and  player.y - player_vel > 0:
        player.y -= player_vel
    if keys[pygame.K_DOWN]  and  player.y + player_vel + player.get_height() < HEIGHT:
        player.y += player_vel
    if keys[pygame.K_SPACE]:
        player.shoot()


    for enemy in enemies[:]:
        # everytime they are on the screen move them down with their velocities
        enemy.move_enemy(enemy_vel)
        # everytime we don't kill the enemies we get lesser number of lives
        enemy.move_lasers(laser_vel, player)
        if enemy.y + enemy.get_height() > HEIGHT:
            lives -= 1
            enemies.remove(enemy)

    player.move_lasers(-laser_vel, enemies) # strelyat' vverh a ne vniz

pygame.quit()
