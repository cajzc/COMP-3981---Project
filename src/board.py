"""Houses the board representation methods."""
import os
import sys
from typing import Tuple, Set
from state_space import *

class Board:
    """Holds the implementation to parse and output a board's representation."""

    # Get the project root directory and test file paths
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller EXE
        PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.executable))
    else:  # Running as a regular Python script
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEST_INPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "input")
    VALID_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "valid_output")
    TEST_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "output")

    @staticmethod
    def initialize_board():
        """
        Initialize the board with all positions as 'N' (neutral/empty)
        
        :returns: the game board representation as dictionary, where keys represent tuples of positions and values represent the value in the position
        """
        return {(x, y): 'N' for x in range(-4, 5) for y in range(-4, 5) if -4 <= x - y <= 4}

    @staticmethod
    def get_default_board():
        """
        Creates a standard Abalone board with the standard initial marble positions.
        
        :returns: Dictionary representing the standard board with initial marble positions
        """
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
    def get_belgian_daisy_board():
        """
        Creates a belgian daisy Abalone board with the standard initial marble positions.
        
        :returns: Dictionary representing the belgian daisy board with initial marble positions
        """

        # Initialize an empty board
        board = Board.initialize_board()

        black_marble_initial_pos = [
            # Group 1
            (-4, -4, 'b'), (-3, -4, 'b'),
            (-4, -3, 'b'), (-3, -3, 'b'), (-2, -3, 'b'),
            (-3, -2, 'b'), (-2, -2, 'b'),

            # Group 2
            (4, 4, 'b'), (3, 4, 'b'),
            (4, 3, 'b'), (3, 3, 'b'), (2, 3, 'b'),
            (3, 2, 'b'), (2, 2, 'b'),
        ]

        white_marbles_initial_pos = [
            # Group 1
            (0, -4, 'w'), (-1, -4, 'w'),
            (1, -3, 'w'), (0, -3, 'w'), (-1, -3, 'w'),
            (0, -2, 'w'), (1, -2, 'w'),

            # Group 2
            (0, 4, 'w'), (1, 4, 'w'),
            (-1, 3, 'w'), (0, 3, 'w'), (1, 3, 'w'),
            (-1, 2, 'w'), (0, 2, 'w')
        ]

        Board.place_marbles(black_marble_initial_pos, board)
        Board.place_marbles(white_marbles_initial_pos, board)

        return board


    @staticmethod
    def get_german_daisy_board():
        """
        Creates a german daisy Abalone board with the standard initial marble positions.
        
        :returns: Dictionary representing the german daisy board with initial marble positions
        """

         # Initialize an empty board
        board = Board.initialize_board()

        black_marble_initial_pos = [
            # Group 1
            (-4, -3, 'b'), (-3, -3, 'b'),
            (-4, -2, 'b'), (-3, -2, 'b'), (-2, -2, 'b'),
            (-3, -1, 'b'), (-2, -1, 'b'),

            # Group 2
            (4, 3, 'b'), (3, 3, 'b'),
            (4, 2, 'b'), (3, 2, 'b'), (2, 2, 'b'), 
            (3, 1, 'b'), (2, 1, 'b')
        ]

        white_marbles_initial_pos = [
            # Group 1
            (0, -3, 'w'), (1, -3, 'w'),
            (0, -2, 'w'), (1, -2, 'w'), (2, -2, 'w'),
            (1, -1, 'w'), (2, -1, 'w'),

            # Group 2
            (-1, 3, 'w'), (0, 3, 'w'),
            (-2, 2, 'w'), (-1, 2, 'w'), (0, 2, 'w'),
            (-2, 1, 'w'), (-1, 1, 'w')
        ]

        Board.place_marbles(black_marble_initial_pos, board)
        Board.place_marbles(white_marbles_initial_pos, board)

        return board


    @staticmethod
    def valid_position(x, y):
        """
        Returns whether a given set of coordinates is a valid position in our game board representation.

        :param x: the x coordinate as an int
        :param y: the x coordinate as an int
        :returns: true if valid else false

        >>> valid_position(4, 5)
        False
        >>> valid_position(-4, -4)
        True
        >>> valid_position(4, 6)
        False
        """
        return -4 <= x <= 4 and -4 <= y <= 4 and -4 <= (x - y) <= 4


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
        
        with open(path, 'r', encoding="utf-8") as f:
            player = f.readline().strip()
            initial_configuration = f.readline().strip().split(',')

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

        with open(path, "w", encoding="utf-8") as move_file:
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

        with open(path, "w", encoding="utf-8") as state_file:
            for state in states:
                state_file.write(state + "\n")

    @staticmethod
    def write_to_input_file(file_name, board, colour):
        """
        Writes a board into a new file as the .input format.
        :param file_name: the name of the file to write to
        :param board: Board dictionary {(x, y): 'b'/'w'/'N'}.
        :param colour: the starting player's colour
        """
        path = os.path.join(Board.TEST_INPUT_FILES_DIR, f"{file_name}.input")
        with open(path, "w", encoding="utf-8") as input_file:
            input_file.write(colour + "\n")
            for line in Board.to_string_board(board):
                input_file.write(line)


    @staticmethod
    def to_string_board(board):
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

    @staticmethod
    def boards_equal(file_name) -> Tuple[bool, Set[str]]:
        """
        Compares two ".board" files to check if they contain the same boards configurations, regardless of order.
        
        :param file_name: the file path of both files to check
        """
        output_file = os.path.join(Board.TEST_OUTPUT_FILES_DIR, file_name)
        valid_output_file = os.path.join(Board.VALID_OUTPUT_FILES_DIR, file_name)
        with open(output_file, 'r') as output, open(valid_output_file, 'r') as valid_output:
            output = {line.strip() for line in output.readlines()}
            valid_output = {line.strip() for line in valid_output.readlines()}
        
        differences = output - valid_output
        return output == valid_output, differences 

    @staticmethod
    def options():
        """Displays the menu for Board debugging."""
        while True:
            print(
                "\nAgent debugging screen\n"
                "----------------------\n"
                "Options\n"
                "(1) Generate boards from .input file(s)\n"
                "(2) Check if .board files are equal\n"
                "(3) Exit\n"
            )
            user_input = input("Enter: ").strip(",.?! ")
            match user_input:
                case "1":
                    Board._handle_input_files()
                case "2":
                    Board._handle_board_files()
                case "3":
                    print("Exiting program...")
                    break
                case _:
                    print("Invalid selection")

    
    @staticmethod
    def get_input_files_from_user():
        """
        Prompts the user to enter filenames ending with '.input' and stores them in a list.
        
        The function will continue asking for filenames until the user enters 'q', 'quit', or 'exit'.
        It validates that each filename ends with '.input' before adding it to the list.
        
        returns: a list of valid input filenames entered by the user
        """
        input_files = []
        print("\nInput file(s) selection\n")
        print("Options:")
        print("- Enter filenames ending with '.input' (one per line)")
        print("- Type 'q' to exit file selection menu\n")
        
        while True:
            user_input = input("Enter filename (or 'q' to quit file selection menu): ").strip()
            
            if user_input.lower() == "q":
                break
            
            if not Board._validate_file(user_input, "input", Board.TEST_INPUT_FILES_DIR): 
                continue

            # Add valid filename to the list
            input_files.append(user_input)
            print(f"Added: {user_input}")
        
        return input_files

    @staticmethod
    def _validate_file(file_name, file_extension, directory, second_dir = None):
        """
        Performs file validations.

        :param file_name: the name of the file
        :param file_extension: the extension of the file. With a ".input" file, an example param would be "input"
        :param directory: the directory of the file
        :return: True if validated else False
        """
        # Validate filename
        if not file_name.endswith(f'.{file_extension}'):
            print(f"Error: Filename must end with '.{file_extension}'")
            return False
        
        if second_dir:
            return Board._file_exists(directory, file_name) and Board._file_exists(second_dir, file_name) 

        return Board._file_exists(directory, file_name) 

        

    @staticmethod
    def _file_exists(directory, file_name):
        """
        Checks if a file exists given a directory.

        :param directory: the name of the directory
        :param file: the name of the file
        :return: whether the file exists or not
        """
        # Check if file exists in the input directory
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            print(f"(Warning) File '{file_name}' not found in {directory}")
            return False 

        return True


    @staticmethod
    def _handle_input_files():
        """Displays the menu to get input file(s) and generates them."""
        user_input_files = Board.get_input_files_from_user() 
        if not user_input_files:
            return
        print("\nGenerated Boards\n")
        for file in user_input_files:
            Board.test_state_space(file)

    @staticmethod
    def _handle_board_files():
        """Handles a user input for comparing an outputted .board file with the valid .board file, displaying a response if equal or not."""
        while True:
            user_input = input("Enter the .board file to compare. (File names to compare should be equal) (Enter q to quit): ")
            if user_input == "q":
                break
            if not Board._validate_file(user_input, "board", Board.TEST_OUTPUT_FILES_DIR, Board.VALID_OUTPUT_FILES_DIR): 
                continue

            eq, board = Board.boards_equal(user_input)

            if eq:
                print("(SUCCESS) Files contain the same board")
            else:
                print("(ERROR) Files do not contain the same board!")
                print(f"test_output/{user_input} contains the following lines that valid_output/{user_input} does not: ", board)


    @staticmethod
    def test_state_space(file, board=None, player="b"):
        """
        Generates the state space and outputs to a file.
    
        :param file: the name of the output and optional .input file
        :param board: an optional board to preconfigure the state space with
        :param player: an optional player to initiate first ply, black by default
        """
        if board is None:
            player, board = Board.get_input_board_representation(file)

        # Generate all possible moves
        all_moves = get_single_moves(player, board) + get_inline_moves(player, board) + get_side_step_moves(player, board)
        file = file.strip(".input")

        # Write moves to file
        Board.write_to_move_file(file, all_moves)
    
        # Apply each move and write new board states
        new_states = []
        for move in all_moves:
            new_board = board.copy()
            apply_move(new_board, move)
            new_states.append(Board.to_string_board(new_board))

        # Write resulting board to file
        Board.write_to_board_file(file, new_states)
   
        print(f"Moves saved to {Board.TEST_OUTPUT_FILES_DIR + "/" + file}.move\nBoard saved to {Board.TEST_OUTPUT_FILES_DIR + "/" + file}.board\n")

def local_tests():
    """Tests the state space for development/debugging purposes."""
    # Input & Output files
    input_file_one = "Test1"
    input_file_two = "Test2"

    belgian_output_white = "test_belgian_white_first"
    belgian_output_black = "test_belgian_black_first"
    german_output_white = "test_german_white_first"
    german_output_black = "test_german_black_first"

    belgian_daisy_board = Board.get_belgian_daisy_board()
    german_daisy_board = Board.get_german_daisy_board()

    # Tests
    Board.test_state_space(input_file_one)
    Board.test_state_space(input_file_two)
    Board.test_state_space(belgian_output_white, belgian_daisy_board, "w")
    Board.test_state_space(belgian_output_black, belgian_daisy_board)
    Board.test_state_space(german_output_white, german_daisy_board, "w")
    Board.test_state_space(german_output_black, german_daisy_board, "b")

