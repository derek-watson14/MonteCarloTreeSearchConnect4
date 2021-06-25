import numpy as np
import pygame
import sys
import time

from game.connectfour import ConnectFourGameState

import logic as l
import graphics as g

# Initialize pygame
pygame.init()
pygame.display.set_caption('Connect Four vs MCTS AI')


class Game:
    def __init__(self, screen):
        self.empty = np.zeros((g.ROW_COUNT, g.COLUMN_COUNT))
        self.screen = screen

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
        self.turn = 0
        board_state = ConnectFourGameState(
            state=self.empty, next_to_move=1)
        self.update_board(board_state)
        self.screen.fill(g.BLACK)
        g.draw_board(self.board)

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


game = Game(g.screen)
game.new_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    game.screen.fill(g.BLACK)

    if not game.ai_time:
        level_buttons = g.draw_ai_level_screen(game.board)
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if level_buttons[0].collidepoint(mouse_pos):
                game.set_ai_time(0.5)
            if level_buttons[1].collidepoint(mouse_pos):
                game.set_ai_time(3)
            if level_buttons[2].collidepoint(mouse_pos):
                game.set_ai_time(9)

    elif game.ai_time and not game.human:
        color_buttons = g.draw_color_screen(game.board)
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
            circle_pos = (int(posx), int(g.SQUARESIZE/2))
            color = g.RED if game.human == 1 else g.YELLOW
            pygame.draw.circle(game.screen, color, circle_pos, g.RADIUS)
            g.draw_board(game.board)
        if event.type == pygame.MOUSEBUTTONUP:
            col = int(event.pos[0] / 80)
            new_board_state = l.play_one_human_turn(game.board_state, col)
            game.update_board(new_board_state)
            g.draw_board(game.board)
            game.turn += 1

    elif game.ai_time and game.next_up == game.ai and not game.is_over:
        g.draw_ai_choice_screen(game.board, game.ai_time)
        new_board_state = l.play_one_ai_turn(game.board_state, game.ai_time)
        game.update_board(new_board_state)
        g.draw_board(game.board)
        game.turn += 1

    elif game.is_over:
        win_message = ""
        if game.result == 0:
            win_message = "Draw! No winner in 42 turns!"
        else:
            win_message = "{0} ({1}) wins in {2} turns! ".format(
                l.interpret_color(game.result).capitalize(),
                l.interpret_player(game.result, game.human, game.ai),
                game.turn
            )
        reset_button = g.draw_win_screen(win_message, game.board)

        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if reset_button.collidepoint(mouse_pos):
                time.sleep(0.2)
                game.new_game()
