import re

DIRECTIONS = {
    '→': (1, 0),    # +x
    '←': (-1, 0),   # -x
    '↖': (0, 1),    # +y
    '↘': (0, -1),   # -y
    '↗': (1, 1),    # +x+y
    '↙': (-1, -1)   # -x-y
}

def get_single_moves(player, board):
    """Generate all valid single marble moves"""
    moves = []
    current_color = player

    for (x,y),color in board.items():
        if color != current_color:
            continue

        for direction,(dx,dy) in DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in board and board[(new_x, new_y)] == 'N':
                # Format: (x1,y1,color)→(x2,y2,color)
                move_str = f"({x}, {y}, {current_color}){direction}({new_x}, {new_y}, {current_color})"
                moves.append(move_str)
    return moves


def get_inline_moves(player, board):
    """Generate all valid inline moves for 2-3 marbles (excluding illegal Sumito pushes)."""
    moves = []

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
                    for i in range(1, 3):  # Check up to 2 opponent marbles ahead
                        next_x, next_y = move_x + dx * i, move_y + dy * i
                        if (next_x, next_y) in board and board[(next_x, next_y)] not in ('N', player):
                            opponent_marbles.append((next_x, next_y))
                        else:
                            break

                    if len(inline_marbles) > len(opponent_marbles) and len(opponent_marbles) <= 2:
                        # ✅ Push is valid if more pushing marbles & <=2 opponent marbles
                        move_str = '-'.join(f"({mx}, {my}, {player})" for mx, my in inline_marbles)
                        move_str += (f"{direction}"
                                     f"p{'-'.join(f'({ox}, {oy}, {board[(ox, oy)]})' for ox, oy in opponent_marbles)}")
                        moves.append(move_str)

    return moves


def get_side_step_moves(player, board):
    """Generate all valid side-step moves for 2-3 aligned marbles."""
    moves = []

    for (x, y), color in board.items():
        if color != player:
            continue

        for direction, (dx, dy) in DIRECTIONS.items():
            aligned_marbles = [(x, y)]  # Start with the current marble

            # Check if 2 or 3 marbles are aligned (in x, y, or x-y direction)
            for i in range(1, 3):  # Check up to 3 marbles in a row
                nx, ny = x + dx * i, y + dy * i
                if (nx, ny) in board and board[(nx, ny)] == player:
                    aligned_marbles.append((nx, ny))
                else:
                    break

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
    print(marble_parts[0]) #for debug

    # Extract (x, y, color) tuples using regex
    marble_pattern = r"\((-?\d+), (-?\d+), (\w)\)"
    marbles_str_list = re.findall(marble_pattern, marble_parts[0])
    marbles = [(int(x), int(y), color) for x, y, color in marbles_str_list]
    player = marbles[0][1]

    print(marbles) # for debug

    # Determine if it's an inline push
    last_marble = marbles[-1][:2]  # (x, y) only
    push_pos = (last_marble[0] + dx, last_marble[1] + dy)
    print(push_pos) #for debug

    opponent_marbles = []
    while push_pos in board and board[push_pos] not in ('N', player):
        opponent_marbles.append(push_pos)
        push_pos = (push_pos[0] + dx, push_pos[1] + dy)
    print(opponent_marbles)  # for debug

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

    # Move the player's marbles
    for x, y, color in reversed(marbles):
        new_x, new_y = x + dx, y + dy
        board[(new_x, new_y)] = board.pop((x, y))

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
