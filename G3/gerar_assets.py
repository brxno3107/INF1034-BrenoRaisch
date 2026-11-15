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
##########################################################################################
tiles = []
t = pygame.Surface((16, 16), pygame.SRCALPHA)
barra_titulo(t)
pygame.draw.line(t, branco, (0, 0), (0, 15))
pygame.draw.rect(t, branco, (3, 4, 7, 7))
pygame.draw.rect(t, azul, (4, 6, 5, 4))
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
barra_titulo(t)
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
barra_titulo(t)
pygame.draw.line(t, preto, (15, 0), (15, 15))
relevo(t, 3, 3, 10, 9)
pygame.draw.line(t, preto, (5, 5), (10, 9), 1)
pygame.draw.line(t, preto, (10, 5), (5, 9), 1)
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
relevo(t, 0, 0, 16, 16)
tiles.append(t)

t = pygame.Surface((16, 16), pygame.SRCALPHA)
t.fill(cinza)
pygame.draw.line(t, branco, (0, 0), (15, 0))
pygame.draw.line(t, claro, (0, 1), (15, 1))
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
pygame.draw.rect(t, amarelo_escuro, (1, 3, 6, 3))
pygame.draw.rect(t, amarelo, (1, 5, 14, 9))
pygame.draw.rect(t, amarelo_escuro, (1, 5, 14, 9), 1)
pygame.draw.line(t, branco, (2, 6), (13, 6))
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
pygame.draw.circle(t, preto, (8, 8), 7)
pygame.draw.circle(t, vermelho, (8, 8), 6)
pygame.draw.line(t, branco, (5, 5), (10, 10), 2)
pygame.draw.line(t, branco, (10, 5), (5, 10), 2)
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
relevo(t, 2, 10, 12, 6)
pygame.draw.rect(t, vermelho, (6, 12, 4, 2))
tiles.append(t)
t = pygame.Surface((16, 16), pygame.SRCALPHA)
pygame.draw.rect(t, cinza, (2, 13, 12, 3))
pygame.draw.line(t, preto, (2, 13), (13, 13))
pygame.draw.line(t, branco, (2, 15), (13, 15))
pygame.draw.rect(t, (0, 170, 0), (6, 14, 4, 1))
tiles.append(t)
def firewall(pontas):
    t = pygame.Surface((16, 16), pygame.SRCALPHA)
    t.fill((130, 30, 25))
    for y in (0, 4, 8, 12):
        pygame.draw.line(t, (70, 20, 20), (0, y), (15, y))
        deslocamento = 0 if y % 8 == 0 else 4
        for x in range(deslocamento, 16, 8):
            pygame.draw.line(t, (70, 20, 20), (x, y), (x, y + 3))
    for centro, ponta in zip((2, 8, 13), pontas):
        pygame.draw.polygon(t, (255, 120, 0), [(centro - 3, 16), (centro, ponta), (centro + 3, 16)])
        pygame.draw.polygon(t, (255, 220, 60), [(centro - 1, 16), (centro, ponta + 5), (centro + 1, 16)])
    return t
tiles.append(firewall((6, 2, 8)))
t = pygame.Surface((16, 16), pygame.SRCALPHA)
for k in range(0, 16, 3):
    for ponto in ((k, 0), (k, 15), (0, k), (15, k)):
        t.set_at(ponto, (170, 40, 30))
tiles.append(t)
tiles.append(firewall((2, 7, 3)))
for cor_disquete in ((90, 90, 90), (0, 0, 170)):
    t = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.rect(t, cor_disquete, (2, 3, 12, 13))
    pygame.draw.rect(t, preto, (2, 3, 12, 13), 1)
    pygame.draw.rect(t, cinza, (5, 3, 6, 4))
    pygame.draw.rect(t, sombra, (8, 4, 2, 2))
    pygame.draw.rect(t, branco, (4, 10, 8, 5))
    tiles.append(t)
tileset =pygame.Surface((16 * len(tiles), 16), pygame.SRCALPHA)
for i in range(len(tiles)):
    tileset.blit(tiles[i], (16 * i, 0))
pygame.image.save(tileset, "assets/tileset.png")
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
