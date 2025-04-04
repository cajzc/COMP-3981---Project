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
from file_paths import *
import multiprocessing, queue
import logging
logging.basicConfig(level=logging.DEBUG)  # Configure logging

class AgentConfiguration:
    """
    Contains data attributes related to a game configuration.
    """


    def __init__(self,
                 colour: Marble,
                 move_limit: int,
                 time_limit: int,
                 heuristic=None,
                 heuristic_weights=None,
                 ):

        """
        A configuration for an abalone playing agent.

        :param colour: The color of the player's marbles ('b' or 'w')
        :param move_limit: maximum allowed moves per game
        :param time_limit: maximum time in seconds allowed for move calculation
        :param heuristic: the heuristic function to use for evaluation
        :param heuristic_weights: weights for the heuristic function
        """
        self.colour = colour
        self.move_limit = move_limit
        self.time_limit = time_limit
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
        self.player_colour = Marble.BLACK.value # Player should always be black
        self.heuristic = player_config.heuristic
        self.heuristic_weights = player_config.heuristic_weights
        self.player_move_limit = player_config.move_limit
        self.player_time_limit = player_config.time_limit
        self.current_move = True if player_config.colour.value == Marble.BLACK.value else False # Determine if the player has the first turn in the game

        # Opponent config
        self.opponent_colour = Marble.WHITE.value # Opponent is always white
        self.opponent_heuristic = opponent_config.heuristic
        self.opponent_heuristic_weights = opponent_config.heuristic_weights
        self.opponent_move_limit = opponent_config.move_limit
        self.opponent_time_limit = opponent_config.time_limit

        # Game config
        self.board = board
        self.board_dict = board.marble_positions
        self.time_limit = player_config.time_limit
        self.depth = 10**9 if depth == -1 else depth # Set an "infinite" depth
        self.game_state = GameState(self.player_colour, board)
        self.transposition_table = TranspositionTable()
        self.game_mode = game_mode
        self.last_read_board_file = None


    def run_game(self):
        """
        Starts the game of Abalone with the model against an opponent.
        If this is the player's first move, a random move is selected.
        """
        print(game_status(self.game_state.board.marble_positions)) # Debug
        # First move logic
        player_first_move = True
        while player_first_move:
            if self.current_move: # Players first move, this will be random
                self._player_first_turn_random()
                player_first_move = False # Player has ran their first move
                print("Random first turn: Applied")
            else:
                self._opponent_turn()

            self.current_move = not self.current_move # Alternate move

            print(game_status(self.game_state.board.marble_positions)) # Debug

        # Game loop
        while not terminal_test(self.game_state.board.marble_positions):

            self.game_state.board.print_board() # Debug

            if self.current_move:
                self._player_turn()

            else:
                self._opponent_turn()
                print("Opponent turn ended")

            self.current_move = not self.current_move # Alternate move

            print(game_status(self.game_state.board.marble_positions)) # Debug

        print("Game over")
        print(check_win(self.game_state.board.marble_positions), "won")


    def _player_turn(self):
        """Handles the agent (player) turn logic."""
        print("\nPlayer Turn\n")
        start = time.time()

        # Add a queue for moves, run the iterative deepening search
        best_move_queue = multiprocessing.Queue()
        search_process = multiprocessing.Process(target=self.iterative_deepening_search, args=(best_move_queue, True, self.heuristic, self.heuristic_weights))
        search_process.start()
        search_process.join(timeout=self.time_limit)

        if search_process.is_alive():
            search_process.terminate()
            search_process.join()
        search_process.close()

        try:
            best_move, depth = best_move_queue.get_nowait()
            print(f"Using best move at depth: {depth}")
        except queue.Empty:
            print("Empty queue")
            best_move = None
            depth = None

        if best_move:
            self.game_state.apply_move(best_move) # Update the board configuration
            self._output_game_state(str(best_move), self.game_state.board.to_string_board()) # Output the data to the file

        end = time.time()
        if depth:
            print(f"Using best move at depth: {depth}. Elapsed time: {end-start}")



    def _opponent_turn(self):
        """Handles the opponent turn logic."""
        print("\nOpponent Turn\n")

        match self.game_mode:
            case GameMode.HUMAN:
                board_str, last_read_board_time = read_from_output_game_file(FilePaths.BOARD_INPUT, self.last_read_board_file)
                self.last_read_board_file = last_read_board_time
                self.board.update_board_from_str(board_str) # NOTE: Updates the board configuration from str
                print("Updated board")
            case GameMode.RANDOM:
                self._opponent_turn_random()
            case GameMode.DIFF_HEURISTIC:
                self._opponent_turn_heuristic()
            case GameMode.SAME_HEURISTIC:
                self._opponent_turn_heuristic()


    def _output_game_state(self, move: str, board_state: str):
        """
        Outputs the current game state of the agent, including: Move and Board configuration.

        :param move: the move string in the format: (0,0,0,b)→(1,0,-1,b)
        :param board_state: the board state in the format C5b, A2w, ...
        """
        write_to_output_game_file(FilePaths.MOVES, move)
        write_to_output_game_file(FilePaths.BOARD_OUTPUT, board_state)


    def _player_first_turn_random(self):
        """Selects and applies a random move from the player."""
        move_to_make = self._get_random_move(self.player_colour)
        if move_to_make:
            self.game_state.apply_move(move_to_make)
            self._output_game_state(str(move_to_make), self.board.to_string_board())


    def _opponent_turn_random(self):
        """Simulates an opponent that makes random moves."""
        move_to_make = self._get_random_move(self.opponent_colour)
        if move_to_make:
            self.game_state.apply_move(move_to_make)


    def _opponent_turn_heuristic(self):
        """Simulates an opponent that uses their own heuristic."""
        move_to_make = self.iterative_deepening_search(
                None,
                False,
                self.opponent_heuristic,
                self.opponent_heuristic_weights
            )
        if move_to_make:
            self.game_state.apply_move(move_to_make)


    def apply_opponent_move_input(self):
        """Applies the move to the game state. This assumes the opponents move is a valid one."""
        move = self._get_opponent_move_input()
        #self.game_state.apply_move(move)

    
    def _get_random_move(self, player_colour: str) -> Move | None:
        """
        Generates all possible moves for the opponent, returning a randomly selected one.

        :param player_colour: the colour of the player who will make the random move
        :return: a randomly selected move for the player or None if there are no generated moves
        """
        possible_moves = generate_move(player_colour, self.board)
        if len(possible_moves) == 0:
            return None
        r = random.randint(0, len(possible_moves) - 1)
        random_move = possible_moves[r]
        return random_move


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

    def iterative_deepening_search(self, best_move_queue, is_player: bool, heuristic, args) -> Move | None:
        self.transposition_table.clear()
        best_move = None

        for depth in range(1, self.depth + 1):
            best_score = -math.inf
            current_best_move = None

            # Generate moves for current depth
            moves = generate_move_dict(self.player_colour if is_player else self.opponent_colour, self.board.marble_positions)

            # # 1) Separate pushes from non-pushes
            # push_moves = [mv for mv in moves if mv.push]
            # non_push_moves = [mv for mv in moves if not mv.push]
            #
            # # 2) Sort the non-push moves by your quick heuristic
            # non_push_moves_sorted = sorted(
            #     non_push_moves,
            #     key=lambda m: self.quick_heuristic_eval(
            #         m,
            #         self.player_colour if is_player else self.opponent_colour,
            #         heuristic,
            #         args
            #     ),
            #     reverse=True
            # )
            #
            # # 3) Keep the top 20 non-push moves
            # top_non_push = non_push_moves_sorted[:10]
            #
            # # 4) Combine them back. This ensures *all push moves* stay in the final list.
            # moves = push_moves + top_non_push

            moves = sorted(
                moves,
                key=lambda m: self.quick_heuristic_eval(
                    m,
                    self.player_colour if is_player else self.opponent_colour,
                    heuristic,
                    args
                ),
                reverse=True
            )[:20]

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
                while not best_move_queue.empty(): # Clear the current queue
                    best_move_queue.get_nowait()
                best_move_queue.put((best_move, depth)) # Add the best move and depth to the queue
            print(best_score,best_move)

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
            new_board = board.copy()
            apply_move_dict(new_board, move)
            child_value = self.min_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                new_board,
                depth - 1,
                alpha,
                beta,
                heuristic,
                args
            )
            v = max(v, child_value)
            if v >= beta:
                self.transposition_table.store(player_colour, board, v, depth, 'lower')
                return v
            alpha = max(alpha, v)

        flag = 'exact' if alpha < v < beta else 'upper'
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
            new_board = board.copy()
            apply_move_dict(new_board, move)
            child_value = self.max_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                new_board,
                depth - 1,
                alpha,
                beta,
                heuristic,
                args
            )
            v = min(v, child_value)
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
        return heuristic(self.game_state.get_next_turn_colour(player_colour), temp_board, *args)

    def get_best_move(self, is_player: bool, heuristic, args, fixed_depth: int) -> Move | None:
        alpha = -math.inf
        beta = math.inf
        best_move = None

        # Generate moves for the current board state.
        moves = generate_move_dict(
            self.player_colour if is_player else self.opponent_colour,
            self.board.marble_positions
        )

        if is_player:
            best_score = -math.inf
            # For each move, apply the move and evaluate it with the minimax algorithm.
            for move in moves:
                new_board = self.board.copy()
                apply_move_dict(new_board, move)
                # We subtract 1 from the depth because the current move is already made.
                score = self.min_value(
                    self.opponent_colour,
                    new_board,
                    fixed_depth - 1,
                    alpha,
                    beta,
                    heuristic,
                    args
                )
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
        else:
            best_score = math.inf
            for move in moves:
                new_board = self.board.copy()
                apply_move_dict(new_board, move)
                score = self.max_value(
                    self.player_colour,
                    new_board,
                    fixed_depth - 1,
                    alpha,
                    beta,
                    heuristic,
                    args
                )
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)

        return best_move



