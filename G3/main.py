import pygame, sys, os
from pygame.locals import QUIT, KEYDOWN
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Vars de ambiente
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Ctrl+Z')
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("segoeui", 18)
cor_desktop = (0, 128, 128)
escala = 3
tile_size = 16 * escala
tileset = pygame.transform.scale_by(pygame.image.load("assets/tileset.png"), escala)
cursor_sheet = pygame.transform.scale_by(pygame.image.load("assets/cursor.png"), escala)

def corte(coluna):
    return (coluna * tile_size, 0, tile_size, tile_size)
cortes = {"[": corte(0), "=": corte(1), "]": corte(2), "#": corte(3), "_": corte(4), "P": corte(5), "e": corte(6)}
corte_botao, corte_botao_apertado, corte_porta_aberta = corte(7), corte(8), corte(10)
cortes_firewall = [corte(9), corte(11)]
solidos = "[=]#_"
mapa = []
limite_ctrlz = 3
with open("fases/fase_teste.txt", encoding="utf-8") as arquivo:
    for linha in arquivo:
        if linha.startswith("limite="):
            limite_ctrlz = int(linha.split("=")[1])
        elif linha.strip():
            mapa.append(linha.rstrip("\n"))
largura_mapa = len(mapa[0]) * tile_size
altura_mapa = len(mapa) * tile_size
colliders = []
botoes = []
portas = []
for i in range(len(mapa)):
    for j in range(len(mapa[i])):
        if mapa[i][j] in solidos:
            colliders.append(pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size))
        elif mapa[i][j] in "123":
            botoes.append((pygame.Rect(j * tile_size, i * tile_size + 10 * escala, tile_size, 6 * escala), int(mapa[i][j])))
        elif mapa[i][j] in "ABC":
            portas.append((pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size), "ABC".index(mapa[i][j]) + 1))
largura_jogador, altura_jogador = 12 * escala, 17 * escala
frames_esq = [cursor_sheet.subsurface((largura_jogador * f, 0, largura_jogador, altura_jogador)) for f in range(4)]
frames_dir = [pygame.transform.flip(img, True, False) for img in frames_esq]
ciclo_andar = [1, 0, 2, 0]
frame_pulo = 3
inicio_x, inicio_y = tile_size, 13 * tile_size - altura_jogador
pos_x, pos_y = inicio_x, inicio_y
vel_y = 0
no_chao = False
olhando_direita = True
velocidade = 0.3
gravidade = 0.0025
forca_pulo = 0.95
vel_max_queda = 1.2
i_ciclo = 0
anim_time = 0
mostrar_colliders = False
tempo_jogo = 0
tempo_rewind = 2000
gravacao = []
ultima_gravacao = []
flash_time = 0
fantasma = []
frames_copia = []
for img in frames_esq + frames_dir:
    copia = img.copy()
    copia.set_alpha(90)
    fantasma.append(copia)
    copia = img.copy()
    copia.fill((140, 190, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
    frames_copia.append(copia)
copia_gravacao = []
copia_inicio = 0
copia_i = 0
copia_terminou = False
usos_ctrlz = limite_ctrlz
aviso_time = 0
fonte_hud = pygame.font.SysFont("tahoma", 15)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w) and no_chao:
                vel_y = -forca_pulo
            if event.key == pygame.K_F1:
                mostrar_colliders = not mostrar_colliders
            if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL and gravacao and usos_ctrlz == 0:
                aviso_time = 1500
            elif event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL and gravacao:
                usos_ctrlz = usos_ctrlz - 1
                ultima_gravacao = gravacao[:]
                _, pos_x, pos_y, vel_y, olhando_direita, _ = gravacao[0]
                gravacao = [gravacao[0]]
                flash_time = 150
                copia_gravacao = ultima_gravacao
                copia_inicio = tempo_jogo
                copia_i = 0
                copia_terminou = False
                _, copia_x, copia_y, copia_vel_y, copia_dir, copia_frame = copia_gravacao[0]
    clock.tick(60)
    dt = min(clock.get_time(), 50)
    tempo_jogo = tempo_jogo + dt
    corpos = [pygame.Rect(pos_x, pos_y, largura_jogador, altura_jogador)]
    if copia_gravacao:
        corpos.append(pygame.Rect(copia_x, copia_y, largura_jogador, altura_jogador))
    canais_ativos = set()
    botoes_apertados = []
    for botao, canal in botoes:
        for corpo in corpos:
            if botao.colliderect(corpo):
                canais_ativos.add(canal)
                botoes_apertados.append(botao)
    solidos_frame = colliders[:]
    for porta, canal in portas:
        ocupada = False
        for corpo in corpos:
            if porta.colliderect(corpo):
                ocupada = True
        if canal not in canais_ativos and not ocupada:
            solidos_frame.append(porta)
    keys = pygame.key.get_pressed()
    andando = False
    old_pos_x = pos_x
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        pos_x = pos_x + velocidade * dt
        olhando_direita = True
        andando = True
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pos_x = pos_x - velocidade * dt
        olhando_direita = False
        andando = True
    pos_x = max(0, min(pos_x, largura_mapa - largura_jogador))
    collider_jogador = pygame.Rect(pos_x, pos_y, largura_jogador, altura_jogador)
    for collider in solidos_frame:
        if collider_jogador.colliderect(collider):
            if pos_x > old_pos_x:
                pos_x = collider.left - largura_jogador
            else:
                pos_x = collider.right
            collider_jogador.x = pos_x
    vel_y = min(vel_y + gravidade * dt, vel_max_queda)
    pos_y = pos_y + vel_y * dt
    collider_jogador = pygame.Rect(pos_x, pos_y, largura_jogador, altura_jogador)
    for collider in solidos_frame:
        if collider_jogador.colliderect(collider):
            if vel_y > 0:
                pos_y = collider.top - altura_jogador
            else:
                pos_y = collider.bottom
            vel_y = 0
            collider_jogador.y = pos_y
    pe = collider_jogador.move(0, 1)
    no_chao = False
    for collider in solidos_frame:
        if pe.colliderect(collider):
            no_chao = True
    if pos_y > altura_mapa:
        pos_x, pos_y, vel_y = inicio_x, inicio_y, 0
        gravacao = []
        copia_gravacao = []
        usos_ctrlz = limite_ctrlz
    if not no_chao:
        frame_atual = frame_pulo
    elif andando:
        anim_time = anim_time + dt
        if anim_time / 1000 > 0.1:
            i_ciclo = (i_ciclo + 1) % len(ciclo_andar)
            anim_time = 0
        frame_atual = ciclo_andar[i_ciclo]
    else:
        i_ciclo = 0
        frame_atual = 0
    gravacao.append((tempo_jogo, pos_x, pos_y, vel_y, olhando_direita, frame_atual))
    while gravacao[0][0] < tempo_jogo - tempo_rewind:
        gravacao.pop(0)
    if copia_gravacao and not copia_terminou:
        tempo_copia = copia_gravacao[0][0] + tempo_jogo - copia_inicio
        while copia_i < len(copia_gravacao) - 1 and copia_gravacao[copia_i + 1][0] <= tempo_copia:
            copia_i = copia_i + 1
        _, copia_x, copia_y, copia_vel_y, copia_dir, copia_frame = copia_gravacao[copia_i]
        if copia_i == len(copia_gravacao) - 1:
            copia_terminou = True
    elif copia_gravacao:
        copia_frame = 0
        copia_vel_y = min(copia_vel_y + gravidade * dt, vel_max_queda)
        copia_y = copia_y + copia_vel_y * dt
        collider_copia = pygame.Rect(copia_x, copia_y, largura_jogador, altura_jogador)
        for collider in solidos_frame:
            if collider_copia.colliderect(collider):
                if copia_vel_y > 0:
                    copia_y = collider.top - altura_jogador
                else:
                    copia_y = collider.bottom
                copia_vel_y = 0
                collider_copia.y = copia_y
        if copia_y > altura_mapa:
            copia_gravacao = []
    cam_x = pos_x + largura_jogador / 2 - screen.get_width() / 2
    cam_y = pos_y + altura_jogador / 2 - screen.get_height() / 2
    cam_x = max(0, min(cam_x, largura_mapa - screen.get_width()))
    cam_y = max(0, min(cam_y, altura_mapa - screen.get_height()))
    screen.fill(cor_desktop)
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            letra = mapa[i][j]
            if letra in cortes:
                screen.blit(tileset, (j * tile_size - cam_x, i * tile_size - cam_y), cortes[letra])
    for botao, canal in botoes:
        screen.blit(tileset, (botao.x - cam_x, botao.y - 10 * escala - cam_y), corte_botao_apertado if botao in botoes_apertados else corte_botao)
    for porta, canal in portas:
        frame_fogo = (int(tempo_jogo // 150) + porta.y // tile_size) % 2
        screen.blit(tileset, (porta.x - cam_x, porta.y - cam_y), cortes_firewall[frame_fogo] if porta in solidos_frame else corte_porta_aberta)
    _, volta_x, volta_y, _, volta_dir, volta_frame = gravacao[0]
    screen.blit(fantasma[volta_frame + 4 * volta_dir], (volta_x - cam_x, volta_y - cam_y))
    if copia_gravacao:
        screen.blit(frames_copia[copia_frame + 4 * copia_dir], (copia_x - cam_x, copia_y - cam_y))
    frames = frames_dir if olhando_direita else frames_esq
    screen.blit(frames[frame_atual], (pos_x - cam_x, pos_y - cam_y))
    if mostrar_colliders:
        for collider in solidos_frame:
            pygame.draw.rect(screen, (0, 0, 255), collider.move(-cam_x, -cam_y), 2)
        pygame.draw.rect(screen, (255, 0, 0), collider_jogador.move(-cam_x, -cam_y), 2)
    if flash_time > 0:
        flash = pygame.Surface(screen.get_size())
        flash.fill((255, 255, 255))
        flash.set_alpha(int(180 * flash_time / 150))
        screen.blit(flash, (0, 0))
        flash_time = flash_time - dt
    screen.blit(fonte.render("← → andar   ESPAÇO pular   CTRL+Z desfazer   F1 colisões", True, (255, 255, 255)), (12, 8))
    texto_hud = fonte_hud.render(f"Memória de desfazer: {usos_ctrlz}", True, (0, 0, 0))
    caixa_hud = pygame.Rect(screen.get_width() - texto_hud.get_width() - 30, 8, texto_hud.get_width() + 20, 26)
    pygame.draw.rect(screen, (192, 192, 192), caixa_hud)
    pygame.draw.lines(screen, (255, 255, 255), False, [caixa_hud.bottomleft, caixa_hud.topleft, caixa_hud.topright])
    pygame.draw.lines(screen, (0, 0, 0), False, [caixa_hud.topright, caixa_hud.bottomright, caixa_hud.bottomleft])
    screen.blit(texto_hud, (caixa_hud.x + 10, caixa_hud.y + 4))
    if aviso_time > 0:
        texto_aviso = fonte_hud.render("Não é possível desfazer: memória insuficiente.", True, (255, 255, 255))
        caixa_aviso = pygame.Rect(0, 0, texto_aviso.get_width() + 30, 36)
        caixa_aviso.center = (screen.get_width() // 2, 70)
        pygame.draw.rect(screen, (170, 0, 0), caixa_aviso)
        pygame.draw.rect(screen, (0, 0, 0), caixa_aviso, 1)
        screen.blit(texto_aviso, (caixa_aviso.x + 15, caixa_aviso.y + 9))
        aviso_time = aviso_time - dt
    pygame.display.update()
