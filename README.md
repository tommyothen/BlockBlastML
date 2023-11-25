# Block Blast! Game with Machine Learning Solver
## Description
Block Blast! is a grid-based puzzle game where players place various shaped blocks onto a grid. The game features row and column clearing mechanics similar to classic puzzle games, with an added twist of machine learning integration for solving the game.

You may find the real downloadable game here: [iOS](https://apps.apple.com/gb/app/block-blast/id1617391485), [Android](https://play.google.com/store/apps/details?id=com.block.juggle) (Surprisingly addictive)

I wanted to learn how to use PyTorch and machine learning models and this game was the current game my friends and I were playing so I thought it would be a fun challenge to try and solve it with a machine learning model! This was my first time using pygame and PyTorch so I'm sure there are many improvements that can be made to the code.

- Tetrimino assets were created by [L-GAD](https://l-gad.itch.io/) and can be found [here](https://l-gad.itch.io/tetriminos-asset-pack).
- Lato Black font was created by [Łukasz Dziedzic](https://www.latofonts.com/lato-free-fonts/) and can be found [here](https://www.latofonts.com/lato-free-fonts/).

## How to Play
- Run the game, and the main window will display the game grid and upcoming blocks.
- Use the text input boxes to enter the index of the block (from the upcoming list) and the x, y coordinates on the grid where you want to place it. (The index of the block is the order in which it appears in the upcoming list, starting from 1 and counting up)
- The game checks for any complete rows or columns and clears them and awards points. (The points don't align with the real game and I haven't added combo points yet)
- The game ends when there's no space left to place any of the upcoming blocks.

## Requirements
- Python 3.x
- Pygame Library

## Installation
To run the game, you'll need Python and Pygame installed on your system. If you don't have Pygame installed, you can install it via pip:

```bash
pip install pygame
```

## Running the Game
To start the game, run the Python script:

```bash
python block_blast.py
```

## Future Enhancements
- Graphical User Interface for block selection and placement.
- Integration of a machine learning model to solve the puzzle automatically.
- Enhanced game-over conditions and scoring system.

## Author
- [Tommy Othen](https://github.com/tommyothen)
