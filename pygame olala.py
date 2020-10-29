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

# Load images
spaceship = pygame.image.load("spaceship.png")
green_laser = pygame.image.load("green_laser.png")
red_laser = pygame.image.load("red_laser.png")
enemy = pygame.image.load("enemy.png")
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # to match the size of our window
spaceship = pygame.transform.scale(spaceship, (block_size, block_size))
green_laser = pygame.transform.scale(green_laser, (block_size, block_size))
red_laser = pygame.transform.scale(red_laser, (block_size, block_size))
enemy = pygame.transform.scale(enemy, (block_size, block_size))


def update_window():  # in order to update the screen
    screen.blit(background, (0, 0))
    level_label = myfont.render(f"Level:{level}", 1, (white))  # f takes the value of the brackets
    lives_label = myfont.render(f"Lives:{lives}", 1, (white))
    screen.blit(lives_label, (10, 10))
    screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    ship.draw(screen)
    pygame.display.update()

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lasers_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))





ship = Ship(300, 650)
level = 1
lives = 5
player_vel = 5
# Game loop
run = True
while run:
    update_window()
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.x - player_vel > 0:
        ship.x -= player_vel
    if keys[pygame.K_RIGHT] and ship.x + player_vel + 50 < WIDTH:
        ship.x += player_vel
    if keys[pygame.K_UP] and  ship.y - player_vel > 0:
        ship.y -= player_vel
    if keys[pygame.K_DOWN]  and  ship.y + player_vel + 50 < HEIGHT:
        ship.y += player_vel


pygame.quit()
