import math
import random
import pygame

## Definições de funções de validação
def valida_email(email):
    return email[-8:] == "@puc.com"

def possui_maiuscula(senha):
    for carac in senha:
        if 'A' <= carac <= 'Z':
            return True
    return False

def possui_minuscula(senha):
    for carac in senha:
        if 'a' <= carac <= 'z':
            return True
    return False

def possui_numero(senha):
    for carac in senha:
        if carac.isnumeric():
            return True
    return False

def valida_senha(senha):
    if len(senha) < 8:
        return False
    if not possui_maiuscula(senha):
        return False
    if not possui_minuscula(senha):
        return False
    if not possui_numero(senha):
        return False
    return True

## Criptografia de César (caracteres válidos: '0' até 'z', faixa de 75 símbolos)
FAIXA_CESAR = ord('z') - ord('0') + 1
DESLOCAMENTO_CESAR = 3

def criptografa(texto, deslocamento=DESLOCAMENTO_CESAR):
    senha_cripto = ""
    for carac in texto:
        if '0' <= carac <= 'z':
            posicao = ord(carac) - ord('0')
            nova_posicao = (posicao + deslocamento) % FAIXA_CESAR
            senha_cripto += chr(nova_posicao + ord('0'))
        else:
            senha_cripto += carac
    return senha_cripto

def descriptografa(texto, deslocamento=DESLOCAMENTO_CESAR):
    senha_original = ""
    for carac in texto:
        if '0' <= carac <= 'z':
            posicao = ord(carac) - ord('0')
            nova_posicao = (posicao - deslocamento) % FAIXA_CESAR
            senha_original += chr(nova_posicao + ord('0'))
        else:
            senha_original += carac
    return senha_original

## Código que testa as funções de criptografia
if __name__ == "__main__":
    senha_teste = "Senha123"
    cripto_teste = criptografa(senha_teste)
    descripto_teste = descriptografa(cripto_teste)
    print(f"Senha original:        {senha_teste}")
    print(f"Senha criptografada:   {cripto_teste}")
    print(f"Senha decriptografada: {descripto_teste}")
    assert descripto_teste == senha_teste

#################################################################################################
## Paleta visual (moderna/minimalista) compartilhada pelas telas de login, resultado e menu
#################################################################################################
corFundo = "#121417"
corCartao = "#1C1F24"
corBorda = "#2B2F36"
corAccent = "#6C8EF5"
corAccentHover = "#7FA0FF"
corTexto = "#F2F3F5"
corTextoMuted = "#8A93A1"
corErro = "#F87171"
corSucesso = "#4ADE80"


def caminhoDoArquivo(nomeArquivo):
    posicao = max(__file__.rfind("\\"), __file__.rfind("/"))
    pasta = __file__[:posicao + 1] if posicao != -1 else ""
    return pasta + nomeArquivo


def desenharCartao(tela, rect):
    pygame.draw.rect(tela, corCartao, rect, border_radius=18)
    pygame.draw.rect(tela, corBorda, rect, width=1, border_radius=18)


def desenharCampoSubline(tela, fontes, rect, rotuloTexto, valor, focado, mascarar=False):
    rotulo = fontes["pequena"].render(rotuloTexto, True, corTextoMuted)
    tela.blit(rotulo, (rect.x, rect.y - 24))
    textoExibido = "•" * len(valor) if mascarar else valor
    renderValor = fontes["corpo"].render(textoExibido or " ", True, corTexto)
    tela.blit(renderValor, renderValor.get_rect(bottomleft=(rect.x, rect.bottom - 10)))
    corLinha = corAccent if focado else corBorda
    espessura = 2 if focado else 1
    pygame.draw.line(tela, corLinha, (rect.x, rect.bottom), (rect.right, rect.bottom), espessura)


def desenharBotaoPrimario(tela, fontes, rect, texto):
    posicaoMouse = pygame.mouse.get_pos()
    cor = corAccentHover if rect.collidepoint(posicaoMouse) else corAccent
    pygame.draw.rect(tela, cor, rect, border_radius=rect.height // 2)
    rotulo = fontes["corpo"].render(texto, True, "#0E1012")
    tela.blit(rotulo, rotulo.get_rect(center=rect.center))


def desenharItemMenu(tela, fontes, rect, titulo, descricao):
    posicaoMouse = pygame.mouse.get_pos()
    emHover = rect.collidepoint(posicaoMouse)
    pygame.draw.rect(tela, corBorda if emHover else corCartao, rect, border_radius=14)
    pygame.draw.rect(tela, corAccent if emHover else corBorda, rect, width=1, border_radius=14)
    renderTitulo = fontes["corpo"].render(titulo, True, corTexto)
    tela.blit(renderTitulo, (rect.x + 20, rect.y + 14))
    renderDescricao = fontes["pequena"].render(descricao, True, corTextoMuted)
    tela.blit(renderDescricao, (rect.x + 20, rect.y + 42))
    seta = fontes["corpo"].render("›", True, corAccent if emHover else corTextoMuted)
    tela.blit(seta, seta.get_rect(midright=(rect.right - 20, rect.centery)))


def telaLogin(tela, relogio, fontes, largura, altura):
    pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Login")
    cartao = pygame.Rect(28, 70, largura - 56, altura - 140)
    campoEmail = pygame.Rect(cartao.x + 32, 190, cartao.width - 64, 36)
    campoSenha = pygame.Rect(cartao.x + 32, 290, cartao.width - 64, 36)
    botaoEntrar = pygame.Rect(cartao.x + 32, cartao.bottom - 76, cartao.width - 64, 48)

    email, senha = "", ""
    campoAtivo = "email"
    mensagemErro = ""

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair", email, senha
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if campoEmail.collidepoint(evento.pos):
                    campoAtivo = "email"
                elif campoSenha.collidepoint(evento.pos):
                    campoAtivo = "senha"
                elif botaoEntrar.collidepoint(evento.pos):
                    if valida_email(email) and valida_senha(senha):
                        return "resultado", email, senha
                    mensagemErro = "E-mail inválido: deve terminar com @puc.com" if not valida_email(email) else "Senha fraca: use 8+ caracteres com maiúscula, minúscula e número."
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    campoAtivo = "senha" if campoAtivo == "email" else "email"
                elif evento.key == pygame.K_RETURN:
                    if valida_email(email) and valida_senha(senha):
                        return "resultado", email, senha
                    mensagemErro = "E-mail inválido: deve terminar com @puc.com" if not valida_email(email) else "Senha fraca: use 8+ caracteres com maiúscula, minúscula e número."
                elif evento.key == pygame.K_BACKSPACE:
                    if campoAtivo == "email":
                        email = email[:-1]
                    else:
                        senha = senha[:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    if campoAtivo == "email":
                        email += evento.unicode
                    else:
                        senha += evento.unicode

        tela.fill(corFundo)
        desenharCartao(tela, cartao)
        titulo = fontes["titulo"].render("Entrar", True, corTexto)
        tela.blit(titulo, (cartao.x + 32, cartao.y + 28))
        subtitulo = fontes["pequena"].render("Use seu e-mail @puc.com", True, corTextoMuted)
        tela.blit(subtitulo, (cartao.x + 32, cartao.y + 68))

        desenharCampoSubline(tela, fontes, campoEmail, "E-MAIL", email, campoAtivo == "email")
        desenharCampoSubline(tela, fontes, campoSenha, "SENHA", senha, campoAtivo == "senha", mascarar=True)
        desenharBotaoPrimario(tela, fontes, botaoEntrar, "Entrar")

        if mensagemErro:
            render = fontes["pequena"].render(mensagemErro, True, corErro)
            tela.blit(render, (cartao.x + 32, botaoEntrar.y - 30))

        pygame.display.update()
        relogio.tick(60)


def telaResultado(tela, relogio, fontes, largura, altura, senha):
    cartao = pygame.Rect(28, 70, largura - 56, altura - 140)
    botaoContinuar = pygame.Rect(cartao.x + 32, cartao.bottom - 76, cartao.width - 64, 48)
    cripto = criptografa(senha)
    descripto = descriptografa(cripto)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return "menu"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botaoContinuar.collidepoint(evento.pos):
                    return "menu"

        tela.fill(corFundo)
        desenharCartao(tela, cartao)
        titulo = fontes["titulo"].render("Login confirmado", True, corSucesso)
        tela.blit(titulo, (cartao.x + 32, cartao.y + 28))

        rotuloCripto = fontes["pequena"].render("SENHA CRIPTOGRAFADA (CÉSAR +3)", True, corTextoMuted)
        tela.blit(rotuloCripto, (cartao.x + 32, cartao.y + 110))
        valorCripto = fontes["corpo"].render(cripto, True, corTexto)
        tela.blit(valorCripto, (cartao.x + 32, cartao.y + 134))

        rotuloDescripto = fontes["pequena"].render("SENHA DECRIPTOGRAFADA", True, corTextoMuted)
        tela.blit(rotuloDescripto, (cartao.x + 32, cartao.y + 190))
        valorDescripto = fontes["corpo"].render(descripto, True, corTexto)
        tela.blit(valorDescripto, (cartao.x + 32, cartao.y + 214))

        desenharBotaoPrimario(tela, fontes, botaoContinuar, "Continuar")
        pygame.display.update()
        relogio.tick(60)


def telaMenu(tela, relogio, fontes, largura, altura):
    pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Menu")
    cartao = pygame.Rect(28, 70, largura - 56, altura - 140)
    itens = [
        ("casinha", "Casinha", "Dia e noite, sol e nuvens interativos"),
        ("ppt", "Pedra, Papel e Tesoura", "Partida rápida contra o computador"),
        ("adivinhacao", "Jogo de Adivinhação", "Você ou o computador tenta adivinhar"),
    ]
    botoes = [
        (pygame.Rect(cartao.x + 24, cartao.y + 96 + indice * 90, cartao.width - 48, 72), chave, titulo, descricao)
        for indice, (chave, titulo, descricao) in enumerate(itens)
    ]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for rect, chave, _, _ in botoes:
                    if rect.collidepoint(evento.pos):
                        return chave

        tela.fill(corFundo)
        desenharCartao(tela, cartao)
        titulo = fontes["titulo"].render("Escolha um projeto", True, corTexto)
        tela.blit(titulo, (cartao.x + 32, cartao.y + 28))

        for rect, _, tituloItem, descricaoItem in botoes:
            desenharItemMenu(tela, fontes, rect, tituloItem, descricaoItem)

        pygame.display.update()
        relogio.tick(60)


#################################################################################################
## Casinha - Dia e Noite
#################################################################################################
def criarSom(frequencia, duracao=0.35, volume=0.4, taxaAmostragem=44100):
    totalAmostras = int(taxaAmostragem * duracao)
    amplitude = int(32767 * volume)
    tempoDeFade = 0.05
    bytesDoSom = bytearray()
    for indice in range(totalAmostras):
        tempo = indice / taxaAmostragem
        volumeNoInstante = min(1.0, (duracao - tempo) / tempoDeFade) if tempo > duracao - tempoDeFade else min(1.0, tempo / tempoDeFade)
        amostra = int(amplitude * volumeNoInstante * math.sin(2 * math.pi * frequencia * tempo)) & 0xFFFF
        byteBaixo, byteAlto = amostra & 0xFF, (amostra >> 8) & 0xFF
        bytesDoSom.append(byteBaixo)
        bytesDoSom.append(byteAlto)
        bytesDoSom.append(byteBaixo)
        bytesDoSom.append(byteAlto)
    return pygame.mixer.Sound(buffer=bytes(bytesDoSom))


def misturarCores(corInicial, corFinal, progresso):
    return tuple(int(corInicial[i] + (corFinal[i] - corInicial[i]) * progresso) for i in range(3))


def limitarEntre(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def rodarCasinha():
    pygame.mixer.init(frequency=44100, size=-16, channels=2)
    largura, altura = 937, 701
    screen = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Casinha - Dia e Noite")
    clock = pygame.time.Clock()
    grama = "#1FA406"
    nuvem = "#FFFFFF"
    telhado = "#F2883B"
    parede = "#6E6E6E"
    porta = "#7A4A1E"
    janela = "#0D1664"
    tronco = "#7A4A1E"
    copa = "#1E9E1E"
    preto = "#000000"
    corDoSol = "#FFF251"

    fonte = pygame.font.Font(caminhoDoArquivo("batmfa__.ttf"), 60)
    ronaldo = pygame.image.load(caminhoDoArquivo("Ronaldo.png")).convert_alpha()
    ronaldo = pygame.transform.scale(ronaldo, (150, 108))

    somDaManha = criarSom(660)
    somDaTarde = criarSom(440)
    somDaNoite = criarSom(220, duracao=0.5, volume=0.3)

    alturaDoChao = 590
    larguraDaNuvem = 255
    velocidadeDaNuvem = 2.0
    nuvemX = 655.0
    nuvemY = 95
    raioDaNuvem = 45
    limiteEsquerdoNuvem = raioDaNuvem
    limiteDireitoNuvem = largura - (larguraDaNuvem - raioDaNuvem)

    solX, solY = 130.0, 105.0
    raioDoSol = 50
    alcanceDosRaios = 95
    velocidadeSolTeclado = 260
    limiteEsquerdoSol = alcanceDosRaios
    limiteDireitoSol = largura - alcanceDosRaios
    limiteSuperiorSol = alcanceDosRaios
    limiteInferiorSol = alturaDoChao - alcanceDosRaios

    corTarde = (135, 206, 250)
    corManha = (255, 179, 126)
    corNoite = (11, 19, 65)

    def calcularCeuEEstagio(alturaDoSol):
        progresso = limitarEntre((alturaDoSol - limiteSuperiorSol) / (limiteInferiorSol - limiteSuperiorSol), 0.0, 1.0)
        if progresso < 0.5:
            cor = misturarCores(corTarde, corManha, progresso / 0.5)
            estagio = "tarde" if progresso < 0.25 else "manha"
        else:
            cor = misturarCores(corManha, corNoite, (progresso - 0.5) / 0.5)
            estagio = "manha" if progresso < 0.75 else "noite"
        return cor, estagio

    sonsPorEstagio = {"manha": somDaManha, "tarde": somDaTarde, "noite": somDaNoite}

    rodando = True
    retorno = "sair"
    while rodando:
        deltaTempo = clock.tick(60) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "sair"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
                retorno = "menu"
            if evento.type == pygame.MOUSEMOTION:
                solX, solY = evento.pos
            if evento.type == pygame.MOUSEBUTTONDOWN:
                _, estagioAtual = calcularCeuEEstagio(solY)
                sonsPorEstagio[estagioAtual].play()
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            solX -= velocidadeSolTeclado * deltaTempo
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            solX += velocidadeSolTeclado * deltaTempo
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            solY -= velocidadeSolTeclado * deltaTempo
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            solY += velocidadeSolTeclado * deltaTempo
        solX = limitarEntre(solX, limiteEsquerdoSol, limiteDireitoSol)
        solY = limitarEntre(solY, limiteSuperiorSol, limiteInferiorSol)
        nuvemX += velocidadeDaNuvem
        if nuvemX <= limiteEsquerdoNuvem:
            nuvemX = limiteEsquerdoNuvem
            velocidadeDaNuvem = abs(velocidadeDaNuvem)
        elif nuvemX >= limiteDireitoNuvem:
            nuvemX = limiteDireitoNuvem
            velocidadeDaNuvem = -abs(velocidadeDaNuvem)
        corDoCeu, estagioDoDia = calcularCeuEEstagio(solY)
        screen.fill(corDoCeu)
        pygame.draw.rect(screen, grama, (0, alturaDoChao, largura, altura - alturaDoChao))
        centroDoSol = (solX, solY)
        for angulo in range(0, 360, 45):
            rad = math.radians(angulo)
            x1 = centroDoSol[0] + math.cos(rad) * 55
            y1 = centroDoSol[1] + math.sin(rad) * 55
            x2 = centroDoSol[0] + math.cos(rad) * 95
            y2 = centroDoSol[1] + math.sin(rad) * 95
            pygame.draw.line(screen, corDoSol, (x1, y1), (x2, y2), 5)
        pygame.draw.circle(screen, corDoSol, centroDoSol, raioDoSol)
        pygame.draw.circle(screen, nuvem, (nuvemX, nuvemY), raioDaNuvem)
        pygame.draw.circle(screen, nuvem, (nuvemX + 55, nuvemY), raioDaNuvem)
        pygame.draw.circle(screen, nuvem, (nuvemX + 110, nuvemY), raioDaNuvem)
        pygame.draw.circle(screen, nuvem, (nuvemX + 165, nuvemY), raioDaNuvem)
        pygame.draw.rect(screen, tronco, (700, 475, 30, 115))
        pygame.draw.circle(screen, copa, (715, 375), 100)
        pygame.draw.rect(screen, parede, (240, 350, 230, 240))
        pygame.draw.polygon(screen, telhado, [(240, 350), (470, 350), (355, 180)])
        pygame.draw.rect(screen, janela, (260, 440, 60, 80))
        pygame.draw.rect(screen, porta, (355, 420, 65, 170))
        pygame.draw.circle(screen, preto, (370, 505), 4)
        screen.blit(ronaldo, (largura - 170, 600))
        texto = fonte.render("SIUUUUUUU", True, preto)
        screen.blit(texto, (largura // 2 - texto.get_width() // 2, 610))
        pygame.display.update()
    return retorno


#################################################################################################
## Pedra, Papel e Tesoura
#################################################################################################
def carregarImagem(nomeArquivo, tamanhoMaximo):
    imagem = pygame.image.load(caminhoDoArquivo(nomeArquivo)).convert()
    larguraOriginal, alturaOriginal = imagem.get_size()
    escala = min(tamanhoMaximo / larguraOriginal, tamanhoMaximo / alturaOriginal)
    novoTamanho = (int(larguraOriginal * escala), int(alturaOriginal * escala))
    return pygame.transform.smoothscale(imagem, novoTamanho)


def decidirVencedor(escolhaJogador, escolhaComputador):
    if escolhaJogador == escolhaComputador:
        return "empate"
    venceDe = {"pedra": "tesoura", "tesoura": "papel", "papel": "pedra"}
    if venceDe[escolhaJogador] == escolhaComputador:
        return "jogador"
    return "computador"


def jogarRodada(estado, itens, escolhaJogador):
    escolhaComputador = random.choice(itens)
    resultado = decidirVencedor(escolhaJogador, escolhaComputador)
    estado["escolhaJogador"] = escolhaJogador
    estado["escolhaComputador"] = escolhaComputador
    estado["resultado"] = resultado
    estado["placar"][resultado] += 1


def reiniciarPpt(estado):
    estado["placar"] = {"jogador": 0, "computador": 0, "empate": 0}
    estado["escolhaJogador"] = None
    estado["escolhaComputador"] = None
    estado["resultado"] = None


def rodarPedraPapelTesoura():
    largura, altura = 480, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Pedra, Papel e Tesoura")
    relogio = pygame.time.Clock()
    fonteTitulo = pygame.font.Font(None, 60)
    fonteTexto = pygame.font.Font(None, 36)

    itens = ["pedra", "papel", "tesoura"]
    arquivosDasImagens = {"pedra": "pedra.jpg", "papel": "papel.jpg", "tesoura": "tesoura.jpg"}
    mensagensDoResultado = {
        "jogador": "Você venceu!",
        "computador": "O computador venceu!",
        "empate": "Empate!",
    }
    imagensDosItens = {item: carregarImagem(arquivo, 130) for item, arquivo in arquivosDasImagens.items()}
    imagensGrandes = {item: carregarImagem(arquivo, 170) for item, arquivo in arquivosDasImagens.items()}
    botoesEscolha = [
        (pygame.Rect(40 + indice * 140, 380, 120, 150), item)
        for indice, item in enumerate(itens)
    ]
    botaoReiniciar = pygame.Rect(largura // 2 - 100, 545, 200, 45)
    estado = {
        "placar": {"jogador": 0, "computador": 0, "empate": 0},
        "escolhaJogador": None,
        "escolhaComputador": None,
        "resultado": None,
    }

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
        rotuloVs = fonteTitulo.render("X", True, corAccent)
        tela.blit(rotuloVs, rotuloVs.get_rect(center=(largura // 2, 200)))
        mensagem = fonteTexto.render(mensagensDoResultado[estado["resultado"]], True, corAccent)
        tela.blit(mensagem, mensagem.get_rect(center=(largura // 2, 335)))

    def desenharBotoesEscolha(botoes):
        posicaoMouse = pygame.mouse.get_pos()
        for rect, item in botoes:
            cor = corAccent if rect.collidepoint(posicaoMouse) else corCartao
            pygame.draw.rect(tela, cor, rect, border_radius=12)
            imagem = imagensDosItens[item]
            tela.blit(imagem, imagem.get_rect(center=rect.center))

    def desenharBotaoReiniciar(rect):
        pygame.draw.rect(tela, corErro, rect, border_radius=12)
        rotulo = fonteTexto.render("Reiniciar (R)", True, corTexto)
        tela.blit(rotulo, rotulo.get_rect(center=rect.center))

    def desenharTela(estado):
        tela.fill(corFundo)
        desenharPlacar(estado)
        desenharEscolhas(estado)
        desenharBotoesEscolha(botoesEscolha)
        desenharBotaoReiniciar(botaoReiniciar)
        pygame.display.update()

    teclasDeEscolha = {pygame.K_1: "pedra", pygame.K_2: "papel", pygame.K_3: "tesoura"}
    rodando = True
    retorno = "sair"
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "sair"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    retorno = "menu"
                elif evento.key in teclasDeEscolha:
                    jogarRodada(estado, itens, teclasDeEscolha[evento.key])
                elif evento.key == pygame.K_r:
                    reiniciarPpt(estado)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botaoReiniciar.collidepoint(evento.pos):
                    reiniciarPpt(estado)
                for rect, item in botoesEscolha:
                    if rect.collidepoint(evento.pos):
                        jogarRodada(estado, itens, item)
        desenharTela(estado)
        relogio.tick(60)
    return retorno


#################################################################################################
## Jogo de Adivinhação
#################################################################################################
MINIMO_ADIVINHACAO = 1
MAXIMO_ADIVINHACAO = 1023


def comparar(numeroGerado, numeroFornecido):
    if numeroGerado < numeroFornecido:
        return -1
    if numeroGerado > numeroFornecido:
        return 1
    return 0


def iniciarUsuarioAdivinha(estado):
    estado.update({
        "papel": "usuario",
        "segredo": random.randint(MINIMO_ADIVINHACAO, MAXIMO_ADIVINHACAO),
        "digitado": "",
        "palpite": None,
        "minimo": MINIMO_ADIVINHACAO,
        "maximo": MAXIMO_ADIVINHACAO,
        "tentativas": 0,
        "feedback": None,
        "vencedor": False,
        "mensagem": f"Tente adivinhar um número entre {MINIMO_ADIVINHACAO} e {MAXIMO_ADIVINHACAO}.",
    })


def iniciarComputadorAdivinha(estado):
    estado.update({
        "papel": "computador",
        "segredo": None,
        "digitado": "",
        "palpite": (MINIMO_ADIVINHACAO + MAXIMO_ADIVINHACAO) // 2,
        "minimo": MINIMO_ADIVINHACAO,
        "maximo": MAXIMO_ADIVINHACAO,
        "tentativas": 1,
        "feedback": None,
        "vencedor": False,
        "mensagem": f"Pense num número entre {MINIMO_ADIVINHACAO} e {MAXIMO_ADIVINHACAO}. O computador vai tentar adivinhar.",
    })


def tentarNumero(estado):
    if estado["digitado"] == "":
        return
    palpite = int(estado["digitado"])
    estado["digitado"] = ""
    if palpite < MINIMO_ADIVINHACAO or palpite > MAXIMO_ADIVINHACAO:
        estado["mensagem"] = f"Digite um número entre {MINIMO_ADIVINHACAO} e {MAXIMO_ADIVINHACAO}."
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


def rodarAdivinhacao():
    largura, altura = 480, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jogo de Adivinhação")
    relogio = pygame.time.Clock()
    fonteTitulo = pygame.font.Font(None, 56)
    fonteGrande = pygame.font.Font(None, 90)
    fonteTexto = pygame.font.Font(None, 36)
    fonteMenor = pygame.font.Font(None, 28)

    corMenor = "#2EC4B6"
    corMaior = corErro
    corAcerto = corAccent

    estado = {
        "papel": None,
        "segredo": None,
        "digitado": "",
        "palpite": None,
        "minimo": MINIMO_ADIVINHACAO,
        "maximo": MAXIMO_ADIVINHACAO,
        "tentativas": 0,
        "feedback": None,
        "vencedor": False,
        "mensagem": "",
    }

    botaoMenuUsuario = pygame.Rect(largura // 2 - 130, 280, 260, 55)
    botaoMenuComputador = pygame.Rect(largura // 2 - 130, 355, 260, 55)
    botaoMenor = pygame.Rect(20, 470, 140, 50)
    botaoAcerto = pygame.Rect(170, 470, 140, 50)
    botaoMaior = pygame.Rect(320, 470, 140, 50)
    botaoTrocarPapel = pygame.Rect(20, 540, 200, 45)
    botaoReiniciar = pygame.Rect(260, 540, 200, 45)

    def desenharBotao(rect, texto, cor=corCartao, fonte=fonteTexto):
        posicaoMouse = pygame.mouse.get_pos()
        corFinal = corAccent if rect.collidepoint(posicaoMouse) and cor == corCartao else cor
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
        titulo = "Você adivinha" if estado["papel"] == "usuario" else "Computador adivinha"
        tituloRender = fonteTitulo.render(titulo, True, corTexto)
        tela.blit(tituloRender, tituloRender.get_rect(center=(largura // 2, 40)))

        mensagemRender = fonteMenor.render(estado["mensagem"], True, corAccent)
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
        desenharBotao(botaoReiniciar, "Reiniciar", corErro)

    def desenharTela(estado):
        tela.fill(corFundo)
        if estado["papel"] is None:
            desenharMenu()
        else:
            desenharJogo(estado)
        pygame.display.update()

    rodando = True
    retorno = "sair"
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "sair"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    retorno = "menu"
                elif estado["papel"] is not None:
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
    return retorno


#################################################################################################
## Orquestração principal
#################################################################################################
def main():
    pygame.init()
    largura, altura = 440, 620
    tela = pygame.display.set_mode((largura, altura))
    relogio = pygame.time.Clock()
    fontes = {
        "titulo": pygame.font.SysFont("segoeui,arial", 30, bold=True),
        "corpo": pygame.font.SysFont("segoeui,arial", 20),
        "pequena": pygame.font.SysFont("segoeui,arial", 15),
    }

    estado = "login"
    senha = ""
    while estado != "sair":
        if estado == "login":
            estado, _, senha = telaLogin(tela, relogio, fontes, largura, altura)
        elif estado == "resultado":
            estado = telaResultado(tela, relogio, fontes, largura, altura, senha)
        elif estado == "menu":
            estado = telaMenu(tela, relogio, fontes, largura, altura)
        elif estado == "casinha":
            retorno = rodarCasinha()
            estado = "sair" if retorno == "sair" else "menu"
        elif estado == "ppt":
            retorno = rodarPedraPapelTesoura()
            estado = "sair" if retorno == "sair" else "menu"
        elif estado == "adivinhacao":
            retorno = rodarAdivinhacao()
            estado = "sair" if retorno == "sair" else "menu"
    pygame.quit()


if __name__ == "__main__":
    main()
