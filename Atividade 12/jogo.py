import pygame, sys, os
from pygame.locals import QUIT, KEYDOWN
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Vars de ambiente
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Atividade 13 - Mapa com tileset')
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("segoeui", 18)
escala = 3
tile_size = 18 * escala
tileset = pygame.transform.scale_by(pygame.image.load("kenney_pixel-platformer/Tilemap/tilemap_packed.png"), escala)
personagens = pygame.transform.scale_by(pygame.image.load("kenney_pixel-platformer/Tilemap/tilemap-characters_packed.png"), escala)

def corte(linha, coluna):
    return (coluna * tile_size, linha * tile_size, tile_size, tile_size)
#dic de cortes tileset
cortes = {"[": corte(1, 1), "G": corte(1, 2), "]": corte(1, 3), "(": corte(6, 1), "T": corte(6, 2), ")": corte(6, 3), "<": corte(0, 1), "P": corte(0, 2), ">": corte(0, 3), "B": corte(1, 6), "!": corte(0, 10), "p": corte(6, 5), "a": corte(6, 6), "c": corte(6, 7), "m": corte(6, 8), "F": corte(5, 11), "|": corte(6, 11), "o": corte(7, 11), "S": corte(3, 8)}
solidos = "[G](T)<P>B!"

#le mapa do txt
mapa = []
with open("mapa.txt", encoding="utf-8") as arquivo:
    for linha in arquivo:
        if linha.strip():
            mapa.append(linha.rstrip("\n"))
largura_mapa = len(mapa[0]) * tile_size
altura_mapa = len(mapa) * tile_size

#colliders dos blocos e espinhos (espinho so metade de baixo)
colliders = []
espinhos = []
for i in range(len(mapa)):
    for j in range(len(mapa[i])):
        if mapa[i][j] in solidos:
            colliders.append(pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size))
        elif mapa[i][j] == "S":
            espinhos.append(pygame.Rect(j * tile_size, i * tile_size + tile_size // 2, tile_size, tile_size // 2))
#player
frame_size = 24 * escala
player_esq = [personagens.subsurface((0, 0, frame_size, frame_size)), personagens.subsurface((frame_size, 0, frame_size, frame_size))]
player_dir = [pygame.transform.flip(img, True, False) for img in player_esq]
offset_x, offset_y = 4 * escala, 1 * escala #collider menor q o sprite p/ nao bater pelo capacete
largura_jogador, altura_jogador = 16 * escala, 23 * escala
inicio_x, inicio_y = tile_size, 10 * tile_size - altura_jogador
pos_x, pos_y = inicio_x, inicio_y
vel_y = 0
no_chao = False
olhando_direita = True
velocidade = 0.3
gravidade = 0.0025
forca_pulo = 0.95
vel_max_queda = 1.2
curr_frame = 0
anim_time = 0
mostrar_colliders = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w) and no_chao:
                vel_y = -forca_pulo
            if event.key == pygame.K_c:
                mostrar_colliders = not mostrar_colliders
    clock.tick(60)
    dt = min(clock.get_time(), 50)
    #movimento horizontal
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
    #colisao no x (encosta na borda do bloco)
    collider_jogador = pygame.Rect(pos_x, pos_y, largura_jogador, altura_jogador)
    for collider in colliders:
        if collider_jogador.colliderect(collider):
            if pos_x > old_pos_x:
                pos_x = collider.left - largura_jogador
            else:
                pos_x = collider.right
            collider_jogador.x = pos_x
    #gravidade + colisao no y
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
    #checa 1px abaixo do pe p/ saber se ta no chao
    pe = collider_jogador.move(0, 1)
    no_chao = False
    for collider in colliders:
        if pe.colliderect(collider):
            no_chao = True
    #caiu do mapa ou bateu no espinho --> volta pro inicio
    morreu = pos_y > altura_mapa
    for espinho in espinhos:
        if collider_jogador.colliderect(espinho):
            morreu = True
    if morreu:
        pos_x, pos_y, vel_y = inicio_x, inicio_y, 0
    #anim do player
    if not no_chao:
        curr_frame = 1
    elif andando:
        anim_time = anim_time + dt
        if anim_time / 1000 > 0.15:
            curr_frame = curr_frame + 1
            if curr_frame > 1:
                curr_frame = 0
            anim_time = 0
    else:
        curr_frame = 0
    #camera segue o player sem passar da borda do mapa
    cam_x = pos_x + largura_jogador / 2 - screen.get_width() / 2
    cam_y = pos_y + altura_jogador / 2 - screen.get_height() / 2
    cam_x = max(0, min(cam_x, largura_mapa - screen.get_width()))
    cam_y = max(0, min(cam_y, altura_mapa - screen.get_height()))
    #desenho
    screen.fill((221, 239, 242))
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            letra = mapa[i][j]
            if letra in cortes:
                screen.blit(tileset, (j * tile_size - cam_x, i * tile_size - cam_y), cortes[letra])
    frames = player_dir if olhando_direita else player_esq
    screen.blit(frames[curr_frame], (pos_x - offset_x - cam_x, pos_y - offset_y - cam_y))
    if mostrar_colliders:
        for collider in colliders + espinhos:
            pygame.draw.rect(screen, (0, 0, 255), collider.move(-cam_x, -cam_y), 2)
        pygame.draw.rect(screen, (255, 0, 0), collider_jogador.move(-cam_x, -cam_y), 2)
    screen.blit(fonte.render("← → andar   ESPAÇO pular   C mostrar colisões", True, (40, 40, 48)), (12, 8))
    pygame.display.update()
