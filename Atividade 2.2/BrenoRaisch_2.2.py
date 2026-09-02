#Breno do Patrocínio Raisch
#2110039
##################################################################################################
from turtle import *
import math
t = Turtle()
t.speed(3)
larguraBandeira = 120
alturaBandeira = 80
espacoX = 20
espacoY = 50
margem = 450
indiceBandeira = 0
##################################################################################################
#funcoes
def posicao(indice):
    colunas = int((2 * margem) // (larguraBandeira + espacoX))
    coluna = indice % colunas
    linha = indice // colunas
    x = -margem + coluna * (larguraBandeira + espacoX)
    y = 200 - linha * (alturaBandeira + espacoY)
    return x, y

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
#bandeiras
##################################################################################################
#franca (facil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
largura = larguraBandeira / 3
desenhaRetangulo(t, x, y, largura, alturaBandeira, "blue")
desenhaRetangulo(t, x + largura, y, largura, alturaBandeira, "white")
desenhaRetangulo(t, x + 2 * largura, y, largura, alturaBandeira, "red")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "França")
##################################################################################################
#turquia (media)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, alturaBandeira, "red")
desenhaMeiaLua(t, x + 40, y + 40, 24, "white", "red", 10, 0, 19)
desenhaEstrelaSolida(t, x + 61, y + 46, 6.5, 2.5, "white")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Turquia")
##################################################################################################
#mauritania (media)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
faixaVermelha = alturaBandeira * 0.2
faixaVerde = alturaBandeira - 2 * faixaVermelha
desenhaRetangulo(t, x, y, larguraBandeira, alturaBandeira, "red")
desenhaRetangulo(t, x, y + faixaVermelha, larguraBandeira, faixaVerde, "green")
cx = x + larguraBandeira / 2
cy = y + faixaVermelha + faixaVerde / 2
desenhaMeiaLua(t, cx, cy, 13, "yellow", "green", 0, 5, 10)
desenhaEstrelaSolida(t, cx, cy + 12, 4.2, 1.6, "yellow")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Mauritânia")
##################################################################################################
#grecia (dificil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
alturaListra = alturaBandeira / 9
for i in range(9):
    cor = "blue" if i % 2 == 0 else "white"
    desenhaRetangulo(t, x, y + i * alturaListra, larguraBandeira, alturaListra, cor)
ladoCantao = alturaListra * 5
desenhaRetangulo(t, x, y + alturaBandeira - ladoCantao, ladoCantao, ladoCantao, "blue")
espessura = ladoCantao / 5
desenhaRetangulo(t, x, y + alturaBandeira - ladoCantao / 2 - espessura / 2, ladoCantao, espessura, "white")
desenhaRetangulo(t, x + ladoCantao / 2 - espessura / 2, y + alturaBandeira - ladoCantao, espessura, ladoCantao, "white")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Grécia")
##################################################################################################
#japao (facil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, alturaBandeira, "white")
desenhaCirculo(t, x + larguraBandeira / 2, y + alturaBandeira / 2, 20, "red")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Japão")
##################################################################################################
#coreia do norte (dificil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, 16, "blue")
desenhaRetangulo(t, x, y + 16, larguraBandeira, 4, "white")
desenhaRetangulo(t, x, y + 20, larguraBandeira, 40, "red")
desenhaRetangulo(t, x, y + 60, larguraBandeira, 4, "white")
desenhaRetangulo(t, x, y + 64, larguraBandeira, 16, "blue")
cxCoreia = x + larguraBandeira * 0.3
cyCoreia = y + 40
desenhaCirculo(t, cxCoreia, cyCoreia, 14, "white")
desenhaEstrelaSolida(t, cxCoreia, cyCoreia, 14, 5.3, "red")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Coreia do Norte")
##################################################################################################
#tuvalu (dificil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, alturaBandeira, "#4aa9e0")
cantaoLargura = 60
cantaoAltura = 30
cx0 = x
cy0 = y + alturaBandeira - cantaoAltura
desenhaRetangulo(t, cx0, cy0, cantaoLargura, cantaoAltura, "#00247d")
desenhaLinha(t, cx0, cy0, cx0 + cantaoLargura, cy0 + cantaoAltura, 8, "white")
desenhaLinha(t, cx0, cy0 + cantaoAltura, cx0 + cantaoLargura, cy0, 8, "white")
desenhaLinha(t, cx0, cy0, cx0 + cantaoLargura, cy0 + cantaoAltura, 4, "red")
desenhaLinha(t, cx0, cy0 + cantaoAltura, cx0 + cantaoLargura, cy0, 4, "red")
desenhaLinha(t, cx0, cy0 + cantaoAltura / 2, cx0 + cantaoLargura, cy0 + cantaoAltura / 2, 10, "white")
desenhaLinha(t, cx0 + cantaoLargura / 2, cy0, cx0 + cantaoLargura / 2, cy0 + cantaoAltura, 10, "white")
desenhaLinha(t, cx0, cy0 + cantaoAltura / 2, cx0 + cantaoLargura, cy0 + cantaoAltura / 2, 5, "red")
desenhaLinha(t, cx0 + cantaoLargura / 2, cy0, cx0 + cantaoLargura / 2, cy0 + cantaoAltura, 5, "red")
estrelas = [(62, 12), (78, 8), (70, 26), (88, 24), (78, 42), (96, 40), (88, 58), (104, 54), (98, 68)]
for i in estrelas:
    desenhaEstrelaSolida(t, x + i[0] + 3, y + i[1] - 1, 3.2, 1.2, "yellow")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Tuvalu")
########################################################################################
#israel(medio)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, alturaBandeira, "white")
desenhaRetangulo(t, x, y + 62, larguraBandeira, 10, "#0038b8")
desenhaRetangulo(t, x, y + 8, larguraBandeira, 10, "#0038b8")
cxIsrael = x + larguraBandeira / 2
cyIsrael = y + alturaBandeira / 2
raioEstrela = 18
desenhaContornoLivre(t, [(cxIsrael, cyIsrael + raioEstrela),
                          (cxIsrael - raioEstrela * 0.866, cyIsrael - raioEstrela * 0.5),
                          (cxIsrael + raioEstrela * 0.866, cyIsrael - raioEstrela * 0.5)], 3, "#0038b8")
desenhaContornoLivre(t, [(cxIsrael, cyIsrael - raioEstrela),
                          (cxIsrael + raioEstrela * 0.866, cyIsrael + raioEstrela * 0.5),
                          (cxIsrael - raioEstrela * 0.866, cyIsrael + raioEstrela * 0.5)], 3, "#0038b8")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Israel")
########################################################################################
#comores (dificil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, 20, "blue")
desenhaRetangulo(t, x, y + 20, larguraBandeira, 20, "red")
desenhaRetangulo(t, x, y + 40, larguraBandeira, 20, "white")
desenhaRetangulo(t, x, y + 60, larguraBandeira, 20, "yellow")
desenhoLivre(t, [(x, y), (x, y + alturaBandeira), (x + 48, y + 40)], "green")
desenhaMeiaLua(t, x + 13, y + 40, 9, "white", "green", 4, 0, 7)
estrelasComores = [(23, 25), (23, 35), (23, 45), (23, 55)]
for i in estrelasComores:
    desenhaEstrelaSolida(t, x + i[0] + 2, y + i[1] - 0.65, 2.1, 0.8, "white")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Comores")
########################################################################################
#marrocos (facil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
desenhaRetangulo(t, x, y, larguraBandeira, alturaBandeira, "red")
cxMarrocos = x + larguraBandeira / 2
cyMarrocos = y + alturaBandeira / 2
tamanhoEstrelaMarrocos = 30
xEstrelaMarrocos = cxMarrocos - tamanhoEstrelaMarrocos / 2
yEstrelaMarrocos = cyMarrocos + tamanhoEstrelaMarrocos * 0.1625
desenhaEstrelaContorno(t, xEstrelaMarrocos, yEstrelaMarrocos, tamanhoEstrelaMarrocos, 3, "green")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Marrocos")
########################################################################################
#romenia (facil)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
larguraFaixa = larguraBandeira / 3
desenhaRetangulo(t, x, y, larguraFaixa, alturaBandeira, "blue")
desenhaRetangulo(t, x + larguraFaixa, y, larguraFaixa, alturaBandeira, "yellow")
desenhaRetangulo(t, x + 2 * larguraFaixa, y, larguraFaixa, alturaBandeira, "red")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Romênia")
########################################################################################
#kiribati (extra)
x, y = posicao(indiceBandeira)
indiceBandeira += 1
horizonteY = y + 40
desenhaRetangulo(t, x, y + 40, larguraBandeira, 40, "red")
numBandas = 6
alturaBanda = 40 / numBandas
amplitudeOnda = 2.5
numOndas = 3
for i in range(numBandas):
    yBase = y + i * alturaBanda
    cor = "white" if i % 2 == 1 else "#1a3a8f"
    desenhaFaixaOndulada(t, x, yBase, larguraBandeira, alturaBanda, amplitudeOnda, numOndas, cor)
cxSol = x + 60
desenhaMeiaSol(t, cxSol, horizonteY, 14, 17, 10, "gold")
cxAve = x + 60
cyAve = y + 68
desenhoLivre(t, [
    (cxAve - 15, cyAve + 0), (cxAve - 9, cyAve + 3), (cxAve - 5, cyAve + 1),
    (cxAve - 7, cyAve + 5), (cxAve - 17, cyAve + 7), (cxAve - 4, cyAve + 3),
    (cxAve + 5, cyAve + 4), (cxAve + 14, cyAve + 7), (cxAve + 6, cyAve + 2),
    (cxAve + 13, cyAve + 0), (cxAve + 7, cyAve - 1), (cxAve + 12, cyAve - 3),
    (cxAve + 3, cyAve - 1), (cxAve - 3, cyAve - 2)
], "gold")
desenhaCirculo(t, cxAve - 10, cyAve + 2, 0.7, "black")
desenhaContorno(t, x, y, larguraBandeira, alturaBandeira)
escreveTitulo(t, x + larguraBandeira / 2, y - 20, "Kiribati - extra")
########################################################################################
t.hideturtle()
mainloop()
