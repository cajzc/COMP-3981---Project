""" this agent will use all the modules to generate a best move"""


class MinimaxAgent:
    """
    Game-playing agent using Minimax algorithm with alpha-beta pruning
    and configurable heuristic evaluation

    Attributes:
        depth (int): Search depth for minimax algorithm
        weights (dict): Weight values for heuristic components
    """

    def __init__(self, depth=3, weights=None):
        """
        Initialize minimax agent with search parameters

        Args:
            depth (int): Maximum search depth (default: 3)
            weights (dict): Heuristic component weights (default: predefined values)
        """
        self.depth = depth
        self.weights = weights or {
            'center_distance': -0.5,  # Negative weight (closer to center = better)
            'coherence': -0.3,  # Negative weight (lower variance = better)
            'danger': -1.0,  # Penalty for endangered marbles
            'opponent_break': 0.8,  # Reward for disrupting opponent
            'score': 2.0  # Direct score difference multiplier
        }