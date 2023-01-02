import random
import copy
import unittest
from src.game.board import Board

class AI:
    @staticmethod
    def get_placement(board):
        """
        Placement phase move generation for the computer
        :param board: current game board
        :return: the move to be executed
        """
        moves = AI.get_possible_placements(board)
        # print(moves)

        for m in moves:
            board_copy = copy.deepcopy(board)
            board_copy.board[m[0]][m[1]] = 'X'
            if board_copy.check_win() == "X":
                return m

        move = random.choice(moves)
        return move

    @staticmethod
    def get_possible_placements(board):
        """
        Generate all possible placement phase moves
        :param board: board
        :return: move list
        """
        moves = []

        for i in range(3):
            for j in range(3):
                if board.board[i][j] == '.':
                    moves.append((i, j))

        return moves

    @staticmethod
    def get_possible_movements(board):
        """
        Generate all possible movement phase moves
        :param board: board
        :return: move list
        """
        moves = []
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (0, -1),
            (1, -1)
        ]

        for i in range(3):
            for j in range(3):
                if board.board[i][j] == 'O':
                    ok = False
                    for d in directions:
                        if -1 < i+d[0] < 3 and -1 < j+d[1] < 3:
                            if board.board[i + d[0]][j + d[1]] == '.':
                                ok = True
                    if ok:
                        moves.append((i, j))

        return moves

    @staticmethod
    def get_movement(board):
        """
            movement phase move generation for the computer
            :param board: current game board
            :return: the move to be executed
        """
        moves = AI.get_possible_movements(board)

        for m in moves:
            board_copy = copy.deepcopy(board)
            board_copy.board[m[0]][m[1]] = 'O'
            if board_copy.check_win() == 'O':
                return m

        move = random.choice(moves)
        return move


class AITester(unittest.TestCase):
    def test_board(self):
        b = Board()
        b.do_placement(1, 1)
        # print(b)
        b.do_placement(1, 2)
        self.assertListEqual(AI.get_possible_placements(b), [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)])
        self.assertListEqual(AI.get_possible_movements(b), [(1, 2)])
        b.do_placement(2, 1)
        self.assertEqual(AI.get_placement(b), (0, 1))
        b.do_placement(0, 1)
        b.do_placement(2, 0)
        b.do_placement(0, 2)
        b.do_placement(2, 2)
        b.do_placement(1, 0)
        # print(b)
        self.assertEqual(AI.get_movement(b), (0, 1))
