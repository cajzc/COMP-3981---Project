"""Contains enums that the model uses."""

from enum import Enum, auto

class Marble(Enum):
    """Represents the possible marble colours."""
    BLACK = "b"
    WHITE = "w"

class GameModes(Enum):
    """Represents the gamemodes."""
    HUMAN = auto()
    RANDOM = auto()
    DIFF_HEURISTIC = auto()
    SAME_HEURISTIC = auto()
