import chess

# Define piece scores for evaluation
piece_score = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# Create a chess board
board = chess.Board()

# Print the board and legal moves
print(board)
print(board.legal_moves)

# Convert legal moves to a list
valid_moves = list(board.legal_moves)

# Print the type of the first legal move
print(type(valid_moves[0]))
print(valid_moves)
# Push the first valid move
board.push(valid_moves[0])


# Print the board after the move
print(board)

# Define the test class for board evaluation
class test:
    def __init__(self):
        self.board = chess.Board()

    def evaluate_board(self):
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            print(piece)
            if piece:
                piece_value = piece_score.get(piece.piece_type, 0)
                print(piece_value)
                score += piece_value if piece.color == chess.WHITE else -piece_value
                print(score)
        return score

# Create an instance of the test class
test_instance = test()

# Evaluate the board score
print(test_instance.evaluate_board())

turn = board.turn == chess.WHITE
print(turn)

print(board.piece_at(chess.SQUARES[23]))
