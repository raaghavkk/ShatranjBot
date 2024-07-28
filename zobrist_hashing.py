import chess
import random

# Initialize Zobrist tables
piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
zobrist_table = {
    piece_type: [[random.getrandbits(64) for _ in range(64)] for _ in range(2)]
    for piece_type in piece_types
}
zobrist_side = random.getrandbits(64)

def compute_zobrist_hash(board):
    h = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece.piece_type
            color = int(piece.color)
            h ^= zobrist_table[piece_type][color][square]
    if board.turn == chess.BLACK:
        h ^= zobrist_side
    return h
