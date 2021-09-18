"""
A simple script for playing tic tac toe.

This script uses the tictactoe module to allow a player to play tic tac toe
through the command line.

Author: Jacob Dentes
Date: 6 September 2021
"""
import tictactoe

def main():
    running = True
    while running:
        p_count = -1
        while True:
            print('\nHow many players?\n')
            print('Please enter "0", "1", or "2".\n' +
            'Or, enter "end" or "restart"\n')
            inp = input()
            if inp == 'restart' or inp == 're':
                continue
            if inp == 'end' or inp == 'break':
                running = False
                break
            if inp.isdigit():
                p_count = int(inp)
                if 0 <= p_count <= 2:
                    print(f'\nChosen {p_count}-player game.')
                    break
                else:
                    print('Please enter "0", "1", or "2".\n' +
                    'Or, enter "end" or "restart"\n')
        if p_count == 2:
            size = 0
            while True:
                print('How large should each dimension of the board be?\n')
                print('Please enter a positive integer without a sign.\n' +
                'Or, enter "end" or "restart"\n')
                inp = input()
                if inp == 'restart' or inp == 're':
                    break
                if inp == 'end' or inp == 'break':
                    running = False
                    break
                if inp.isdigit():
                    size = int(inp)
                    if size > 0:
                        print(f'\nChosen {size}x{size} board.\n')
                        tictactoe.play_2p(size)
                        break
                    else:
                        print('Please enter a size greater than 0.\n' +
                        'Or, enter "end" or "restart"\n')
        if p_count == 1:
            size = 0
            while True:
                print('How large should each dimension of the board be?\n')
                print('Please enter a positive integer 4 or less.\n' +
                'Or, enter "end" or "restart"\n')
                inp = input()
                if inp == 'restart' or inp == 're':
                    break
                if inp == 'end' or inp == 'break':
                    running = False
                    break
                if inp.isdigit() and 0 < int(inp) <= 4:
                    size = int(inp)
                    if size > 0:
                        print(f'\nChosen {size}x{size} board.\n')
                        tictactoe.play_1p(size)
                        break
                    else:
                        print('Please enter a size greater than 0.\n' +
                        'Or, enter "end" or "restart"\n')
        if p_count == 0:
            size = 0
            while True:
                print('How large should each dimension of the board be?\n')
                print('Please enter a positive integer 4 or less.\n' +
                'Or, enter "end" or "restart"\n')
                inp = input()
                if inp == 'restart' or inp == 're':
                    break
                if inp == 'end' or inp == 'break':
                    running = False
                    break
                if inp.isdigit() and 0 < int(inp) <= 4:
                    size = int(inp)
                    if size > 0:
                        print(f'\nChosen {size}x{size} board.\n')
                        tictactoe.play_0p(size)
                        break
                    else:
                        print('Please enter a size greater than 0.\n' +
                        'Or, enter "end" or "restart"\n')

if __name__ == '__main__':
    main()
