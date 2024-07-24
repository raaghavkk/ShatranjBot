import chess
import chess.engine

class ShatranjBot:
     def __init__(self):
         self.board = chess.Board()


     def uci(self):
         print("id name ShatranjBot")
         print("id author Raaghav")
         print("uciok")

     def isready(self):
         print("readyok")

     def ucinewgame(self):
         self.board.reset()
     #to reset board after each play

     def position(self, command):
         if "startpos" in command:
             self.board.reset()
             moves = command.split("moves") [1] if "moves" in command else ""
         else:
             fen = command.split("position fen ")[1].split(" moves")[0]
             moves = command.split(" moves ")[1] if " moves " in command else ""
             self.board.set_fen(fen)

         for move in moves.split():
             self.board.push(chess.Move.from_uci(move))

     def go(self):
         move = self.board.legal_moves.__next__()
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
         elif command.startswith("position")
             self.position(command)
         elif command.startswith("go"):
             self.go()
         elif command == "stop":
             self.stop()
         elif command == "quit"
             self.quit()

if __name__ == "__main__":
    engine = ShatranjBot()
    while True:
        try:
            command = input()
            engine.process_command(command)
        except (EOFError, KeyboardInterrupt):
            break
