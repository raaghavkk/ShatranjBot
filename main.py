import chess
import subprocess

# Command to run the custom engine script
custom_engine_command = ["python", "smartmovefinder.py"]

# Create the board
board = chess.Board()

# Initialize two instances of your custom engine
engine_1_process = subprocess.Popen(
    custom_engine_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True
)
engine_2_process = subprocess.Popen(
    custom_engine_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True
)

# Function to communicate with the custom engine
def custom_engine_play(engine_process, board):
    engine_process.stdin.write(board.fen() + "\n")
    engine_process.stdin.flush()
    move = engine_process.stdout.readline().strip()
    return chess.Move.from_uci(move)

# Function to play a move using the given engine process
def play_move(engine_process, board):
    move = custom_engine_play(engine_process, board)
    board.push(move)
    print(board)
    print()

# Play the game
try:
    while not board.is_game_over():
        # Engine 1 plays
        play_move(engine_1_process, board)
        if board.is_game_over():
            break

        # Engine 2 plays
        play_move(engine_2_process, board)

    print("Game over")
    print("Result: ", board.result())
finally:
    engine_1_process.terminate()
    engine_2_process.terminate()


