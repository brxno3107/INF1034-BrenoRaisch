#Breno do Patrocínio Raisch
#2110039
##################################################################################################
from turtle import *
import math
import unicodedata
t = Turtle()
t.speed(3)
larguraBandeira = 120
alturaBandeira = 80
espacoX = 20
espacoY = 50
margem = 450
##################################################################################################
#funcoes auxiliares
def posicao(indice):
    colunas = int((2 * margem) // (larguraBandeira + espacoX))
    coluna = indice % colunas
    linha = indice // colunas
    x = -margem + coluna * (larguraBandeira + espacoX)
    y = 200 - linha * (alturaBandeira + espacoY)
    return x, y

def normaliza(texto):
    semAcento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return semAcento.strip().lower()

##################################################################################################
#funcoes que desenham figuras geometricas
def desenhaRetangulo(turt, x, y, largura, altura, cor):
    turt.pu()
    turt.goto(x, y)
    turt.setheading(0)
    turt.pd()
    turt.color(cor)
    turt.begin_fill()
    for i in range(2):
        turt.forward(largura)
        turt.left(90)
        turt.forward(altura)
        turt.left(90)
    turt.end_fill()

def desenhaCirculo(turt, x, y, raio, cor):
    turt.pu()
    turt.goto(x, y - raio)
    turt.setheading(0)
    turt.pd()
    turt.color(cor)
    turt.begin_fill()
    turt.circle(raio)
    turt.end_fill()

def desenhoLivre(turt, pontos, cor):
    turt.pu()
    turt.goto(pontos[0])
    turt.pd()
    turt.color(cor)
    turt.begin_fill()
    for i in pontos[1:]:
        turt.goto(i)
    turt.goto(pontos[0])
    turt.end_fill()

def desenhaContornoLivre(turt, pontos, espessura, cor):
    turt.pu()
    turt.goto(pontos[0])
    turt.pensize(espessura)
    turt.color(cor)
    turt.pd()
    for i in pontos[1:]:
        turt.goto(i)
    turt.goto(pontos[0])
    turt.pu()
    turt.pensize(1)


def desenhaLinha(turt, xIni, yIni, xFim, yFim, espessura, cor):
    turt.pu()
    turt.goto(xIni, yIni)
    turt.pensize(espessura)
    turt.color(cor)
    turt.pd()
    turt.goto(xFim, yFim)
    turt.pu()
    turt.pensize(1)

def pontosOnda(xIni, yBase, largura, amplitude, numOndas, passos=24):
    return [(xIni + (i / passos) * largura,
             yBase + amplitude * math.sin((i / passos) * numOndas * 2 * math.pi))
            for i in range(passos + 1)]

def desenhaFaixaOndulada(turt, x, yBase, largura, altura, amplitude, numOndas, cor):
    cima = pontosOnda(x, yBase + altura, largura, amplitude, numOndas)
    baixo = pontosOnda(x, yBase, largura, amplitude, numOndas)
    baixo.reverse()
    desenhoLivre(turt, cima + baixo, cor)

def desenhaEstrelaSolida(turt, cx, cy, raioExterno, raioInterno, cor):
    pontos = [(cx + (raioExterno if i % 2 == 0 else raioInterno) * math.cos(math.radians(90 - i * 36)),
               cy + (raioExterno if i % 2 == 0 else raioInterno) * math.sin(math.radians(90 - i * 36)))
              for i in range(10)]
    desenhoLivre(turt, pontos, cor)

def desenhaRaio(turt, cx, cy, raioInterno, raioExterno, anguloCentro, anguloMeio, cor):
    a1 = math.radians(anguloCentro - anguloMeio)
    a2 = math.radians(anguloCentro + anguloMeio)
    aCentro = math.radians(anguloCentro)
    p1 = (cx + raioInterno * math.cos(a1), cy + raioInterno * math.sin(a1))
    p2 = (cx + raioExterno * math.cos(aCentro), cy + raioExterno * math.sin(aCentro))
    p3 = (cx + raioInterno * math.cos(a2), cy + raioInterno * math.sin(a2))
    desenhoLivre(turt, [p1, p2, p3], cor)

def desenhaMeiaSol(turt, cx, cy, raio, numRaios, comprimentoRaio, cor):
    anguloMeio = (160 / (numRaios - 1)) / 2.2
    for i in range(numRaios):
        anguloCentro = 10 + i * (160 / (numRaios - 1))
        desenhaRaio(turt, cx, cy, raio, raio + comprimentoRaio, anguloCentro, anguloMeio, cor)
    turt.pu()
    turt.goto(cx + raio, cy)
    turt.setheading(90)
    turt.pd()
    turt.color(cor)
    turt.begin_fill()
    turt.circle(raio, 180)
    turt.goto(cx + raio, cy)
    turt.end_fill()

def desenhaMeiaLua(turt, x, y, raio, corLua, corFundo, deslocX, deslocY, raioCorte):
    desenhaCirculo(turt, x, y, raio, corLua)
    desenhaCirculo(turt, x + deslocX, y + deslocY, raioCorte, corFundo)

def desenhaEstrelaContorno(turt, x, y, tamanho, espessura, cor):
    turt.pu()
    turt.goto(x, y)
    turt.setheading(0)
    turt.pensize(espessura)
    turt.color(cor)
    turt.pd()
    for i in range(5):
        turt.forward(tamanho)
        turt.right(144)
    turt.pu()
    turt.pensize(1)

def desenhaContorno(turt, x, y, largura, altura, cor="black", espessura=2):
    turt.pu()
    turt.goto(x, y)
    turt.setheading(0)
    turt.pensize(espessura)
    turt.color(cor)
    turt.pd()
    for i in range(2):
        turt.forward(largura)
        turt.left(90)
        turt.forward(altura)
        turt.left(90)
    turt.pu()
    turt.pensize(1)

def escreveTitulo(turt, x, y, texto):
    turt.pu()
    turt.goto(x, y)
    turt.color("black")
    turt.write(texto, align="center", font=("Arial", 10, "bold"))

##################################################################################################
#uma funcao por bandeira (cada uma usa as funcoes de desenho geometrico acima)
##################################################################################################
def bandeiraFranca(turt, x, y):
    largura = larguraBandeira / 3
    desenhaRetangulo(turt, x, y, largura, alturaBandeira, "blue")
    desenhaRetangulo(turt, x + largura, y, largura, alturaBandeira, "white")
    desenhaRetangulo(turt, x + 2 * largura, y, largura, alturaBandeira, "red")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "França")

def bandeiraTurquia(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, alturaBandeira, "red")
    desenhaMeiaLua(turt, x + 40, y + 40, 24, "white", "red", 10, 0, 19)
    desenhaEstrelaSolida(turt, x + 61, y + 46, 6.5, 2.5, "white")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Turquia")

def bandeiraMauritania(turt, x, y):
    faixaVermelha = alturaBandeira * 0.2
    faixaVerde = alturaBandeira - 2 * faixaVermelha
    desenhaRetangulo(turt, x, y, larguraBandeira, alturaBandeira, "red")
    desenhaRetangulo(turt, x, y + faixaVermelha, larguraBandeira, faixaVerde, "green")
    cx = x + larguraBandeira / 2
    cy = y + faixaVermelha + faixaVerde / 2
    desenhaMeiaLua(turt, cx, cy, 13, "yellow", "green", 0, 5, 10)
    desenhaEstrelaSolida(turt, cx, cy + 12, 4.2, 1.6, "yellow")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Mauritânia")

def bandeiraGrecia(turt, x, y):
    alturaListra = alturaBandeira / 9
    for i in range(9):
        cor = "blue" if i % 2 == 0 else "white"
        desenhaRetangulo(turt, x, y + i * alturaListra, larguraBandeira, alturaListra, cor)
    ladoCantao = alturaListra * 5
    desenhaRetangulo(turt, x, y + alturaBandeira - ladoCantao, ladoCantao, ladoCantao, "blue")
    espessura = ladoCantao / 5
    desenhaRetangulo(turt, x, y + alturaBandeira - ladoCantao / 2 - espessura / 2, ladoCantao, espessura, "white")
    desenhaRetangulo(turt, x + ladoCantao / 2 - espessura / 2, y + alturaBandeira - ladoCantao, espessura, ladoCantao, "white")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Grécia")

def bandeiraJapao(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, alturaBandeira, "white")
    desenhaCirculo(turt, x + larguraBandeira / 2, y + alturaBandeira / 2, 20, "red")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Japão")

def bandeiraCoreiaDoNorte(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, 16, "blue")
    desenhaRetangulo(turt, x, y + 16, larguraBandeira, 4, "white")
    desenhaRetangulo(turt, x, y + 20, larguraBandeira, 40, "red")
    desenhaRetangulo(turt, x, y + 60, larguraBandeira, 4, "white")
    desenhaRetangulo(turt, x, y + 64, larguraBandeira, 16, "blue")
    cxCoreia = x + larguraBandeira * 0.3
    cyCoreia = y + 40
    desenhaCirculo(turt, cxCoreia, cyCoreia, 14, "white")
    desenhaEstrelaSolida(turt, cxCoreia, cyCoreia, 14, 5.3, "red")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Coreia do Norte")

def bandeiraTuvalu(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, alturaBandeira, "#4aa9e0")
    cantaoLargura = 60
    cantaoAltura = 30
    cx0 = x
    cy0 = y + alturaBandeira - cantaoAltura
    desenhaRetangulo(turt, cx0, cy0, cantaoLargura, cantaoAltura, "#00247d")
    desenhaLinha(turt, cx0, cy0, cx0 + cantaoLargura, cy0 + cantaoAltura, 8, "white")
    desenhaLinha(turt, cx0, cy0 + cantaoAltura, cx0 + cantaoLargura, cy0, 8, "white")
    desenhaLinha(turt, cx0, cy0, cx0 + cantaoLargura, cy0 + cantaoAltura, 4, "red")
    desenhaLinha(turt, cx0, cy0 + cantaoAltura, cx0 + cantaoLargura, cy0, 4, "red")
    desenhaLinha(turt, cx0, cy0 + cantaoAltura / 2, cx0 + cantaoLargura, cy0 + cantaoAltura / 2, 10, "white")
    desenhaLinha(turt, cx0 + cantaoLargura / 2, cy0, cx0 + cantaoLargura / 2, cy0 + cantaoAltura, 10, "white")
    desenhaLinha(turt, cx0, cy0 + cantaoAltura / 2, cx0 + cantaoLargura, cy0 + cantaoAltura / 2, 5, "red")
    desenhaLinha(turt, cx0 + cantaoLargura / 2, cy0, cx0 + cantaoLargura / 2, cy0 + cantaoAltura, 5, "red")
    estrelas = [(62, 12), (78, 8), (70, 26), (88, 24), (78, 42), (96, 40), (88, 58), (104, 54), (98, 68)]
    for i in estrelas:
        desenhaEstrelaSolida(turt, x + i[0] + 3, y + i[1] - 1, 3.2, 1.2, "yellow")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Tuvalu")

def bandeiraIsrael(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, alturaBandeira, "white")
    desenhaRetangulo(turt, x, y + 62, larguraBandeira, 10, "#0038b8")
    desenhaRetangulo(turt, x, y + 8, larguraBandeira, 10, "#0038b8")
    cxIsrael = x + larguraBandeira / 2
    cyIsrael = y + alturaBandeira / 2
    raioEstrela = 18
    desenhaContornoLivre(turt, [(cxIsrael, cyIsrael + raioEstrela),
                              (cxIsrael - raioEstrela * 0.866, cyIsrael - raioEstrela * 0.5),
                              (cxIsrael + raioEstrela * 0.866, cyIsrael - raioEstrela * 0.5)], 3, "#0038b8")
    desenhaContornoLivre(turt, [(cxIsrael, cyIsrael - raioEstrela),
                              (cxIsrael + raioEstrela * 0.866, cyIsrael + raioEstrela * 0.5),
                              (cxIsrael - raioEstrela * 0.866, cyIsrael + raioEstrela * 0.5)], 3, "#0038b8")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Israel")

def bandeiraComores(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, 20, "blue")
    desenhaRetangulo(turt, x, y + 20, larguraBandeira, 20, "red")
    desenhaRetangulo(turt, x, y + 40, larguraBandeira, 20, "white")
    desenhaRetangulo(turt, x, y + 60, larguraBandeira, 20, "yellow")
    desenhoLivre(turt, [(x, y), (x, y + alturaBandeira), (x + 48, y + 40)], "green")
    desenhaMeiaLua(turt, x + 13, y + 40, 9, "white", "green", 4, 0, 7)
    estrelasComores = [(23, 25), (23, 35), (23, 45), (23, 55)]
    for i in estrelasComores:
        desenhaEstrelaSolida(turt, x + i[0] + 2, y + i[1] - 0.65, 2.1, 0.8, "white")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Comores")

def bandeiraMarrocos(turt, x, y):
    desenhaRetangulo(turt, x, y, larguraBandeira, alturaBandeira, "red")
    cxMarrocos = x + larguraBandeira / 2
    cyMarrocos = y + alturaBandeira / 2
    tamanhoEstrelaMarrocos = 30
    xEstrelaMarrocos = cxMarrocos - tamanhoEstrelaMarrocos / 2
    yEstrelaMarrocos = cyMarrocos + tamanhoEstrelaMarrocos * 0.1625
    desenhaEstrelaContorno(turt, xEstrelaMarrocos, yEstrelaMarrocos, tamanhoEstrelaMarrocos, 3, "green")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Marrocos")

def bandeiraRomenia(turt, x, y):
    larguraFaixa = larguraBandeira / 3
    desenhaRetangulo(turt, x, y, larguraFaixa, alturaBandeira, "blue")
    desenhaRetangulo(turt, x + larguraFaixa, y, larguraFaixa, alturaBandeira, "yellow")
    desenhaRetangulo(turt, x + 2 * larguraFaixa, y, larguraFaixa, alturaBandeira, "red")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Romênia")

def bandeiraKiribati(turt, x, y):
    horizonteY = y + 40
    desenhaRetangulo(turt, x, y + 40, larguraBandeira, 40, "red")
    numBandas = 6
    alturaBanda = 40 / numBandas
    amplitudeOnda = 2.5
    numOndas = 3
    for i in range(numBandas):
        yBase = y + i * alturaBanda
        cor = "white" if i % 2 == 1 else "#1a3a8f"
        desenhaFaixaOndulada(turt, x, yBase, larguraBandeira, alturaBanda, amplitudeOnda, numOndas, cor)
    cxSol = x + 60
    desenhaMeiaSol(turt, cxSol, horizonteY, 14, 17, 10, "gold")
    cxAve = x + 60
    cyAve = y + 68
    desenhoLivre(turt, [
        (cxAve - 15, cyAve + 0), (cxAve - 9, cyAve + 3), (cxAve - 5, cyAve + 1),
        (cxAve - 7, cyAve + 5), (cxAve - 17, cyAve + 7), (cxAve - 4, cyAve + 3),
        (cxAve + 5, cyAve + 4), (cxAve + 14, cyAve + 7), (cxAve + 6, cyAve + 2),
        (cxAve + 13, cyAve + 0), (cxAve + 7, cyAve - 1), (cxAve + 12, cyAve - 3),
        (cxAve + 3, cyAve - 1), (cxAve - 3, cyAve - 2)
    ], "gold")
    desenhaCirculo(turt, cxAve - 10, cyAve + 2, 0.7, "black")
    desenhaContorno(turt, x, y, larguraBandeira, alturaBandeira)
    escreveTitulo(turt, x + larguraBandeira / 2, y - 20, "Kiribati")

##################################################################################################
#lista com todas as bandeiras disponiveis (nome exibido, funcao que desenha)
bandeiras = [
    ("França", bandeiraFranca),
    ("Turquia", bandeiraTurquia),
    ("Mauritânia", bandeiraMauritania),
    ("Grécia", bandeiraGrecia),
    ("Japão", bandeiraJapao),
    ("Coreia do Norte", bandeiraCoreiaDoNorte),
    ("Tuvalu", bandeiraTuvalu),
    ("Israel", bandeiraIsrael),
    ("Comores", bandeiraComores),
    ("Marrocos", bandeiraMarrocos),
    ("Romênia", bandeiraRomenia),
    ("Kiribati", bandeiraKiribati),
]

def desenhaTodas():
    for indice, (_, funcao) in enumerate(bandeiras):
        x, y = posicao(indice)
        funcao(t, x, y)

def desenhaUma(funcao):
    funcao(t, -larguraBandeira / 2, -alturaBandeira / 2)

##################################################################################################
#escolha da bandeira via textinput, repetindo ate digitar SAIR (EXTRA)
nomes = ", ".join(nome for nome, _ in bandeiras)
t.hideturtle()

while True:
    resposta = textinput("Escolha a bandeira",
                          "Digite o nome da bandeira (" + nomes + ")\n"
                          "deixe em branco para ver todas\n"
                          "ou digite SAIR para fechar o programa:")

    if resposta and normaliza(resposta) == "sair":
        break

    t.clear()

    funcaoEscolhida = None
    if resposta:
        respostaNormalizada = normaliza(resposta)
        for nome, funcao in bandeiras:
            if normaliza(nome) == respostaNormalizada:
                funcaoEscolhida = funcao
                break

    if funcaoEscolhida:
        desenhaUma(funcaoEscolhida)
    else:
        desenhaTodas()

bye()
