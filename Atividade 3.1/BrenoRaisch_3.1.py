#ATIVIDADE 3.1
#BRENO DO PATROCÍNIO RAISCH
#2110039
import random
from turtle import *
####################################################
t = Turtle()
t.speed(8)
limiteX = 300
limiteY = 300
#############################################################
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

def posicaoAleatoria(quadrante, margem=80):
    if quadrante == 1:
        x = random.randint(margem, limiteX - margem)
        y = random.randint(margem, limiteY - margem)
    elif quadrante == 2:
        x = random.randint(-limiteX + margem, -margem)
        y = random.randint(margem, limiteY - margem)
    elif quadrante == 3:
        x = random.randint(-limiteX + margem, -margem)
        y = random.randint(-limiteY + margem, -margem)
    else:
        x = random.randint(margem, limiteX - margem)
        y = random.randint(-limiteY + margem, -margem)
    return x, y

def desenhaPoligono(x, y, tamanho, cor, lados):
    t.pu()
    t.goto(x, y)
    t.setheading(0)
    t.pd()
    t.color(cor)
    t.begin_fill()
    angulo = 360 / lados
    for i in range(lados):
        t.forward(tamanho)
        t.left(angulo)
    t.end_fill()

def desenhaCirculo(x, y, tamanho, cor):
    t.pu()
    t.goto(x, y - tamanho)
    t.setheading(0)
    t.pd()
    t.color(cor)
    t.begin_fill()
    t.circle(tamanho)
    t.end_fill()

def desenhaEspiral(x, y, tamanho, cor):
    t.pu()
    t.goto(x, y)
    t.setheading(0)
    t.pd()
    t.color(cor)
    raio = tamanho
    for num in range(20):
        t.circle(raio, 90)
        raio += tamanho
###########################################################################
#BLOCO PRINCIPAL
desenhaPlanoCartesiano()
#hexagono
x, y = posicaoAleatoria(1)
color = textinput("Escolha da cor", "Digite a cor do hexágono (em inglês, ex: red, blue, yellow):")
desenhaPoligono(x, y, 30, color, 6)
#pentagono
x, y = posicaoAleatoria(2)
color = textinput("Escolha da cor", "Digite a cor do pentágono (em inglês, ex: red, blue, yellow):")
desenhaPoligono(x, y, 30, color, 5)
#circulo
x, y = posicaoAleatoria(3, margem=100)
color = textinput("Escolha da cor", "Digite a cor do círculo (em inglês, ex: red, blue, yellow):")
desenhaCirculo(x, y, 40, color)
#octogono
x, y = posicaoAleatoria(4)
color = textinput("Escolha da cor", "Digite a cor do octógono (em inglês, ex: red, blue, yellow):")
desenhaPoligono(x, y, 22, color, 8)
#espiral
x, y = posicaoAleatoria(1, margem=90)
color = textinput("Escolha da cor", "Digite a cor da espiral (em inglês, ex: red, blue, yellow):")
desenhaEspiral(x, y, 2, color)
#################################################
mainloop()
