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

