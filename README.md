
# ShatranjBot

ShatranjBot, uses advanced algorithms and techniques to find the optimal moves in a game of chess. It employs alpha-beta pruning with negamax search and Zobrist hashing for efficient transposition table management. The engine is designed to learn from all previous games, dynamically improving its performance over time. This trait was inspired by a character called "Mahoraga" who adapts to attacks and improves over time. 



![Logo](https://i.ibb.co/YyZjJ9J/SHATRANJ-BOT-1.png)


## Features
- **Alpha-Beta Pruning with Negamax Search**: Efficient search algorithm that reduces the number of nodes evaluated in the game tree.
- **Zobrist Hashing**: Fast hashing of board states for effective use of transposition tables.
- **Persistent Learning**: Transposition tables are saved after each game and loaded at the start, allowing the engine to learn from all previous games.
- **Piece-Square Tables**: Evaluation function that takes into account piece positions on the board.
- **UCI Protocol Support**: Implements the Universal Chess Interface (UCI) protocol for compatibility with various chess GUIs.
- **Stalemate and Checkmate Detection**: Accurately evaluates game-ending conditions. (most of the time anyways :/ )
## Installation

#### Clone the repository :

```bash
  git clone https://github.com/raaghavkk/ShatranjBot
```

#### Install dependencies :

```bash
  pip install -r requirements.txt
```

#### Compile to run with Arena GUI :

```bash
  pyinstaller --onefile findbestmove.py 
```

##### this will create a findbestmove.exe inside the dist directory which can be opened by the Arena GUI

## Play, Adapt, Conquer

![Inspired from Mahoraga](https://i.ibb.co/zXtxCB9/untit1ed.png)


## UCI Commands
### The engine supports the following UCI commands:

**uci** : Initializes the engine and prints engine details.

**isready** : Confirms the engine is ready.

**ucinewgame** : Resets the board for a new game.

**position [fen|startpos moves ...]** : Sets up the board position.

**go** : Starts the move search.

**stop** : Stops the move search.

**quit** : Exits the engine and saves the transposition table.

## How It Works :

### Transposition Table Management

- **Loading**: At startup, the engine loads all previous transposition table files from the `transposition_tables` directory, merging them to utilize all past game data.
- **Saving**: After each game, the current transposition table is saved with a timestamp, ensuring continuous learning.

### Search Algorithm

- The `alphabetaNegaMax` method performs the alpha-beta pruning within the negamax framework, efficiently exploring the game tree.
- Zobrist hashing is used to uniquely identify board states, enabling effective use of transposition tables to avoid redundant calculations.

### Board Evaluation

- Piece-square tables provide a static evaluation of piece positions, contributing to the overall board evaluation function used by the search algorithm.

## Authors

- [@raaghavkk](https://github.com/raaghavkk/) 
- [@LakinduGimantha](https://github.com/LakinduGimantha)


## Acknowledgements

 - [Sebastian Lague on Youtube](https://www.youtube.com/watch?v=U4ogK0MIzqk)
 - [Python Chess README](https://python-chess.readthedocs.io/en/latest/)
 - [Playlist by Eddie Sharick](https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_)


## Optimizations

Need to make a lot of Optimizations :0

