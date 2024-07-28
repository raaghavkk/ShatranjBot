import chess
import sys
import random
from piece_tables import piece_position_score

CHECKMATE = 1000
STALEMATE = 0
piece_score = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 0
}
DEPTH = 5

class FindBestMove:
    def __init__(self):
        self.board = chess.Board()
        self.nextmove = None
        self.transposition_table = {}

    def findbestmove(self):
        self.nextmove = None
        valid_moves = list(self.board.legal_moves)
        random.shuffle(valid_moves)
        self.alphabetaNegaMax(valid_moves, DEPTH, -CHECKMATE, CHECKMATE)
        return self.nextmove

    def alphabetaNegaMax(self, validmoves, depth, alpha, beta):
        turn_multiplier = 1 if self.board.turn == chess.WHITE else -1

        board_hash = self.board.zobrist_hash(self.board)

        if board_hash in self.transposition_table:
            entry = self.transposition_table[board_hash]
            if entry['depth'] >= depth:
                return entry['value']

        if depth == 0:
            return turn_multiplier * self.scoreBoard()
        # move ordering around here.
        maxScore = -CHECKMATE
        for move in validmoves:
            self.board.push(move)
            nextmoves = list(self.board.legal_moves)
            score = -self.alphabetaNegaMax(nextmoves, depth - 1, -beta, -alpha)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    self.nextmove = move
            self.board.pop()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        self.transposition_table[board_hash] = {'value' : maxScore, 'depth' : depth}
        return maxScore

    def scoreBoard(self):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -CHECKMATE  #Black wins
            else:
                return CHECKMATE  #White wins
        elif self.board.is_stalemate():
            return STALEMATE

        else:
            score = 0
            for square in chess.SQUARES:
                piece = self.board.piece_at(square)
                if piece:
                    piece_value = piece_score.get(piece.piece_type, 0)
                    squaren = square if piece.color == chess.WHITE else chess.square_mirror(square)
                    piece_position_value = piece_position_score.get(piece.piece_type, 0)[squaren]
                    if piece.color == chess.WHITE:
                        score += piece_value + piece_position_value
                    else:
                        score -= piece_value + piece_position_value
            return score

    def uci(self):
        print("id name FindBestMove")
        print("id author Lakindu")
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
        best_move = self.findbestmove()
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
