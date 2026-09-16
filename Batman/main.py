import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True

fonte = pygame.font.Font("batmfa__.ttf", 50)
image = pygame.image.load("batman.png")
image = pygame.transform.scale(image, (200, 200))
pygame.mixer.music.load("batman_1966.mp3")
pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#97D1FA")
    pygame.draw.rect(screen, "#0D1664", (100, 200, 200, 50))
    pygame.draw.circle(screen, "#FFF251", (80, 80), 50)
    pygame.draw.polygon(screen, "#F2883B", [(400, 300), (450, 300), (425, 250)])
    pygame.draw.line(screen, "#FFF251", (10, 150), (100, 20), 4)

    screen.blit(image, (500, 300))

    steve_text = fonte.render("I am BATMAN!", True, "#000000")
    screen.blit(steve_text, (500, 250))

    pygame.display.update()