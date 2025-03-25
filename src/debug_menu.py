"""Houses a menu for debugging and testing the model."""

import os, sys
from typing import List, Set, Tuple, Dict
from board import Board, BoardConfiguration
import state_space 
from minmax_agent import MinimaxAgent


class DebugMenu:
    """
    A menu for debugging and testing an abalone model. 
    Options include:
    - Generating moves from a .input file to a file
    - Generating moves from a given board representation (i.e., default, belgian, german) to a file
    """

    # Get the project root directory and test file paths
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller EXE
        PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.executable))
    else:  # Running as a regular Python script
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEST_INPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "input")
    VALID_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "valid_output")
    TEST_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "output")

    @staticmethod
    def options():
        """Displays the menu for Board debugging."""
        while True:
            print(
                "\nAgent debugging screen\n"
                "----------------------\n"
                "Options\n"
                "(1) Run model\n"
                "(2) Generate boards from .input file(s)\n"
                "(3) Check if .board files are equal\n"
                "(4) Exit\n"
            )
            user_input = input("Enter: ").strip(",.?! ")
            match user_input:
                case "1":
                    DebugMenu._run_model()
                case "2":
                    DebugMenu._handle_input_files()
                case "3":
                    DebugMenu._handle_board_files()
                case "4":
                    print("Exiting program...")
                    break
                case _:
                    print("Invalid selection")

    @staticmethod
    def _run_model():
        while True:
            print(
                "Enter the board configuration\n"
                "(1) Default\n"
                "(2) Belgian Daisy\n"
                "(3) German Daisy\n"
            )

            user_input = input("Enter: ").strip(",.?! ")

            match user_input:
                case "1":
                    board = Board.create_board(BoardConfiguration.DEFAULT)
                case "2":
                    board = Board.create_board(BoardConfiguration.BELGIAN)
                case "3":
                    board = Board.create_board(BoardConfiguration.GERMAN)
                case _:
                    print("Invalid selection")
                    continue

            player = input("Enter the player turn ('b' or 'w')")
            if player not in ["b", "w"]:
                print("Invalid selection")
                continue

            break
            

        agent = MinimaxAgent(board, player)

        agent.run_game()


    @staticmethod
    def write_to_move_file(file_name, moves):
        """
        Writes an array of moves to a .move file.
        :param file_name: the name of the file to write to
        :param moves: an array of generated moves
        """
        path = os.path.join(DebugMenu.TEST_OUTPUT_FILES_DIR, f"{file_name}.move")

        with open(path, "w", encoding="utf-8") as move_file:
            for move in moves:
                move_file.write(str(move) + "\n")

    @staticmethod
    def write_to_board_file(file_name: str, states: List[str]):
        path = os.path.join(DebugMenu.TEST_OUTPUT_FILES_DIR, f"{file_name}.board")
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
        path = os.path.join(DebugMenu.TEST_INPUT_FILES_DIR, f"{file_name}.input")
        with open(path, "w", encoding="utf-8") as input_file:
            input_file.write(colour + "\n")
            for line in Board.to_string_board(board):
                input_file.write(line)

    @staticmethod
    def boards_equal(file_name) -> Tuple[bool, Set[str]]:
        """
        Compares two ".board" files to check if they contain the same boards configurations, regardless of order.
        
        :param file_name: the file path of both files to check
        """
        output_file = os.path.join(DebugMenu.TEST_OUTPUT_FILES_DIR, file_name)
        valid_output_file = os.path.join(DebugMenu.VALID_OUTPUT_FILES_DIR, file_name)
        with open(output_file, 'r') as output, open(valid_output_file, 'r') as valid_output:
            output = {line.strip() for line in output.readlines()}
            valid_output = {line.strip() for line in valid_output.readlines()}
        
        differences = output - valid_output
        return output == valid_output, differences 
    
    
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
            
            if not DebugMenu._validate_file(user_input, "input", DebugMenu.TEST_INPUT_FILES_DIR): 
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
            return DebugMenu._file_exists(directory, file_name) and DebugMenu._file_exists(second_dir, file_name) 

        return DebugMenu._file_exists(directory, file_name) 
        

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
        user_input_files = DebugMenu.get_input_files_from_user() 
        if not user_input_files:
            return
        print("\nGenerated Boards\n")
        for file in user_input_files:
            DebugMenu.test_state_space(file)


    @staticmethod
    def _handle_board_files():
        """Handles a user input for comparing an outputted .board file with the valid .board file, displaying a response if equal or not."""
        while True:
            user_input = input("Enter the .board file to compare. (File names to compare should be equal) (Enter q to quit): ")
            if user_input == "q":
                break
            if not DebugMenu._validate_file(user_input, "board", DebugMenu.TEST_OUTPUT_FILES_DIR, DebugMenu.VALID_OUTPUT_FILES_DIR): 
                continue

            eq, board = DebugMenu.boards_equal(user_input)

            if eq:
                print("(SUCCESS) Files contain the same board")
            else:
                print("(ERROR) Files do not contain the same board!")
                print(f"test_output/{user_input} contains the following lines that valid_output/{user_input} does not: ", board)

    @staticmethod
    def get_input_board_representation(file_name: str) -> Tuple[str, Board]:
        """
        Reads a .input file. Where the first line is the player's turn and the second line is a comma-separated list of marble notations (e.g., "C5b").
        Instantiates a new board and converts them into cube coordinates and returns (player, marble_positions dictionary).

        :param file_name: the .input file to read from
        :return: the player and a Board object with new positions
        """
        path = os.path.join(DebugMenu.TEST_INPUT_FILES_DIR, file_name)
        with open(path, "r", encoding="utf-8") as f:
            player = f.readline().strip()
            marbles = f.readline().strip().split(',')

        board = Board()
        player, _ = board.get_input_board_representation(player, marbles)

        return player, board


    @staticmethod
    def test_state_space(file, board=None, player="b"):
        """
        Generates the state space and outputs to a file.
    
        :param file: the name of the output and optional .input file
        :param board: an optional board to preconfigure the state space with
        :param player: an optional player to initiate first ply, black by default
        """
        # FIXME:
        # if board is None: 
        #     player, positions, board = DebugMenu.get_input_board_representation(file)

        player, board = DebugMenu.get_input_board_representation(file)


        # Generate all possible moves
        all_moves = state_space.get_single_moves(player, board) + state_space.get_inline_moves(player, board) + state_space.get_side_step_moves(player, board)

        # Write moves to file
        DebugMenu.write_to_move_file(file.strip(".input"), all_moves)
    
        # Apply each move and write new board states
        move_file_path = os.path.join(DebugMenu.TEST_OUTPUT_FILES_DIR, f"{file.strip(".input")}.move")
        board_states = []
        with open(move_file_path, "r", encoding="utf-8") as f:
            move_lines = f.read().strip().splitlines()
            board_new = Board()

        for move in move_lines:
            # Create a fresh board from Test2.input.
            path = os.path.join(DebugMenu.TEST_INPUT_FILES_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                player = f.readline().strip()
                marbles = f.readline().strip().split(',')

            board_new.reset_board()
            board_new.get_input_board_representation(player, marbles)

            state_space.apply_move(board_new, move)
            # Recompute empty_positions after each move.
            board_new.empty_positions = {
                (q, r, s)
                for q in range(-4, 5)
                for r in range(-4, 5)
                for s in range(-4, 5)
                if q + r + s == 0 and (q, r, s) not in board_new.marble_positions.keys()
            }
            # Convert current board state to string and save it.
            state_str = board_new.to_string_board()
            board_states.append(state_str)


        # Write resulting board to file
        DebugMenu.write_to_board_file(file.strip(".input"), board_states)
   
        print(f"Moves saved to {DebugMenu.TEST_OUTPUT_FILES_DIR + "/" + file}.move\nBoard saved to {DebugMenu.TEST_OUTPUT_FILES_DIR + "/" + file}.board\n")

