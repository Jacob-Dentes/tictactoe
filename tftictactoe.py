"""
A script for playing tictactoe with a tensorflow ai.

This module utilizes a trained tensorflow model and the minimax algorithm
to improve the predictions of an ai on tictactoe boards size 4x4 and greater.
Currently, there is only one model trained for a 4x4 size but there are plans
to expand this number. It relies on tensorflow model files provided in the
project.

Author: Jacob Dentes
Date: 13 September 2021
"""
import tictactoe
import tensorflow as tf
import time

MIN_SIZE = 4
MAX_SIZE = 5

models = {4: 'tf_ttt_model', 5: 'tf_ttt_model_5'}
MODEL = None

def clamp(x, min, max):
    """
    Returns x clamped between min and max.

    Returns min if x < min, returns max if x > max,
    returns x if min <= x <= max. Will return int if all arguments are int,
    will return float if any argument is float.

    Parameter x: The value to be clamped
    Precondition: x is an int or float

    Parameter min: The lower bound for the retun value
    Precondition: min is an int or float

    Parameter max: The upper bound for the reuturn value
    Precondition: max is an int or float
    """
    return min * (x < min) + max * (x > max) + x * (min <= x <= max)

def eval(self) -> float:
    """
    Returns a float representing a board's value.

    The function feeds the input into a tensorflow model to generate the
    value. -1 < value < 1.
    """
    input = self.flatten()
    input.append(1 if self.x_turn else -1)
    input = [input]

    return clamp(self.MODEL.predict(input)[0], -0.999, 0.999)

def play_0p(model, size=4, max_think=30):
    """
    Start an ai vs ai game on a board of the designated size with the designated
    ai think time.

    Will ensure that the size is between the minimum and maximum supported
    board sizes.

    Parameter model: A tensorflow model for evaluating boards
    Precondition: model is a tensorflow model with input shape equal to size + 1

    Parameter size: The width and height of the board to be played.
    Precondition: size is an int or float.

    Parameter max_think: The maximum amount of time the ai can spend per move.
    Precondition: max_think is an int or float and max_think > 0.
    """
    size = int(clamp(size, MIN_SIZE, MAX_SIZE))
    board = tictactoe.new_board(size)
    board.MODEL = model
    board.change_eval(eval)

    while not board.check_game_end()[0]:
        print(board)
        turn = 'X' if board.x_turn else 'O'
        print(f'AI for {turn} thinking')
        t1 = time.time()
        choice = board.ai(max_think)
        print(f'AI chose {choice} in {time.time() - t1} seconds.')
        board.move(choice)

    print(board)
    end = board.check_game_end()
    if end[1] == 0:
        print('Draw.')
    else:
        winner = 'X' if end[1] == 1 else 'O'
        print(f'{winner} wins!')

def play_1p(model, size=4, max_think=30):
    """
    Start a player vs ai game on a board of the designated size with the designated
    ai think time.

    Will ensure that the size is between the minimum and maximum supported
    board sizes.

    Parameter model: A tensorflow model for evaluating boards
    Precondition: model is a tensorflow model with input shape equal to size + 1

    Parameter size: The width and height of the board to be played.
    Precondition: size is an int or float.

    Parameter max_think: The maximum amount of time the ai can spend per move.
    Precondition: max_think is an int or float and max_think > 0.
    """
    size = int(clamp(size, MIN_SIZE, MAX_SIZE))
    board = tictactoe.new_board(size)
    board.MODEL = model
    board.change_eval(eval)

    player_turn = True

    choosing = True
    while choosing:
        print('\nYou can always type "end" to leave the game.')
        inp = input('Play first? Enter y/n for yes/no or r for random: ')
        if inp == 'end' or inp == 'stop':
            return
        if inp == 'y':
            choosing = False
        elif inp == 'n':
            choosing = False
            player_turn = False
        elif inp == 'r':
            choosing = False
            from random import randrange
            if randrange(2) == 0:
                player_turn = False
                print('You are O')
            else:
                print('You are X')
    while not board.check_game_end()[0]:
        print(board)
        if player_turn:
            choosing = True
            while choosing:
                print('\nYou can always type "end" to leave the game.')
                turn = 'X' if board.x_turn else 'O'
                inp = input(f'{turn} player enter move: ')
                if inp == 'end':
                    return
                if inp.isdigit() and board.move(int(inp)):
                    choosing = False
            player_turn = not player_turn
        else:
            print('AI thinking...')
            t1 = time.time()
            choice = board.ai(max_think)
            print(f'AI chose {choice} in {time.time() - t1} seconds.')
            board.move(choice)
            player_turn = not player_turn
    print(board)
    end = board.check_game_end()
    if end[1] == 0:
        print('Draw.')
    else:
        winner = 'X' if end[1] == 1 else 'O'
        print(f'{winner} wins!')

def play_loop(players):
    """
    Loops through several games, asks for user input between each one.

    Parameter players: How many people are playing
    Precondition: players is an int and 0 <= players <= 1
    """
    players = int(clamp(players, 0, 1))
    playing = True
    inp = 'a'
    while True:
        print('\nYou can always type "end" to end the program.')
        while playing:
            inp = input(f'Enter a board size between {MIN_SIZE} ' + \
                f'and {MAX_SIZE}: ')
            if inp == 'end' or inp == 'stop':
                playing = False
            if inp.isdigit():
                break
        while playing:
            think_input = input('How many seconds can the AI think for? ')
            if think_input == 'end' or think_input == 'stop':
                playing = False
            if think_input.isdigit():
                break
        if not playing:
            break
        size = int(clamp(int(inp), MIN_SIZE, MAX_SIZE))
        MODEL = models[size]
        if players == 0:
            play_0p(MODEL, size = int(inp), max_think = int(think_input))
        else:
            play_1p(MODEL, size = int(inp), max_think = int(think_input))

def main():
    while True:
        print('\nYou can always type "end" to end the program.')
        inp = input('How many players? Enter "0" or "1": ')
        if inp == 'end' or inp == 'stop':
            break
        if inp.isdigit():
            play_loop(int(inp))

if __name__ == '__main__':
    main()
