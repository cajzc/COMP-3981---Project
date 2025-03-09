from board import Board
from moves import get_single_moves, get_inline_moves, get_side_step_moves, apply_move


def main():
    player, board = Board.get_input_board_representation("../test_files/Test1.input")

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
    print(Board.tostring_board(board))


    print("\nBefore Move:")
    print(Board.tostring_board(board))

    move = "(0, -1, b)-(1, 0, b)-(2, 1, b)↗p(3, 2, w)-(4, 3, w)"  # Example move
    apply_move(board, move)  # Directly modifies board

    print("\nAfter Move:")
    print(Board.tostring_board(board))


if __name__ == '__main__':
    main()