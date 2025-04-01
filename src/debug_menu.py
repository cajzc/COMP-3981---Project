"""Houses a menu for debugging and testing the model."""

import os, sys
from typing import List, Set, Tuple, Dict, Optional, Any
from board import Board, BoardConfiguration
import state_space 
from minmax_agent import MinimaxAgent, AgentConfiguration
from enums import Marble, GameMode
from heuristic import c_heuristic, b_heuristic, heuristic, yz_heuristic
import json


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
    CONFIGURATION_FILE = os.path.join(PROJECT_ROOT, "game", "config.json")


    @staticmethod
    def options():
        """Displays the menu for Board debugging."""
        while True:
            print(
                "\nAgent debugging screen\n"
                "----------------------\n"
                "Options\n"
                "(1) Run model in Game Maker\n"
                "(2) Run model in Terminal\n"
                "(3) Generate boards from .input file(s)\n"
                "(4) Check if .board files are equal\n"
                "(5) Exit"
            )
            user_input = input("Enter: ").strip(",.?! ")
            match user_input:
                case "1":
                    DebugMenu._run_game_maker()
                case "2":
                    DebugMenu._run_terminal()
                    pass
                case "3":
                    DebugMenu._handle_input_files()
                case "4":
                    DebugMenu._handle_board_files()
                case "5":
                    print("Exiting program...")
                    break
                case _:
                    print("Invalid selection")

    @staticmethod
    def _run_game_maker():
        # Create the configuration
        agent = DebugMenu._create_mini_max_agent_from_file()
        if agent is None:
            print("Error creating agent. Returning to menu")
            return

        # Display the configuration
        DebugMenu._display_game_configuration(agent)
        # agent.run_game()
        # pass


    @staticmethod
    def _run_terminal():
        config= DebugMenu.get_game_configuration()
        print()

        agent = MinimaxAgent(
            config.board,
            config.player_colour,
            config,
            config.time_limit,
            config.depth,
        ) 
        if config.ai_human:
            print("Not yet implemented")
            return
        agent.run_game()

    
    @staticmethod
    def _get_board_configuration() -> Board:
        """
        Prompts the user to select the board configuration, returning their selected board configuration.

        :return: a Board object
        """
        while True:
            print(
                "Enter the board configuration\n"
                "(1) Default\n"
                "(2) Belgian Daisy\n"
                "(3) German Daisy"
            )

            user_input = input("Enter: ").strip(",.?! ")

            match user_input:
                case "1":
                    return Board.create_board(BoardConfiguration.DEFAULT)
                case "2":
                    return Board.create_board(BoardConfiguration.BELGIAN)
                case "3":
                    return Board.create_board(BoardConfiguration.GERMAN)
                case _:
                    print("Invalid selection. Please try again.")
                    continue

    @staticmethod
    def _get_player_colour() -> Marble:
        """
        Prompts the user to select the player turn ('b' or 'w'), returning the colour they select as an enum.

        :return: a Marble object
        """
        while True:
            player = input("Enter the player turn ('b' for black or 'w' for white, default 'b'): ").strip().lower()
            print("Note only select 'b' as of the development state") # TODO:
            if not player:  # No input, use default value 'b'
                return Marble("b")
            elif player in ["b", "w"]:
                return Marble(player)
            else:
                print("Invalid selection. Please enter 'b' for black or 'w' for white.")
                continue

    @staticmethod
    def _get_weights() -> list[float]:
        """
        Prompts the user to input custom weights, or use defaults if no input is provided.

        :return: a dictionary of weights
        """

        default_weights = {
            'center_distance': -0.5,
            'coherence': -0.3,
            # 'danger': -1.0,
            # 'opponent_break': 0.8,
            'score': -5.0,
            # 'triangle_formation': 1.0
        }

        weights = []

        print("Enter weights for the following parameters (Enter -1 to omit the weight. Enter <Enter> to use default values)")
        for key, default_value in default_weights.items():
            user_input_weight = input(f"{key} (default {default_value}): ").strip()
            if user_input_weight == "-1": # Skip the weight
                continue
            if not user_input_weight:  # No input, use default value
                weights.append(default_value)
            else:
                try:
                    weights.append(float(user_input_weight))
                except ValueError:
                    print(f"Invalid input for {key}, using default value of {default_value}.")
                    weights.append(default_value)

        return weights

    @staticmethod
    def _get_time_limit() -> int:
        """
        Prompts the user to input the time limit.

        :return: the time limit as an int
        """
        while True:
            user_input = input(f"Enter the time limit in seconds (default 5): ").strip()
            if not user_input:  # No input, use default value
                return 5
            try:
                time_limit = int(user_input)
                if time_limit > 0:
                    return time_limit
                else:
                    print("Time limit must be a positive integer. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the time limit.")

    @staticmethod
    def _get_depth() -> int:
        """
        Prompts the user to input the depth.

        :return: the depth of the search
        """
        while True:
            user_input = input(f"Enter the search depth (Enter `-1` for no depth. Enter <Enter> to use a default of 3): ").strip()
            if not user_input:  # No input, use default value
                return 3
            try:
                depth = int(user_input)
                if depth == -1 or depth > 0:
                    return depth
                else:
                    print("Invalid depth. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the depth.")


    @staticmethod
    def _get_game_mode() -> GameMode:
        """
        Prompts the user to select a game mode.

        :return: the selected GameMode as an enum
        """
        print("Select a game mode:\n"
            "1. Human\n"
            "2. Random\n"
            "3. Different Heuristic\n"
            "4. Same Heuristic")

        while True:
            user_input = input("Enter: ").strip()

            match user_input:
                case "1":
                    return GameMode.HUMAN
                case "2":
                    return GameMode.RANDOM
                case "3":
                    return GameMode.DIFF_HEURISTIC
                case "4":
                    return GameMode.SAME_HEURISTIC
                case _:
                    print("Invalid choice. Please enter a number between 1 and 4.")

    @staticmethod
    def get_game_configuration() -> AgentConfiguration:
        """
        Prompts a user for the game configuration.
        - AI vs AI (same heuristic)
        - AI vs AI (different heuristics)
        - AI vs Human
        - AI vs Random
        """
        print()
        board = DebugMenu._get_board_configuration()
        print()
        player_colour = DebugMenu._get_player_colour()
        print()
        time_limit = DebugMenu._get_time_limit()
        print()
        depth = DebugMenu._get_depth()
        print()

        while True:
            print(
                "(1) AI vs AI (Same Heuristic)\n"
                "(2) AI vs AI (Different Heuristic)\n"
                "(3) AI vs Human\n"
                "(4) AI vs Random\n"
            )
            user_input = input("Enter the Game Mode: ").strip()
            print()
            
            if user_input in ["1", "2", "3", "4"]:
                return AgentConfiguration(
                    player_colour,
                    board,
                    depth,
                    time_limit,
                    True if user_input == "1" else False,
                    True if user_input == "2" else False, # FIXME:
                    True if user_input == "3" else False,
                    True if user_input == "4" else False,
                    DebugMenu.get_heuristic("Select first heuristic:"),
                    DebugMenu._get_weights(),
                    DebugMenu.get_heuristic("Select second heuristic:") if user_input == "2" else None,
                    DebugMenu._get_weights() if user_input == "2" else None
                )
            else:
                print("Invalid selection. Please try again.")

    @staticmethod
    def get_heuristic(prompt: str):
        """
        Prompts the user to select a heuristic function, returning it.
        """
        while True:
            print(f"{prompt}\n(1) Main heuristic\n(2) c_heuristic\n(3) b_heuristic\n(4) yz_heuristic\n")
            heuristic_input = input("Enter your choice: ").strip()
            if heuristic_input == "1":
                return heuristic
            elif heuristic_input == "2":
                return c_heuristic
            elif heuristic_input == "3":
                return b_heuristic
            elif heuristic_input == "4":
                return yz_heuristic
            else:
                print("Invalid selection. Please try again.")


    @staticmethod
    def write_to_move_file(file_name, moves):
        """
        Writes an array of moves to a .move file.
        :param file_name: the name of the file to write to
        :param moves: an array of generated moves
        """
        print("file name", file_name)
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
   
        print(f"Moves saved to {DebugMenu.TEST_OUTPUT_FILES_DIR + "/" + file.strip(".input")}.move\nBoard saved to {DebugMenu.TEST_OUTPUT_FILES_DIR + "/" + file.strip(".input")}.board\n")


    @staticmethod
    def _create_mini_max_agent_from_file() -> Optional[MinimaxAgent]:
        """
        Creates a minimax agent with player and opponent configuratios from a json file.

        :returns: the MinimaxAgent object if no error, else None
        """
        return DebugMenu._load_configurations_from_file()


    @staticmethod
    def _load_configurations_from_file() -> Optional[MinimaxAgent]:
        """
        Loads a single player's configuration. Returning the Agent object.

        :returns: the MinimaxAgent object if no error, else None
        """
        #TODO: This should do polling
        if not os.path.exists(DebugMenu.CONFIGURATION_FILE):
            print(f"Configuration file {DebugMenu.CONFIGURATION_FILE} not found")
            return None
        with open(DebugMenu.CONFIGURATION_FILE, "r") as file:

            data = json.load(file)

            board = DebugMenu._get_board_from_file(data)
            player1_configuration = DebugMenu._create_configuration(data, 1)
            player2_configuration = DebugMenu._create_configuration(data, 2)

            depth = DebugMenu._get_depth()
            game_mode = DebugMenu._get_game_mode()

            if board is None:
                return None

            if player1_configuration is None:
                return None

            if player2_configuration is None:
                return None


            return MinimaxAgent(
                board,
                player1_configuration,
                player2_configuration,
                game_mode,
                depth
            )



    @staticmethod
    def _get_board_from_file(file) -> Optional[Board]:
        """
        Returns a setup Board object given a file input.

        :returns: the Board object if no error, else None
        """

        try:
            layout = file["initial_board_layout"]
        except KeyError:
            print(f"No attribute `initial_board_layout` in file")
            return None

        match layout:
            case "standard":
                board = Board.create_board(BoardConfiguration.DEFAULT)
            case "belgian":
                board = Board.create_board(BoardConfiguration.BELGIAN)
            case "german":
                board = Board.create_board(BoardConfiguration.GERMAN)
            case _:
                print(f"Error reading attribute `initial_board_layout` from {DebugMenu.CONFIGURATION_FILE}. Cannot parse {layout}")
                return None

        return board



    @staticmethod
    def _create_configuration(file, player_number:int) -> Optional[AgentConfiguration]:
        """
        Given a configuration json file and a player's colour, returns a single AgentConfiguration object.
        
        :param file: the configuration json file to read from
        :param player_number: the number of the player to read
        :returns: the configuration object if no error, else None
        """

        try:
            config = file[f"player{player_number}"]
            color = config["color"]
            if color not in ["w", "b"]: # Invalid format
                raise KeyError
            move_limit = config["move_limit"]
            time_limit = config["time_limit"]
            first_move = config["first_move"]
            player_colour = Marble(color)
        except (KeyError, ValueError) as e:
            print(f"Error reading player{player_number} configuration, {e}")
            return None

        return AgentConfiguration(
            player_colour,
            move_limit,
            time_limit,
            first_move

        )


    @staticmethod
    def _display_game_configuration(agent: MinimaxAgent):
        """
        Prints the configuration of the game.

        :param agent: the agent of the game to print configuration
        """

        print("\nGame Configuration")
        print("-------------")
        print("Depth:", agent.depth)
        print("Game Mode:", agent.game_mode)
        print("Board:", agent.board)
        first_move = "Agent" if agent.player_has_first_move else "Opponent"
        print("First move:", first_move)

        print("-------------")
        print("Agent Configuration")
        print("-------------")
        print("Colour:", agent.player_colour)
        print("Time Limit:", agent.player_time_limit)
        print("Move Limit:", agent.player_move_limit)
        if agent.heuristic and agent.heuristic_weights is not None:
            print("Heuristic:", agent.heuristic.__name__)
            print("Weights:", agent.heuristic_weights)

        print("-------------")
        print("Opponent Configuration")
        print("-------------")
        print("Colour:", agent.opponent_colour)
        print("Time Limit:", agent.opponent_time_limit)
        print("Move Limit:", agent.opponent_move_limit)
        if agent.opponent_heuristic and agent.opponent_heuristic_weights is not None:
            print("Heuristic:", agent.opponent_heuristic.__name__)
            print("Weights:", agent.opponent_heuristic_weights)


def _display_agent_configuration(self):
        """
        Displays the configuration of the agent, prompting a user to enter to begin the game.
        """
        print("\nCONFIGURATION")
        print("-------------")
        print("Depth: ", self.depth)
        print("Heuristic 1:", self.config.h1.__name__)
        print("Weights:", self.config.h1_weights)
        if self.config.h2:
            print("Heuristic 2:", self.config.h2.__name__)
            print("Weights:", self.config.h2_weights)
        print("-------------\n")
        input("Enter to begin")

