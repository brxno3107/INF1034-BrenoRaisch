import math
import pygame


def desenharFolha(tela, posicao, raio, cor):
    pygame.draw.circle(tela, cor, posicao, raio)


def corPorProfundidade(profundidade, profundidadeMaxima):
    progresso = 1 - profundidade / profundidadeMaxima
    return pygame.Color("#7A4A1E").lerp("#4ADE80", progresso)


def desenharArvore(tela, x, y, comprimento, angulo, profundidade, profundidadeMaxima, abertura=22, fatorReducao=0.74):
    if profundidade == 0 or comprimento < 4:
        desenharFolha(tela, (x, y), 4, corPorProfundidade(0, profundidadeMaxima))
        return
    anguloRad = math.radians(angulo)
    xFim = x + comprimento * math.sin(anguloRad)
    yFim = y - comprimento * math.cos(anguloRad)
    cor = corPorProfundidade(profundidade, profundidadeMaxima)
    pygame.draw.line(tela, cor, (x, y), (xFim, yFim), max(1, profundidade))
    for desvio in (-abertura, 0, abertura):
        desenharArvore(tela, xFim, yFim, comprimento * fatorReducao, angulo + desvio,
                        profundidade - 1, profundidadeMaxima, abertura, fatorReducao)


def desenharKoch(tela, p1, p2, profundidade, cor, anguloPico=60):
    if profundidade == 0:
        pygame.draw.line(tela, cor, p1, p2, 2)
        return

    x1, y1 = p1
    x2, y2 = p2
    dx = (x2 - x1) / 3
    dy = (y2 - y1) / 3

    pontoA = (x1 + dx, y1 + dy)
    pontoB = (x1 + 2 * dx, y1 + 2 * dy)

    vetorX = pontoB[0] - pontoA[0]
    vetorY = pontoB[1] - pontoA[1]
    anguloRad = math.radians(-anguloPico)
    pico = (
        pontoA[0] + vetorX * math.cos(anguloRad) - vetorY * math.sin(anguloRad),
        pontoA[1] + vetorX * math.sin(anguloRad) + vetorY * math.cos(anguloRad),
    )

    desenharKoch(tela, p1, pontoA, profundidade - 1, cor, anguloPico)
    desenharKoch(tela, pontoA, pico, profundidade - 1, cor, anguloPico)
    desenharKoch(tela, pico, pontoB, profundidade - 1, cor, anguloPico)
    desenharKoch(tela, pontoB, p2, profundidade - 1, cor, anguloPico)


def desenharFlocoDeNeve(tela, centro, raio, profundidade, cor, anguloPico=60):
    verticeTopo = (centro[0], centro[1] - raio)
    verticeEsquerda = (centro[0] - raio * math.sin(math.radians(60)), centro[1] + raio * math.cos(math.radians(60)))
    verticeDireita = (centro[0] + raio * math.sin(math.radians(60)), centro[1] + raio * math.cos(math.radians(60)))

    desenharKoch(tela, verticeTopo, verticeDireita, profundidade, cor, anguloPico)
    desenharKoch(tela, verticeDireita, verticeEsquerda, profundidade, cor, anguloPico)
    desenharKoch(tela, verticeEsquerda, verticeTopo, profundidade, cor, anguloPico)


pygame.init()
largura, altura = 700, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Fractais - 1: espiral  2: arvore  3: koch")
fonte = pygame.font.SysFont("segoeui,arial", 18)

PROFUNDIDADE_ARVORE = 8
PROFUNDIDADE_KOCH = 4

## Desenho inicial (espiral): feito direto aqui, sem função, como pede o enunciado
tela.fill("#121417")
centro = (largura // 2, altura // 2)
tamanho = 260
angulo = 0
for i in range(30):
    pontos = [(centro[0] + tamanho * math.cos(math.radians(angulo + lado * 90)),
               centro[1] + tamanho * math.sin(math.radians(angulo + lado * 90))) for lado in range(4)]
    cor = pygame.Color("#6C8EF5").lerp("#4ADE80", i / 30)
    pygame.draw.polygon(tela, cor, pontos, 2)
    tamanho *= 0.88
    angulo += 12
legenda = fonte.render("1: espiral   2: árvore   3: floco de Koch", True, "#8A93A1")
tela.blit(legenda, (16, altura - 30))
pygame.display.update()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                ## Espiral: desenho direto aqui, sem função (mesma lógica do início)
                tela.fill("#121417")
                centro = (largura // 2, altura // 2)
                tamanho = 260
                angulo = 0
                for i in range(30):
                    pontos = [(centro[0] + tamanho * math.cos(math.radians(angulo + lado * 90)),
                               centro[1] + tamanho * math.sin(math.radians(angulo + lado * 90))) for lado in range(4)]
                    cor = pygame.Color("#6C8EF5").lerp("#4ADE80", i / 30)
                    pygame.draw.polygon(tela, cor, pontos, 2)
                    tamanho *= 0.88
                    angulo += 12
            elif evento.key == pygame.K_2:
                tela.fill("#121417")
                desenharArvore(tela, largura // 2, altura - 40, 110, 0, PROFUNDIDADE_ARVORE, PROFUNDIDADE_ARVORE)
            elif evento.key == pygame.K_3:
                tela.fill("#121417")
                desenharFlocoDeNeve(tela, (largura // 2, altura // 2 + 40), 240, PROFUNDIDADE_KOCH, "#6C8EF5")
            legenda = fonte.render("1: espiral   2: árvore   3: floco de Koch", True, "#8A93A1")
            tela.blit(legenda, (16, altura - 30))
            pygame.display.update()

pygame.quit()
