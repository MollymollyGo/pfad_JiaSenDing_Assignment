import pygame
import subprocess
import sys

#Initialize pygame
pygame.init()

#set up the interface screen size
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Run Scripts")

#set up the color in interface
canvasGRAY = (215, 215, 215)
BLACK = (0, 0, 0)

#create two button
button1 = pygame.Rect(50, 100, 300, 50)
button2 = pygame.Rect(50, 200, 300, 50)

#the main function loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                # run script1.py
                subprocess.run([sys.executable, 'shooter.py'])
            elif button2.collidepoint(event.pos):
                # run script2.py
                subprocess.run([sys.executable, 'Shooter_Client.py'])


    screen.fill(canvasGRAY)


    pygame.draw.rect(screen, BLACK, button1)
    pygame.draw.rect(screen, BLACK, button2)

    #fill the name, text in the button
    font = pygame.font.Font(None, 36)
    text1 = font.render('PVE', True, canvasGRAY)
    text2 = font.render('PVP', True, canvasGRAY)
    screen.blit(text1, (button1.x + 20, button1.y + 10))
    screen.blit(text2, (button2.x + 20, button2.y + 10))


    pygame.display.flip()


pygame.quit()