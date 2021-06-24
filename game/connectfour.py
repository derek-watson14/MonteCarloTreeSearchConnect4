import numpy as np
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction


class ConnectFourMove(AbstractGameAction):
    def __init__(self, row_coord, col_coord, player):
        self.row_coord = row_coord
        self.col_coord = col_coord
        self.player = player

    def __repr__(self):
        return "{0} dropped a piece at ({1}, {2})".format(
            self.interpret_player().capitalize(),
            self.row_coord,
            self.col_coord
        )

    def interpret_player(self):
        if self.player == 1:
            return "red"
        elif self.player == -1:
            return "yellow"
        else:
            return "invalid"


class ConnectFourGameState(TwoPlayersAbstractGameState):

    R = 1
    Y = -1

    def __init__(self, state, next_to_move=1):
        shape = state.shape
        if len(shape) != 2 or shape[0] < 4 or shape[1] < 4:
            raise ValueError("Only 2D boards allowed")
        self.board = state
        self.board_height = state.shape[0]
        self.board_width = state.shape[1]
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        # Horizontal Check
        for i in range(self.board_height):
            for j in range(self.board_width - 3):
                empty = self.board[i][j] == 0
                equal = (self.board[i][j]
                         == self.board[i][j+1]
                         == self.board[i][j+2]
                         == self.board[i][j+3])

                if equal and not empty:
                    return self.board[i][j]

        # Vertical Check
        for i in range(self.board_width):
            for j in range(self.board_height - 3):
                empty = self.board[j][i] == 0
                equal = (self.board[j][i]
                         == self.board[j+1][i]
                         == self.board[j+2][i]
                         == self.board[j+3][i])

                if equal and not empty:
                    return self.board[j][i]

        # Descending Diagonal Check
        for i in range(3, self.board_width):
            for j in range(3, self.board_height):
                empty = self.board[j][i] == 0
                equal = (self.board[j][i]
                         == self.board[j-1][i-1]
                         == self.board[j-2][i-2]
                         == self.board[j-3][i-3])

                if equal and not empty:
                    return self.board[j][i]

        # Ascending Diagonal Check
        for i in range(3, self.board_height):
            for j in range(0, self.board_width - 3):
                empty = self.board[i][j] == 0
                equal = (self.board[i][j]
                         == self.board[i-1][j+1]
                         == self.board[i-2][j+2]
                         == self.board[i-3][j+3])

                if equal and not empty:
                    return self.board[i][j]

        # No winner but all squares full - draw
        if np.all(self.board != 0):
            return 0.

        # if not over - no result
        return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.player != self.next_to_move:
            return (False, "Not your turn")

        # check if inside the board on x-axis
        x_in_range = (0 <= move.row_coord < self.board_height)
        if not x_in_range:
            return (False, "Row OOB")

        # check if inside the board on y-axis
        y_in_range = (0 <= move.col_coord < self.board_width)
        if not y_in_range:
            return (False, "Col OOB")

        # check if board cell not occupied yet
        occupied = not self.board[move.row_coord][move.col_coord] == 0
        if occupied:
            return (False, "Space occupied")

        # Or it is bottom row
        bottom = move.row_coord + 1 == self.board_height
        if bottom:
            return (True, "")

        # Finally, make sure board cell below is full
        below_full = not self.board[move.row_coord +
                                    1][move.col_coord] == 0

        return (below_full, "Below is empty")

    def move(self, move):
        legal = self.is_move_legal(move)
        if not legal[0]:
            raise ValueError(
                "\nMove {0} is not legal on board:\n {1} .\nMessage: {2}". format(
                    move, self.board, legal[1])
            )
        new_board = np.copy(self.board)
        new_board[move.row_coord, move.col_coord] = move.player
        if self.next_to_move == ConnectFourGameState.R:
            next_to_move = ConnectFourGameState.Y
        else:
            next_to_move = ConnectFourGameState.R

        return ConnectFourGameState(new_board, next_to_move)

    def get_legal_actions(self):
        # Prepare to store moves
        moves = []

        # Iterate through columns of board
        for col_coord in range(self.board_width):
            # Get list of cells in this column
            column_cells = self.board[:, col_coord]

            # Iterate bottom to top through cells in this column
            for row_coord in range(len(column_cells)-1, -1, -1):
                # Bool checking if cell is empty
                empty = column_cells[row_coord] == 0

                # If empty, add move to list, stop searching this column
                if empty:
                    moves.append(
                        ConnectFourMove(
                            row_coord,
                            col_coord,
                            self.next_to_move
                        )
                    )
                    break
        return moves
