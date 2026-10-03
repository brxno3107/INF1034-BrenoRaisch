import pygame

pygame.init()
largura, altura = 360, 560
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Calculadora")
relogio = pygame.time.Clock()
fonteVisor = pygame.font.Font(None, 64)
fonteMenor = pygame.font.Font(None, 30)
fonteBotao = pygame.font.Font(None, 44)
margem = 12
alturaVisor = 130
alturaBotao = 70
larguraBotao = (largura - 5 * margem) // 4
corFundo = "#222831"
corVisor = "#EEEEEE"
corTextoVisor = "#222831"
corBotaoNumero = "#393E46"
corBotaoOperador = "#FF9F1C"
corBotaoIgual = "#00ADB5"
corBotaoLimpar = "#E84855"
corTextoBotao = "#FFFFFF"
layout = [
    ["C", "<", "/", "*"],["7", "8", "9", "-"],["4", "5", "6", "+"],["1", "2", "3", "="],["0", "."],
]
estado = {"entrada": "", "memoria": None, "operador": None, "mensagem": ""}
##################################################################################################
def calcular(valorA, operador, valorB):
    if operador == "+":
        return valorA + valorB
    if operador == "-":
        return valorA - valorB
    if operador == "*":
        return valorA * valorB
    if valorB == 0:
        return None
    return valorA / valorB

def formatarResultado(valor):
    if valor == int(valor):
        return str(int(valor))
    return str(valor)

def montarBotoes():
    botoes = []
    for linha, textos in enumerate(layout):
        for coluna, texto in enumerate(textos):
            x = margem + coluna * (larguraBotao + margem)
            y = alturaVisor + margem + linha * (alturaBotao + margem)
            botoes.append((pygame.Rect(x, y, larguraBotao, alturaBotao), texto))
    return botoes

def digitar(estado, caractere):
    if caractere == "." and "." in estado["entrada"]:
        return
    if estado["entrada"] == "0" and caractere != ".":
        estado["entrada"] = ""
    if estado["entrada"] == "" and caractere == ".":
        estado["entrada"] = "0"
    if len(estado["entrada"]) < 12:
        estado["entrada"] += caractere

def fecharOperacao(estado):
    if estado["entrada"] == "":
        return True
    numero = float(estado["entrada"])
    if estado["memoria"] is None or estado["operador"] is None:
        estado["memoria"] = numero
    else:
        resultado = calcular(estado["memoria"], estado["operador"], numero)
        if resultado is None:
            estado["mensagem"] = "Erro: divisão por zero"
            return False
        estado["memoria"] = resultado
    estado["entrada"] = ""
    estado["operador"] = None
    return True

def pressionarOperador(estado, operador):
    if estado["entrada"] == "" and estado["memoria"] is None:
        return
    if not fecharOperacao(estado):
        return
    estado["operador"] = operador

def pressionarIgual(estado):
    fecharOperacao(estado)

def apagarUltimo(estado):
    estado["entrada"] = estado["entrada"][:-1]

def limpar(estado):
    estado["entrada"] = ""
    estado["memoria"] = None
    estado["operador"] = None

def pressionar(estado, texto):
    estado["mensagem"] = ""
    if texto in "0123456789.":
        digitar(estado, texto)
    elif texto in ["+", "-", "*", "/"]:
        pressionarOperador(estado, texto)
    elif texto == "=":
        pressionarIgual(estado)
    elif texto == "<":
        apagarUltimo(estado)
    elif texto == "C":
        limpar(estado)

def textoDaTecla(evento):
    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        return "="
    if evento.key == pygame.K_BACKSPACE:
        return "<"
    if evento.key == pygame.K_ESCAPE:
        return "C"
    if evento.unicode and evento.unicode in "0123456789.+-*/=":
        return evento.unicode
    if evento.unicode and evento.unicode in "cC":
        return "C"
    return None

def desenharBotao(rect, texto):
    if texto in "0123456789.":
        cor = corBotaoNumero
    elif texto == "=":
        cor = corBotaoIgual
    elif texto == "C" or texto == "<":
        cor = corBotaoLimpar
    else:
        cor = corBotaoOperador
    pygame.draw.rect(tela, cor, rect, border_radius=12)
    rotulo = fonteBotao.render(texto, True, corTextoBotao)
    tela.blit(rotulo, rotulo.get_rect(center=rect.center))

def desenharVisor(estado):
    pygame.draw.rect(tela, corVisor, (0, 0, largura, alturaVisor))
    if estado["memoria"] is not None and estado["operador"] is not None:
        linhaAnterior = f"{formatarResultado(estado['memoria'])} {estado['operador']}"
        superior = fonteMenor.render(linhaAnterior, True, corTextoVisor)
        tela.blit(superior, superior.get_rect(topright=(largura - margem, 14)))
    if estado["entrada"]:
        principal = estado["entrada"]
    elif estado["memoria"] is not None:
        principal = formatarResultado(estado["memoria"])
    else:
        principal = "0"
    textoPrincipal = fonteVisor.render(principal, True, corTextoVisor)
    tela.blit(textoPrincipal, textoPrincipal.get_rect(bottomright=(largura - margem, alturaVisor - 22)))
    if estado["mensagem"]:
        aviso = fonteMenor.render(estado["mensagem"], True, "#E84855")
        tela.blit(aviso, aviso.get_rect(bottomleft=(margem, alturaVisor - 8)))

def desenharTela(estado, botoes):
    tela.fill(corFundo)
    desenharVisor(estado)
    for rect, texto in botoes:
        desenharBotao(rect, texto)
    pygame.display.update()
###################################################################################################
botoes = montarBotoes()
while 1==1:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            texto = textoDaTecla(evento)
            if texto is not None:
                pressionar(estado, texto)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for rect, texto in botoes:
                if rect.collidepoint(evento.pos):
                    pressionar(estado, texto)
    desenharTela(estado, botoes)
    relogio.tick(60)
####################################################################################################
pygame.quit()
