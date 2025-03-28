""" this agent will use all the modules to generate a best move"""
from state_space import GameState, apply_move_dict, generate_move, terminal_test, generate_move_dict
from transposition_tables import TranspositionTable
from typing import List, Tuple, Dict, Set
from moves import Move
import  math
import time 
from heuristic import heuristic, c_heuristic
from enums import Marble
from board import Board
import random

class AgentConfiguration:
    """
    Contains data attributes related to a game configuration.
    """


    def __init__(self,
                 ai_player: bool,
                 ai_same_heuristic: bool,
                 ai_diff_heuristic: bool,
                 ai_random: bool,
                 h1= None,
                 h2= None,
                 h1_weights= None,
                 h2_weights= None,
                 ):

        """
        A configuration for an abalone playing agent.

        :param ai_player: True if the model should run ai vs player (user input)
        :param ai_same_heuristic: True if the model should run ai vs its own heuristic
        :param ai_diff_heuristic: True if the model should run two different heuristics
        :param ai_random: True if the model should run ai vs random moves
        """
        self.ai_player = ai_player
        self.ai_same_heuristic = ai_same_heuristic
        self.ai_diff_heuristic = ai_diff_heuristic
        self.ai_random = ai_random
        self.h1 = h1
        self.h2 = h2


class MinimaxAgent:
    """
    Game-playing agent using Minimax algorithm with alpha-beta pruning
    and configurable heuristic evaluation

    Attributes:
        depth (int): Search depth for minimax algorithm
        weights (dict): Weight values for heuristic components
        transposition_table (TranspositionTable): Cache for game state evaluations
    """

    def __init__(self,
                 board: Board,
                 player_colour: Marble,
                 config: AgentConfiguration,
                 time_limit=5,
                 depth=3,
                 weights=None):
        self.transposition_table = TranspositionTable()
        """
        Initialize minimax agent with search parameters

        :param board: the initial configuration of the Abalone game board
        :param player_colour: the colour of the player as an enum
        :param depth:  maximum search depth (default: 3)
        :param weights: heuristic component weights as a dict 
        """
        self.board = board
        self.board_dict = board.marble_positions
        self.player_colour = player_colour.value
        self.time_limit = time_limit
        self.depth = depth
        self.weights = weights or {
            'center_distance': -0.5,  # Negative weight (closer to center = better)
            'coherence': -0.3,  # Negative weight (lower variance = better)
            'danger': -1.0,  # Penalty for endangered marbles
            'opponent_break': 0.8,  # Reward for disrupting opponent
            'score': 2.0,  # Direct score difference multiplier
            'triangle_formation': 1.0  # Multiplier for obtaining a triangle formation
        }
        self.game_state = GameState(self.player_colour, board)
        self.current_move = True if self.player_colour == Marble.BLACK.value else False
        self.opponent_colour = Marble.BLACK.value if self.player_colour == Marble.WHITE.value else Marble.WHITE.value
        self.config = config
        self.transposition_table = TranspositionTable()
        print("Weights: ", self.weights)


    def run_game(self):
        """
        AI vs random
        Starts the game of Abalone with the model against an opponent.
        """
        while not self.game_state.terminal_test():
            self.game_state.board.print_board() # Debug
            if self.current_move: # Player turn
                print("\nPlayer Turn\n")

                s = time.time() # Debug
                # Get the next move 
                move_to_make = self.iterative_deepening_search(
                    True, 
                    generate_move(self.player_colour, self.game_state.board),
                    self.config.h1
                )
                e = time.time() # Debug
                print(f"Time to generate move of depth {self.depth}: ", e-s) # Debug

                # Terminal state reached
                if move_to_make is None:
                    break

                # Apply the move to the game state
                self.game_state.apply_move(move_to_make)

            # Opponent turn
            else:
                print("\nOpponent Turn\n")
                applied_move = self.apply_opponent_move_random()
                if not applied_move:
                    break


            self.current_move = not self.current_move # Alternate move

            print(self.game_state) # Debug

        print("Game over")
        print(self.game_state.check_win(), "won")


    def run_game_diff_heuristic(self):
        """
        AI vs another heuristic
        Starts the game of Abalone with the model against an opponent.
        """
        while not self.game_state.terminal_test():
            self.game_state.board.print_board() # Debug
            if self.current_move: # Player turn
                print("\nPlayer Turn\n")

                s = time.time() # Debug
                # Get the next move 
                move_to_make = self.iterative_deepening_search(
                    True, 
                    generate_move(self.player_colour, self.game_state.board),
                    self.config.h1
                )
                e = time.time() # Debug
                print(f"Time to generate move of depth {self.depth}: ", e-s) # Debug

                # Terminal state reached
                if move_to_make is None:
                    break

                # Apply the move to the game state
                self.game_state.apply_move(move_to_make)

            # Opponent turn
            else:
                print("\nOpponent Turn\n")
                applied_move = self.apply_opponent_move_random()
                if not applied_move:
                    break


            self.current_move = not self.current_move # Alternate move

            print(self.game_state) # Debug

        print("Game over")
        print(self.game_state.check_win(), "won")


    def apply_opponent_move_random(self) -> bool:
        """
        Applies a randomly generated opponent move to the game state.

        :return: True if the move was applied, False if not and the game is over
        """
        move = self._get_opponent_move_random()
        if not move:
            return False
        self.game_state.apply_move(move)
        return True


    def apply_opponent_move_input(self):
        """Applies the move to the game state. This assumes the opponents move is a valid one."""
        move = self._get_opponent_move_input()
        self.game_state.apply_move(move)
    
    def _get_opponent_move_random(self) -> Move | None:
        """
        Generates all possible moves for the opponent, returning a randomly selected one.

        :return: a randomly selected move for the opponent or None if there are no generated moves
        """
        possible_opponent_moves = generate_move(self.opponent_colour, self.game_state.board)
        if len(possible_opponent_moves) == 0:
            return None
        r = random.randint(0, len(possible_opponent_moves) - 1)
        opponent_move = possible_opponent_moves[r]
        return opponent_move


    # FIXME: This should return a Move object
    def _get_opponent_move_input(self) -> Tuple[int, int, int, str]:
        """
        Gets the opponents move from user input. Handles errors appropriately, reprompting the opponent. 

        :return: the user inputted move as a tuple in notation (q, r, s, colour)
        """
        while True:
            opponent_move = input("Enter the opponent move position: ")
            try:
                opponent_move = f"{opponent_move}{self.opponent_colour}"
                opponent_move = Board.convert_marble_notation(opponent_move)
                # Convert the tuple into a Move object
            except ValueError:
                print("Invalid move entered")
            except Exception as e:
                print("Unknown error parsing opponent move:", e)
            else:
                return opponent_move


    def iterative_deepening_search(self, is_player: bool, moves: List[Move], heuristic) -> Move | None:
        """
        Runs an iterative deepening search using the mini-max algorithm
        with a heuristic function to determine the best move to take
        for the agent, returning the best move for the agent to take.

        :param is_player: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param moves: a List of the moves to run iterative deepening and mini max on
        :return: the move for the agent to take as a Move object
        """
        self.transposition_table.clear()
        best_move = None
        best_score = -math.inf
        
        # Iterative search
        for depth in range(1, self.depth + 1): 
            # Visit every node (move)
            for move in moves:
                # Create the resulting game state
                board = self.game_state.board.marble_positions.copy()
                empty_positions = self.game_state.board.empty_positions.copy()
                apply_move_dict(board, empty_positions, move)
                # result_game_state = self.game_state.deep_copy()
                # apply_move_obj(result_game_state.board, move)

                score = self.mini_max(
                    not is_player, # Switch turn
                    board,
                    empty_positions,
                    depth, 
                    heuristic,
                    self.weights["center_distance"], 
                    self.weights["coherence"], 
                    self.weights["triangle_formation"]
                )
                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move


    def mini_max(self, is_player: bool, board: Dict[Tuple[int, int, int], str], empty_positions: Set[Tuple[int, int, int]], depth: int, heuristic, *args) -> float:
        """
        Minimax algorithm.

        :param is_player: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :param args: the weights
        :return: the move for the player to take as str
        """
        if is_player:
            return self.max_value(
                self.player_colour,
                board,
                empty_positions,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                *args
        )
        else:
            return self.min_value(
                self.opponent_colour,
                board,
                empty_positions,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                *args
        )


    def max_value(
            self,
            player_colour: str,
            board: Dict[Tuple[int, int, int], str],
            empty_positions: Set[Tuple[int, int, int]],
            depth: int,
            alpha: float,
            beta: float,
            heuristic,
            *args
    ) -> float:
        """
        A minimax algorithm that determines the best move to take for the current player.
        
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :param args: the weights
        :return: the utility value of a given game state
        """
        entry = self.transposition_table.lookup(player_colour, board)
        if entry and entry.depth >= depth:
            if entry.flag == 'exact':
                return entry.value
            elif entry.flag == 'lower' and entry.value >= beta:
                return entry.value
            elif entry.flag == 'upper' and entry.value <= alpha:
                return entry.value

        if depth == 0 or terminal_test(board):
            value = heuristic(player_colour, board, *args)
            self.transposition_table.store(player_colour, board, value, depth, 'exact')
            return value

        v = -math.inf
        moves_generated = generate_move_dict(player_colour, board, empty_positions)
        for move in moves_generated:

            # Create the resulting game state
            board = board.copy()
            empty_positions = empty_positions.copy()
            apply_move_dict(board, empty_positions, move)


            v = max(v, self.min_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                board,
                empty_positions,
                depth-1,
                -math.inf,
                math.inf,
                heuristic,
                *args
            ))

            if v >= beta:
                self.transposition_table.store(player_colour, board, v, depth, 'lower')
                return v
            alpha = max(alpha, v)

        self.transposition_table.store(player_colour, board, v, depth, 'exact' if v > alpha else 'upper')
        return v


    def min_value(
            self,
            player_colour: str,
            board: Dict[Tuple[int, int, int], str],
            empty_positions: Set[Tuple[int, int, int]],
            depth: int,
            alpha: float,
            beta: float,
            heuristic,
            *args
        ) -> float:
        """
        A minimax algorithm that determines the best move to take for the opponent.
        
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :param args: the weights
        :return: the utility value of a given game state
        """
        entry = self.transposition_table.lookup(player_colour, board)
        if entry and entry.depth >= depth:
            if entry.flag == 'exact':
                return entry.value
            elif entry.flag == 'lower' and entry.value >= beta:
                return entry.value
            elif entry.flag == 'upper' and entry.value <= alpha:
                return entry.value

        if depth == 0 or terminal_test(board):
            value = heuristic(player_colour, board, *args)
            self.transposition_table.store(player_colour, board, value, depth, 'exact')
            return value

        v = math.inf

        moves_generated = generate_move_dict(player_colour, board, empty_positions)

        for move in moves_generated:
            # Create the resulting game state
            board = board.copy()
            empty_positions = empty_positions.copy()
            apply_move_dict(board, empty_positions, move)

            v = min(v, self.max_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                board,
                empty_positions,
                depth-1,
                alpha,
                beta,
                heuristic,
                *args
                )
            )
            if v <= alpha:
                self.transposition_table.store(player_colour, board, v, depth, 'upper')
                return v
            beta = min(beta, v)

        self.transposition_table.store(player_colour, board, v, depth, 'exact' if v < beta else 'lower')

        return v


