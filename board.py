"""Class that defines the board for Mine Sweeper game.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
import numpy as np
from collections import deque


class MSBoard(object):
    """Define a Mine Sweeper Game Board."""

    def __init__(self, board_width, board_height, num_mines):
        """The init function of Mine Sweeper Game.

        Parameters
        ----------
        board_width : int
            the width of the board (> 0)
        board_height : int
            the height of the board (> 0)
        num_mines : int
            the number of mines, cannot be larger than
            (board_width x board_height)
        """
        if (board_width <= 0):
            raise ValueError("the board width cannot be non-positive!")
        else:
            self.board_width = board_width

        if (board_height <= 0):
            raise ValueError("the board height cannot be non-positive!")
        else:
            self.board_height = board_height

        if (num_mines >= (board_width*board_height)):
            raise ValueError("The number of mines cannot be larger than "
                             "number of grids!")
        else:
            self.num_mines = num_mines

        self.init_board()

    def init_board(self):
        """Init a valid board by given settings.

        Parameters
        ----------
        mine_map : numpy.ndarray
            the map that defines the mine
            0 is empty, 1 is mine
        info_map : numpy.ndarray
            the map that presents to gamer
            0-8 is number of mines in srrounding.
            9 is flagged field.
            10 is questioned field.
            11 is undiscovered field.
            12 is a mine field.
        """
        self.mine_map = np.zeros((self.board_height, self.board_width),
                                 dtype=np.uint8)
        idx_list = np.random.permutation(self.board_width*self.board_height)
        idx_list = idx_list[:self.num_mines]

        for idx in idx_list:
            idx_x = int(idx % self.board_width)
            idx_y = int(idx / self.board_width)

            self.mine_map[idx_y, idx_x] = 1

        self.info_map = np.ones((self.board_height, self.board_width),
                                dtype=np.uint8)*11

    

    def print_board(self):
        """Print board in structural way."""
        print(self.board_msg())

    def board_msg(self):
        """Structure a board as in print_board."""
        board_str = "s\t\t"
        for i in range(self.board_width):
            board_str += str(i)+"\t"
        board_str = board_str.expandtabs(4)+"\n\n"

        for i in range(self.board_height):
            temp_line = str(i)+"\t\t"
            for j in range(self.board_width):
                if self.info_map[i, j] == 9:
                    temp_line += "@\t"
                elif self.info_map[i, j] == 10:
                    temp_line += "?\t"
                elif self.info_map[i, j] == 11:
                    temp_line += "*\t"
                elif self.info_map[i, j] == 12:
                    temp_line += "!\t"
                else:
                    temp_line += str(self.info_map[i, j])+"\t"
            board_str += temp_line.expandtabs(4)+"\n"

        return board_str

    def create_board(self, board_width, board_height, num_mines):
        """Create a board by given parameters.
        Parameters
        ----------
        board_width : int
            the width of the board (> 0)
        board_height : int
            the height of the board (> 0)
        num_mines : int
            the number of mines, cannot be larger than
            (board_width x board_height)
        Returns
        -------
        board : MSBoard
        """
        return MSBoard(board_width, board_height, num_mines)