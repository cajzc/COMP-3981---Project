import re
from dataclasses import dataclass, field
from typing import List, Tuple

DIRECTIONS = {
    '→':  (1,  0, -1),  # East
    '↗':  (1, -1,  0),  # Northeast
    '↖':  (0, -1,  1),  # Northwest
    '←':  (-1, 0,  1),  # West
    '↙':  (-1, 1,  0),  # Southwest
    '↘':  (0,  1, -1),  # Southeast
}

@dataclass
class Move:
    """
    Represents a move in (q,r,s) coordinates with a known direction arrow
    (e.g. '→','↗','↖','←','↙','↘') and a move_type to differentiate
    single/inline/side-step/push, etc.
    """
    player: str  # 'b' or 'w'
    direction: str | None = None  # arrow symbol from DIRECTIONS (e.g. '→')
    move_type: str = "single"  # 'single','inline','side_step','push'

    moved_marbles: List[Tuple[int, int, int, str]] = field(default_factory=list)
    dest_positions: List[Tuple[int, int, int, str]] = field(default_factory=list)

    push: bool = False
    pushed_off: bool = False
    pushed_marbles: List[Tuple[int, int, int, str]] = field(default_factory=list)
    pushed_dest_positions: List[Tuple[int, int, int, str]] = field(default_factory=list)

    def __str__(self) -> str:
        """
        Builds notation showing the arrow (self.direction) and a suffix
        for move_type ('s','i','p', etc.), while matching the number of marbles.

        Expected outputs:

          - Single (direction='→'):
              "b: (0,0,0,b)→(1,0,-1,b)"

          - Side-step (direction='→'), 2 marbles:
              "w: (0,1,-1,w)-(0,2,-2,w)→s(1,1,-2,w)-(1,2,-3,w)"
              (The marbles, originally aligned along ↘, side-step east by adding (1,0,-1).)

          - Inline (direction='↗'), 2 marbles:
              "b: (0,0,0,b)-(1,-1,0,b)↗i(1,-1,0,b)-(2,-2,0,b)"

          - Push (direction='→'):
              # Example 1: Two marbles pushing one opponent marble:
              "b: (0,0,0,b)-(1,0,-1,b)→p(2,0,-2,w)"

              # Example 2: Three marbles pushing two opponent marbles:
              "b: (0,0,0,b)-(1,0,-1,b)-(2,0,-2,b)→p(3,0,-3,w)-(4,0,-4,w)"
        """

        def marble_str(q, r, s, c):
            return f"({q},{r},{s},{c})"

        # 1) Base arrow from self.direction (using DIRECTIONS) or "??" if invalid.
        arrow = self.direction if (self.direction in DIRECTIONS) else "??"

        # 2) Append suffix for move_type:
        #    "single" => no suffix,
        #    "inline" => "i",
        #    "side_step" => "s",
        #    "push" => "p",
        #    Otherwise, add "?".
        match self.move_type:
            case "inline":
                arrow += "i"
            case "side_step":
                arrow += "s"
            case "push":
                arrow += "p"
            case "single":
                pass
            case _:
                arrow += "?"

        # 3) Build the "moved" chain.
        moved_chain = "-".join(marble_str(*m) for m in self.moved_marbles)

        # 4) Build the "destination" chain.
        dest_chain = "-".join(marble_str(*pos) for pos in self.dest_positions)

        # 5) If push, simply join the pushed marbles.
        if self.push or self.move_type == "push":
            opp_chain = "-".join(marble_str(*pos) for pos in self.pushed_marbles)
            return f"{moved_chain}{arrow}{opp_chain}"

        # 6) Otherwise, show moved -> destination.
        return f"{moved_chain}{arrow}{dest_chain}"

def opposite_direction(direction):
    """Returns the opposite direction symbol."""
    opposite_map = {
        '→': '←',
        '←': '→',
        '↖': '↘',
        '↘': '↖',
        '↗': '↙',
        '↙': '↗'}
    return opposite_map.get(direction, None)
