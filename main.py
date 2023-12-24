import numpy as np
import sys
import random
import pygame
from pygame.locals import *
from constants import CP

N = 4
grid = np.zeros((N, N), dtype=int)
W = 500
H = W
SPACING = 10
score = 0

pygame.init()  # initialize imported pygame modules
pygame.display.set_caption("2048")  # game title
custom_font = pygame.font.SysFont("Calibre", 30)
screen = pygame.display.set_mode((W, H))  # game resolution


def new_number(k=1):  # generate only one number (because of k = 1) after each move
    # insert the value (2 or 4) only in an available empty square
    free_poss = list(zip(*np.where(grid == 0)))
    for pos in random.sample(free_poss, k=k):
        if random.random() < .1:
            grid[pos] = 4
        else:
            grid[pos] = 2


def _get_nums(array):
    array_n = array[array != 0]
    array_n_final = []
    skip = False

    for j in range(len(array_n)):
        if skip:
            skip = False
            continue
        if j != len(array_n) - 1 and array_n[j] == array_n[j + 1]:
            new_n = array_n[j] * 2
            skip = True
        else:
            new_n = array_n[j]

        array_n_final.append(new_n)

    return np.array(array_n_final)  # return the new list after the move


def make_move(move):
    global score

    for i in range(N):
        if move in "lr":
            array = grid[i, :]
        else:
            array = grid[:, i]

        flipped = False
        if move in "rd":
            flipped = True
            array = array[::-1]

        array_n = _get_nums(array)
        new_array = np.zeros_like(array)
        new_array[:len(array_n)] = array_n

        if flipped:
            new_array = new_array[::-1]

        if move in "lr":
            grid[i, :] = new_array
        else:
            grid[:, i] = new_array

    # ??? TODO: calculate score


def draw_game():
    screen.fill(CP["background"])

    for i in range(N):
        for j in range(N):
            n = grid[i][j]

            rect_x = j * W // N + SPACING
            rect_y = i * H // N + SPACING
            rect_w = W // N - 2 * SPACING
            rect_h = H // N - 2 * SPACING

            pygame.draw.rect(screen,
                             CP[n],
                             pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                             border_radius=8)

            if n == 0:
                continue
            text_surface = custom_font.render(str(n), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
            screen.blit(text_surface, text_rect)


def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    return "u"
                elif event.key == K_RIGHT:
                    return "r"
                elif event.key == K_LEFT:
                    return "l"
                elif event.key == K_DOWN:
                    return "d"
                elif event.key == K_ESCAPE or event.key == K_q:  # a custom forced stop (e.g. with q)
                    end()


def game_over():
    global grid
    grid_bu = grid.copy()
    for move in 'lrud':
        make_move(move)
        # if the matrix before the move is different
        # after a move, if the old matrix already differs from the new one => game still not over
        if not all((grid == grid_bu).flatten()):
            grid = grid_bu
            return False
    return True


def game_over_text(final_score):
    screen.fill(CP["menu"])

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()

        game_over_surface = custom_font.render("Game over!", True, CP["text_finish"])
        score_surface = custom_font.render("Score: {}".format(final_score), True, (0, 0, 0))

        game_over_rect = game_over_surface.get_rect(center=(W // 2, H // 2 - 20))
        score_rect = score_surface.get_rect(center=(W // 2, H // 2 + 20))

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(score_surface, score_rect)

        pygame.display.update()


def end():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def play():
    new_number(k=2)  # start the game with 2 valued squares
    print(grid)
    while True:
        draw_game()
        pygame.display.flip()
        cmd = wait_for_key()
        old_grid = grid.copy()
        make_move(cmd)
        print("Move:", cmd)
        print(grid)
        print("Score:", score)
        if game_over():
            game_over_text(score)
        if not all((grid == old_grid).flatten()):
            new_number()


play()
