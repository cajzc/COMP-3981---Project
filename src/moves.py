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

# get to a single neighbor position align one direction
def neighbor(pos, direction):
    q, r, s = pos
    dq, dr, ds = DIRECTIONS[direction]
    return q + dq, r + dr, s + ds


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

def get_single_moves(player: str, board_obj) -> List[Move]:
    """
    Generates all valid single-marble moves for the given player,
    using board_obj.marble_positions for occupied cells and
    board_obj.empty_positions for empties.

    A move is valid if, for a marble at (q,r,s) belonging to player,
    one of the six neighbors (computed via DIRECTIONS) is in board_obj.empty_positions.
    """
    moves = []
    for (q, r, s), color in board_obj.marble_positions.items():
        if color != player:
            continue
        for dir_symbol, (dq, dr, ds) in DIRECTIONS.items():
            new_pos = (q + dq, r + dr, s + ds)
            if new_pos in board_obj.empty_positions:
                move_obj = Move(
                    player=player,
                    direction=dir_symbol,
                    moved_marbles=[(q, r, s, color)],
                    dest_positions=[(new_pos[0], new_pos[1], new_pos[2], color)]
                )
                moves.append(move_obj)
    return moves

def get_inline_moves(player, board):
    """Generate all valid inline moves for 2-3 marbles (excluding illegal Sumito pushes)."""
    moves = []
    opponent = 'b' if player == 'w' else 'w'

    for (x, y), color in board.items():
        if color != player:
            continue

        for direction, (dx, dy) in DIRECTIONS.items():
            inline_marbles = [(x, y)]  # Start with the current marble

            # Check if 2 or 3 marbles are aligned in the given direction
            for i in range(1, 3):  # Check up to 3 marbles
                nx, ny = x + dx * i, y + dy * i
                if (nx, ny) in board and board[(nx, ny)] == player:
                    inline_marbles.append((nx, ny))
                else:
                    break  # Stop if we hit an opponent or empty space

            if len(inline_marbles) >= 2:  # Only consider inline moves for 2+ marbles
                # Check if the move destination is empty or has an opponent marble
                move_x, move_y = inline_marbles[-1][0] + dx, inline_marbles[-1][1] + dy

                if (move_x, move_y) not in board:
                    continue  # Move is out of bounds

                destination = board[(move_x, move_y)]

                # **Check if move is valid**
                if destination == 'N':  # ✅ Can move into empty space
                    move_str = '-'.join(f"({mx}, {my}, {player})" for mx, my in inline_marbles)
                    move_str += f"{direction}({move_x}, {move_y}, {player})"
                    moves.append(move_str)

                elif destination != player:  # Encounter an opponent marble
                    opponent_marbles = [(move_x, move_y)]
                    no_adjacent = True
                    for i in range(1, 3):  # Check up to 2 opponent marbles ahead
                        next_x, next_y = move_x + dx * i, move_y + dy * i
                        if (next_x, next_y) in board and board[(next_x, next_y)] == opponent:
                            opponent_marbles.append((next_x, next_y))
                        elif (next_x, next_y) in board and board[(next_x, next_y)] == player:
                            no_adjacent = False
                        else:
                            break

                    if len(inline_marbles) > len(opponent_marbles) and len(opponent_marbles) <= 2 and no_adjacent:
                        # ✅ Push is valid if more pushing marbles & <=2 opponent marbles
                        move_str = '-'.join(f"({mx}, {my}, {player})" for mx, my in inline_marbles)
                        move_str += (f"{direction}"
                                     f"p{'-'.join(f'({ox}, {oy}, {board[(ox, oy)]})' for ox, oy in opponent_marbles)}")
                        moves.append(move_str)

    return moves


def get_side_step_moves(player, board):
    """Generate all valid side-step moves for 2-3 aligned marbles."""
    moves = []
    processed_groups = set()  # To keep track of already processed aligned marble groups

    for (x, y), color in board.items():
        if color != player:
            continue

        for direction, (dx, dy) in DIRECTIONS.items():
            aligned_marbles = [(x, y)]  # Start with the current marble
            aligned_marble_group = {(x, y)}

            # Check if 2 or 3 marbles are aligned (in x, y, or x-y direction)
            for i in range(1, 3):  # Check up to 3 marbles in a row
                nx, ny = x + dx * i, y + dy * i
                if (nx, ny) in board and board[(nx, ny)] == player:
                    aligned_marbles.append((nx, ny))
                    aligned_marble_group.add((nx, ny))
                else:
                    break

            # Skip already processed aligned marble groups
            if frozenset(aligned_marble_group) in processed_groups:
                continue
            processed_groups.add(frozenset(aligned_marble_group))

            if len(aligned_marbles) >= 2:  # Only consider side-step moves for 2+ marbles
                for side_dir, (sx, sy) in DIRECTIONS.items():  # Try all side-step directions
                    if side_dir == direction or side_dir == opposite_direction(direction):
                        continue  # Skip in-line directions

                    side_moved = []
                    for mx, my in aligned_marbles:
                        new_x, new_y = mx + sx, my + sy
                        if (new_x, new_y) in board and board[(new_x, new_y)] == 'N':
                            side_moved.append((new_x, new_y))
                        else:
                            break

                    if len(side_moved) == len(aligned_marbles):  # All marbles can move
                        move_str = '-'.join(
                            f"({mx}, {my}, {player})" for mx, my in aligned_marbles
                        ) + f"{side_dir}s" + '-'.join(
                            f"({nx}, {ny}, {player})" for (nx, ny) in side_moved
                        )
                        moves.append(move_str)

    return moves

def apply_move(board, move_str):
    """
    Applies a move to the given board and updates it in place.

    :param board: The board dictionary {(x, y): 'b'/'w'/'N'}.
    :param move_str: Move string in the format "(x1, y1, color)→(x2, y2, color)"
    :return: None (board is updated in place).
    """
    # Extract direction from move_str
    direction = next((d for d in DIRECTIONS if d in move_str), None)
    if not direction:
        raise ValueError(f"Invalid move format: {move_str}")

    dx, dy = DIRECTIONS[direction]

    # Extract moving marbles from move string
    marble_parts = move_str.split(direction)

    # Extract (x, y, color) tuples using regex
    marble_pattern = r"\((-?\d+), (-?\d+), (\w)\)"
    marbles_str_list = re.findall(marble_pattern, marble_parts[0])
    marbles = [(int(x), int(y), color) for x, y, color in marbles_str_list]
    player = marbles[0][2]

    # Determine if it's an inline push
    last_marble = marbles[-1][:2]  # (x, y) only
    push_pos = (last_marble[0] + dx, last_marble[1] + dy)

    opponent_marbles = []
    while push_pos in board and board[push_pos] not in ('N', player):
        opponent_marbles.append(push_pos)
        push_pos = (push_pos[0] + dx, push_pos[1] + dy)

    # Validate Sumito push
    if len(marbles) > len(opponent_marbles) and len(opponent_marbles) <= 2:
        # Move opponent marbles one step further
        for ox, oy in reversed(opponent_marbles):  # Start from the last in the line
            new_ox, new_oy = ox + dx, oy + dy
            if (new_ox, new_oy) in board:
                # If still on board, move it
                board[(new_ox, new_oy)] = 'b' if player == 'w' else 'w'
            else:  # If out of board, remove it (pushed off)
                pass #update score here

    # move one by one and let the previous position be 'N'
    for x,y,color in reversed(marbles):
        board[(x, y)] = 'N'
        board[(x + dx, y + dy)] = color

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
