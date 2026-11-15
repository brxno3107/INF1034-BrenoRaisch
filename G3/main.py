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
solidos = "[=]#_"
mapa = []
with open("fases/fase_teste.txt", encoding="utf-8") as arquivo:
    for linha in arquivo:
        if linha.strip():
            mapa.append(linha.rstrip("\n"))
largura_mapa = len(mapa[0]) * tile_size
altura_mapa = len(mapa) * tile_size
colliders = []
for i in range(len(mapa)):
    for j in range(len(mapa[i])):
        if mapa[i][j] in solidos:
            colliders.append(pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size))
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
            if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL and gravacao:
                ultima_gravacao = gravacao[:]
                _, pos_x, pos_y, vel_y, olhando_direita, _ = gravacao[0]
                gravacao = [gravacao[0]]
                flash_time = 150
                copia_gravacao = ultima_gravacao
                copia_inicio = tempo_jogo
                copia_i = 0
                copia_terminou = False
    clock.tick(60)
    dt = min(clock.get_time(), 50)
    tempo_jogo = tempo_jogo + dt
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
    for collider in colliders:
        if collider_jogador.colliderect(collider):
            if pos_x > old_pos_x:
                pos_x = collider.left - largura_jogador
            else:
                pos_x = collider.right
            collider_jogador.x = pos_x
    vel_y = min(vel_y + gravidade * dt, vel_max_queda)
    pos_y = pos_y + vel_y * dt
    collider_jogador = pygame.Rect(pos_x, pos_y, largura_jogador, altura_jogador)
    for collider in colliders:
        if collider_jogador.colliderect(collider):
            if vel_y > 0:
                pos_y = collider.top - altura_jogador
            else:
                pos_y = collider.bottom
            vel_y = 0
            collider_jogador.y = pos_y
    pe = collider_jogador.move(0, 1)
    no_chao = False
    for collider in colliders:
        if pe.colliderect(collider):
            no_chao = True
    if pos_y > altura_mapa:
        pos_x, pos_y, vel_y = inicio_x, inicio_y, 0
        gravacao = []
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
        for collider in colliders:
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
    _, volta_x, volta_y, _, volta_dir, volta_frame = gravacao[0]
    screen.blit(fantasma[volta_frame + 4 * volta_dir], (volta_x - cam_x, volta_y - cam_y))
    if copia_gravacao:
        screen.blit(frames_copia[copia_frame + 4 * copia_dir], (copia_x - cam_x, copia_y - cam_y))
    frames = frames_dir if olhando_direita else frames_esq
    screen.blit(frames[frame_atual], (pos_x - cam_x, pos_y - cam_y))
    if mostrar_colliders:
        for collider in colliders:
            pygame.draw.rect(screen, (0, 0, 255), collider.move(-cam_x, -cam_y), 2)
        pygame.draw.rect(screen, (255, 0, 0), collider_jogador.move(-cam_x, -cam_y), 2)
    if flash_time > 0:
        flash = pygame.Surface(screen.get_size())
        flash.fill((255, 255, 255))
        flash.set_alpha(int(180 * flash_time / 150))
        screen.blit(flash, (0, 0))
        flash_time = flash_time - dt
    screen.blit(fonte.render("← → andar   ESPAÇO pular   CTRL+Z desfazer   F1 colisões", True, (255, 255, 255)), (12, 8))
    pygame.display.update()
