import math
import pygame
#################################################################################################


def caminhoDoArquivo(nomeArquivo):
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
corDoSol = "#FFF251"
#################################################################################################
fonte = pygame.font.Font(caminhoDoArquivo("batmfa__.ttf"), 60)
ronaldo = pygame.image.load(caminhoDoArquivo("Ronaldo.png")).convert_alpha()
ronaldo = pygame.transform.scale(ronaldo, (150, 108))


def criarSom(frequencia, duracao=0.35, volume=0.4, taxaAmostragem=44100):
    totalAmostras = int(taxaAmostragem * duracao)
    amplitude = int(32767 * volume)
    tempoDeFade = 0.05
    bytesDoSom = bytearray()
    for indice in range(totalAmostras):
        tempo = indice / taxaAmostragem
        volumeNoInstante = min(1.0, (duracao - tempo) / tempoDeFade) if tempo > duracao - tempoDeFade else min(1.0, tempo / tempoDeFade)
        amostra = int(amplitude * volumeNoInstante * math.sin(2 * math.pi * frequencia * tempo)) & 0xFFFF
        byteBaixo, byteAlto = amostra & 0xFF, (amostra >> 8) & 0xFF
        bytesDoSom.append(byteBaixo)
        bytesDoSom.append(byteAlto)
        bytesDoSom.append(byteBaixo)
        bytesDoSom.append(byteAlto)
    return pygame.mixer.Sound(buffer=bytes(bytesDoSom))


somDaManha = criarSom(660)
somDaTarde = criarSom(440)
somDaNoite = criarSom(220, duracao=0.5, volume=0.3)
#################################################################################################
alturaDoChao = 590
larguraDaNuvem = 255
velocidadeDaNuvem = 2.0
nuvemX = 655.0
nuvemY = 95
raioDaNuvem = 45
limiteEsquerdoNuvem = raioDaNuvem
limiteDireitoNuvem = largura - (larguraDaNuvem - raioDaNuvem)
#################################################################################################
solX, solY = 130.0, 105.0
raioDoSol = 50
alcanceDosRaios = 95
velocidadeSolTeclado = 260
limiteEsquerdoSol = alcanceDosRaios
limiteDireitoSol = largura - alcanceDosRaios
limiteSuperiorSol = alcanceDosRaios
limiteInferiorSol = alturaDoChao - alcanceDosRaios
#################################################################################################
corTarde = (135, 206, 250)
corManha = (255, 179, 126)
corNoite = (11, 19, 65)


def misturarCores(corInicial, corFinal, progresso):
    return tuple(int(corInicial[i] + (corFinal[i] - corInicial[i]) * progresso) for i in range(3))


def limitarEntre(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def calcularCeuEEstagio(alturaDoSol):
    progresso = limitarEntre((alturaDoSol - limiteSuperiorSol) / (limiteInferiorSol - limiteSuperiorSol), 0.0, 1.0)
    if progresso < 0.5:
        cor = misturarCores(corTarde, corManha, progresso / 0.5)
        estagio = "tarde" if progresso < 0.25 else "manha"
    else:
        cor = misturarCores(corManha, corNoite, (progresso - 0.5) / 0.5)
        estagio = "manha" if progresso < 0.75 else "noite"
    return cor, estagio


sonsPorEstagio = {"manha": somDaManha, "tarde": somDaTarde, "noite": somDaNoite}
#################################################################################################
while running:
    deltaTempo = clock.tick(60) / 1000
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.MOUSEMOTION:
            solX, solY = evento.pos
        if evento.type == pygame.MOUSEBUTTONDOWN:
            _, estagioAtual = calcularCeuEEstagio(solY)
            sonsPorEstagio[estagioAtual].play()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        solX -= velocidadeSolTeclado * deltaTempo
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        solX += velocidadeSolTeclado * deltaTempo
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        solY -= velocidadeSolTeclado * deltaTempo
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        solY += velocidadeSolTeclado * deltaTempo

    solX = limitarEntre(solX, limiteEsquerdoSol, limiteDireitoSol)
    solY = limitarEntre(solY, limiteSuperiorSol, limiteInferiorSol)

    nuvemX += velocidadeDaNuvem
    if nuvemX <= limiteEsquerdoNuvem:
        nuvemX = limiteEsquerdoNuvem
        velocidadeDaNuvem = abs(velocidadeDaNuvem)
    elif nuvemX >= limiteDireitoNuvem:
        nuvemX = limiteDireitoNuvem
        velocidadeDaNuvem = -abs(velocidadeDaNuvem)

    corDoCeu, estagioDoDia = calcularCeuEEstagio(solY)

    screen.fill(corDoCeu)
    pygame.draw.rect(screen, grama, (0, alturaDoChao, largura, altura - alturaDoChao))

    centroDoSol = (solX, solY)
    for angulo in range(0, 360, 45):
        rad = math.radians(angulo)
        x1 = centroDoSol[0] + math.cos(rad) * 55
        y1 = centroDoSol[1] + math.sin(rad) * 55
        x2 = centroDoSol[0] + math.cos(rad) * 95
        y2 = centroDoSol[1] + math.sin(rad) * 95
        pygame.draw.line(screen, corDoSol, (x1, y1), (x2, y2), 5)
    pygame.draw.circle(screen, corDoSol, centroDoSol, raioDoSol)

    pygame.draw.circle(screen, nuvem, (nuvemX, nuvemY), raioDaNuvem)
    pygame.draw.circle(screen, nuvem, (nuvemX + 55, nuvemY), raioDaNuvem)
    pygame.draw.circle(screen, nuvem, (nuvemX + 110, nuvemY), raioDaNuvem)
    pygame.draw.circle(screen, nuvem, (nuvemX + 165, nuvemY), raioDaNuvem)

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
