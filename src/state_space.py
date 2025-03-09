from board import Board
from moves import get_single_moves, get_inline_moves, get_side_step_moves, apply_move

class StateSpace:
    def __init__(self, player, board):
        self._player = player
        self._board = board
        self._score = self.get_score(board)

    def get_score(self, board):
        """
        Calculates the score for both players based on the number of opponent marbles pushed off the board.

        :param board: Dictionary representing the board state {(x, y): 'b'/'w'/'N'}
        :return: Dictionary with scores {'b': int, 'w': int}
        """
        initial_black_marbles = 14  # Standard Abalone setup
        initial_white_marbles = 14

        current_black_marbles = sum(1 for v in self._board.values() if v == 'b')
        current_white_marbles = sum(1 for v in self._board.values() if v == 'w')

        black_score = initial_white_marbles - current_white_marbles  # Black's score = White marbles pushed off
        white_score = initial_black_marbles - current_black_marbles  # White's score = Black marbles pushed off

        return {
            'b': black_score,
            'w': white_score}

    def check_victory(self):
        if self._score['b'] >= 6:
            print("Black wins!")
            return 'b'
        elif self._score['w'] >= 6:
            print("White wins!")
            return 'w'
        return None

def main():
    input_name = "Test1"
    player, board = Board.get_input_board_representation(f"{input_name}.input")

    # Generate all possible moves
    all_moves = get_single_moves(player, board) + get_inline_moves(player, board) + get_side_step_moves(player, board)

    # Write moves to file
    Board.write_to_move_file(input_name, all_moves)
    
    # Apply each move and write new board states
    new_states = []
    for move in all_moves:
        new_board = board.copy()
        apply_move(new_board, move)
        new_states.append(Board.tostring_board(new_board))

    Board.write_to_board_file(input_name, new_states)
   
    print("Moves and new board states have been saved to files.")

    # print("\nSingle Marble Moves:")
    # for move in get_single_moves(player, board):
    #     print(move)
    #
    # print("\nInline Moves:")
    # for move in get_inline_moves(player, board):
    #     print(move)
    #
    # print("\nSide-Step Moves:")
    # for move in get_side_step_moves(player, board):
    #     print(move)
    #
    # print("\nBoard Representation:\n")
    # print(Board.tostring_board(board))
    #
    #
    # print("\nBefore Move:")
    # print(Board.tostring_board(board))
    #
    # move = "(0, -1, b)-(1, 0, b)-(2, 1, b)↗p(3, 2, w)-(4, 3, w)"  # Example move
    # apply_move(board, move)  # Directly modifies board
    #
    # print("\nAfter Move:")
    # print(Board.tostring_board(board))


if __name__ == '__main__':
    main()
