import random
import chess
import sys
import logging

logging.basicConfig(filename='smartmovefinder.log', level=logging.DEBUG)

def find_random_move(board):
    valid_moves = list(board.legal_moves)
    return random.choice(valid_moves)

def uci():
    logging.debug("uci")
    print("id name SmartMoveFinder")
    print("id author YourName")
    print("uciok")
    sys.stdout.flush()

def isready():
    logging.debug("isready")
    print("readyok")
    sys.stdout.flush()

def ucinewgame():
    logging.debug("ucinewgame")
    global board
    board = chess.Board()

def position(command):
    logging.debug(f"position {command}")
    global board
    board = chess.Board()
    if command.startswith("startpos"):
        moves = command.split()[2:]
        for move in moves:
            board.push(chess.Move.from_uci(move))
    elif command.startswith("fen"):
        fen = command[4:].split(" moves ")[0]
        board.set_fen(fen)
        if " moves " in command:
            moves = command.split(" moves ")[1].split()
            for move in moves:
                board.push(chess.Move.from_uci(move))

def go():
    logging.debug("go")
    move = find_random_move(board)
    print(f"bestmove {move.uci()}")
    sys.stdout.flush()

def quit():
    logging.debug("quit")
    sys.exit()

board = chess.Board()

while True:
    command = input().strip()
    logging.debug(f"Received command: {command}")
    if command == "uci":
        uci()
    elif command == "isready":
        isready()
    elif command == "ucinewgame":
        ucinewgame()
    elif command.startswith("position"):
        position(command[len("position "):])
    elif command.startswith("go"):
        go()
    elif command == "quit":
        quit()
