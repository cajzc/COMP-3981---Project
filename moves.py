from board import Board

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
                        move_str += f"{direction}p({move_x}, {move_y}, {player}) "
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
                        move_str = ' + '.join(
                            f"({mx}, {my}, {player}){side_dir}({nx}, {ny}, {player})"
                            for (mx, my), (nx, ny) in zip(aligned_marbles, side_moved)
                        )
                        moves.append(move_str)

    return moves


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


def main():
    player, board = Board.get_input_board_representation("Test2.input")

    print("\nSingle Marble Moves:")
    for move in get_single_moves(player, board):
        print(move)

    print("\nInline Moves:")
    for move in get_inline_moves(player, board):
        print(move)

    print("\nSide-Step Moves:")
    for move in get_side_step_moves(player, board):
        print(move)

    print("\nBoard Representation:\n")
    print(Board.tostring_board(player, board))


if __name__ == '__main__':
    main()