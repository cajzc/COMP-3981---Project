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

    def __init__(self):
        self.marble_positions = {} # (q,r,s):color only store marbles in the dict saving space
        self.empty_positions = set((q,r,s) for q in range(-4,5)
                                           for r in range(-4,5)
                                           for s in range(-4,5)
                                           if q+r+s == 0)

    def reset_board(self):
        """
        Resets the board by clearing all marble positions and regenerating empty positions.
        """
        self.marble_positions.clear()
        self.empty_positions = set(
            (q, r, s) for q in range(-4, 5)
            for r in range(-4, 5)
            for s in range(-4, 5)
            if q + r + s == 0
        )

    def set_default_board(self):
        """
        Creates a standard Abalone board with black marbles on the bottom
        (rows A–C) and white marbles on top (rows G–I).
        """
        # Black marble initial positions (bottom 3 rows)
        black_marble_initial_pos = [
            # Row A (r=+4), cols 1..5 => q=-4..0, s=-q-r
            (-4, 4, 0), (-3, 4, -1), (-2, 4, -2), (-1, 4, -3), (0, 4, -4),
            # Row B (r=+3), cols 1..6 => q=-4..1
            (-4, 3, 1), (-3, 3, 0), (-2, 3, -1), (-1, 3, -2), (0, 3, -3), (1, 3, -4),
            # Row C (r=+2), cols 4..6 => q=-1..1
            (-1, 2, -1), (0, 2, -2), (1, 2, -3)
        ]

        # White marble initial positions (top 3 rows)
        white_marble_initial_pos = [
            # Row G (r=-2), cols 4..6 => q=-1..1
            (-1, -2, 3), (0, -2, 2), (1, -2, 1),
            # Row H (r=-3), cols 4..9 => q=-1..4
            (-1, -3, 4), (0, -3, 3), (1, -3, 2), (2, -3, 1), (3, -3, 0), (4, -3, -1),
            # Row I (r=-4), cols 5..9 => q=0..4
            (0, -4, 4), (1, -4, 3), (2, -4, 2), (3, -4, 1), (4, -4, 0)
        ]

        self.reset_board()

        # Place black marbles
        for pos in black_marble_initial_pos:
            self.marble_positions[pos] = 'black'

        # Place white marbles
        for pos in white_marble_initial_pos:
            self.marble_positions[pos] = 'white'

        # Remove these positions from empty_positions
        self.empty_positions -= set(black_marble_initial_pos + white_marble_initial_pos)

    def set_belgian_daisy_board(self):
        """
        Places the Belgian Daisy layout with Black marbles on rows near A
        and White marbles on rows near I, using (q,r,s) with row A=+4, row I=-4.
        """

        # -----------------------------
        # Black marbles (two 'daisies' at the bottom left and top right)
        # -----------------------------
        black_marble_initial_pos = [
            # Bottom-left daisy (rows A to C):
            # Row A 
            (-4, 4, 0), (-3, 4, -1),
            # Row B 
            (-4, 3, 1), (-3, 3, 0), (-2, 3, -1),
            # Row C 
            (-3, +2, +1), (-2, +2, 0),

            # Top-right daisy (rows I to G):
            # Row I 
            (3, -4, 1), (4, -4, 0),
            # Row H 
            (2, -3, 1), (3, -3, 0), (4, -3, -1),
            # Row G 
            (2, -2, 0), (3, -2, -1)
        ]

        # -----------------------------
        # White marbles (two 'daisies' at the bottom right and top left)
        # -----------------------------
        white_marbles_initial_pos = [
            # Bottom-right daisy (rows A to C):
            # Row A 
            (-1, 4, -3), (0, 4, -4),
            # Row B 
            (-1, 3, -2), (0, 3, -3), (1, 3, -4),
            # Row C 
            (0, 2, -2), (1, 2, -3),

            # Top-left daisy (rows I to G):
            # Row I 
            (0, -4, 4), (1, -4, 3),
            # Row H 
            (-1, -3, 4), (0, -3, 3), (1, -3, 2),
            # Row G 
            (-1, -2, 3), (0, -2, 2)
        ]

        # Clear and place on board
        self.reset_board()
        for pos in black_marble_initial_pos:
            self.marble_positions[pos] = 'black'
        for pos in white_marbles_initial_pos:
            self.marble_positions[pos] = 'white'
        self.empty_positions -= set(black_marble_initial_pos + white_marbles_initial_pos)

    def set_german_daisy_board(self):
        """
        Places the German Daisy layout with Black on bottom daisies,
        White on top daisies, under the same row A=+4 -> row I=-4 orientation.
        """

        # -----------------------------
        # Black marbles (two arcs near the bottom-left and top-right)
        # -----------------------------
        black_marble_initial_pos = [
            # Bottom-left arc
            (-4, 3, 1), (-3, 3, 0),
            (-4, 2, 2), (-3, 2, 1), (-2, 2, 0),
            (-3, 1, 2), (-2, 1, 1),


            # Top-right arc
            (3, -3, 0), (4, -3, -1),
            (2, -2, 0), (3, -2, -1), (4, -2, 0),
            (2, -1, -1), (3, -1, -2)
        ]

        # -----------------------------
        # White marbles (two arcs near the top-left and bottom-right)
        # -----------------------------
        white_marbles_initial_pos = [
            # Bottom-right arc
            (1, 1, -2), (2, 1, -3),
            (0, 2, -2), (1, 2, -3), (2, 2, -4),
            (0, 3, -3), (1, 3, -4),

            # Top-left arc
            (-1, -3, 4), (0, -3, 3),
            (-2, -2, 4), (-1, -2, 3), (0, -2, 2),
            (-2, -1, 3), (-1, -1, 2)
        ]

        # Clear and place on board
        self.reset_board()
        for pos in black_marble_initial_pos:
            self.marble_positions[pos] = 'black'
        for pos in white_marbles_initial_pos:
            self.marble_positions[pos] = 'white'
        self.empty_positions -= set(black_marble_initial_pos + white_marbles_initial_pos)

    def place_marbles(self, coloured_marbles):
        """
        Places marbles on the board at specified positions with specified colours.

        :param coloured_marbles: List of tuples (q, r, s, colour) where q, r, s are coordinates and colour is 'b', 'w'
        """
        for (q, r, s, colour) in coloured_marbles:
            self.marble_positions[(q, r, s)] = colour
            self.empty_positions.discard((q, r, s))

    def get_input_board_representation(self, file_name):
        """
        Reads an input board configuration from a file and converts it into the team's board format.

        :param file_name: the name of the input file
        :returns: tuple containing (player turn, game board representation as dictionary)
        """
        self.reset_board()
        path = os.path.join(self.TEST_INPUT_FILES_DIR, file_name)

        with open(path, 'r', encoding="utf-8") as f:
            player = f.readline().strip()
            marbles = f.readline().strip().split(',')

        for marble in marbles:
            q = int(marble[1]) - 5
            r = ord('E') - ord(marble[0])
            s = -q-r
            self.marble_positions[(q, r, s)] = marble[2]
            self.empty_positions.discard((q, r, s))

        return player

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
                move_file.write(str(move) + "\n")

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

    def to_string_board(self):
        """
        Converts the board's marble_positions (q,r,s -> 'b'/'w') into a
        comma-separated string like 'A1b,A2b,...'.
        Uses the row mapping: r=+4 -> 'A' down to r=-4 -> 'I',
        and the column mapping: q=-4 -> col=1 up to q=+4 -> col=9.
        """
        marble_list = []
        for (q, r, s), color in self.marble_positions.items():
            # Convert r to row letter: A=+4, B=+3, ... I=-4
            row_letter = chr(ord('A') + (4 - r))
            # Convert q to column (1..9)
            col_number = q + 5

            # Build something like "A2b" or "C3w"
            notation = f"{row_letter}{col_number}{color}"

            # Keep a tuple for sorting: (color, row_letter, col_number, "A2b")
            marble_list.append((color, row_letter, col_number, notation))

        # Sort by color first, then row letter, then column
        sorted_marbles = sorted(marble_list, key=lambda item: (item[0], item[1], item[2]))

        # Return just the comma-separated notation pieces
        return ",".join(item[3] for item in sorted_marbles)

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

def main():
    board = Board()
    player = board.get_input_board_representation("Test1.input")
    print(player)
    print(board.marble_positions)
    print(board.to_string_board())
    singe_moves = get_single_moves(player,board)
    inline_moves = get_inline_moves(player,board)
    side_step_moves = get_side_step_moves(player,board)
    moves = singe_moves + inline_moves + side_step_moves
    for move in moves:
        print(move)
    Board.write_to_move_file("test1.txt", moves)


if __name__ == "__main__":
    main()


