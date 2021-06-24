from tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from tree.search import MonteCarloTreeSearch
from game.connectfour import ConnectFourGameState, ConnectFourMove


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
        return "Player Error"


def play_one_ai_turn(current_board, seconds):
    root = TwoPlayersGameMonteCarloTreeSearchNode(state=current_board)
    search_node = MonteCarloTreeSearch(root)

    best_move = search_node.best_action(total_simulation_seconds=seconds)

    return best_move.state


def play_one_human_turn(current_board, col_coord):
    player = current_board.next_to_move
    board = current_board.board
    columns = [(col, all(col)) for col in board.T]
    column = columns[col_coord][0]

    row_coord = 0
    for i in range(len(column)-1, -1, -1):
        if column[i] == 0:
            row_coord = i
            break

    move = ConnectFourMove(row_coord, col_coord, player)
    new_board = current_board.move(move)
    return new_board
