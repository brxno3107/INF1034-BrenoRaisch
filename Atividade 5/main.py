import math
import pygame
#################################################################################################
pygame.init()
LARGURA, ALTURA = 937, 701
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Casinha")
running = True
#################################################################################################
CEU = "#97D1FA"
GRAMA = "#1FA406"
SOL = "#FFF251"
NUVEM = "#FFFFFF"
TELHADO = "#F2883B"
PAREDE = "#6E6E6E"
PORTA = "#7A4A1E"
JANELA = "#0D1664"
TRONCO = "#7A4A1E"
COPA = "#1E9E1E"
PRETO = "#000000"
#################################################################################################
fonte = pygame.font.Font("batmfa__.ttf", 60)
ronaldo = pygame.image.load("Ronaldo.png").convert_alpha()
ronaldo = pygame.transform.scale(ronaldo, (150, 108))
pygame.mixer.music.load("Hino Fluminense ESTOURADO Volume 2000%       #hino #fluminense.mp3")
pygame.mixer.music.play(-1)
#################################################################################################
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(CEU)
    pygame.draw.rect(screen, GRAMA, (0, 590, LARGURA, ALTURA - 590))
    sol_centro = (130, 105)
    for angulo in range(0, 360, 45):
        rad = math.radians(angulo)
        x1 = sol_centro[0] + math.cos(rad) * 55
        y1 = sol_centro[1] + math.sin(rad) * 55
        x2 = sol_centro[0] + math.cos(rad) * 95
        y2 = sol_centro[1] + math.sin(rad) * 95
        pygame.draw.line(screen, SOL, (x1, y1), (x2, y2), 5)
    pygame.draw.circle(screen, SOL, sol_centro, 50)
    pygame.draw.circle(screen, NUVEM, (655, 95), 45)
    pygame.draw.circle(screen, NUVEM, (700, 80), 50)
    pygame.draw.circle(screen, NUVEM, (750, 85), 48)
    pygame.draw.circle(screen, NUVEM, (795, 95), 42)
    pygame.draw.rect(screen, NUVEM, (655, 95, 140, 45))
    pygame.draw.rect(screen, TRONCO, (700, 475, 30, 115))
    pygame.draw.circle(screen, COPA, (715, 375), 100)
    pygame.draw.rect(screen, PAREDE, (240, 350, 230, 240))
    pygame.draw.polygon(screen, TELHADO, [(240, 350), (470, 350), (355, 180)])
    pygame.draw.rect(screen, JANELA, (260, 440, 60, 80))
    pygame.draw.rect(screen, PORTA, (355, 420, 65, 170))
    pygame.draw.circle(screen, PRETO, (370, 505), 4)
    screen.blit(ronaldo, (LARGURA - 170, 600))
    texto = fonte.render("SIUUUUUUU", True, PRETO)
    screen.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 610))
    pygame.display.update()
#################################################################################################
pygame.quit()
