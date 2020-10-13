import pygame
pygame.init()
size=(900,500)
screen=pygame.display.set_mode(size)
clock=pygame.time.Clock()
done=False
fps=100

black=(0,0,0)
white=(255,255,255)
yellow=(255,255,0)
grey=(192,192,192)
red=(200,0,0)
graphcolor=yellow
gridcolor=grey

screen.fill(white)

font=pygame.font.SysFont('arial',14) #шрифт и размер текста

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            done

    pygame.display.flip()
    clock.tick(fps)
pygame.quit
