""" this agent will use all the modules to generate a best move"""
from state_space import GameState, apply_move_dict, generate_move, terminal_test, generate_move_dict, check_win, game_status
from transposition_tables import TranspositionTable
from typing import Tuple, Dict, List
from moves import Move
import  math
import time
from enums import Marble, GameMode
from board import Board
import random

class AgentConfiguration:
    """
    Contains data attributes related to a game configuration.
    """


    def __init__(self,
                 colour: Marble,
                 move_limit: int,
                 time_limit: int,
                 first_move: bool,
                 heuristic=None,
                 heuristic_weights=None,
                 ):

        """
        A configuration for an abalone playing agent.

        :param colour: The color of the player's marbles ('b' or 'w')
        :param move_limit: maximum allowed moves per game
        :param time_limit: maximum time in seconds allowed for move calculation
        :param first_move: True if this player has the first move
        :param heuristic: the heuristic function to use for evaluation
        :param heuristic_weights: weights for the heuristic function
        """
        self.colour = colour
        self.move_limit = move_limit
        self.time_limit = time_limit
        self.first_move = first_move
        self.heuristic = heuristic
        self.heuristic_weights = heuristic_weights

    
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
                 player_config: AgentConfiguration,
                 opponent_config: AgentConfiguration,
                 game_mode: GameMode,
                 depth = 3
                 ):
        """
        Initialize minimax agent with search parameters

        :param board: the initial configuration of the Abalone game board as a Board object
        :param player_config: the configuration of the Model 
        :param opponent_config: the configuration of the opponent
        :param game_mode: the game mode to play, as an enum
        :param depth: maximum search depth (default: 3). A depth of -1 is valid and is considered an "infinite" depth. This depth makes the model continue the search until time runs out
        """
        # Player config
        self.player_colour = player_config.colour.value
        self.heuristic = player_config.heuristic
        self.heuristic_weights = player_config.heuristic_weights
        self.player_has_first_move = player_config.first_move
        self.player_move_limit = player_config.move_limit
        self.player_time_limit = player_config.time_limit
        self.current_move = self.player_has_first_move

        # Opponent config
        self.opponent_colour = opponent_config.colour.value
        self.opponent_heuristic = opponent_config.heuristic
        self.opponent_heuristic_weights = opponent_config.heuristic_weights
        self.opponent_has_first_move = opponent_config.first_move
        self.opponent_move_limit = opponent_config.move_limit
        self.opponent_time_limit = opponent_config.time_limit

        # Game config
        self.board = board
        self.board_dict = board.marble_positions
        self.time_limit = player_config.time_limit
        self.depth = depth
        self.game_state = GameState(self.player_colour, board)
        self.transposition_table = TranspositionTable()
        self.game_mode = game_mode
        

    def run_game(self):
        """
        Starts the game of Abalone with the model against an opponent.
        """

        while not terminal_test(self.game_state.board.marble_positions):

            self.game_state.board.print_board() # Debug

            if self.current_move: 
                self._player_turn()

            else:
                self._opponent_turn() 

            self.current_move = not self.current_move # Alternate move

            print(game_status(self.game_state.board.marble_positions)) # Debug

        print("Game over")
        print(check_win(self.game_state.board.marble_positions), "won")


    def _player_turn(self):
        """Handles the agent (player) turn logic."""
        print("\nPlayer Turn\n")
        start = time.time()
        move_to_make = self.iterative_deepening_search(
            True,
            self.heuristic,
            self.heuristic_weights
        )
        if move_to_make:
            self.game_state.apply_move(move_to_make)
        end = time.time()
        print(f"Time to make move at depth {self.depth}: {end - start}")


    def _opponent_turn(self):
        """Handles the opponent turn logic."""
        print("\nOpponent Turn\n")

        match self.game_mode:
            case GameMode.HUMAN:
                print("In development...")
            case GameMode.RANDOM:
                self._opponent_turn_random()
            case GameMode.DIFF_HEURISTIC:
                self._opponent_turn_heuristic()
            case GameMode.SAME_HEURISTIC:
                self._opponent_turn_heuristic()

            

    def _opponent_turn_random(self):
        """Simulates an opponent that makes random moves."""
        move_to_make = self._get_opponent_move_random()
        if move_to_make:
            self.game_state.apply_move(move_to_make)

    def _opponent_turn_heuristic(self):
        """Simulates an opponent that uses their own heuristic."""
        move_to_make = self.iterative_deepening_search(
                False,
                self.opponent_heuristic,
                self.opponent_heuristic_weights
            )
        if move_to_make:
            self.game_state.apply_move(move_to_make)



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

    def iterative_deepening_search(self, is_player: bool, heuristic, args) -> Move | None:
        self.transposition_table.clear()
        best_move = None

        best_score = -math.inf
        for depth in range(1, self.depth + 1):
            current_best_move = None

            # Generate moves for current depth
            moves = generate_move_dict(self.player_colour if is_player else self.opponent_colour, self.board.marble_positions)

            # 1) Separate pushes from non-pushes
            push_moves = [mv for mv in moves if mv.push]
            non_push_moves = [mv for mv in moves if not mv.push]

            # 2) Sort the non-push moves by your quick heuristic
            non_push_moves_sorted = sorted(
                non_push_moves,
                key=lambda m: self.quick_heuristic_eval(
                    m,
                    self.player_colour if is_player else self.opponent_colour,
                    heuristic,
                    args
                ),
                reverse=True
            )

            # 3) Keep the top 20 non-push moves
            top_non_push = non_push_moves_sorted[:10]

            # 4) Combine them back. This ensures *all push moves* stay in the final list.
            moves = push_moves + top_non_push

            for move in moves:
                new_board = self.board.copy()
                apply_move_dict(new_board, move)

                score = self.mini_max(
                    not is_player,
                    new_board,
                    depth,
                    heuristic,
                    args,
                )
                if score > best_score:
                    best_score = score
                    current_best_move = move

            if current_best_move is not None:
                best_move = current_best_move
        print("Best score:", best_score)

        return best_move


    def mini_max(self, is_player: bool, board: Dict[Tuple[int, int, int], str], depth: int, heuristic, args) -> float:
        """
        Minimax algorithm.

        :param is_player: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param board: the current board state as a dictionary
        :param depth: the depth to run the search
        :param heuristic: the heuristic function to use
        :param args: the weights
        :return: the move with the best score for the player to take 
        """
        if is_player:
            return self.max_value(
                self.player_colour,
                board,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                args,
        )
        else:
            return self.min_value(
                self.opponent_colour,
                board,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                args 
        )


    def max_value(
            self,
            player_colour: str,
            board: Dict[Tuple[int, int, int], str],
            depth: int,
            alpha: float,
            beta: float,
            heuristic,
            args
    ) -> float:
        """
        A minimax algorithm that determines the best move to take for the current player.

        :param player_colour: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param board: the current board state as a dictionary
        :param depth: the depth to run the search
        :param alpha: the alpha value of the caller
        :param beta: the beta value of the caller
        :param heuristic: the heuristic function to use
        :param args: the weights
        :return: the move with the best score for the player to take for maximizing
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
        moves_generated = generate_move_dict(player_colour, board)
        for move in moves_generated:
            # Create the resulting game state
            new_board = board.copy()
            apply_move_dict(new_board, move)

            v = max(v, self.min_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                new_board,
                depth-1,
                alpha,
                beta,
                heuristic,
                args
            ))

            if v >= beta:
                self.transposition_table.store(player_colour, board, v, depth, 'lower')
                return v
            alpha = max(alpha, v)

        flag = 'exact' if alpha < v < beta else 'upper' #important fixing from Yiming
        self.transposition_table.store(player_colour, board, v, depth, flag)
        return v

    def min_value(
            self,
            player_colour: str,
            board: Dict[Tuple[int, int, int], str],
            depth: int,
            alpha: float,
            beta: float,
            heuristic,
            args
        ) -> float:
        """
        A minimax algorithm that determines the best move to take for the opponent.

        :param player_colour: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param board: the current board state as a dictionary
        :param depth: the depth to run the search
        :param alpha: the alpha value of the caller
        :param beta: the beta value of the caller
        :param heuristic: the heuristic function to use
        :param args: the weights
        :return: the move with the best score for the player to take for maximizing
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

        moves_generated = generate_move_dict(player_colour, board)

        for move in moves_generated:
            # Create the resulting game state
            new_board = board.copy()
            apply_move_dict(new_board, move)

            v = min(v, self.max_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                new_board,
                depth-1,
                alpha,
                beta,
                heuristic,
                args
                )
            )
            if v <= alpha:
                self.transposition_table.store(player_colour, board, v, depth, 'upper')
                return v
            beta = min(beta, v)

        flag = 'exact' if alpha < v < beta else 'lower'
        self.transposition_table.store(player_colour, board, v, depth, flag)

        return v

    def quick_heuristic_eval(self, move: Move, player_colour: str, heuristic, args):
        """
        Quickly evaluates a move using the heuristic without recursion.
        """
        temp_board = self.board.copy()
        apply_move_dict(temp_board, move)
        return heuristic(player_colour, temp_board, *args)

    
