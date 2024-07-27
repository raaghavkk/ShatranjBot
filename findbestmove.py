import chess
import sys
import random

CHECKMATE = 1000
STALEMATE = 0
piece_score = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


class FindBestMove:
    def __init__(self):
        self.board = chess.Board()

    def evaluate_board(self):
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_value = piece_score.get(piece.piece_type, 0)
                score += piece_value if piece.color == chess.WHITE else -piece_value
        return score

    def find_best_move(self):
        valid_moves = list(self.board.legal_moves)
        turn_multiplier = 1 if self.board.turn == chess.WHITE else -1
        opponent_minimax_score = CHECKMATE
        best_player_move = None
        random.shuffle(valid_moves)

        for player_move in valid_moves:
            self.board.push(player_move)
            opponent_moves = list(self.board.legal_moves)
            if self.board.is_checkmate():
                score = -turn_multiplier * CHECKMATE
            elif self.board.is_stalemate():
                score = STALEMATE
            else:
                opponent_max_score = -CHECKMATE
                for opponent_move in opponent_moves:
                    self.board.push(opponent_move)
                    if self.board.is_checkmate():
                        score = CHECKMATE
                    elif self.board.is_stalemate():
                        score = STALEMATE
                    else:
                        score = -turn_multiplier * self.evaluate_board()
                    if score > opponent_max_score:
                        opponent_max_score = score
                    self.board.pop()
                if opponent_max_score < opponent_minimax_score:
                    opponent_minimax_score = opponent_max_score
                    best_player_move = player_move
            self.board.pop()
        return best_player_move

    def uci(self):
        print("id name FindBestMove")
        print("id author YourName")
        print("uciok")

    def isready(self):
        print("readyok")

    def ucinewgame(self):
        self.board.reset()

    def position(self, command):
        if "startpos" in command:
            self.board.reset()
            moves = command.split(" moves ")[1] if " moves " in command else ""
        else:
            fen = command.split("position fen ")[1].split(" moves ")[0]
            moves = command.split(" moves ")[1] if " moves " in command else ""
            self.board.set_fen(fen)
        for move in moves.split():
            self.board.push(chess.Move.from_uci(move))

    def go(self):
        best_move = self.find_best_move()
        if best_move:
            print(f"bestmove {best_move}")

    def stop(self):
        pass

    def quit(self):
        sys.exit()

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
    engine = FindBestMove()
    while True:
        try:
            command = input().strip()
            engine.process_command(command)
        except (EOFError, KeyboardInterrupt):
            break


