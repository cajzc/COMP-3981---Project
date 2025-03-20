import math

"""1. distance to center """
def distance_to_center(board,player):
    """
    Calculate the average Euclidean distance of a player's marbles to the board center.

    Args:
        board (dict): The game board represented as a dictionary of positions.
        player (str): The player ('b' for black, 'w' for white).

    Returns:
        float: The average distance to the center for the player's marbles.
    """
    xy_player = [(x, y) for (x, y), color in board.items() if color == player]

    avg_x = sum(x for x, y in xy_player) / len(xy_player)
    avg_y = sum(y for x, y in xy_player) / len(xy_player)

    return math.sqrt(avg_x ** 2 + avg_y ** 2)

""" 2. coherence, marbles stick together """
def marbles_coherence(board,player):
    """
    Measure the spatial coherence (clustering) of a player's marbles using variance.

    Args:
        board (dict): The game board represented as a dictionary of positions.
        player (str): The player ('b' or 'w').

    Returns:
        float: The average variance of marble positions (lower values indicate tighter clusters).
    """
    marbles = [(x, y) for (x, y), color in board.items() if color == player]
    x_positions = [x for x, y in marbles]
    y_positions = [y for x, y in marbles]

    mean_x = sum(x_positions) / len(x_positions)
    mean_y = sum(y_positions) / len(y_positions)

    # Calculate variance for x and y coordinates
    variance_x = sum((x - mean_x) ** 2 for x in x_positions) / len(x_positions)
    variance_y = sum((y - mean_y) ** 2 for y in y_positions) / len(y_positions)

    return (variance_x + variance_y) / 2

def marbles_in_danger(board, player):
    """
    Count the number of the player's marbles in danger (surrounded by opponent marbles).

    Args:
        board (dict): The game board.
        player (str): The player ('b' or 'w').

    Returns:
        int: Number of marbles at risk of being pushed off the board.
    """
    danger_count = 0
    opponent = 'w' if player == 'b' else 'b'

    for (x, y), color in board.items():
        if color == player:
            # Check adjacent positions for opponent marbles
            opponent_neighbors = 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]:
                if board.get((x + dx, y + dy)) == opponent:
                    opponent_neighbors += 1
            # A marble is considered in danger if surrounded by ≥2 opponent marbles
            if opponent_neighbors >= 2:
                danger_count += 1
    return danger_count

def break_opponent_formation(board, player):
    """
    Estimate the disruption to the opponent's formation caused by the player.

    Args:
        board (dict): The game board.
        player (str): The player ('b' or 'w').

    Returns:
        float: A score representing the opponent's loss of coherence due to the player's moves.
    """
    opponent = 'w' if player == 'b' else 'b'
    original_coherence = marbles_coherence(board, opponent)

    # Simplified metric: Assume each active marble reduces opponent's coherence
    # (This can be refined based on specific attack patterns)
    disrupted_coherence = sum(
        1 for (x, y), color in board.items()
        if color == player and (x, y) in opponent_territory(board, opponent)
    )

    return original_coherence - disrupted_coherence


def opponent_territory(board, opponent):
    """
    Identify positions considered the opponent's territory (advanced positions).

    Args:
        board (dict): The game board.
        opponent (str): The opponent's identifier.

    Returns:
        set: Coordinates (x, y) in the opponent's territory.
    """
    # Example: Define territory as positions where the opponent has ≥3 marbles
    opponent_marbles = [(x, y) for (x, y), color in board.items() if color == opponent]
    return {(x, y) for x, y in opponent_marbles if x + y > 1}  # Adjust based on strategy