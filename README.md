
# ShatranjBot

A UCI chess bot created using python's chess library for the InnovateX Hackathon. We have taken inspiration from game theory videos and implemented the play algorithm using a mini-max algorithm with alpha and beta pruning to a max depth of 2 since it is a DFS algorithm. There is also an exe build available to be tested against real players using arena UI. We plan to update the bot so that it performs better against players and can also execute well known gambits.




![Logo](https://i.ibb.co/YyZjJ9J/SHATRANJ-BOT-1.png)


## Authors

- [@raaghavkk](https://github.com/raaghavkk/) 
- [@LakinduGimantha](https://github.com/LakinduGimantha)


## Acknowledgements

 - [Sebastian Lague on Youtube](https://www.youtube.com/watch?v=U4ogK0MIzqk)
 - [Python Chess README](https://python-chess.readthedocs.io/en/latest/)
 - [Playlist by Eddie Sharick](https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_)


## Documentation

Summary of UCI Commands

    uci: Initialize the engine.
    isready: Check if the engine is ready.
    ucinewgame: Start a new game.
    position startpos [moves ...]: Set the position and make moves.
    go: Calculate the best move.
    quit: Exit the engine

You can also use the engine using the provided exe in the repository under the dist folder and link it to arena UI
## Optimizations

Need to make a lot of Optimizations :0

