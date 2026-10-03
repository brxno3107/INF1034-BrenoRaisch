import random
import pygame
##################################################################################################
def caminhoDoArquivo(nomeArquivo):
    posicao = max(__file__.rfind("\\"), __file__.rfind("/"))
    pasta = __file__[:posicao + 1] if posicao != -1 else ""
    return pasta + nomeArquivo
###################################################################################################
pygame.init()
largura, altura = 480, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pedra, Papel e Tesoura")
relogio = pygame.time.Clock()
fonteTitulo = pygame.font.Font(None, 60)
fonteTexto = pygame.font.Font(None, 36)
fonteMenor = pygame.font.Font(None, 28)
corFundo = "#222831"
corTexto = "#EEEEEE"
corBotao = "#393E46"
corBotaoHover = "#00ADB5"
corBotaoReiniciar = "#E84855"
corDestaque = "#FF9F1C"

ITENS = ["pedra", "papel", "tesoura"]
arquivosDasImagens = {"pedra": "pedra.jpg", "papel": "papel.jpg", "tesoura": "tesoura.jpg"}
mensagensDoResultado = {
    "jogador": "Você venceu!",
    "computador": "O computador venceu!",
    "empate": "Empate!",
}
def carregarImagem(nomeArquivo, tamanhoMaximo):
    imagem = pygame.image.load(caminhoDoArquivo(nomeArquivo)).convert()
    larguraOriginal, alturaOriginal = imagem.get_size()
    escala = min(tamanhoMaximo / larguraOriginal, tamanhoMaximo / alturaOriginal)
    novoTamanho = (int(larguraOriginal * escala), int(alturaOriginal * escala))
    return pygame.transform.smoothscale(imagem, novoTamanho)
imagensDosItens = {item: carregarImagem(arquivo, 130) for item, arquivo in arquivosDasImagens.items()}
imagensGrandes = {item: carregarImagem(arquivo, 170) for item, arquivo in arquivosDasImagens.items()}
botoesEscolha = [
    (pygame.Rect(40 + indice * 140, 380, 120, 150), item)
    for indice, item in enumerate(ITENS)
]
####################################################################################################
botaoReiniciar = pygame.Rect(largura // 2 - 100, 545, 200, 45)
estado = {
    "placar": {"jogador": 0, "computador": 0, "empate": 0},
    "escolhaJogador": None,
    "escolhaComputador": None,
    "resultado": None,
}
#####################################################################################################
def decidirVencedor(escolhaJogador, escolhaComputador):
    if escolhaJogador == escolhaComputador:
        return "empate"
    venceDe = {"pedra": "tesoura", "tesoura": "papel", "papel": "pedra"}
    if venceDe[escolhaJogador] == escolhaComputador:
        return "jogador"
    return "computador"

def jogarRodada(estado, escolhaJogador):
    escolhaComputador = random.choice(ITENS)
    resultado = decidirVencedor(escolhaJogador, escolhaComputador)
    estado["escolhaJogador"] = escolhaJogador
    estado["escolhaComputador"] = escolhaComputador
    estado["resultado"] = resultado
    estado["placar"][resultado] += 1

def reiniciar(estado):
    estado["placar"] = {"jogador": 0, "computador": 0, "empate": 0}
    estado["escolhaJogador"] = None
    estado["escolhaComputador"] = None
    estado["resultado"] = None

def desenharPlacar(estado):
    placar = estado["placar"]
    textoPlacar = f"Você: {placar['jogador']}   Computador: {placar['computador']}   Empates: {placar['empate']}"
    render = fonteTexto.render(textoPlacar, True, corTexto)
    tela.blit(render, render.get_rect(center=(largura // 2, 40)))

def desenharEscolhas(estado):
    if estado["escolhaJogador"] is None:
        aviso = fonteTexto.render("Escolha pedra, papel ou tesoura", True, corTexto)
        tela.blit(aviso, aviso.get_rect(center=(largura // 2, 250)))
        return
    imagemJogador = imagensGrandes[estado["escolhaJogador"]]
    imagemComputador = imagensGrandes[estado["escolhaComputador"]]
    tela.blit(imagemJogador, imagemJogador.get_rect(center=(largura // 4, 200)))
    tela.blit(imagemComputador, imagemComputador.get_rect(center=(3 * largura // 4, 200)))
    rotuloVs = fonteTitulo.render("X", True, corDestaque)
    tela.blit(rotuloVs, rotuloVs.get_rect(center=(largura // 2, 200)))
    mensagem = fonteTexto.render(mensagensDoResultado[estado["resultado"]], True, corDestaque)
    tela.blit(mensagem, mensagem.get_rect(center=(largura // 2, 335)))

def desenharBotoesEscolha(botoes):
    posicaoMouse = pygame.mouse.get_pos()
    for rect, item in botoes:
        cor = corBotaoHover if rect.collidepoint(posicaoMouse) else corBotao
        pygame.draw.rect(tela, cor, rect, border_radius=12)
        imagem = imagensDosItens[item]
        tela.blit(imagem, imagem.get_rect(center=rect.center))

def desenharBotaoReiniciar(rect):
    pygame.draw.rect(tela, corBotaoReiniciar, rect, border_radius=12)
    rotulo = fonteTexto.render("Reiniciar (R)", True, corTexto)
    tela.blit(rotulo, rotulo.get_rect(center=rect.center))

def desenharTela(estado):
    tela.fill(corFundo)
    desenharPlacar(estado)
    desenharEscolhas(estado)
    desenharBotoesEscolha(botoesEscolha)
    desenharBotaoReiniciar(botaoReiniciar)
    pygame.display.update()
######################################################################################################
teclasDeEscolha = {pygame.K_1: "pedra", pygame.K_2: "papel", pygame.K_3: "tesoura"}
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key in teclasDeEscolha:
                jogarRodada(estado, teclasDeEscolha[evento.key])
            elif evento.key == pygame.K_r:
                reiniciar(estado)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if botaoReiniciar.collidepoint(evento.pos):
                reiniciar(estado)
            for rect, item in botoesEscolha:
                if rect.collidepoint(evento.pos):
                    jogarRodada(estado, item)
    desenharTela(estado)
    relogio.tick(60)
#####################################################################################################
pygame.quit()
