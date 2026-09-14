#ATIVIDADE 4.1
#BRENO DO PATROCÍNIO RAISCH
#2110039

import math
import random
import time
from turtle import *

t = Turtle()
t.speed(8)

limiteX = 400
limiteY = 400
escala = 20


def desenhaPlanoCartesiano():
    t.pensize(2)
    t.color("black")
    t.pu()
    t.goto(-limiteX, 0)
    t.pd()
    t.goto(limiteX, 0)
    t.pu()
    t.goto(0, -limiteY)
    t.pd()
    t.goto(0, limiteY)
    t.pu()
    t.home()


def desenhaFuncao(funcao, cor, xMin=-10, xMax=10, passo=0.05):
    t.pensize(2)
    t.color(cor)
    t.pu()
    ultimoValido = False
    x = xMin
    while x <= xMax:
        try:
            y = funcao(x)
            px, py = x * escala, y * escala
            if abs(py) > limiteY * 3:
                ultimoValido = False
            else:
                t.goto(px, py)
                if ultimoValido:
                    t.pd()
                else:
                    t.pu()
                    t.goto(px, py)
                    t.pd()
                ultimoValido = True
        except (ValueError, ZeroDivisionError, OverflowError):
            ultimoValido = False
        x += passo
    t.pu()


def desenhaPodio(colocacoes):
    t.clear()
    t.pu()
    t.home()

    alturas = [100, 70, 50]
    larguraBloco = 80
    posicoesX = [0, -180, 180]
    ordemPodio = [0, 1, 2]

    for posicao in ordemPodio:
        if posicao >= len(colocacoes):
            continue
        numero, cor = colocacoes[posicao]
        x = posicoesX[posicao]
        altura = alturas[posicao]

        t.pu()
        t.goto(x - larguraBloco / 2, -150)
        t.setheading(0)
        t.pd()
        t.color("black", cor)
        t.begin_fill()
        for lado in range(2):
            t.forward(larguraBloco)
            t.left(90)
            t.forward(altura)
            t.left(90)
        t.end_fill()

        t.pu()
        t.goto(x, -170)
        t.color("black")
        t.write(f"{posicao + 1}º - Tartaruga {numero}", align="center", font=("Arial", 12, "bold"))

    t.pu()
    t.home()


def nitroDoMaxVerstappen(tartaruga, numero, linhaChegada):
    if random.randint(1, 10000) == 1:
        tartaruga.goto(linhaChegada, tartaruga.ycor())
        print(f"NITRO DO MAX VERSTAPPEN! A tartaruga {numero} disparou até a linha de chegada!")
        return True
    return False


def corridaDeTartarugas(n):
    linhaChegada = limiteX - 20
    espacamentoY = 40
    cores = ["red", "blue", "green", "orange", "purple", "brown", "black", "deeppink", "cyan", "gold"]

    tartarugas = []
    labels = []
    for i in range(n):
        tartaruga = Turtle()
        tartaruga.shape("turtle")
        tartaruga.color(cores[i % len(cores)])
        tartaruga.pu()
        tartaruga.goto(-limiteX + 20, (i - (n - 1) / 2) * espacamentoY)
        tartaruga.setheading(0)
        tartarugas.append(tartaruga)

        label = Turtle()
        label.hideturtle()
        label.pu()
        label.color("black")
        labels.append(label)

    def atualizaLabel(indice):
        tartaruga = tartarugas[indice]
        label = labels[indice]
        label.clear()
        label.goto(tartaruga.xcor(), tartaruga.ycor() + 15)
        label.write(str(indice + 1), align="center", font=("Arial", 10, "bold"))

    for i in range(n):
        atualizaLabel(i)

    alturaLinha = (n - 1) / 2 * espacamentoY + 20
    t.pu()
    t.goto(linhaChegada, -alturaLinha)
    t.setheading(90)
    t.pd()
    t.pensize(3)
    t.color("red")
    t.forward(alturaLinha * 2)
    t.pu()

    colocacoes = []
    restantes = list(range(n))
    numeroTop3 = min(3, n)

    while len(colocacoes) < numeroTop3 and restantes:
        for i in list(restantes):
            tartaruga = tartarugas[i]
            if not nitroDoMaxVerstappen(tartaruga, i + 1, linhaChegada):
                tartaruga.forward(random.randint(1, 10))
            atualizaLabel(i)
            if tartaruga.xcor() >= linhaChegada:
                colocacoes.append((i + 1, cores[i % len(cores)]))
                restantes.remove(i)
                if len(colocacoes) >= numeroTop3:
                    break

    for tartaruga in tartarugas:
        tartaruga.hideturtle()
    for label in labels:
        label.clear()

    desenhaPodio(colocacoes)


funcoes = [
    (lambda x: math.sqrt(x), "blue"),
    (lambda x: 1 / x, "red"),
    (lambda x: 2 ** x, "green"),
    (lambda x: 5 - x ** 2, "purple"),
    (lambda x: x ** 2 - 5 * x + 6, "orange"),
    (lambda x: x ** 3 - x ** 2 - x + 1, "brown"),
]

for funcao, cor in funcoes:
    desenhaPlanoCartesiano()
    desenhaFuncao(funcao, cor)
    time.sleep(2)
    t.clear()

n = int(textinput("Corrida de tartarugas", "Quantas tartarugas você quer que corram?"))
corridaDeTartarugas(n)

mainloop()
