"""
A program for creating datasets to train a tictactoe model.

This program follows the basic structure of DeepMind's AlphaZero. It creates
random tictactoe boards and plays them to completion, recording the outcome of
the board. It is intended to be used in conjunction with a minimax algorithm
on tictactoe boards of size 4x4 or greater

Author: Jacob Dentes
Date: 18 September 2021
"""
import tictactoe
import pickle
import random

data_size = 0
save_frequency = 0

load_inputs = False
board_size = 4
think_time = 4

def eval(i):
    global board_size
    global think_time
    board = tictactoe.new_board(board_size)
    # Randomly play a random number of moves (undo move if game ends)
    for _ in range(random.randrange(board_size * board_size)):
        if len(board.legal_moves) <= 0 or board.check_game_end()[0]:
            board.unmove()
            break
        move = board.shuffled_legal_moves[0]
        board.move(move)
    # Save board state (and turn) as a useful neural net input
    input = board.flatten()
    input.append(1 if board.x_turn else -1)
    output = 0
    # Have our ai play through the rest of the game
    while True:
        board.move(board.ai(think_time))
        game_res = board.check_game_end()
        if game_res[0]:
            # Record the result of the game as the answer to the board state
            output = game_res[1]
            break
    return input, output

def main():
    file = input('Enter name of output file: ')
    inp = input('Load file? y/n ')
    if inp == 'y':
        load_inputs = True
    elif inp == 'n':
        load_inputs = False
    else:
        print('Invalid input, quitting program.')
        return

    data_size = int(input('Enter number of data points to generate: '))
    save_frequency = int(input('Enter how often to save: '))

    board_size = int(input('Enter board size: '))
    think_time = int(input('Enter max time per turn in seconds: '))

    import time
    t1 = time.time()

    io_list = []
    if load_inputs:
        with open(file, 'rb') as f:
            io_list = pickle.load(f)

    from multiprocessing import Pool
    for i in range(data_size//save_frequency):
        with Pool() as p:
            io_list.extend(list(p.map(eval, range(save_frequency))))
        print('\r' + str((i + 1) * save_frequency), end='')
        with open(file, 'wb') as f:
            pickle.dump(io_list, f)

    print('\n', io_list)
    print(f'Finished in {time.time() - t1}.')

if __name__ == '__main__':
    main()
