from src.game.board import Board
from src.ai.ai import AI


class UI:
    def __init__(self):
        pass

    @staticmethod
    def print_welcome():
        print("WELCOME TO ACHI\n")

    @staticmethod
    def print_board(board):
        print(board)

    @staticmethod
    def print_phase(board):
        if board.phase == 1:
            print("PLACEMENT PHASE ONGOING")
        else:
            print("MOVEMENT PHASE ONGOING")

    @staticmethod
    def get_input():

        y = int(input("Y = "))
        x = int(input("X = "))
        return y, x

    @staticmethod
    def print_ai_move(move):
        print(f"\nAI executed the move: {move}\n")

    @staticmethod
    def print_win(param):
        if param == 'X':
            print("\nPLAYER WINS\n")
        else:
            print("\nCOMPUTER WINS\n")


class Game:
    def __init__(self):
        # self.ui = UI()
        self.board = Board()

    def start(self):
        UI.print_welcome()
        UI.print_board(self.board)
        UI.print_phase(self.board)

        while self.board.phase == 1:
            # Placement phase
            if self.board.player_to_move:
                i = None
                while i is None:
                    try:
                        i = UI.get_input()
                    except:
                        print("Invalid input")

                try:
                    self.board.do_placement(i[0], i[1])
                    if self.board.check_win() is not None:
                        UI.print_win(self.board.check_win())
                        return
                except ValueError as ve:
                    print(ve)
            else:
                move = AI.get_placement(self.board)
                self.board.do_placement(move[0], move[1])
                UI.print_ai_move(move)

            UI.print_board(self.board)
            if self.board.check_win() is not None:
                UI.print_win(self.board.check_win())
                return

        UI.print_phase(self.board)
        while self.board.phase == 2:
            # Movement Phase
            if self.board.player_to_move:
                i = None
                while i is None:
                    try:
                        i = UI.get_input()
                    except:
                        print("Invalid input")

                try:
                    self.board.do_movement(i[0], i[1])
                except ValueError as ve:
                    print(ve)
            else:
                move = AI.get_movement(self.board)
                self.board.do_movement(move[0], move[1])
                UI.print_ai_move(move)

            UI.print_board(self.board)
            if self.board.check_win() is not None:
                UI.print_win(self.board.check_win())
                running = False
                return


if __name__ == "__main__":
    game = Game()
    game.start()
