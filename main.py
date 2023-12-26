import numpy as np
import sys
import random
import pygame
import asyncio  # to be able to convert pygame GUI to Web
from pygame.locals import *
from constants import CP

GRID_SIZE = 4
WIDTH = 500
HEIGHT = 600
SPACING = 10
SCORE_SPACING = 50

grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
score = 0
is_game_lost = False

pygame.init()  # initialize imported pygame modules
pygame.display.set_caption("2048")  # game title
game_font = pygame.font.SysFont("Calibre", 30)
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))  # game resolution


async def initialize_game():
    new_number(k=2)  # start the game with 2 valued squares
    # print("Starting grid:")
    # print(grid)
    while True:
        draw_game()
        pygame.display.flip()
        user_command = await wait_for_key()
        old_grid = grid.copy()
        make_move(user_command)
        score_calculation(old_grid, grid, user_command)
        # print("Move:", user_command)
        if game_over():
            await game_finish_text(score)
        if game_win():
            await game_finish_text(score)
        if not all((grid == old_grid).flatten()):
            # print("Grid after move (no new number):")
            # print(grid)
            new_number()
            # print("Grid after move (with new number):")
            # print(grid)
        # print("Score:", score)
        await asyncio.sleep(0)


# generate k number/s after each move - insert the random value (2 or 4) only in an available empty squares
def new_number(k=1):
    free_pos = list(zip(*np.where(grid == 0)))

    for pos in random.sample(free_pos, k=k):
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

    return np.array(array_n_final)


def make_move(move):
    left_right_moves = "lr"
    right_down_moves = "rd"

    for i in range(GRID_SIZE):
        if move in left_right_moves:
            array = grid[i, :]
        else:
            array = grid[:, i]

        flipped = False
        if move in right_down_moves:
            flipped = True
            array = array[::-1]

        array_n = _get_nums(array)
        new_array = np.zeros_like(array)
        new_array[:len(array_n)] = array_n

        if flipped:
            new_array = new_array[::-1]

        if move in left_right_moves:
            grid[i, :] = new_array
        else:
            grid[:, i] = new_array


async def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_end()
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
                    game_end()
        await asyncio.sleep(0)


def score_calculation(grid_before_move, grid_after_move, move):
    global score
    up_down_moves = "ud"

    # Check if the matrices are equal after a move
    if np.array_equal(grid_before_move, grid_after_move):
        return

    # Reverse matrix - switch columns with rows (to keep same algorithm for move lr and ud)
    if move in up_down_moves:
        grid_before_move = grid_before_move.T

    for row in grid_before_move:
        row_not_null = row[row != 0]
        for el in range(len(row_not_null)):
            if el != len(row_not_null) - 1 and row_not_null[el] == row_not_null[el + 1]:
                score += row_not_null[el] * 2


def draw_game():
    game_screen.fill(CP["background"])

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            n = grid[i][j]

            rect_x = j * WIDTH // GRID_SIZE + SPACING
            rect_y = i * (HEIGHT - SCORE_SPACING) // GRID_SIZE + SPACING
            rect_w = WIDTH // GRID_SIZE - 2 * SPACING
            rect_h = (HEIGHT - SCORE_SPACING) // GRID_SIZE - 2 * SPACING

            pygame.draw.rect(
                game_screen,
                CP[n],
                pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                border_radius=8
            )

            if n == 0:
                continue

            text_surface = game_font.render(str(n), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
            game_screen.blit(text_surface, text_rect)

    # Display the score at the bottom of the grid
    score_surface = game_font.render("Score: {}".format(score), True, (0, 0, 0))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT - SCORE_SPACING // 2))
    game_screen.blit(score_surface, score_rect)


def game_win():
    return any(tile == 2048 for row in grid for tile in row)


def game_over():
    global grid
    global is_game_lost
    left_right_up_down_moves = "lrud"

    grid_copy = grid.copy()
    for move in left_right_up_down_moves:
        make_move(move)
        # after a move, if the old matrix already differs from the new one => game still not over
        if not all((grid == grid_copy).flatten()):
            grid = grid_copy
            return False

    is_game_lost = True
    return True


async def game_finish_text(final_score):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_end()
        await asyncio.sleep(0)

        final_text = "Congratulations! You Win!"
        if is_game_lost:
            final_text = "Game over! You Lost!"

        game_over_surface = game_font.render(final_text, True, CP["text_finish"])
        # score_surface = game_font.render("Score: {}".format(final_score), True, (0, 0, 0))

        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        # score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

        game_screen.blit(game_over_surface, game_over_rect)
        # game_screen.blit(score_surface, score_rect)

        pygame.display.update()


def game_end():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


asyncio.run(initialize_game())
