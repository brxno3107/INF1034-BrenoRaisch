#ATIVIDADE 2.1
#BRENO DO PATROCÍNIO RAISCH
#2110039

from turtle import *

t = Turtle()
t.speed(7)

#Plano cartesiano
t.pensize(2)
t.color("black")
t.pu()
t.goto(-450, 0)
t.pd()
t.goto(450, 0)
t.pu()
t.goto(0, -350)
t.pd()
t.goto(0, 350)
t.pu()
t.home()

#1o quadrante - hexágono
t.pu()
t.goto(70, 70)
t.setheading(0)
t.pd()
color = textinput("Escolha da cor", "Digite a cor do hexágono (em inglês, ex: red, blue, yellow):")
t.color(color)
t.begin_fill()
for num in range(6):
    t.forward(30)
    t.left(60)
t.end_fill()

#2o quadrante - pentágono
t.pu()
t.goto(-190, 70)
t.setheading(0)
t.pd()
color = textinput("Escolha da cor", "Digite a cor do pentágono (em inglês, ex: red, blue, yellow):")
t.color(color)
t.begin_fill()
for num in range(5):
    t.forward(30)
    t.left(72)
t.end_fill()

#3o quadrante - hexadecágono
t.pu()
t.goto(-190, -110)
t.setheading(0)
t.pd()
color = textinput("Escolha da cor", "Digite a cor do hexadecágono (em inglês, ex: red, blue, yellow):")
t.color(color)
t.begin_fill()
for num in range(16):
    t.forward(15)
    t.left(22.5)
t.end_fill()

#4o quadrante - octógono
t.pu()
t.goto(70, -190)
t.setheading(0)
t.pd()
color = textinput("Escolha da cor", "Digite a cor do octógono (em inglês, ex: red, blue, yellow):")
t.color(color)
t.begin_fill()
for num in range(8):
    t.forward(22)
    t.left(45)
t.end_fill()

#espiral
t.pu()
t.goto(250, 250)
t.setheading(0)
t.pd()
color = textinput("Escolha da cor", "Digite a cor da espiral (em inglês, ex: red, blue, yellow):")
t.color(color)
tamanho = 0
for num in range(60):
    t.forward(tamanho)
    t.right(91)
    tamanho += 2

mainloop()
