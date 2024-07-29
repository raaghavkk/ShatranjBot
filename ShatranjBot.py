import chess
import sys
import random
import os
# As a file format to store transposition table
import pickle
from datetime import datetime
# imports the piece position scores for each type of piece for each position on the board.
from piece_tables import piece_position_score
# imports the Zobrist hash to get the hashing of the chess board for each position.
from zobrist_hashing import compute_zobrist_hash

# constants for certain game states of the game and  value of each chess piece is established.
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

# This variable determine how far will the algorithm will check from the current position.
DEPTH = 5

# Inside this directory transposition table files.
TABLES_DIR = 'transposition_tables'


class ShatranjBot:
    # Initialize the chess board, next move and load transposition tables.
    def __init__(self):
        self.board = chess.Board()
        self.nextmove = None
        self.transposition_table = self.load_all_transposition_tables()

    # Save the current transposition table to a file.
    def save_transposition_table(self):
        if not os.path.exists(TABLES_DIR):
            os.makedirs(TABLES_DIR)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(TABLES_DIR, f'transposition_table_{timestamp}.pkl')
        with open(file_path, 'wb') as f:
            pickle.dump(self.transposition_table, f)

    # Load all the transposition tables and merge them into one table
    def load_all_transposition_tables(self):
        combined_table = {}
        if not os.path.exists(TABLES_DIR):
            return combined_table

        files = [f for f in os.listdir(TABLES_DIR) if f.startswith('transposition_table') and f.endswith('.pkl')]
        for file in files:
            file_path = os.path.join(TABLES_DIR, file)
            with open(file_path, 'rb') as f:
                table = pickle.load(f)
                for key, value in table.items():
                    if key not in combined_table or table[key]['depth'] > combined_table[key]['depth']:
                        combined_table[key] = value
        return combined_table

    # Initiate negamax search algorithm with alphabeta pruning to a given depth and output the next move.
    def findbestmove(self):
        self.nextmove = None
        # get the available valid moves from the current position of the game
        valid_moves = list(self.board.legal_moves)
        # to prevent the repetitive moves at the beginning of the game
        random.shuffle(valid_moves)
        # Initiating the search algorithm
        self.alphabetaNegaMax(valid_moves, DEPTH, -CHECKMATE, CHECKMATE)
        # This is to avoid chess engine getting frozen when it detects its inevitable checkmate and defeat
        if self.nextmove == None:
            return random.choice(valid_moves)
        else:
            return self.nextmove

    # Find the best move according to the scoring method for the current position of the chess board to a given depth.
    # alpha is given the worst possible scenario score and beta is given the best possible scenario score as inputs
    def alphabetaNegaMax(self, validmoves, depth, alpha, beta):
        # Identify the whose turn within the search algorithm
        turn_multiplier = 1 if self.board.turn == chess.WHITE else -1

        # Take the hashing for the current positioning of the board
        board_hash = compute_zobrist_hash(self.board)

        # Below codes are implemented to decrease the processing time of the search engine.
        # Check whether search algorithm evaluated a best move in previous attempts
        if board_hash in self.transposition_table:
            entry = self.transposition_table[board_hash]
            # This is implemented in order check whether the move that got selected is best for the given depth.
            if entry['depth'] >= depth:
                return entry['value']

        # This initiate the scoring for the current position when it reach the end of a search for a given depth.
        if depth == 0:
            return turn_multiplier * self.scoreBoard()

        # negamax search algorithm with alphabeta pruning truly start from here.
        # maxScore is given the worst possible outcome from player perspective where opponent is checkmating the player.
        # This is reasoning for the negative mark.
        maxScore = -CHECKMATE
        for move in validmoves:
            # move is implemented from the validmoves list.
            self.board.push(move)
            # Generate the next list of valid moves for the current positioning.
            nextmoves = list(self.board.legal_moves)
            # search algorithm is recursively implemented until it reach the end(depth = 0).
            score = -self.alphabetaNegaMax(nextmoves, depth - 1, -beta, -alpha)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    self.nextmove = move
            # moves are undone to get the board to it previous state before implementing next path of the moves
            self.board.pop()
            # pruning happen here to prevent the loop from executing useless moves for a current position.
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break

        # value and depth is stored for the current positioning.
        self.transposition_table[board_hash] = {'value': maxScore, 'depth': depth}
        return maxScore

    # Scoring mechanism of the chess engine
    def scoreBoard(self):
        # check the positions on the board to see whether there is checkmate.
        if self.board.is_checkmate():
            # following lines of code are used to determine who is checkmated.
            if self.board.turn == chess.WHITE:
                return -CHECKMATE  # Black wins
            else:
                return CHECKMATE  # White wins
        # Here checking for stalemate
        elif self.board.is_stalemate():
            return STALEMATE

        # Each square of the chessboard is evaluated
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            # Here checks whether there is a piece inside the square
            if piece:
                # piece value is taken from piece_score dictionary using piece type at that square.
                piece_value = piece_score.get(piece.piece_type, 0)
                # This is implemented because piece positioning score for each piece is written in white piece perspective.
                # mirroring is used to identify how black side of the board will see the position in the perspective white side.
                squaren = square if piece.color == chess.WHITE else chess.square_mirror(square)
                # piece position value is obtained from the square it is in and the type of the piece
                piece_position_value = piece_position_score.get(piece.piece_type, 0)[squaren]
                #score is added to the total if piece is white and score is substracted from the total if the piece is black
                if piece.color == chess.WHITE:
                    score += piece_value + piece_position_value
                else:
                    score -= piece_value + piece_position_value
        return score

    # uci integration protocols
    def uci(self):
        print("id name Mahoraga")
        print("id author Lakindu & Raaghav")
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

    # Here chess initiate its algorithm for its each turn using the function suggested.
    def go(self):
        best_move = self.findbestmove()
        if best_move:
            print(f"bestmove {best_move}")

    # In here we save the data even if we stop the game before reaching its end.
    def stop(self):
        self.save_transposition_table()
        sys.exit()

    # After ending the game the transposition data is saved.
    def quit(self):
        self.save_transposition_table()
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
    engine = ShatranjBot()
    while True:
        try:
            command = input().strip()
            engine.process_command(command)
        except (EOFError, KeyboardInterrupt):
            engine.quit()
            break
