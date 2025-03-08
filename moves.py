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

def main():

    (player, board) = Board.get_input_board_representation("Test1.input")
    moves = get_single_moves(player, board)
    for move in moves:
        print(move)

if __name__ == '__main__':
    main()
