import math

"""1. distance to center """
def distance_to_center(board,player):
    xy_player = [(x,y) for (x,y), color in board.items() if color == player ]

    avg_x = sum(x for x,y in xy_player) / len(xy_player)
    avg_y = sum(y for x,y in xy_player) / len(xy_player)

    return math.sqrt(avg_x**2 + avg_y**2)

""" 2. coherence, marbles stick together """
def marbles_coherence(board,player):
    marbles = [(x,y) for (x,y),color in board.items() if color == player ]
    x_positions = [x for x, y in marbles]
    y_positions = [y for x, y in marbles]

    mean_x = sum(x_positions) / len(x_positions)
    mean_y = sum(y_positions) / len(y_positions)

    # Calculate deviation for x and y
    variance_x = sum((x - mean_x) ** 2 for x in x_positions) / len(x_positions)
    variance_y = sum((y - mean_y) ** 2 for y in y_positions) / len(y_positions)

    return (variance_x + variance_y) / 2

"""3. marbles in danger """
def marbles_in_danger(board,player):
    pass

"""4. break opponent formation """
def break_opponent_formation(board,player):
    pass
