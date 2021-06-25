import pygame


# Colors
RED = (180, 54, 87)
YELLOW = (249, 248, 113)
BLUE = (4, 101, 189)
BLACK = (25, 25, 25)
WHITE = (250, 250, 250)
EASY = (174, 221, 255)
MEDIUM = (140, 190, 255)
HARD = (104, 159, 254)

# Fonts
pygame.font.init()
titleFont = pygame.font.SysFont('ariel', 32)
buttonFont = pygame.font.SysFont('ariel', 24)

# Cell dimensions
SQUARESIZE = 80
RADIUS = int((SQUARESIZE / 2) - 4)

# Board dimensions
COLUMN_COUNT = 7
ROW_COUNT = 6
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# Screen
screen = pygame.display.set_mode(SIZE)


def draw_board(board):
    # Draw board row cell by cell
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            rectangle_pos = (c*SQUARESIZE, (r+1)*SQUARESIZE,
                             SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(screen, BLUE, rectangle_pos)

            circle_pos = (int((c*SQUARESIZE)+(SQUARESIZE/2)),
                          int((((r+1)*SQUARESIZE)+(SQUARESIZE/2))))
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (circle_pos), RADIUS)
            elif board[r][c] == -1:
                pygame.draw.circle(
                    screen, YELLOW, (circle_pos), RADIUS)
            else:
                pygame.draw.circle(screen, BLACK, (circle_pos), RADIUS)

    # Update display
    pygame.display.update()


def draw_top_button(left_edge_pos, text, text_color, bg_color):
    button = pygame.Rect(
        left_edge_pos, SQUARESIZE/4, SQUARESIZE*1.5, SQUARESIZE/2)
    button_text = buttonFont.render(text, True, text_color)
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button.center
    pygame.draw.rect(screen, bg_color, button)
    screen.blit(button_text, button_text_rect)
    return button


def draw_title(center_x, text):
    title = titleFont.render(text, True, WHITE)
    title_rect = title.get_rect()
    title_rect.center = (
        center_x, SQUARESIZE/2)
    screen.blit(title, title_rect)


def draw_color_screen(board):
    draw_title(int(SQUARESIZE * 3.5), "Go first or second?")
    first_button = draw_top_button(SQUARESIZE * 0.25, "First", BLACK, RED)
    second_button = draw_top_button(SQUARESIZE * 5.25, "Second", BLACK, YELLOW)

    draw_board(board)
    return (first_button, second_button)


def draw_ai_level_screen(board):
    draw_title(int(SQUARESIZE * 0.75), "AI Level:")
    easy = draw_top_button(SQUARESIZE * 1.75, "Normal", BLACK, WHITE)
    medium = draw_top_button(SQUARESIZE * 3.5, "Hard", BLACK, MEDIUM)
    hard = draw_top_button(SQUARESIZE * 5.25, "Hardest", BLACK, HARD)

    draw_board(board)
    return (easy, medium, hard)


def draw_win_screen(win_message, board):
    draw_title(int((SQUARESIZE * 5)/2), win_message)
    reset_button = draw_top_button(
        SQUARESIZE * 5.25, "Play Again", BLACK, WHITE)

    draw_board(board)
    return reset_button


def draw_ai_choice_screen(board, time):
    text = f"AI thinking for {time} seconds..."
    draw_title(int((SQUARESIZE * 7)/2), text)
    draw_board(board)
