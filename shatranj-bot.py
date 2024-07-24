import chess


class Shatranjbot:
    def __init__(self):
        self.board = chess.Board()

    def evaluate(self):
        return sum([self.piece_value(piece) for piece in self.board.piece_map().values()])

    def piece_value(self, piece):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values[piece.piece_type] * (1 if piece.color == chess.WHITE else -1)

    def minimax(self, depth, maximizing):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate()

        if maximizing:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, depth):
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
        print("id name ShatranjBot")
        print("id author Raaghav")
        print("uciok")

    def isready(self):
        print("readyok")

    def ucinewgame(self):
        self.board.reset()

    def position(self, command):
        if "startpos" in command:
            self.board.reset()
            moves = command.split("moves")[1] if "moves" in command else ""
        else:
            fen = command.split("position fen ")[1].split(" moves ")[0]
            moves = command.split(" moves ")[1] if " moves " in command else ""
            self.board.set_fen(fen)

        for move in moves.split():
            self.board.push(chess.Move.from_uci(move))

    def go(self):
        move = self.find_best_move(2)
        print(f"bestmove {move}")

    def stop(self):
        pass

    def quit(self):
        exit()

    def process_command(self, command):
        if command == "uci":
            self.uci()
        elif command == "isready":
            self.isready()
        elif command == "ucinewgame":
            self.ucinewgame()
        elif command.startswith("position"):
            self.position(command)
        elif command.startswith("go"):
            self.go()
        elif command == "stop":
            self.stop()
        elif command == "quit":
            self.quit()


if __name__ == "__main__":
    engine = Shatranjbot()
    while True:
        try:
            command = input()
            engine.process_command(command)
        except (EOFError, KeyboardInterrupt):
            break
