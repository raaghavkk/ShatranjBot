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

    def findbestmove(self):
        self.nextmove = None
        valid_moves = list(self.board.legal_moves)
        random.shuffle(valid_moves)
        self.alphabetaNegaMax(valid_moves, DEPTH, -CHECKMATE, CHECKMATE)
        return self.nextmove

    def alphabetaNegaMax(self, validmoves, depth, alpha, beta):
        turn_multiplier = 1 if self.board.turn == chess.WHITE else -1
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
        return maxScore

    def scoreBoard(self):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -CHECKMATE  #Black wins
            else:
                return CHECKMATE  #White
