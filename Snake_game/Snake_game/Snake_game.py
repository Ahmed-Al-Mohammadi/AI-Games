import pygame
import time
import random

pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
gray = (169, 169, 169)

snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()


snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction


apple_pos = [random.randrange(1, (width // snake_block)) * snake_block,
             random.randrange(1, (height // snake_block)) * snake_block]
apple_spawn = True


game_paused = False


def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(win, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(win, color, (x, y, width, height))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surface = small_text.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    win.blit(text_surface, text_rect)


def pause_game():
    global game_paused
    game_paused = True


def resume_game():
    global game_paused
    game_paused = False


def move_towards_apple():
    global direction
    if snake_pos[0] < apple_pos[0]:
        direction = 'RIGHT'
    elif snake_pos[0] > apple_pos[0]:
        direction = 'LEFT'
    elif snake_pos[1] < apple_pos[1]:
        direction = 'DOWN'
    elif snake_pos[1] > apple_pos[1]:
        direction = 'UP'


def game_loop():
    global direction, change_to, apple_spawn, apple_pos, game_paused
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if not game_paused:
            move_towards_apple()

            
            if direction == 'UP':
                snake_pos[1] -= snake_block
            if direction == 'DOWN':
                snake_pos[1] += snake_block
            if direction == 'LEFT':
                snake_pos[0] -= snake_block
            if direction == 'RIGHT':
                snake_pos[0] += snake_block

            
            snake_body.insert(0, list(snake_pos))
            if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
                apple_spawn = False
            else:
                snake_body.pop()
            
            if not apple_spawn:
                apple_pos = [random.randrange(1, (width // snake_block)) * snake_block,
                             random.randrange(1, (height // snake_block)) * snake_block]
            apple_spawn = True

            
            if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
                game_over = True
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    game_over = True

        
        win.fill(white)

        
        pygame.draw.rect(win, red, pygame.Rect(apple_pos[0], apple_pos[1], snake_block, snake_block))

        
        for pos in snake_body:
            pygame.draw.rect(win, green, pygame.Rect(pos[0], pos[1], snake_block, snake_block))

        
        draw_button("Pause", 650, 50, 100, 50, gray, blue, pause_game)
        draw_button("Resume", 650, 120, 100, 50, gray, blue, resume_game)

        
        pygame.display.update()

        
        clock.tick(snake_speed)

    pygame.quit()


game_loop()
