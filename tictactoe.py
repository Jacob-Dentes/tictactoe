"""
A simple implementation of tic tac toe

This module creates a system for creating a tic tac toe
board of any square size, generating legal moves, and playing moves.
The module contains a minimax algorithm for generating the best possible moves.
The module also contains functions for playing simple command-line
tic tac toe games.


Author: Jacob Dentes
Date: 14 September 2021
"""
class Board():
    """
    A class representing a tic tac toe board.

    Attribute width: The width of the tic tac toe board in number of spaces
    Invariant: width is an int and width == height

    Attribute width: The height of the tic tac toe board in number of spaces
    Invariant: height is an int and width == height

    Attribute size: The total number of spaces on the board
    Invariant: size is an int and size == width * height

    Attribute board_list: A list of lists holding the contents of the board rows
    Invariant: board_list is a list with len height holding lists with len width

    Attribute x_turn: True when it is currently the X player's turn
    Invariant: x_turn is a bool

    Attribute moves: Holds a list of moves that have been played so far
    Invariant: moves is a list of int with len <= size

    Attribute legal_moves: Holds a dynamic list of the board's legal moves
    Invariant: legal_moves is a list of int with len == size - len(moves)
    """
    def __init__(self, size: int = 3):
        """
        Create a board with size WxH where W and H are size.

        Instantiates a new board based on size. Handles initial move generation.

        Parameter size: The width and height of the board
        Precondition: size is an int and size > 0
        """
        if size <= 0:
            print('Sizes must be positive.')
            del self
        else:
            self.width = size
            self.height = size
            self.size = size * size
            self.board_list = []
            self.x_turn = True
            self.moves = []
            for i in range(self.height):
                self.board_list.append([None for _ in range(self.width)])
            self.legal_moves = self.generate_legal_moves()

    def __str__(self) -> str:
        """
        Returns an ascii representation of the current boardstate.

        The columns are separated by '|' and the rows are separated by '-'.
        Each cell is filled with an 'X' or an 'O' if a player has played there
        or the index of the cell if it is empty.
        """
        return_string = '\n'
        tindex = 0
        for index, row in enumerate(self.board_list):
            for i2, column in enumerate(row):
                temp = ' '
                if column is not None:
                    temp = column
                    if self.size > 11:
                        temp += ' '
                else:
                    if self.size > 11:
                        if tindex >= 10:
                            temp = tindex
                        else:
                            temp = str(tindex) + ' '
                    else:
                        temp = tindex
                return_string += f'  {temp}  '
                tindex += 1
                if i2 != self.width - 1:
                    return_string += '|'
            if index != self.height - 1:
                return_string += '\n' + ('-' * (7 * self.width)) + '\n'
        return return_string + '\n'
    def __hash__(self):
        """Returns a hash based on the flattened board and current turn."""
        x = self.flatten()
        if self.x_turn:
            x.append(1)
        else:
            x.append(-1)
        return hash(tuple(x))
    def __gt__(self, other) -> bool:
        """
        Returns a bool for whether or not a board is greater than another.

        A board is greater than another if more moves have been played.
        """
        return len(self.moves) > len(other.moves)
    def __lt__(self, other) -> bool:
        """
        Returns a bool for whether or not a board is less than another.

        A board is less than another if fewer moves have been played.
        """
        return len(self.moves) < len(other.moves)
    def __eq__(self, other) -> bool:
        """
        Returns a bool for whether or not two boards are the same.

        Two boards are the same when they have the same size, the same letters
        in the same places, and have the same player as the current turn.
        """
        self_board = self.flatten()
        self_board.append(1 if self.x_turn else -1)
        other_board = other.flatten()
        other_board.append(1 if other.x_turn else -1)
        return self_board == other_board

    def generate_legal_moves(self) -> list:
        """Returns a list of all legal moves for the current board."""
        board = self.board_list
        index = 0
        return_list = []
        for row in board:
            for column in row:
                if column is None:
                    return_list.append(index)
                index += 1
        return return_list
    @property
    def shuffled_legal_moves(self) -> list:
        """
        A randomized list of the legal moves.

        Invariant: shuffled_legal_moves is a list with len == len(legal_moves).
        """
        from copy import copy
        from random import shuffle
        x = copy(self.legal_moves)
        shuffle(x)
        return x

    def create_copy(self):
        """Returns a copy of the board."""
        from copy import copy, deepcopy
        x = new_board(self.width)
        x.board_list = deepcopy(self.board_list)
        x.x_turn = copy(self.x_turn)
        x.moves = copy(self.moves)
        x.legal_moves = copy(self.legal_moves)
        return x
    def flatten(self) -> list:
        """
        Returns the board as a one-dimensional list.

        Removes the two-dimensional structure of the board to create a single
        list of -1s, 1s, and 0s. The list goes from left to right and top down
        for the given board. -1 represents 'O', 1 represents 'X', and 0
        represents an empty space.
        """
        board = self.board_list
        return_list = []
        for row in board:
            for column in row:
                if column is None:
                    column = 0
                elif column == 'X':
                    column = 1
                elif column == 'O':
                    column = -1
                return_list.append(column)
        return return_list

    def check_game_end(self) -> tuple:
        """
        Returns a tuple representing if the game is over and which side won

        Returns a tuple. The first value will be True if the game ended. The
        second value will be 0 for a draw or tie, 1 if X won, and -1 if O won.
        """
        board = self.board_list
        game_over = False
        if len(self.generate_legal_moves()) <= 0:
            game_over = True
        # Checks every horizontal win condition
        for horizontal_list in board:
            if all([item == 'X' for item in horizontal_list]):
                return (True, 1)
            if all([item == 'O' for item in horizontal_list]):
                return (True, -1)
        # Checks every vertical win condition
        for vertical_list in zip(*board):
            if all([item == 'X' for item in vertical_list]):
                return (True, 1)
            if all([item == 'O' for item in vertical_list]):
                return (True, -1)
        # Checks the diagonal win condition from top left
        diag_list = []
        index = 0
        while index < self.width and index < self.height:
            diag_list.append(board[index][index])
            index += 1
        if all([item == 'X' for item in diag_list]):
            return (True, 1)
        if all([item == 'O' for item in diag_list]):
            return (True, -1)
        # Checks the diagonal win condition from top right
        diag_list = []
        index = self.width - 1
        h_index = 0
        while 0 <= index and index < self.width and h_index < self.height:
            diag_list.append(board[h_index][index])
            index -= 1
            h_index += 1
        if all([item == 'X' for item in diag_list]):
            return (True, 1)
        if all([item == 'O' for item in diag_list]):
            return (True, -1)

        return (game_over, 0)
    def insert(self, item, target: int):
        """
        Inserts a string into the board at the specified target index.

        Parameter item: The string to be inserted into the board.
        Precondition: item is 'X', 'O', or None.

        Parameter target: The location to insert the item, 0 indexed.
        Precondition: target is an int and 0 <= target < board size.
        """
        board = self.board_list
        index = 0
        for row, _ in enumerate(board):
            for column, _ in enumerate(board[row]):
                if index == target:
                    board[row][column] = item
                    return
                index += 1
    def unmove(self):
        """Undoes the previous move."""
        self.insert(None, self.moves.pop())
        self.legal_moves = self.generate_legal_moves()
        self.x_turn = not self.x_turn
    def move(self, input) -> bool:
        """
        Returns a bool if a given move is successful and makes the move.

        Parameter input: The desired location for the move, 0 indexed.
        Precondition: input is an int or a digit string and 0 <= input < size
        """
        if not type(input) == type(5):
            input = int(input) if input.isdigit() else None

        if (input is not None) and (input in self.legal_moves):
            item = 'X' if self.x_turn else 'O'
            self.insert(item, input)
            self.moves.append(input)
            self.legal_moves = self.generate_legal_moves()
            self.x_turn = not self.x_turn
            return True
        else:
            return False

    def eval_board(self) -> float:
        """
        Returns a float estimate for the board value, higher means better for X.

        Returns a float -1 < x < 1, it is a rough estimate based on the most
        letters in a row without an opponent blocking.
        """
        most_row_x = 0
        most_row_o = 0
        board = self.board_list
        # Checks every horizontal
        for horizontal_list in board:
            if all([item != 'O' for item in horizontal_list]):
                most_row_x = max(most_row_x, horizontal_list.count('X'))
            if all([item != 'X' for item in horizontal_list]):
                most_row_o = max(most_row_o, horizontal_list.count('O'))
        # Checks every vertical
        for vertical_list in zip(*board):
            if all([item != 'O' for item in vertical_list]):
                most_row_x = max(most_row_x, vertical_list.count('X'))
            if all([item != 'X' for item in vertical_list]):
                most_row_o = max(most_row_o, vertical_list.count('O'))
        # Checks the diagonal from top left
        diag_list = []
        index = 0
        while index < self.width and index < self.height:
            diag_list.append(board[index][index])
            index += 1
        if all([item != 'O' for item in diag_list]):
            most_row_x = max(most_row_x, diag_list.count('X'))
        if all([item != 'X' for item in diag_list]):
            most_row_o = max(most_row_o, diag_list.count('O'))
        # Checks the diagonal from top right
        diag_list = []
        index = self.width - 1
        h_index = 0
        while 0 <= index and index < self.width and h_index < self.height:
            diag_list.append(board[h_index][index])
            index -= 1
            h_index += 1
        if all([item != 'O' for item in diag_list]):
            most_row_x = max(most_row_x, diag_list.count('X'))
        if all([item != 'X' for item in diag_list]):
            most_row_o = max(most_row_o, diag_list.count('O'))
        if most_row_x > most_row_o:
            return most_row_x / (self.width)
        elif most_row_o > most_row_x:
            return - most_row_o / (self.width)
        return 0
    def ai(self, max_time) -> int:
        """
        Returns the integer choice for an algorithm's guess for best move.

        An alpha-beta pruning minimax algorithm will determine the best move for
        the board based on eval_board. The ai will continue searching until it
        finds a move or exceeds max_time.

        Parameter max_time: The approximate maximum time for the algorithm.
        Precondition: max_time is an int or float and max_time > 0
        """
        from functools import lru_cache
        from random import shuffle
        # Minimax implementation with alpha-beta pruning
        # Created by following the psuedocode from
        # https://en.wikipedia.org/wiki/Alpha-beta_pruning
        @lru_cache
        def minimax(node: Board, depth: int, alpha, beta, max_player: bool):
            # Exit condition
            x = node.check_game_end()
            if depth == 0 or x[0]:
                if x[0]:
                    return x[1]
                return node.eval_board()
            # Runs when it is x's turn
            if max_player:
                value = -float('inf')
                for move in node.shuffled_legal_moves:
                    child_board = node.create_copy()
                    child_board.move(move)
                    value = max(value,
                            minimax(child_board, depth - 1, alpha, beta, False))
                    if value >= beta:
                        break
                    alpha = max(alpha, value)
                return value
            # Runs when it is o's turn
            else:
                value = float('inf')
                for move in node.shuffled_legal_moves:
                    child_board = node.create_copy()
                    child_board.move(move)
                    value = min(value,
                            minimax(child_board, depth - 1, alpha, beta, True))
                    if value <= alpha:
                        break
                    beta = min(beta, value)
                return value

        from copy import copy
        import time
        t1 = time.time()
        moves = copy(self.shuffled_legal_moves)
        ratings = []
        depth = 0
        best_guess = 0
        while (time.time() - t1 < max_time):
            depth += 1
            for move in moves:
                if (time.time() - t1 > max_time):
                    break
                child_board = self.create_copy()
                child_board.move(move)
                ratings.append(minimax(
                            child_board, depth, -1, 1, child_board.x_turn))
            else:
                move_rating = list(zip(moves, ratings))
                move_rating.sort(key=lambda x: x[1], reverse=self.x_turn)
                best_guess = move_rating[0][1]
                moves = [i[0] for i in move_rating]
                if (moves[0] == 1 and self.x_turn) or (
                            moves[0] == -1 and not self.x_turn):
                    return moves[0]
                if depth > len(self.legal_moves):
                    return moves[0]
                ratings.clear()
        return moves[0]
    def change_eval(self, func):
        """
        Changes the ai's board evaluation function.

        Parameter func: The new evaluation function.
        Precondition: func is a function that takes a board and returns a float
        with -1 < float < 1
        """
        self.eval_board = func

def new_board(size: int = 3):
    """
    Returns a new board of the specified size. In size x size.

    Creates and returns a new instance of the board class.

    Parameter size: The width and height of the board.
    Precondition: size is an int and size > 0
    """
    return Board(size)

def play_2p(size: int = 3, max_time = 10):
    """
    Creates a command-line game for two players with the designated board size.

    The commands to play the game are: type 'end', 'stop', or 'break' to end
    the game, type 'restart' or 're' to start the game over, type 'r' when
    prompted to randomly choose a starting player, type an integer representing
    the location to move when making a move, and type 'ai' to get a prediction
    for the best move.

    Parameter size: The width and height of the board to be played.
    Precondition: size is an int and size > 0.

    Parameter max_time: The approximate maximum time the ai can think for.
    Precondition: max_time is an int or float and max_time > 0.
    """
    if type(size) != type(5):
        size = 3
    if size < 1:
        size = 1
    looping = True
    while looping:
        print('\nStarting two player game...\n')

        board = new_board(size)
        print(board)

        print('\nX player enter your move.' +
            '\nOr type "r" for the program to decide which player starts.' +
            '\nYou can always type "restart" or "end"' +
            ' to restart or end the game.\n')

        inp = input()
        if inp == 'r':
            import random
            if random.randrange(2) > 0.5:
                print('Player on the left starts.\n')
                inp = input()
            else:
                print('Player on the right starts.\n')
                inp = input()

        while True:
            if inp == 'restart' or inp == 're':
                break
            if inp == 'stop' or inp == 'break' or inp == 'end':
                looping = False
                break
            if inp == 'ai':
                import time
                t1 = time.time()
                print('AI thinking...')
                print(f'The AI found move {board.ai(max_time)}' +
                        f' in {time.time() - t1}s.\n')
                inp = input()
            if board.move(inp):
                print(board)
            else:
                print(f'Illegal move, enter an integer between 0 ' +
                    f'and {board.size} that has not been taken.\n')
                print(f'The current legal moves are: {board.legal_moves}\n')
            if (end := board.check_game_end())[0] == True:
                if end[1] == 0:
                    print('Draw.\n')
                elif end[1] == 1:
                    print('X wins!\n')
                elif end[1] == -1:
                    print('O wins!\n')
                break
            temp = 'O'
            if board.x_turn:
                temp = 'X'
            print(temp + ' player enter a move.\n')
            inp = input()

def play_1p(size: int = 3, max_time = 10):
    """
    Creates a command-line game of player vs. ai with the designated board size.

    The commands to play the game are: type 'end', 'stop', or 'break' to end
    the game, type 'restart' or 're' to start the game over, type 'r' when
    prompted to randomly choose a starting player, and type an integer
    representing the location to move when making a move.

    Parameter size: The width and height of the board to be played.
    Precondition: size is an int and 0 < size <= 4.

    Parameter max_time: The approximate maximum time the ai can think for.
    Precondition: max_time is an int or float and max_time > 0.
    """
    if type(size) != type(5):
        size = 3
    if size < 1:
        size = 1
    if size > 4:
        size = 4
    looping = True
    while looping:
        print('\nStarting game against AI...\n')
        player_x = True
        play = True
        while True:
            print('Play first? Type "y"/"n" for yes or no.'+
                    ' Type "r" for random.\n' +
                    'You can always type "restart" or "end"' +
                    ' to restart or end the game.\n')
            inp = input()
            if inp == 'y':
                break
            elif inp == 'n':
                player_x = False
                break
            elif inp == 'r':
                import random
                if random.randrange(2) == 0:
                    print('You are X.')
                    break
                else:
                    print('You are O.')
                    player_x = False
                    break
            if inp == 'restart' or inp == 're':
                play = False
                break
            if inp == 'stop' or inp == 'break' or inp == 'end':
                looping = False
                play = False
                break
        if play:
            board = new_board(size)
            print(board)
            while True:
                if player_x == board.x_turn:
                    temp = 'O'
                    if board.x_turn:
                        temp = 'X'
                    print(temp + ' player enter a move.\n')
                    inp = input()
                else:
                    print('AI thinking...')
                    import time
                    t1 = time.time()
                    inp = board.ai(max_time)
                    print(f'AI chose {inp} in {time.time() - t1}s.')
                if inp == 'restart' or inp == 're':
                    break
                if inp == 'stop' or inp == 'break' or inp == 'end':
                    looping = False
                    break
                if board.move(inp):
                    print(board)
                else:
                    print(f'Illegal move, enter an integer between 0 ' +
                        f'and {board.size} that has not been taken.\n')
                    print(f'The current legal moves are: {board.legal_moves}\n')
                if (end := board.check_game_end())[0] == True:
                    if end[1] == 0:
                        print('Draw.\n')
                    elif end[1] == 1:
                        print('X wins!\n')
                    elif end[1] == -1:
                        print('O wins!\n')
                    break

def play_0p(size: int = 3, max_time = 10):
    """
    Creates a command-line game of ai vs. ai with the designated board size.

    Parameter size: The width and height of the board to be played.
    Precondition: size is an int and 0 < size <= 4.

    Parameter max_time: The approximate maximum time the ai can think for.
    Precondition: max_time is an int or float and max_time > 0.
    """
    if type(size) != type(5):
        size = 3
    if size > 4:
        size = 4
    elif size < 1:
        size = 1
    print('Starting AI vs AI game...\n')
    board = new_board(size)
    print(board)
    while not board.check_game_end()[0]:
        import time
        t1 = time.time()
        print('AI thinking...')
        choice = board.ai(max_time)
        board.move(choice)
        print(f'AI chose {choice} in {time.time() - t1}s.')
        print(board)
    result = board.check_game_end()[1]
    if result == 0:
        print('Draw.')
    elif result == 1:
        print('X wins!')
    elif result == -1:
        print('O wins!')
