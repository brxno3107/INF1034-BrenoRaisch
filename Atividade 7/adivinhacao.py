import random
import pygame

pygame.init()
largura, altura = 480, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Adivinhação")
relogio = pygame.time.Clock()
fonteTitulo = pygame.font.Font(None, 56)
fonteGrande = pygame.font.Font(None, 90)
fonteTexto = pygame.font.Font(None, 36)
fonteMenor = pygame.font.Font(None, 28)

corFundo = "#222831"
corTexto = "#EEEEEE"
corBotao = "#393E46"
corBotaoHover = "#00ADB5"
corBotaoRemover = "#E84855"
corDestaque = "#FF9F1C"
corMenor = "#2EC4B6"
corMaior = "#E84855"
corAcerto = "#00ADB5"

MINIMO = 1
MAXIMO = 1023

estado = {
    "papel": None,
    "segredo": None,
    "digitado": "",
    "palpite": None,
    "minimo": MINIMO,
    "maximo": MAXIMO,
    "tentativas": 0,
    "feedback": None,
    "vencedor": False,
    "mensagem": "",
}


def comparar(numeroGerado, numeroFornecido):
    if numeroGerado < numeroFornecido:
        return -1
    if numeroGerado > numeroFornecido:
        return 1
    return 0


def iniciarUsuarioAdivinha(estado):
    estado.update({
        "papel": "usuario",
        "segredo": random.randint(MINIMO, MAXIMO),
        "digitado": "",
        "palpite": None,
        "minimo": MINIMO,
        "maximo": MAXIMO,
        "tentativas": 0,
        "feedback": None,
        "vencedor": False,
        "mensagem": f"Tente adivinhar um número entre {MINIMO} e {MAXIMO}.",
    })


def iniciarComputadorAdivinha(estado):
    estado.update({
        "papel": "computador",
        "segredo": None,
        "digitado": "",
        "palpite": (MINIMO + MAXIMO) // 2,
        "minimo": MINIMO,
        "maximo": MAXIMO,
        "tentativas": 1,
        "feedback": None,
        "vencedor": False,
        "mensagem": f"Pense num número entre {MINIMO} e {MAXIMO}. O computador vai tentar adivinhar.",
    })


def tentarNumero(estado):
    if estado["digitado"] == "":
        return
    palpite = int(estado["digitado"])
    estado["digitado"] = ""
    if palpite < MINIMO or palpite > MAXIMO:
        estado["mensagem"] = f"Digite um número entre {MINIMO} e {MAXIMO}."
        return
    estado["tentativas"] += 1
    estado["palpite"] = palpite
    estado["feedback"] = comparar(estado["segredo"], palpite)
    if estado["feedback"] == 0:
        estado["vencedor"] = True
        estado["mensagem"] = f"Acertou em {estado['tentativas']} tentativa(s)!"
    else:
        estado["mensagem"] = "O número secreto é menor." if estado["feedback"] == -1 else "O número secreto é maior."


def responderComputador(estado, feedback):
    if feedback == 0:
        estado["vencedor"] = True
        estado["feedback"] = 0
        estado["mensagem"] = f"O computador acertou em {estado['tentativas']} tentativa(s)!"
        return
    if feedback == -1:
        estado["maximo"] = estado["palpite"] - 1
    else:
        estado["minimo"] = estado["palpite"] + 1
    if estado["minimo"] > estado["maximo"]:
        estado["mensagem"] = "Resposta inconsistente. Reinicie o jogo."
        return
    estado["palpite"] = (estado["minimo"] + estado["maximo"]) // 2
    estado["tentativas"] += 1
    estado["feedback"] = feedback
    estado["mensagem"] = f"Tentativa {estado['tentativas']}: o computador chuta {estado['palpite']}."


def pressionarDigito(estado, caractere):
    if estado["papel"] != "usuario" or estado["vencedor"]:
        return
    if len(estado["digitado"]) < 4:
        estado["digitado"] += caractere


def apagarUltimo(estado):
    estado["digitado"] = estado["digitado"][:-1]


def desenharBotao(rect, texto, cor=corBotao, fonte=fonteTexto):
    posicaoMouse = pygame.mouse.get_pos()
    corFinal = corBotaoHover if rect.collidepoint(posicaoMouse) and cor == corBotao else cor
    pygame.draw.rect(tela, corFinal, rect, border_radius=12)
    rotulo = fonte.render(texto, True, corTexto)
    tela.blit(rotulo, rotulo.get_rect(center=rect.center))


def desenharMenu():
    tituloRender = fonteTitulo.render("Quem vai adivinhar?", True, corTexto)
    tela.blit(tituloRender, tituloRender.get_rect(center=(largura // 2, 200)))
    desenharBotao(botaoMenuUsuario, "Eu adivinho")
    desenharBotao(botaoMenuComputador, "Computador adivinha")


def desenharIndicadorFeedback(feedback):
    if feedback is None:
        return
    cores = {-1: corMenor, 1: corMaior, 0: corAcerto}
    textos = {-1: "-1", 1: "1", 0: "0"}
    caixa = pygame.Rect(largura // 2 - 60, 290, 120, 90)
    pygame.draw.rect(tela, cores[feedback], caixa, border_radius=14)
    rotulo = fonteGrande.render(textos[feedback], True, corTexto)
    tela.blit(rotulo, rotulo.get_rect(center=caixa.center))


def desenharJogo(estado):
    if estado["papel"] == "usuario":
        titulo = "Você adivinha"
    else:
        titulo = "Computador adivinha"
    tituloRender = fonteTitulo.render(titulo, True, corTexto)
    tela.blit(tituloRender, tituloRender.get_rect(center=(largura // 2, 40)))

    mensagemRender = fonteMenor.render(estado["mensagem"], True, corDestaque)
    tela.blit(mensagemRender, mensagemRender.get_rect(center=(largura // 2, 100)))

    if estado["papel"] == "usuario":
        digitadoRender = fonteGrande.render(estado["digitado"] or "_", True, corTexto)
        tela.blit(digitadoRender, digitadoRender.get_rect(center=(largura // 2, 200)))
    else:
        palpiteRender = fonteGrande.render(str(estado["palpite"]), True, corTexto)
        tela.blit(palpiteRender, palpiteRender.get_rect(center=(largura // 2, 200)))

    desenharIndicadorFeedback(estado["feedback"])

    tentativasRender = fonteMenor.render(f"Tentativas: {estado['tentativas']}", True, corTexto)
    tela.blit(tentativasRender, tentativasRender.get_rect(center=(largura // 2, 410)))

    if estado["papel"] == "computador" and not estado["vencedor"]:
        desenharBotao(botaoMenor, "-1", corMenor, fonteGrande)
        desenharBotao(botaoAcerto, "0", corAcerto, fonteGrande)
        desenharBotao(botaoMaior, "1", corMaior, fonteGrande)

    desenharBotao(botaoTrocarPapel, "Trocar papel")
    desenharBotao(botaoReiniciar, "Reiniciar", corBotaoRemover)


def desenharTela(estado):
    tela.fill(corFundo)
    if estado["papel"] is None:
        desenharMenu()
    else:
        desenharJogo(estado)
    pygame.display.update()


botaoMenuUsuario = pygame.Rect(largura // 2 - 130, 280, 260, 55)
botaoMenuComputador = pygame.Rect(largura // 2 - 130, 355, 260, 55)
botaoMenor = pygame.Rect(20, 470, 140, 50)
botaoAcerto = pygame.Rect(170, 470, 140, 50)
botaoMaior = pygame.Rect(320, 470, 140, 50)
botaoTrocarPapel = pygame.Rect(20, 540, 200, 45)
botaoReiniciar = pygame.Rect(260, 540, 200, 45)

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and estado["papel"] is not None:
            if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and estado["papel"] == "usuario":
                if not estado["vencedor"]:
                    tentarNumero(estado)
            elif evento.key == pygame.K_BACKSPACE:
                apagarUltimo(estado)
            elif evento.unicode and evento.unicode in "0123456789":
                pressionarDigito(estado, evento.unicode)
            elif evento.key == pygame.K_r:
                if estado["papel"] == "usuario":
                    iniciarUsuarioAdivinha(estado)
                else:
                    iniciarComputadorAdivinha(estado)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado["papel"] is None:
                if botaoMenuUsuario.collidepoint(evento.pos):
                    iniciarUsuarioAdivinha(estado)
                elif botaoMenuComputador.collidepoint(evento.pos):
                    iniciarComputadorAdivinha(estado)
            elif botaoReiniciar.collidepoint(evento.pos):
                if estado["papel"] == "usuario":
                    iniciarUsuarioAdivinha(estado)
                else:
                    iniciarComputadorAdivinha(estado)
            elif botaoTrocarPapel.collidepoint(evento.pos):
                if estado["papel"] == "usuario":
                    iniciarComputadorAdivinha(estado)
                else:
                    iniciarUsuarioAdivinha(estado)
            elif estado["papel"] == "computador" and not estado["vencedor"]:
                if botaoMenor.collidepoint(evento.pos):
                    responderComputador(estado, -1)
                elif botaoAcerto.collidepoint(evento.pos):
                    responderComputador(estado, 0)
                elif botaoMaior.collidepoint(evento.pos):
                    responderComputador(estado, 1)

    desenharTela(estado)
    relogio.tick(60)

pygame.quit()
