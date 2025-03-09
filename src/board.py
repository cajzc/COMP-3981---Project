"""Houses the board representation methods."""
import os

class Board:
    """Holds the implementation to parse and output a board's representation."""

    # Get the project root directory and test file paths
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEST_INPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "input")
    TEST_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "output")


    @staticmethod
    def initialize_board():
        """
        Initialize the board with all positions as 'N' (neutral/empty)
        
        :returns: the game board representation as dictionary, where keys represent tuples of positions and values represent the value in the position
        """
        return {(x, y): 'N' for x in range(-4, 5) for y in range(-4, 5) if -4 <= x - y <= 4}

    @staticmethod
    def get_standard_board():

        # Initialize an empty board
        board = Board.initialize_board()

        black_marble_initial_pos = [
             (-4, -4, 'b'), (-3, -4, 'b'), (-2, -4, 'b'), (-1, -4, 'b'), (0, -4, 'b'), # Row 1
             (-4, -3, 'b'), (-3, -3, 'b'), (-2, -3, 'b'), (-1, -3, 'b'), (0, -3, 'b'), (1, -3, 'b'), # Row 2j
             (-2, -2, 'b'),  (-1, -2, 'b'), (0, -2, 'b') # Row 3
         ]

        # White marble initial positions
        white_marbles_initial_pos = [
            (0,4,'w'), (1,4,'w'), (2,4,'w'), (3,4,'w'), (4,4,'w'), # Row 1
            (-1,3,'w'), (0,3,'w'), (1,3,'w'), (2,3,'w'), (3,3,'w'), (4,3,'w'), # Row 2
            (0,2,'w'), (1,2,'w'), (2,2,'w') # Row 3
        ]

        Board.place_marbles(black_marble_initial_pos, board)
        Board.place_marbles(white_marbles_initial_pos, board)

        return board

    @staticmethod
    def place_marbles(coloured_marbles, board):
        """
        Places marbles on the board at specified positions with specified colours.
        
        :param coloured_marbles: List of tuples (x, y, colour) where x and y are coordinates and colour is 'b', 'w', or 'N'
        :param board: Dictionary representing the board where keys are (x, y) coordinates and values are marble colours
        """
        
        for (x, y, colour) in coloured_marbles:
            board[(x, y)] = colour


    @staticmethod
    def get_input_board_representation(file_name):
        """
        Given the class example files with the suffix ".input", returns the player turn and converts a given input board position from an example format:

        Into the team's specific game board format, i.e:
        {(-4, -4): 'N', ..., (-2, -2): 'W', ..., (4, 4): 'N'}

        :param file_name: the name of the input file
        :returns: tuple containing (player turn, game board representation as dictionary)
        """
        current_board = Board.initialize_board()

        path = os.path.join(Board.TEST_INPUT_FILES_DIR, file_name)
        
        with open(path, 'r') as f:
            player = f.readline().strip()
            initial_configuration = f.readline().strip().split(',')

        print("Input board configuration:")
        print(initial_configuration)

        for marble in initial_configuration:
            x = int(marble[1]) - 5
            y = ord(marble[0]) - ord('E')
            current_board[(x, y)] = marble[2]

        return player, current_board

    @staticmethod
    def write_to_move_file(file_name, moves):
        """
        Writes an array of moves to a .move file.
        :param file_name: the name of the file to write to
        :param moves: an array of generated moves
        """
        path = os.path.join(Board.TEST_OUTPUT_FILES_DIR, f"{file_name}.move")

        with open(path, "w") as move_file:
            for move in moves:
                move_file.write(move + "\n")

    @staticmethod
    def write_to_board_file(file_name, states):
        """
        Writes an array of board configuration to a .board file.
        :param file_name: the name of the file to write to
        :param states: an array of board state
        """
        path = os.path.join(Board.TEST_OUTPUT_FILES_DIR, f"{file_name}.board")

        with open(path, "w") as state_file:
            for state in states:
                state_file.write(state + "\n")

    @staticmethod
    def tostring_board(board):
        """
        Converts the board state back to the input file format.

        :param board: Board dictionary {(x, y): 'b'/'w'/'N'}.
        :return: String formatted as the input file (player + marbles).
        """
        marble_list = []
        for (x, y), color in board.items():
            if color == 'N':
                continue  # Skip empty cells
            row = chr(y + 69)  # Convert y to row letter (A-I)
            column = x + 5  # Convert x to column number (1-9)
            marble_str = f"{row}{column}{color}"

            marble_list.append((color,row,column,marble_str)) # append tuple for sorting

        sorted_marbles = sorted(marble_list, key=lambda item: (item[0],item[1],item[2]))

        marble_strs = [item[3] for item in sorted_marbles]

        # return f"{player}\n{','.join(marble_strs)}"
        return f"{','.join(marble_strs)}"


