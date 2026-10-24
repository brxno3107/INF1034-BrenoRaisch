import math
import random
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN

larguraTela, alturaTela = 900, 600
corFundo = (24, 26, 33)
corTexto = (230, 232, 238)
corTextoSuave = (150, 155, 170)
corEixo = (210, 214, 224)
corGrade = (46, 50, 62)
corErro = (240, 110, 110)
graficoEsq, graficoDir, graficoTopo, graficoBase = 90, larguraTela - 50, 160, alturaTela - 120
numsEstaticos = [
    100, 120, 130, 120, 150, 100, 160, 200, 190, 110, 115, 125, 135, 170, 130
]

faixasHist1 = 6
faixasHist2 = 4
faixasHist3 = 3
#############################################################################################
def contabilizaTotais(nums, numCat):
    # Adaptação de contabiliza_totais do código do professor
    #cria um contador zerado para cada faixa/categoria
    totais = [0] * numCat
    #sem números não há como calcular limites, então devolve tudo zerado
    if not nums:
        return totais, None
    #O menor e o maior valor da lista definem o início e o fim do eixo x
    numMin = min(nums)
    numMax = max(nums)
    #Largura de cada faixa: a amplitude total dividida pela quantidade de faixas
    tamCat = (numMax - numMin) / numCat
    # Para cada número na lista
    for num in nums:
        # O maior valor é tratado à parte: como o limite superior é exclusivo (<),
        # ele não cairia em nenhuma faixa, então vai direto para a última
        if num == numMax:
            totais[-1] += 1
            continue
        # Para cada faixa/categoria
        for iCat in range(numCat):
            # Obtém os limites inferior e superior da faixa atual
            limInf = numMin + iCat * tamCat
            limSup = numMin + (iCat + 1) * tamCat
            #Se o número está entre esses limites, conta nessa faixa e para de procurar
            if limInf <= num < limSup:
                totais[iCat] += 1
                break
        else:
            #Proteção contra arredondamento de float: se não coube em nenhuma, é da última
            totais[-1] += 1

    #retorna as contagens e os limites usados para marcar o eixo x
    return totais, (numMin, numMax)
#############################################################################################
def totaisAleatorios(nums, numCat):
    totais = [0] * numCat
    quantidade = random.randint(1, len(nums))
    for _ in range(quantidade):
        totais[random.randrange(numCat)] += 1
    return totais, (min(nums), max(nums))

def coresAleatorias(quantidade):
    return [tuple(random.randint(70, 235) for _ in range(3)) for _ in range(quantidade)]

def criarHistograma1():
    nums = [random.randint(0, 100) for _ in range(60)]
    totais, limites = contabilizaTotais(nums, faixasHist1)
    return {
        "titulo": "Histograma 1 - Lista aleatória",
        "descricao": f"{len(nums)} números aleatórios entre 0 e 100  |  {faixasHist1} faixas  |  R: sortear de novo",
        "numCat": faixasHist1,
        "totais": totais,
        "limites": limites,
        "cores": coresAleatorias(faixasHist1),
    }

def criarHistograma2():
    totais, limites = totaisAleatorios(numsEstaticos, faixasHist2)
    return {
        "titulo": "Histograma 2 - Lista estática, totais sorteados",
        "descricao": f"Soma dos totais: {sum(totais)} de {len(numsEstaticos)} números  |  {faixasHist2} faixas  |  R: sortear de novo",
        "numCat": faixasHist2,
        "totais": totais,
        "limites": limites,
        "cores": coresAleatorias(faixasHist2),
    }

def criarHistograma3():
    return {
        "titulo": "Histograma 3 - Números digitados",
        "descricao": f"Enter: adicionar  |  Backspace: apagar  |  Delete: limpar lista  |  {faixasHist3} faixas",
        "numCat": faixasHist3,
        "totais": [0] * faixasHist3,
        "limites": None,
        "cores": coresAleatorias(faixasHist3),
    }

def formatarNumero(valor):
    arredondado = round(valor, 1)
    return f"{arredondado:g}"

def desenharTextoCentralizado(tela, fonte, texto, cor, centro):
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, imagem.get_rect(center=centro))

def desenharEixos(tela, fontes, totais):
    maxTotal = max(totais)
    passo = max(1, math.ceil(maxTotal / 8))
    topoEscala = max(passo, math.ceil(maxTotal / passo) * passo)
    alturaUtil = graficoBase - graficoTopo
    for valor in range(0, topoEscala + 1, passo):
        y = graficoBase - valor / topoEscala * alturaUtil
        if valor > 0:
            pygame.draw.line(tela, corGrade, (graficoEsq, y), (graficoDir, y))
        pygame.draw.line(tela, corEixo, (graficoEsq - 6, y), (graficoEsq, y), 2)
        rotulo = fontes["pequena"].render(str(valor), True, corTextoSuave)
        tela.blit(rotulo, rotulo.get_rect(midright=(graficoEsq - 10, y)))
    pygame.draw.line(tela, corEixo, (graficoEsq, graficoBase), (graficoDir + 20, graficoBase), 2)
    pygame.draw.polygon(tela, corEixo, [(graficoDir + 28, graficoBase), (graficoDir + 18, graficoBase - 5), (graficoDir + 18, graficoBase + 5)])
    pygame.draw.line(tela, corEixo, (graficoEsq, graficoBase), (graficoEsq, graficoTopo - 25), 2)
    pygame.draw.polygon(tela, corEixo, [(graficoEsq, graficoTopo - 33), (graficoEsq - 5, graficoTopo - 23), (graficoEsq + 5, graficoTopo - 23)])
    tituloY = pygame.transform.rotate(fontes["pequena"].render("Frequência", True, corTexto), 90)
    tela.blit(tituloY, tituloY.get_rect(center=(28, (graficoTopo + graficoBase) / 2)))
    desenharTextoCentralizado(tela, fontes["pequena"], "Faixas de valores", corTexto, ((graficoEsq + graficoDir) / 2, graficoBase + 45))
    return topoEscala

def desenharHistograma(tela, fontes, hist):
    numCat = hist["numCat"]
    totais = hist["totais"]
    topoEscala = desenharEixos(tela, fontes, totais)
    larguraBarra = (graficoDir - graficoEsq) / numCat
    for i in range(numCat):
        x = graficoEsq + i * larguraBarra
        altura = totais[i] / topoEscala * (graficoBase - graficoTopo)
        if altura > 0:
            retangulo = pygame.Rect(round(x) + 2, round(graficoBase - altura), round(larguraBarra) - 4, round(altura))
            pygame.draw.rect(tela, hist["cores"][i], retangulo)
            corBorda = tuple(c // 2 for c in hist["cores"][i])
            pygame.draw.rect(tela, corBorda, retangulo, 2)
            desenharTextoCentralizado(tela, fontes["pequena"], str(totais[i]), corTexto, (x + larguraBarra / 2, graficoBase - altura - 12))
    if hist["limites"] is None:
        desenharTextoCentralizado(tela, fontes["media"], "Sem dados ainda: digite números acima", corTextoSuave, ((graficoEsq + graficoDir) / 2, (graficoTopo + graficoBase) / 2))
        return
    numMin, numMax = hist["limites"]
    tamCat = (numMax - numMin) / numCat
    for i in range(numCat + 1):
        x = graficoEsq + i * larguraBarra
        pygame.draw.line(tela, corEixo, (x, graficoBase), (x, graficoBase + 6), 2)
        desenharTextoCentralizado(tela, fontes["pequena"], formatarNumero(numMin + i * tamCat), corTextoSuave, (x, graficoBase + 18))

def desenharEntrada(tela, fontes, estado):
    caixa = pygame.Rect(graficoEsq, 88, 200, 34)
    pygame.draw.rect(tela, (36, 39, 50), caixa, border_radius=6)
    pygame.draw.rect(tela, corEixo, caixa, 2, border_radius=6)
    texto = fontes["media"].render(estado["textoDigitado"], True, corTexto)
    tela.blit(texto, texto.get_rect(midleft=(caixa.x + 10, caixa.centery)))
    if pygame.time.get_ticks() // 500 % 2 == 0:
        xCursor = caixa.x + 12 + texto.get_width()
        pygame.draw.line(tela, corTexto, (xCursor, caixa.y + 7), (xCursor, caixa.bottom - 7), 2)
    if estado["erro"]:
        mensagem = fontes["pequena"].render(estado["erro"], True, corErro)
    else:
        numsUsuario = estado["numsUsuario"]
        ultimos = ", ".join(formatarNumero(n) for n in numsUsuario[-12:])
        reticencias = "..., " if len(numsUsuario) > 12 else ""
        mensagem = fontes["pequena"].render(f"{len(numsUsuario)} números: {reticencias}{ultimos}", True, corTextoSuave)
    tela.blit(mensagem, mensagem.get_rect(midleft=(caixa.right + 16, caixa.centery)))

def botoesMenu():
    raio = 20
    y = alturaTela - 35
    return pygame.Rect(graficoEsq - raio, y - raio, raio * 2, raio * 2), pygame.Rect(graficoDir - raio, y - raio, raio * 2, raio * 2)

def desenharMenu(tela, fontes, estado):
    botaoEsq, botaoDir = botoesMenu()
    mouse = pygame.mouse.get_pos()
    for botao, sentido in ((botaoEsq, -1), (botaoDir, 1)):
        cor = (70, 76, 95) if botao.collidepoint(mouse) else (48, 52, 66)
        pygame.draw.circle(tela, cor, botao.center, botao.width // 2)
        cx, cy = botao.center
        pygame.draw.polygon(tela, corTexto, [(cx + 7 * sentido, cy), (cx - 5 * sentido, cy - 8), (cx - 5 * sentido, cy + 8)])
    total = len(estado["histogramas"])
    for i in range(total):
        x = larguraTela / 2 + (i - (total - 1) / 2) * 24
        if i == estado["atual"]:
            pygame.draw.circle(tela, corTexto, (x, alturaTela - 35), 7)
        else:
            pygame.draw.circle(tela, corTextoSuave, (x, alturaTela - 35), 5, 2)

def desenharTela(tela, fontes, estado):
    tela.fill(corFundo)
    hist = estado["histogramas"][estado["atual"]]
    tela.blit(fontes["titulo"].render(hist["titulo"], True, corTexto), (graficoEsq - 60, 18))
    tela.blit(fontes["pequena"].render(hist["descricao"], True, corTextoSuave), (graficoEsq - 60, 58))
    if estado["atual"] == 2:
        desenharEntrada(tela, fontes, estado)
    desenharHistograma(tela, fontes, hist)
    desenharMenu(tela, fontes, estado)

def mudarHistograma(estado, sentido):
    estado["atual"] = (estado["atual"] + sentido) % len(estado["histogramas"])

def adicionarNumero(estado):
    texto = estado["textoDigitado"].replace(",", ".")
    try:
        valor = float(texto)
    except ValueError:
        estado["erro"] = f'"{estado["textoDigitado"]}" não é um número válido'
        return
    estado["numsUsuario"].append(int(valor) if valor.is_integer() else valor)
    estado["textoDigitado"] = ""
    estado["erro"] = ""
    atualizarHistograma3(estado)

def atualizarHistograma3(estado):
    hist = estado["histogramas"][2]
    hist["totais"], hist["limites"] = contabilizaTotais(estado["numsUsuario"], hist["numCat"])

def tratarEvento(evento, estado):
    if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
        botaoEsq, botaoDir = botoesMenu()
        if botaoEsq.collidepoint(evento.pos):
            mudarHistograma(estado, -1)
        elif botaoDir.collidepoint(evento.pos):
            mudarHistograma(estado, 1)
    if evento.type != KEYDOWN:
        return
    if evento.key == pygame.K_LEFT:
        mudarHistograma(estado, -1)
    elif evento.key == pygame.K_RIGHT:
        mudarHistograma(estado, 1)
    elif estado["atual"] == 2:
        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            adicionarNumero(estado)
        elif evento.key == pygame.K_BACKSPACE:
            estado["textoDigitado"] = estado["textoDigitado"][:-1]
            estado["erro"] = ""
        elif evento.key == pygame.K_DELETE:
            estado["numsUsuario"].clear()
            estado["erro"] = ""
            atualizarHistograma3(estado)
        elif evento.unicode and evento.unicode in "0123456789-.," and len(estado["textoDigitado"]) < 10:
            estado["textoDigitado"] += evento.unicode
            estado["erro"] = ""
    elif evento.key == pygame.K_r:
        if estado["atual"] == 0:
            estado["histogramas"][0] = criarHistograma1()
        else:
            estado["histogramas"][1] = criarHistograma2()
#############################################################################################
def main():
    pygame.init()
    tela = pygame.display.set_mode((larguraTela, alturaTela))
    pygame.display.set_caption("Atividade 10 - Histogramas")
    relogio = pygame.time.Clock()
    fontes = {
        "titulo": pygame.font.SysFont("segoeui", 30, bold=True),
        "media": pygame.font.SysFont("segoeui", 22),
        "pequena": pygame.font.SysFont("segoeui", 16),
    }
    estado = {
        "histogramas": [criarHistograma1(), criarHistograma2(), criarHistograma3()],
        "atual": 0,
        "numsUsuario": [],
        "textoDigitado": "",
        "erro": "",
    }
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            tratarEvento(evento, estado)
        desenharTela(tela, fontes, estado)
        pygame.display.update()
        relogio.tick(60)
#############################################################################################
if __name__ == "__main__":
    main()
