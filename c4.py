import numpy as np
import time

from tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from tree.search import MonteCarloTreeSearch
from game.connectfour import ConnectFourGameState, ConnectFourMove


def print_welcome_screen():
    print("\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print("O                               O")
    print("O    CONNECT FOUR vs MCST AI    O")
    print("O                               O")
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n")


def choose_order():
    human_player = None
    print("Do you want to go first or second?")
    print("1. First")
    print("2. Second")
    while human_player == None:
        choice = input("Press 1 or 2 on your keyboard then enter: ")
        if not choice in ["1", "2"]:
            print("> Please enter the number 1 for first or 2 for second")
            continue
        else:
            if choice == "1":
                print("> You will go first!\n")
                human_player = 1
            else:
                print("You will go second!\n")
                human_player = -1
    return human_player


def print_board(board, last=None):
    interpreted = []
    it = np.nditer(board, flags=['multi_index'])
    for cell in it:
        cell_mark = "_"
        if cell == 1:
            cell_mark = "r"
        elif cell == -1:
            cell_mark = "y"
        if last and it.multi_index[0] == last.row_coord and it.multi_index[1] == last.col_coord:
            cell_mark = cell_mark.capitalize()
        interpreted.append(cell_mark)
    reshaped_board = np.reshape(interpreted, (6, 7))
    column_labels = ""
    for i in range(board.shape[1]):
        column_labels += f"   {i + 1}"
    print(column_labels)
    print(reshaped_board, "\n")


def interpret_color(player):
    if player == 1:
        return "red"
    if player == 0:
        return "tie"
    if player == -1:
        return "yellow"


def interpret_player(player, human, ai):
    if player == human:
        return "Human"
    elif player == ai:
        return "AI"
    else:
        return "Tie"


def play_one_ai_turn(current_board, seconds):
    print("AI Thinking...")

    root = TwoPlayersGameMonteCarloTreeSearchNode(state=current_board)
    search_node = MonteCarloTreeSearch(root)

    start = time.time()
    best_move = search_node.best_action(total_simulation_seconds=seconds)
    end = time.time()
    print(f"AI decision made in {round(end-start)} seconds. New Board:")

    print_board(best_move.state.board, best_move.last_move)
    return best_move.state


def play_one_human_turn(current_board, col=None):
    player = current_board.next_to_move
    board = current_board.board
    width = current_board.board_width
    columns = [(col, all(col)) for col in board.T]

    col_coord = None
    if col == None:
        start = time.time()
        while type(col_coord) != int or not 0 <= col_coord <= width or columns[col_coord][1] == True:
            choice = input(f"Choose column to play in (1 - {width}): ")
            try:
                choice = int(choice)
            except:
                print(f"> Please input an integer between 1 and {width}")
                continue
            try:
                if columns[choice - 1][1] == True:
                    print("Column is full.\n")
                    continue
                else:
                    col_coord = int(choice) - 1
            except IndexError:
                print(f"> Column out of bounds. Choose an integer 1 - {width}")
                continue

        end = time.time()
        print(
            f"Player made decision in {round(end-start, 2)} seconds. New Board:")
    else:
        col_coord = col

    column = columns[col_coord][0]
    row_coord = 0
    for i in range(len(column)-1, -1, -1):
        if column[i] == 0.:
            row_coord = i
            break

    move = ConnectFourMove(row_coord, col_coord, player)
    new_board = current_board.move(move)
    print_board(new_board.board, move)
    return new_board


def play_cl_game():
    print_welcome_screen()
    human_player = choose_order()
    state = np.zeros((6, 7))
    current_board = ConnectFourGameState(state=state, next_to_move=1)
    print_board(current_board.board)

    turn = 0
    while not current_board.is_game_over():
        current_player = current_board.next_to_move
        player_type = "Human" if human_player == current_player else "AI"

        turn += 1
        print("> ({0}) {1}'s Turn! ({2})".format(
            turn,
            interpret_color(current_player).capitalize(),
            player_type
        ))
        if human_player == current_player:
            current_board = play_one_human_turn(current_board)
        else:
            current_board = play_one_ai_turn(current_board, 1)

    print("> Result: {0} ({1}) wins in {2} turns! ".format(
        interpret_color(current_board.game_result).upper(),
        player_type,
        turn
    ))


# play_cl_game()
