#gera os pngs do jogo (tileset estilo windows 95 + spritesheet do cursor)
#so precisa rodar de novo se mudar algum desenho aqui
import pygame, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("assets", exist_ok=True)

branco = (255, 255, 255)
claro = (223, 223, 223)
cinza = (192, 192, 192)
sombra = (128, 128, 128)
preto = (0, 0, 0)
azul = (0, 0, 128)
amarelo = (255, 222, 89)
amarelo_escuro = (196, 160, 0)
vermelho = (220, 0, 0)

def relevo(tile, x, y, w, h):
    #borda 3d classica do win95: claro em cima/esq, escuro embaixo/dir
    pygame.draw.rect(tile, cinza, (x, y, w, h))
    pygame.draw.line(tile, branco, (x, y), (x + w - 1, y))
    pygame.draw.line(tile, branco, (x, y), (x, y + h - 1))
    pygame.draw.line(tile, preto, (x, y + h - 1), (x + w - 1, y + h - 1))
    pygame.draw.line(tile, preto, (x + w - 1, y), (x + w - 1, y + h - 1))
    pygame.draw.line(tile, claro, (x + 1, y + 1), (x + w - 2, y + 1))
    pygame.draw.line(tile, claro, (x + 1, y + 1), (x + 1, y + h - 2))
    pygame.draw.line(tile, sombra, (x + 1, y + h - 2), (x + w - 2, y + h - 2))
    pygame.draw.line(tile, sombra, (x + w - 2, y + 1), (x + w - 2, y + h - 2))

def barra_titulo(tile):
    tile.fill(azul)
    pygame.draw.line(tile, branco, (0, 0), (15, 0))
    pygame.draw.line(tile, cinza, (0, 15), (15, 15))

#tileset: cada tile 16x16, numa linha so
tiles = []

t = pygame.Surface((16, 16), pygame.SRCALPHA) #[ inicio da barra de titulo (com iconezinho)
barra_titulo(t)
pygame.draw.line(t, branco, (0, 0), (0, 15))
pygame.draw.rect(t, branco, (3, 4, 7, 7))
pygame.draw.rect(t, azul, (4, 6, 5, 4))
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA) #= meio da barra de titulo
barra_titulo(t)
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA) #] fim da barra de titulo (botao X)
barra_titulo(t)
pygame.draw.line(t, preto, (15, 0), (15, 15))
relevo(t, 3, 3, 10, 9)
pygame.draw.line(t, preto, (5, 5), (10, 9), 1)
pygame.draw.line(t, preto, (10, 5), (5, 9), 1)
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA) ## bloco de janela
relevo(t, 0, 0, 16, 16)
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA) #_ barra de tarefas (chao)
t.fill(cinza)
pygame.draw.line(t, branco, (0, 0), (15, 0))
pygame.draw.line(t, claro, (0, 1), (15, 1))
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA) #P pasta (decoracao, depois vira a saida)
pygame.draw.rect(t, amarelo_escuro, (1, 3, 6, 3))
pygame.draw.rect(t, amarelo, (1, 5, 14, 9))
pygame.draw.rect(t, amarelo_escuro, (1, 5, 14, 9), 1)
pygame.draw.line(t, branco, (2, 6), (13, 6))
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA) #e icone de erro (decoracao)
pygame.draw.circle(t, preto, (8, 8), 7)
pygame.draw.circle(t, vermelho, (8, 8), 6)
pygame.draw.line(t, branco, (5, 5), (10, 10), 2)
pygame.draw.line(t, branco, (10, 5), (5, 10), 2)
tiles.append(t)

tileset = pygame.Surface((16 * len(tiles), 16), pygame.SRCALPHA)
for i in range(len(tiles)):
    tileset.blit(tiles[i], (16 * i, 0))
pygame.image.save(tileset, "assets/tileset.png")

#cursor: X = contorno preto, W = branco. 4 frames: parado, passo 1, passo 2, pulo
corpo = [
    "X...........",
    "XX..........",
    "XWX.........",
    "XWWX........",
    "XWWWX.......",
    "XWWWWX......",
    "XWWWWWX.....",
    "XWWWWWWX....",
    "XWWWWWWWX...",
    "XWWWWWWWWX..",
    "XWWWWWXXXXX.",
    "XWWXWWX.....",
]
#so a "cauda" do cursor muda entre os frames, e ela que faz o papel das pernas
caudas = [
    ["XWX.XWWX....", "XX..XWWX....", "X....XWWX...", ".....XWWX...", "......XX...."],
    ["XWX.XWWX....", "XX...XWWX...", "X.....XWWX..", "......XWWX..", ".......XX..."],
    ["XWX.XWWX....", "XX..XWWX....", "X...XWWX....", "....XWWX....", ".....XX....."],
    ["XWX.XWWX....", "XX..XWWX....", "X...XWWX....", "....XWWX....", "....XWWX...."],
]
cursor = pygame.Surface((12 * len(caudas), 17), pygame.SRCALPHA)
for f in range(len(caudas)):
    linhas = corpo + caudas[f]
    for y in range(len(linhas)):
        for x in range(len(linhas[y])):
            if linhas[y][x] == "X":
                cursor.set_at((12 * f + x, y), preto)
            elif linhas[y][x] == "W":
                cursor.set_at((12 * f + x, y), branco)
pygame.image.save(cursor, "assets/cursor.png")
print("assets gerados")
