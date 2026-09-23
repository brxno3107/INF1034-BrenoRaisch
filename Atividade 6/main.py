import math
import pygame
#################################################################################################


def caminho(nomeArquivo):
    posicao = max(__file__.rfind("\\"), __file__.rfind("/"))
    pasta = __file__[:posicao + 1] if posicao != -1 else ""
    return pasta + nomeArquivo


pygame.mixer.init(frequency=44100, size=-16, channels=2)
pygame.init()
largura, altura = 937, 701
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Casinha - Dia e Noite")
running = True
clock = pygame.time.Clock()
#################################################################################################
grama = "#1FA406"
nuvem = "#FFFFFF"
telhado = "#F2883B"
parede = "#6E6E6E"
porta = "#7A4A1E"
janela = "#0D1664"
tronco = "#7A4A1E"
copa = "#1E9E1E"
preto = "#000000"
solCor = "#FFF251"
#################################################################################################
fonte = pygame.font.Font(caminho("batmfa__.ttf"), 60)
ronaldo = pygame.image.load(caminho("Ronaldo.png")).convert_alpha()
ronaldo = pygame.transform.scale(ronaldo, (150, 108))


def gerarSfx(freq, duracao=0.35, volume=0.4, sampleRate=44100):
    nSamples = int(sampleRate * duracao)
    amplitude = int(32767 * volume)
    fade = 0.05
    buf = bytearray()
    for i in range(nSamples):
        t = i / sampleRate
        envelope = min(1.0, (duracao - t) / fade) if t > duracao - fade else min(1.0, t / fade)
        amostra = int(amplitude * envelope * math.sin(2 * math.pi * freq * t)) & 0xFFFF
        baixo, alto = amostra & 0xFF, (amostra >> 8) & 0xFF
        buf.append(baixo)
        buf.append(alto)
        buf.append(baixo)
        buf.append(alto)
    return pygame.mixer.Sound(buffer=bytes(buf))


sfxManha = gerarSfx(660)
sfxTarde = gerarSfx(440)
sfxNoite = gerarSfx(220, duracao=0.5, volume=0.3)
#################################################################################################
gramaY = 590
larguraNuvem = 255
velocidadeNuvem = 2.0
nuvemX = 655.0
nuvemY = 95
raioNuvem = 45
nuvemXMin = raioNuvem
nuvemXMax = largura - (larguraNuvem - raioNuvem)
#################################################################################################
solX, solY = 130.0, 105.0
raioSol = 50
raioRaios = 95
velSolTeclado = 260
solXMin = raioRaios
solXMax = largura - raioRaios
solYMin = raioRaios
solYMax = gramaY - raioRaios
#################################################################################################
corTarde = (135, 206, 250)
corManha = (255, 179, 126)
corNoite = (11, 19, 65)


def lerpCor(c1, c2, k):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))


def clamp(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def corEEstagioDoCeu(solY):
    t = clamp((solY - solYMin) / (solYMax - solYMin), 0.0, 1.0)
    if t < 0.5:
        cor = lerpCor(corTarde, corManha, t / 0.5)
        estagio = "tarde" if t < 0.25 else "manha"
    else:
        cor = lerpCor(corManha, corNoite, (t - 0.5) / 0.5)
        estagio = "manha" if t < 0.75 else "noite"
    return cor, estagio


sfxPorEstagio = {"manha": sfxManha, "tarde": sfxTarde, "noite": sfxNoite}
#################################################################################################
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            solX, solY = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            _, estagioAtual = corEEstagioDoCeu(solY)
            sfxPorEstagio[estagioAtual].play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        solX -= velSolTeclado * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        solX += velSolTeclado * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        solY -= velSolTeclado * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        solY += velSolTeclado * dt

    solX = clamp(solX, solXMin, solXMax)
    solY = clamp(solY, solYMin, solYMax)

    nuvemX += velocidadeNuvem
    if nuvemX <= nuvemXMin:
        nuvemX = nuvemXMin
        velocidadeNuvem = abs(velocidadeNuvem)
    elif nuvemX >= nuvemXMax:
        nuvemX = nuvemXMax
        velocidadeNuvem = -abs(velocidadeNuvem)

    ceu, estagio = corEEstagioDoCeu(solY)

    screen.fill(ceu)
    pygame.draw.rect(screen, grama, (0, gramaY, largura, altura - gramaY))

    solCentro = (solX, solY)
    for angulo in range(0, 360, 45):
        rad = math.radians(angulo)
        x1 = solCentro[0] + math.cos(rad) * 55
        y1 = solCentro[1] + math.sin(rad) * 55
        x2 = solCentro[0] + math.cos(rad) * 95
        y2 = solCentro[1] + math.sin(rad) * 95
        pygame.draw.line(screen, solCor, (x1, y1), (x2, y2), 5)
    pygame.draw.circle(screen, solCor, solCentro, raioSol)

    pygame.draw.circle(screen, nuvem, (nuvemX, nuvemY), raioNuvem)
    pygame.draw.circle(screen, nuvem, (nuvemX + 55, nuvemY), raioNuvem)
    pygame.draw.circle(screen, nuvem, (nuvemX + 110, nuvemY), raioNuvem)
    pygame.draw.circle(screen, nuvem, (nuvemX + 165, nuvemY), raioNuvem)

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
#################################################################################################
pygame.quit()
