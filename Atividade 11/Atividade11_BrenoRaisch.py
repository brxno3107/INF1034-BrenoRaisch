import pygame, sys, os
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
os.chdir(os.path.dirname(os.path.abspath(__file__)))

clock = pygame.time.Clock()

curr_frame_dog = 0
anim_time_dog = 0
dog_list = pygame.image.load_animation("chiens-funnyanimals.gif")

curr_frame = 0
anim_time = 0
hero_x = 0
hero_walk_list = []
for i in range(16):
    hero_walk_list.append(pygame.image.load(f"assets/assets/Hero_Walk_{i+1:02d}.png"))

run_animation = False
curr_frame_mm = 0
anim_time_mm = 0
megaman_spritesheet = pygame.image.load("megaman_spritesheet.png")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hello World!')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                run_animation = True
        if event.type == MOUSEBUTTONDOWN:
            run_animation = True
    clock.tick(60)
    dt = clock.get_time()
    anim_time_dog = anim_time_dog + dt
    if anim_time_dog > dog_list[curr_frame_dog][1]:
        curr_frame_dog = curr_frame_dog + 1
        if curr_frame_dog > len(dog_list) - 1:
            curr_frame_dog = 0
        anim_time_dog = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        hero_x = hero_x + 3
        if hero_x > 800:
            hero_x = -128
        anim_time = anim_time + dt
        anim_time_sec = anim_time/1000
        if anim_time_sec > 0.06:
            curr_frame = curr_frame + 1
            if curr_frame > len(hero_walk_list) - 1:
                curr_frame = 0
            anim_time = 0
    if run_animation:
        anim_time_mm = anim_time_mm + dt
        anim_time_mm_sec = anim_time_mm/1000
        if anim_time_mm_sec > 0.1:
            curr_frame_mm = curr_frame_mm + 1
            if curr_frame_mm > 9:
                curr_frame_mm = 0
                run_animation = False
            anim_time_mm = 0
    screen.fill((247, 247, 247))
    screen.blit(dog_list[curr_frame_dog][0], (560, 20))
    screen.blit(hero_walk_list[curr_frame], (hero_x, 400))
    screen.blit(megaman_spritesheet, (400, 250), (60*(curr_frame_mm%5), 12 + 59*(curr_frame_mm//5), 60, 50))
    pygame.display.update()
