"""Houses file paths and directories."""
from contextlib import AbstractAsyncContextManager
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

    # Main dir
    # GAME_OUTPUT = os.path.join(PROJECT_ROOT, "Abalone GameMaker")

    ABALONE_DIR = os.path.join(PROJECT_ROOT, "Abalone")

    # Exe
    GAME_MAKER_EXE = os.path.join(ABALONE_DIR, "Abalone.exe")

    # Files
    CONFIGURATION_FILE = os.path.join(ABALONE_DIR, "AbaloneConfig.json")
    MOVES = os.path.join(ABALONE_DIR, "moves.txt")
    BOARD_INPUT = os.path.join(ABALONE_DIR, "board_input.txt") # Where the agent reads its' moves (from the gui)
    BOARD_OUTPUT = os.path.join(ABALONE_DIR, "board_output.txt") # Where the agent writes its' moves (to the gui)



def write_to_output_game_file(file_path: FilePaths, data: str):
    """
    Writes the game state to an output .txt file. Creates the file if it doesn't exist. Writes only to the first line
    in the file. Overwrites any data.

    This might be used to write the ai's generated move, or current board state in the format C5b, ...
    """
    with open(file_path.value, "w", encoding="utf-8") as file:
        file.write(data)


def read_from_output_game_file(file_path: FilePaths, last_modified_time) -> Tuple[str, float]:
    """
    Reads a game state from an output .txt file. Reads the single first line.

    This might be used to read the output board configuration from the GUI, in the format C5b, ...

    :param file_path: the path of the file to read from as an enum
    :param last_modified_time: the last time the file has been read from
    :returns: the data in the file as a str and the timestamp from which it was modified
    """
    # Wait for the file to exist
    while not os.path.exists(file_path.value):
        print(f"File {file_path.value} not found. Waiting...")
        time.sleep(0.3)

    
    input("<Enter> to read opponent move")
    with open(file_path.value, "r", encoding="utf-8") as file:
        board_str = file.readline().strip()

        return board_str, last_modified_time  # Reads, updates, and keeps running

