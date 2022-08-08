import pygame
import random
from constants import *
from pygame.constants import *
import sys

pygame.init()

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

LARGE_MESSAGE_FONT = pygame.font.SysFont('tlwgtypo', 100, bold=True)
MESSAGE_FONT = pygame.font.SysFont('tlwgtypo', 15, bold=True)


def draw_snake(snake_list):
    for x,coord in enumerate(snake_list):
        if x == 0:
            pygame.draw.rect(window, BLACK_COLOR, [coord[0] * BOX_WIDTH, coord[1] * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT])
        else:
            pygame.draw.rect(window, RED_COLOR, [coord[0] * BOX_WIDTH, coord[1] * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT])


def draw_food(food):
    pygame.draw.rect(window, GREEN_COLOR, [food[0] * BOX_WIDTH, food[1] * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT])


def draw_grid():
    for row in range(ROWS):
        y = row * BOX_HEIGHT
        pygame.draw.line(window, BLACK_COLOR, (0, y), (WIN_WIDTH, y))

    for col in range(COLS):
        x = col * BOX_WIDTH
        pygame.draw.line(window, BLACK_COLOR, (x, 0), (x, WIN_HEIGHT))


def move_snake(direction, snake_list: list, food: list, lastFood):
    velocity = [0, 0]

    lastFood += 1
    if direction == 'LEFT':
        velocity = [-1, 0]
    elif direction == 'RIGHT':
        velocity = [1, 0]
    elif direction == 'UP':
        velocity = [0, -1]
    elif direction == 'DOWN':
        velocity = [0, 1]

    head = snake_list[0]
    new_head = [head[0] + velocity[0], head[1] + velocity[1]]

    snake_list.insert(0, new_head)
    if new_head == food:
        food = generate_food()
        lastFood = 0
    else:
        snake_list.pop()

    return snake_list, food, lastFood


def movement_control(direction):
    keys = pygame.key.get_pressed()
    if keys[K_UP] or keys[K_w]:
        direction = 'UP'
    elif keys[K_DOWN] or keys[K_s]:
        direction = 'DOWN'
    elif keys[K_LEFT] or keys[K_a]:
        direction = 'LEFT'
    elif keys[K_RIGHT] or keys[K_d]:
        direction = 'RIGHT'

    return direction


def generate_food():
    return [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)]


def check_lose(snake_list: list):
    head = snake_list[0]

    if head[0] < 0 or head[0] > COLS or head[1] < 0 or head[1] > ROWS:
        return True

    for coord in snake_list:
        if snake_list.count(coord) > 1:
            return True
    return False


def draw_game(food,snake_list):
    window.fill(GRAY_COLOR)
    draw_food(food)
    draw_snake(snake_list)
    draw_grid()


def gameLoop():
    start()

    snake_list = [[ROWS // 2, COLS // 2]]
    direction = 'RIGHT'
    lastFood = 0
    food = generate_food()

    clock = pygame.time.Clock()

    lose = False
    while not lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(SNAKE_SPEED)

        snake_list, food, lastFood = move_snake(direction, snake_list, food, lastFood)

        draw_game(food,snake_list)
        direction = movement_control(direction)
        lose = check_lose(snake_list)

        pygame.display.flip()

    # display the score for 10 sec
    start_tick = pygame.time.get_ticks() / 1000
    time_elapsed = 0

    text = MESSAGE_FONT.render("You have collected {} points".format(len(snake_list)), True, BLUE_COLOR)
    textRect = text.get_rect()
    textRect.center = WIN_CENTER_COORDS

    while time_elapsed < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        end_tick = pygame.time.get_ticks() / 1000
        time_elapsed = end_tick - start_tick

        window.fill(GRAY_COLOR)
        window.blit(text, textRect)
        pygame.display.flip()


def start():
    started = False
    start_button = LARGE_MESSAGE_FONT.render("START", True, BLACK_COLOR, LIGHTBLUE_COLOR)
    start_button_rect = start_button.get_rect()
    start_button_rect.center = WIN_CENTER_COORDS

    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    # check if the button is pressed
                    if start_button_rect.x <= x <= start_button_rect.x + start_button_rect.w and \
                            start_button_rect.y <= y <= start_button_rect.y + start_button_rect.w:
                        started = True

        window.fill(GRAY_COLOR)
        # draw the button
        window.blit(start_button, start_button_rect)

        pygame.display.flip()


if __name__ == '__main__':
    while True:
        gameLoop()
