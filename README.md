# tictactoe
A python module for playing tic tac toe of any square board size with a minimax implementation and a tensorflow-trained AI.

This is a simple project for playing 0, 1, or 2 player games of tic tac toe.
The project has a main tictactoe.py module for creating tic tac toe games of any square board size, and playing games of 0, 1, or 2 players. It contains move generation, a simple board evaluation function, and an implementation of alpha-beta pruning minimax with iterative deepening.

The playttt.py script utilizes the tictactoe module to play command-line games of tic tac toe.

The tttdatasets.py, traintfttt.py, and tftictactoe.py scripts are used to create datasets to train a tensorflow model, train the model, and play against the model, respectively. The latter two rely on tensorflow. They train and use a simple sequential model to evaluate a board state for the minimax algorithm. Models for 4x4 boards and 5x5 boards (each trained on about 15,000 games and tested on about 2,000 games) are provided.
