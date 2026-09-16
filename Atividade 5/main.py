import math
import pygame
#################################################################################################
pygame.init()
largura, altura = 937, 701
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Casinha")
running = True
#################################################################################################
ceu = "#97D1FA"
grama = "#1FA406"
sol = "#FFF251"
nuvem = "#FFFFFF"
telhado = "#F2883B"
parede = "#6E6E6E"
porta = "#7A4A1E"
janela = "#0D1664"
tronco = "#7A4A1E"
copa = "#1E9E1E"
preto = "#000000"
#################################################################################################
fonte = pygame.font.Font("batmfa__.ttf", 60)
ronaldo = pygame.image.load("Ronaldo.png").convert_alpha()
ronaldo = pygame.transform.scale(ronaldo, (150, 108))
pygame.mixer.music.load("Hino Fluminense ESTOURADO Volume 2000%       #hino #fluminense.mp3")
pygame.mixer.music.play(-1)
#################################################################################################
clock = pygame.time.Clock()
larguraNuvem = 255
velocidadeNuvem = 2
nuvemX = 655.0
#################################################################################################
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    nuvemX += velocidadeNuvem
    if nuvemX > largura:
        nuvemX = -larguraNuvem
    screen.fill(ceu)
    pygame.draw.rect(screen, grama, (0, 590, largura, altura - 590))
    solCentro = (130, 105)
    for angulo in range(0, 360, 45):
        rad = math.radians(angulo)
        x1 = solCentro[0] + math.cos(rad) * 55
        y1 = solCentro[1] + math.sin(rad) * 55
        x2 = solCentro[0] + math.cos(rad) * 95
        y2 = solCentro[1] + math.sin(rad) * 95
        pygame.draw.line(screen, sol, (x1, y1), (x2, y2), 5)
    pygame.draw.circle(screen, sol, solCentro, 50)
    pygame.draw.circle(screen, nuvem, (nuvemX, 95), 45)
    pygame.draw.circle(screen, nuvem, (nuvemX + 55, 95), 45)
    pygame.draw.circle(screen, nuvem, (nuvemX + 110, 95), 45)
    pygame.draw.circle(screen, nuvem, (nuvemX + 165, 95), 45)
    pygame.draw.rect(screen, tronco, (700, 475, 30, 115))
    pygame.draw.circle(screen, copa, (715, 375), 100)
    pygame.draw.rect(screen, parede, (240, 350, 230, 240))
    pygame.draw.polygon(screen, telhado, [(240, 350), (470, 350), (355, 180)])
    pygame.draw.rect(screen, janela, (260, 440, 60, 80))
    pygame.draw.rect(screen, porta, (355, 420, 65, 170))
    pygame.draw.circle(screen, preto, (370, 505), 4)
    screen.blit(ronaldo, (largura - 170, 600))
    texto = fonte.render("SIUUUUUUU", True, preto)
    screen.blit(texto, (largura // 2 - texto.get_width() // 2, 610))
    pygame.display.update()
    clock.tick(60)
#################################################################################################
pygame.quit()
