

from __future__ import print_function
import numpy as np
from collections import deque

#Definimos el tablero del juego
class MinesweeperBoard(object):
   

    def __init__(self, board_width, board_height, num_mines):
       #Parámetros del init:
       # board_width : int  --> [Ancho del tablero(> 0)]
       # board_height : int  --> [Altura del tablero (> 0)]
       # num_mines : int  --> [número de minas, no puede ser mayor que (board_width x board_height)]
      
        if (board_width <= 0):
            raise ValueError("El tablero no puede ser negativo")
        else:
            self.board_width = board_width

        if (board_height <= 0):
            raise ValueError("No puede tener una altura negativa el tablero")
        else:
            self.board_height = board_height

        if (num_mines >= (board_width*board_height)):
            raise ValueError("El número de minas no puede ser mayoy que el ancho-alto del tablero")

        else:
            self.num_mines = num_mines

        self.init_board()

    def init_board(self):
        #Crea un tablero válido dados los parámetros (board_width, board_height, num_mines)
        # 
        # PARÁMETROS:
        #  mine_map : numpy.ndarray [el map que define las minas: 0 is empty, 1 is mine]
        #  info_map : numpy.ndarray [mapa que se le presenta al jugador:
        #               0-8 número de minas alrededor,
        #               11 celda marcada con bandera,
        #               7 celda marcada con interrogación,
        #               88 celda sin descibrir,
        #               99 mina.
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
        print(self.board_msg())

    def board_msg(self):
       #Estructuramos el tablero para imprimirlo.
        board_str = "s\t\t"
        for i in range(self.board_width):
            board_str += str(i)+"\t"
        board_str = board_str.expandtabs(4)+"\n\n"

        for i in range(self.board_height):
            temp_line = str(i)+"\t\t"
            for j in range(self.board_width):
                if self.info_map[i, j] == 11:
                    temp_line += "@\t"
                elif self.info_map[i, j] == 7:
                    temp_line += "?\t"
                elif self.info_map[i, j] == 88:
                    temp_line += "*\t"
                elif self.info_map[i, j] == 99:
                    temp_line += "!\t"
                else:
                    temp_line += str(self.info_map[i, j])+"\t"
            board_str += temp_line.expandtabs(4)+"\n"

        return board_str

    def create_board(self, board_width, board_height, num_mines):
        #Parámetros:
       # board_width : int  --> [Ancho del tablero(> 0)]
       # board_height : int  --> [Altura del tablero (> 0)]
       # num_mines : int  --> [número de minas, no puede ser mayor que (board_width x board_height)]
        return MinesweeperBoard(board_width, board_height, num_mines)

