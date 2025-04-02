"""Houses file paths and directories."""
import os
import sys
from enum import Enum


class FilePaths(Enum):
    """Represents the file paths for the running program."""
    PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    TEST_INPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "input")
    VALID_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "valid_output")
    TEST_OUTPUT_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files", "output")

    GAME_OUTPUT = os.path.join(PROJECT_ROOT, "game")
    CONFIGURATION_FILE = os.path.join(GAME_OUTPUT, "config.json")
    MOVES = os.path.join(GAME_OUTPUT, "moves.txt")
    BOARD_INPUT = os.path.join(GAME_OUTPUT, "board_input.txt")
    BOARD_OUTPUT = os.path.join(GAME_OUTPUT, "board_output.txt")


def write_to_output_game_file(file_path: FilePaths, data: str):
    """
    Writes the game state to an output .txt file. Creates the file if it doesn't exist. Writes only to the first line
    in the file. Overwrites any data.

    This might be used to write the ai's generated move, or current board state in the format C5b, ...
    """
    with open(file_path.value, "w") as file:
        file.write(data)


def read_from_output_game_file(file_path: FilePaths) -> str:
    """
    Reads a game state from an output .txt file. Reads the single first line.

    This might be used to read the output board configuration from the GUI, in the format C5b, ...
    """
    try:
        with open(file_path.value, "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        return ""

