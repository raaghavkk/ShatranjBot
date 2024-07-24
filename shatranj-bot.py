import chess


class Shatranjbot:
    def __init__(self):
        #initialise the ches board
        self.board = chess.Board()

    def evaluate(self):
        # evaluate the board by summation of values of all pieces
        return sum([self.piece_value(piece) for piece in self.board.piece_map().values()])

    def piece_value(self, piece):
        # Assign values to pieces: pawn=1, knight=3, bishop=3, rook=5, queen=9, king=0
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        # Multiply value by 1 if piece is white, -1 if piece is black (this is stupid but it works like my own signed integer)
        return values[piece.piece_type] * (1 if piece.color == chess.WHITE else -1)

    def minimax(self, depth, maximizing):
        # Minimax algorithm to evaluate board positions to a certain depth (inspiration taken from stackoverflow)
        if depth == 0 or self.board.is_game_over():
            return self.evaluate()

        if maximizing:
            # Maximizing player (white)
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            # Minimizing player (black)
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, depth):
        # Find the best move by evaluating all legal moves
        best_move = None
        best_value = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = self.minimax(depth - 1, False)
            self.board.pop()
            if board_value > best_value:
                best_value = board_value
                best_move = move
        return best_move

    def uci(self):
        # Output engine identification and UCI support status
        print("id name ShatranjBot")
        print("id author Raaghav")
        print("uciok")

    def isready(self):
        # Confirm engine readiness (so that there are no bugs
        print("readyok")

    def ucinewgame(self):
        #reset the board for a new game
        self.board.reset()

    def position(self, command):
        # set up the board position based on the command
        if "startpos" in command:
            # Standard starting position
            self.board.reset()
            moves = command.split("moves")[1] if "moves" in command else ""
        else:
            # custom position given by fen string
            fen = command.split("position fen ")[1].split(" moves ")[0]
            moves = command.split(" moves ")[1] if " moves " in command else ""
            self.board.set_fen(fen)

        #apply all moves to the board
        for move in moves.split():
            self.board.push(chess.Move.from_uci(move))

    def go(self):
        #calculate the best move to a depth of 2 and output it
        move = self.find_best_move(2)
        print(f"bestmove {move}")

    def stop(self):
        # am supposed to implement a stop search (I havent yet lmao)
        pass

    def quit(self):
        #exit the engine
        exit()

    def process_command(self, command):
        #to initialise the engine
        if command == "uci":
            self.uci()
        #Check if the engine is ready
        elif command == "isready":
            self.isready()
        # Start a new game and reset old pos
        elif command == "ucinewgame":
            self.ucinewgame()
        # use position startpos [moves] to set the position and moves
        elif command.startswith("position"):
            self.position(command)
        # go to callculate the best move
        elif command.startswith("go"):
            self.go()
        elif command == "stop":
            self.stop()
        # exit the engine
        elif command == "quit":
            self.quit()


if __name__ == "__main__":
    # Main loop to read commands from standard input
    engine = Shatranjbot()
    while True:
        try:
            command = input()
            engine.process_command(command)
        except (EOFError, KeyboardInterrupt):
            # exit on end of input or keyboard interrupt
            break
