import chess
import sys
import logging
import random

board = chess.Board()
pieceScore={"K": 0, "Q": 10, "R": 5, "N": 3,"B": 3, "p": 1}
CHECKMATE=1000
STALEMATE=0

def findbm(board):
    valid_moves = list(board.legal_moves)
    turnmultiplier = 1 if board.turn else -1
    OpponentminmaxScore = CHECKMATE
    bestPleyermove = None
    random.shuffle(valid_moves)
    for playerMove in valid_moves:
        board.push(playerMove)
        Opponentmoves = list(board.legal_moves)
        if board.is_checkmate():
            score = -turnmultiplier * CHECKMATE
        elif board.is_stalemate():
            score = STALEMATE
        else:
            Opponentmaxscore = -CHECKMATE
            for opponentmove in Opponentmoves:
                board.push(opponentmove)
                if board.is_checkmate():
                    score = -turnmultiplier * CHECKMATE
                elif board.is_stalemate():
                    score = STALEMATE
                score = -turnmultiplier * scoring(board)
                if score > Opponentmaxscore:
                    OpponentmaxScore = score
                board.pop(opponentmove)
        if OpponentmaxScore < OpponentminmaxScore:
            OpponentminmaxScore = OpponentmaxScore
            bestPleyermove = playerMove
        board.pop(playerMove)
    return bestPleyermove
def scoring(board):
    score=0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] =='b':
                score -= pieceScore[square[1]]
    return score