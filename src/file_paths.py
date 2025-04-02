"""Houses file paths and directories."""
import os
import sys
from enum import Enum
import time
from typing import Tuple

class FilePaths(Enum):
    """Represents the file paths for the running program."""
    PROJECT_ROOT =  os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser("~"))) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    TEST_INPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "input")
    VALID_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "valid_output")
    TEST_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "output")

    GAME_OUTPUT = os.path.join(PROJECT_ROOT, "Abalone")
    CONFIGURATION_FILE = os.path.join(GAME_OUTPUT, "config.json")
    MOVES = os.path.join(GAME_OUTPUT, "moves.txt")
    BOARD_INPUT = os.path.join(GAME_OUTPUT, "board_input.txt") # Where the agent reads its' moves (from the gui)
    BOARD_OUTPUT = os.path.join(GAME_OUTPUT, "board_output.txt") # Where the agent writes its' moves (to the gui)

    GAME_MAKER_EXE = os.path.join(PROJECT_ROOT, "Abalone.exe") # FIXME: The exe


def write_to_output_game_file(file_path: FilePaths, data: str):
    """
    Writes the game state to an output .txt file. Creates the file if it doesn't exist. Writes only to the first line
    in the file. Overwrites any data.

    This might be used to write the ai's generated move, or current board state in the format C5b, ...
    """
    with open(file_path.value, "w") as file:
        file.write(data)


def read_from_output_game_file(file_path: FilePaths, last_modified_time) -> Tuple[str, float]:
    """
    Reads a game state from an output .txt file. Reads the single first line.

    This might be used to read the output board configuration from the GUI, in the format C5b, ...

    :param file_path: the path of the file to read from as an enum
    :param last_modified_time: the last time the file has been read from
    :returns: the data in the file as a str and the timestamp from which it was modified
    """
    # Wait for the file to be created
    while not os.path.exists(file_path.value):
        print(f"File {file_path.value} not found.")
        time.sleep(0.1)

    # Wait for the file to be modified
    while True:
        current_modified_time = os.path.getmtime(file_path.value)
        print(f"Waiting for modifications to {file_path.value}.")

        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time

            with open(file_path.value, "r") as file:
                return (file.readline().strip(), last_modified_time)

        time.sleep(0.1)

