from moves import get_single_moves, get_inline_moves, get_side_step_moves, apply_move







class GameState:
    """Represents the complete game state an Abalone game."""

    def __init__(self, player, board):
        """
        Initialize a new game state.
        
        :param player: First player to move ('b' for black or 'w' for white)
        :param board: Dictionary representing the board state {(x, y): 'b'/'w'/'N'}
        """
        self._player = player
        self._board = board
        self._score = self.get_score()

    def get_score(self):
        """
        Calculates the score for both players based on the number of opponent marbles pushed off the board.

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
        """
        Checks if either player has won the game by pushing 6 or more opponent marbles off the board.
        
        :return: 'b' if black wins, 'w' if white wins, None if no winner 
        """
        if self._score['b'] >= 6:
            print("Black wins!")
            return 'b'
        elif self._score['w'] >= 6:
            print("White wins!")
            return 'w'
        return None

# def test_state_space(file, board=None, player="b"):
#     """
#     Generates the state space and outputs to a file.
#
#     :param file: the name of the output and optional .input file
#     :param board: an optional board to preconfigure the state space with
#     :param player: an optional player to initiate first ply, black by default
#     """
#     if board is None:
#         player, board = Board.get_input_board_representation(file)
#
#     # Generate all possible moves
#     all_moves = get_single_moves(player, board) + get_inline_moves(player, board) + get_side_step_moves(player, board)
#     file = file.strip(".input")
#
#     # Write moves to file
#     Board.write_to_move_file(file, all_moves)
#
#     # Apply each move and write new board states
#     new_states = []
#     for move in all_moves:
#         new_board = board.copy()
#         apply_move(new_board, move)
#         new_states.append(Board.to_string_board(new_board))
#
#     # Write resulting board to file
#     Board.write_to_board_file(file, new_states)
#
#     print(f"Moves saved to {Board.TEST_OUTPUT_FILES_DIR + "/" + file}.move\nBoard saved to {Board.TEST_OUTPUT_FILES_DIR + "/" + file}.board\n")
#
#
# def local_tests():
#     """Tests the state space for development/debugging purposes."""
#     # Input & Output files
#     input_file_one = "Test1"
#     input_file_two = "Test2"
#
#     belgian_output_white = "test_belgian_white_first"
#     belgian_output_black = "test_belgian_black_first"
#     german_output_white = "test_german_white_first"
#     german_output_black = "test_german_black_first"
#
#     belgian_daisy_board = Board.get_belgian_daisy_board()
#     german_daisy_board = Board.get_german_daisy_board()
#
#     # Tests
#     test_state_space(input_file_one)
#     test_state_space(input_file_two)
#     test_state_space(belgian_output_white, belgian_daisy_board, "w")
#     test_state_space(belgian_output_black, belgian_daisy_board)
#     test_state_space(german_output_white, german_daisy_board, "w")
#     test_state_space(german_output_black, german_daisy_board, "b")


def main():
    pass
    # belgian_daisy_board = Board.get_belgian_daisy_board()
    # german_daisy_board = Board.get_german_daisy_board()
    # Board.write_to_input_file("belgian_daisy_board_white", belgian_daisy_board, "w")  
    # Board.write_to_input_file("belgian_daisy_board_black", belgian_daisy_board, "b")  
    # Board.write_to_input_file("german_daisy_board_white", german_daisy_board, "w")  
    # Board.write_to_input_file("german_daisy_board_black", german_daisy_board, "b")  
    

    # print("Test State Space Generator")
    # print("--------------------------")
    # user_input_files = Board.get_input_files_from_user()
    # if not user_input_files:
    #     return
    # print("\nGenerated Boards\n")
    # for file in user_input_files:
    #     test_state_space(file)
    # input("Press any key to exit")
    #
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
    # """ add single move debug code"""
    # player, board = Board.get_input_board_representation("Test2.input")
    # print("\nBefore Move:")
    # print(Board.to_string_board(board))
    #
    # move = "(-2, -1, w)↙(-3, -2, w)"  # Example move
    # apply_move(board, move)  # Directly modifies board
    #
    # print("\nAfter Move:")
    # print(Board.to_string_board(board))


if __name__ == '__main__':
    main()
