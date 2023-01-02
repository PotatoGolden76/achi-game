from texttable import Texttable
import unittest


class Board:
    def __init__(self):
        self._board_size = 3
        self._board = None
        self._init_board()

        self._player_move = True

        self._p_pieces = 4
        self._c_pieces = 4

        self._phase = 1  # 1 - placement; 2 - movement

    """
    Properites
    """
    @property
    def size(self):
        return self._board_size

    @property
    def player_pieces(self):
        return self._p_pieces

    @property
    def computer_pieces(self):
        return self._c_pieces

    @property
    def phase(self):
        return self._phase

    @property
    def player_to_move(self):
        return self._player_move

    @property
    def board(self):
        return self._board

    def _init_board(self):
        """
        Board initialisation
        :return: N/A
        """
        self._board = []
        for i in range(self._board_size):
            y = []
            for j in range(self._board_size):
                y.append(".")
            self._board.append(y)

    def __str__(self):
        """
        String representation using texttable
        :return: string of the board
        """
        table = Texttable()
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])

        for i in range(self._board_size):
            table.add_row(self._board[i])

        return table.draw()

    def do_placement(self, y, x):
        """
        Placement phase move
        :param y: y coord
        :param x: x coord
        :return: N/A
        """
        if not -1 < x < 3:
            raise ValueError("Invalid coord")
        if not -1 < y < 3:
            raise ValueError("Invalid coord")
        if self._board[y][x] != '.':
            raise ValueError("Invalid coord")

        code = None
        if self._player_move:
            code = 'X'
            self._p_pieces -= 1
        else:
            self._c_pieces -= 1
            code = 'O'

        self._board[y][x] = code
        if self._p_pieces == 0 and self._c_pieces == 0:
            self._phase = 2
            self._player_move = True
        else:
            self._player_move = not self._player_move

    def do_movement(self, y, x):
        """
        Movement phase move
        :param y: y coord
        :param x: x coord
        :return: N/A
        """
        code = None
        if self._player_move:
            code = 'X'
        else:
            code = 'O'

        if not -1 < x < 3:
            raise ValueError("Invalid coord")
        if not -1 < y < 3:
            raise ValueError("Invalid coord")
        if self._board[y][x] != code:
            raise ValueError("Invalid coord")

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

        directions = [d for d in directions if -1 < d[0]+y < 3 and -1 < d[1]+x < 3]
        # print(directions)
        directions = [d for d in directions if self._board[y + d[0]][x + d[1]] == '.']
        # print(directions)

        if len(directions) > 0:
            self._board[y + directions[0][0]][x + directions[0][1]] = code
            self._board[y][x] = '.'
            self._player_move = not self._player_move

    def check_win(self):
        """
        Win checking fucnction
        :return: None, if no win is present, X if the Player wins, O if the Computer wins
        """
        # print("CHECKING WIN")
        code = None

        for i in range(3):  # line check
            ok = True
            for j in range(2):
                if self._board[i][j] != self._board[i][2]:
                    ok = False
            if ok and self._board[i][2] != '.':
                code = self._board[i][2]
                # print(1)
                return code

        for i in range(3):  # col check
            ok = True
            for j in range(2):
                if self._board[j][i] != self._board[2][i]:
                    ok = False
            if ok and self._board[2][i] != '.':
                code = self._board[2][i]
                # print(2)
                return code

        ok = True
        for i in range(2):  # main diag check

            if self._board[i][i] != self._board[2][2]:
                # print(self._board[i][i])

                ok = False
            if ok and self._board[2][2] != '.':
                code = self._board[2][2]
                # print(3)
                return code

        ok = True
        for i in range(2):  # seco diag check

            if self._board[i][2-i] != self._board[2][0]:
                ok = False
            if ok and self._board[2][0] != '.':
                code = self._board[2][0]
                # print(4)
                return code

        # print(code)
        return code


class BoardTester(unittest.TestCase):
    def test_board(self):
        b = Board()

        self.assertEqual(b.size, 3)
        self.assertEqual(b.phase, 1)
        self.assertEqual(b.computer_pieces, 4)
        self.assertEqual(b.player_pieces, 4)

        with self.assertRaises(ValueError):
            b.do_placement(-1, 1)
        with self.assertRaises(ValueError):
            b.do_placement(1, -1)
        with self.assertRaises(ValueError):
            b.do_placement(3, 3)

        with self.assertRaises(ValueError):
            b.do_movement(-1, 1)
        with self.assertRaises(ValueError):
            b.do_movement(1, -1)
        with self.assertRaises(ValueError):
            b.do_movement(3, 3)

        b.do_placement(1, 1)
        # print(b)
        b.do_placement(1, 2)
        # print(b)
        with self.assertRaises(ValueError):
            b.do_placement(1, 1)

        b.do_movement(1, 1)
        # print(b)
        b.do_movement(1, 2)
        # print(b)
        self.assertEqual(b.board[0][0], "X")
        self.assertEqual(b.board[0][1], "O")
        b.do_placement(1, 0)
        # print(b)
        b.do_placement(1, 1)
        b.do_placement(2, 0)
        self.assertEqual(b.check_win(), "X")

