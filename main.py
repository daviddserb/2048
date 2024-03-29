import numpy as np
import sys
import random
import pygame
import asyncio  # to be able to convert pygame GUI to Web
from pygame.locals import *
from constants import COLORS

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
    new_number(k=2)
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
            await game_finish_text()
        if game_win():
            await game_finish_text()
        if not all((grid == old_grid).flatten()):
            # print("Grid after move (no new number):")
            # print(grid)
            new_number()
            # print("Grid after move (with new number):")
            # print(grid)
        # print("Score:", score)
        await asyncio.sleep(0)


# generate k number after each move - insert the random value (2 or 4) only in an available empty squares
def new_number(k=1):
    grid_free_pos = list(zip(*np.where(grid == 0)))

    for pos in random.sample(grid_free_pos, k=k):
        if random.random() < .1:
            grid[pos] = 4
        else:
            grid[pos] = 2


def _get_nums(array):
    array_non_zeros = array[array != 0]
    array_non_zeros_final = []
    skip = False

    for pos in range(len(array_non_zeros)):
        if skip:
            skip = False
            continue
        if pos != len(array_non_zeros) - 1 and array_non_zeros[pos] == array_non_zeros[pos + 1]:
            new_n = array_non_zeros[pos] * 2
            skip = True
        else:
            new_n = array_non_zeros[pos]

        array_non_zeros_final.append(new_n)

    return np.array(array_non_zeros_final)


def make_move(move):
    left_right_moves = "lr"
    right_down_moves = "rd"

    for i in range(GRID_SIZE):
        # if move is LEFT OR RIGHT, we get the ROWS of the grid
        if move in left_right_moves:
            array = grid[i, :]
        # else (move is UP OR DOWN), we get the COLUMNS of the grid
        else:
            array = grid[:, i]

        # if move is RIGHT or DOWN, we get the REVERSED order of the array
        # we do this to don't change the algorithm of calculating the values in the array
        flipped = False
        if move in right_down_moves:
            flipped = True
            array = array[::-1]

        array_non_zeros = _get_nums(array)
        new_array = np.zeros_like(array)
        new_array[:len(array_non_zeros)] = array_non_zeros

        # if it was flipped (move was RIGHT or DOWN), we flip it back again, so it comes back to the original state
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
    game_screen.fill(COLORS["background"])

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            n = grid[row][col]

            rect_x = col * WIDTH // GRID_SIZE + SPACING
            rect_y = row * (HEIGHT - SCORE_SPACING) // GRID_SIZE + SPACING
            rect_w = WIDTH // GRID_SIZE - 2 * SPACING
            rect_h = (HEIGHT - SCORE_SPACING) // GRID_SIZE - 2 * SPACING

            pygame.draw.rect(
                game_screen,
                COLORS[n],
                pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                border_radius=8
            )

            if n == 0:
                continue

            text_surface = game_font.render(str(n), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
            game_screen.blit(text_surface, text_rect)

    # Display the score at the bottom of the grid
    score_surface = game_font.render("Score: {}".format(score), True, COLORS["score"])
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


async def game_finish_text():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_end()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse click is within the restart button area
                if WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and HEIGHT // 2 + 40 <= event.pos[1] <= HEIGHT // 2 + 80:
                    await reset_game()

        await asyncio.sleep(0)

        final_text = "Congratulations! You Win!"
        if is_game_lost:
            final_text = "Game over! You Lost!"

        finish_text = game_font.render(final_text, True, COLORS["text_finish"])

        finish_text_rect = finish_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 40, 100, 40)  # restart button

        # restart button and his text
        pygame.draw.rect(game_screen, COLORS["button"], restart_button_rect, border_radius=8)
        restart_text_surface = game_font.render("Restart", True, (0, 0, 0))
        restart_text_rect = restart_text_surface.get_rect(center=restart_button_rect.center)

        game_screen.blit(finish_text, finish_text_rect)
        game_screen.blit(restart_text_surface, restart_text_rect)

        pygame.display.update()


def game_end():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


async def reset_game():
    global grid, score, is_game_lost
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    score = 0
    is_game_lost = False
    await initialize_game()


asyncio.run(initialize_game())
