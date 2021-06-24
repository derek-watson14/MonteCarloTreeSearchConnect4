import numpy as np
import pygame
import sys
import time

import logic

# Initialize pygame
pygame.init()
pygame.display.set_caption('Connect Four vs MCTS AI')

# Colors
RED = (180, 54, 87)
YELLOW = (249, 248, 113)
BLUE = (4, 101, 189)
BLACK = (25, 25, 25)
WHITE = (250, 250, 250)
EASY = (174, 221, 255)
MEDIUM = (140, 190, 255)
HARD = (104, 159, 254)


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
    hard = draw_top_button(SQUARESIZE * 5.25, "!*@?", BLACK, HARD)

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


class Game:
    def __init__(self):
        self.empty = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.running = True
        self.human = False
        self.ai = False
        self.ai_time = False
        self.turn = 0

        self.board_state = None
        self.board = None
        self.next_up = None
        self.result = None
        self.is_over = False

    def new_game(self):
        self.human = False
        self.ai = False
        self.ai_time = False
        board_state = logic.ConnectFourGameState(
            state=self.empty, next_to_move=1)
        self.update_board(board_state)
        screen.fill(BLACK)
        draw_board(self.board)

    def update_board(self, board_state):
        self.board_state = board_state
        self.board = board_state.board
        self.next_up = board_state.next_to_move
        self.result = board_state.game_result
        self.is_over = board_state.is_game_over()

    def increment_turn(self):
        self.turn += 1

    def set_human_player(self, player):
        self.human = player
        self.ai = player * -1

    def set_ai_time(self, time):
        self.ai_time = time

    def end_game(self):
        self.running = False


# Cell dimensions
SQUARESIZE = 80
RADIUS = int((SQUARESIZE / 2) - 4)

# Board dimensions
COLUMN_COUNT = 7
ROW_COUNT = 6
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)

titleFont = pygame.font.SysFont('bahnschrift', 24)
buttonFont = pygame.font.SysFont('bahnschrift', 16)

game = Game()
game.new_game()

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    if not game.ai_time:
        level_buttons = draw_ai_level_screen(game.board)
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if level_buttons[0].collidepoint(mouse_pos):
                game.set_ai_time(0.5)
            if level_buttons[1].collidepoint(mouse_pos):
                game.set_ai_time(3)
            if level_buttons[2].collidepoint(mouse_pos):
                game.set_ai_time(7)

    elif game.ai_time and not game.human:
        color_buttons = draw_color_screen(game.board)
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if color_buttons[0].collidepoint(mouse_pos):
                game.set_human_player(1)
            if color_buttons[1].collidepoint(mouse_pos):
                game.set_human_player(-1)

    elif game.ai_time and game.next_up == game.human and not game.is_over:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            circle_pos = (int(posx), int(SQUARESIZE/2))
            color = RED if game.human == 1 else YELLOW
            pygame.draw.circle(screen, color, circle_pos, RADIUS)
            draw_board(game.board)
        if event.type == pygame.MOUSEBUTTONUP:
            col = int(event.pos[0] / 80)
            new_board_state = logic.play_one_human_turn(game.board_state, col)
            game.update_board(new_board_state)
            draw_board(game.board)
            game.turn += 1

    elif game.ai_time and game.next_up == game.ai and not game.is_over:
        draw_ai_choice_screen(game.board, game.ai_time)
        new_board_state = logic.play_one_ai_turn(
            game.board_state, game.ai_time)
        game.update_board(new_board_state)
        draw_board(game.board)
        game.turn += 1

    elif game.is_over:
        win_message = ""
        if game.result == 0:
            win_message = "Draw! No winner in 42 turns!"
        else:
            win_message = "{0} ({1}) wins in {2} turns! ".format(
                logic.interpret_color(game.result).capitalize(),
                logic.interpret_player(game.result, game.human, game.ai),
                game.turn
            )
        reset_button = draw_win_screen(win_message, game.board)

        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if reset_button.collidepoint(mouse_pos):
                time.sleep(0.2)
                game.new_game()
