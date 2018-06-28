"""Class that defines the Mine Sweeper Game.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
import socket
from msboard import MSBoard
import numpy as np



class MSGame(object):
    """Define a Mine Sweeper game."""

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
        port : int
            UDP port number, default is 5678
        ip_add : string
            the ip address for receiving the command,
            default is localhost.
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

        # self.TCP_PORT = port
        # self.TCP_IP = ip_add
        # self.BUFFER_SIZE = 1024

        self.move_types = ["click", "flag", "unflag", "question"]

        self.init_new_game()

    def init_new_game(self, with_tcp=False):
        """Init a new game.

        Parameters
        ----------
        board : MSBoard
            define a new board.
        game_status : int
            define the game status:
            0: lose, 1: win, 2: playing
        moves : int
            how many moves carried out.
        """
        self.board = self.create_board(self.board_width, self.board_height,
                                       self.num_mines)
        self.game_status = 2
        self.num_moves = 0
        self.move_history = []

    def reset_game(self):
        """Reset game."""
        self.init_new_game(with_tcp=False)

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

    def check_move(self, move_type, move_x, move_y):
        """Check if a move is valid.

        If the move is not valid, then shut the game.
        If the move is valid, then setup a dictionary for the game,
        and update move counter.

        TODO: maybe instead of shut the game, can end the game or turn it into
        a valid move?

        Parameters
        ----------
        move_type : string
            one of four move types:
            "click", "flag", "unflag", "question"
        move_x : int
            X position of the move
        move_y : int
            Y position of the move
        """
        if move_type not in self.move_types:
            raise ValueError("This is not a valid move!")
        if move_x < 0 or move_x >= self.board_width:
            raise ValueError("This is not a valid X position of the move!")
        if move_y < 0 or move_y >= self.board_height:
            raise ValueError("This is not a valid Y position of the move!")

        move_des = {}
        move_des["move_type"] = move_type
        move_des["move_x"] = move_x
        move_des["move_y"] = move_y
        self.num_moves += 1

        return move_des

    def play_move(self, move_type, move_x, move_y):
        """Updat board by a given move.

        Parameters
        ----------
        move_type : string
            one of four move types:
            "click", "flag", "unflag", "question"
        move_x : int
            X position of the move
        move_y : int
            Y position of the move
        """
        # record the move
        if self.game_status == 2:
            self.move_history.append(self.check_move(move_type, move_x,
                                                     move_y))
        else:
            self.end_game()

        # play the move, update the board
        if move_type == "click":
            self.board.click_field(move_x, move_y)
        elif move_type == "flag":
            self.board.flag_field(move_x, move_y)
        elif move_type == "unflag":
            self.board.unflag_field(move_x, move_y)
        elif move_type == "question":
            self.board.question_field(move_x, move_y)

        # check the status, see if end the game
        if self.board.check_board() == 0:
            self.game_status = 0  # game loses
            # self.print_board()
            self.end_game()
        elif self.board.check_board() == 1:
            self.game_status = 1  # game wins
            # self.print_board()
            self.end_game()
        elif self.board.check_board() == 2:
            self.game_status = 2  # game continues
            # self.print_board()

    def print_board(self):
        """Print board."""
        self.board.print_board()

    def get_board(self):
        """Get board message."""
        return self.board.board_msg()

    def get_info_map(self):
        """Get info map."""
        return self.board.info_map

    def get_nodes(self):
        """Get info map."""
        return self.board.list_nodes
    
    def name_nodes(self):
        """ Recorre la matriz de información del juego y les da nombre
        a los elementos respecto de su posicíon (i,j) en la matriz.
        La posición de (0,0) correspondería con X00 hasta (m,n) dónde nombraría Xmn """
        nodes_names = []
        for i in range(self.board.board_width):
            for j in range(self.board.board_height):
                nodes_names.append("X" + str(i) + str(j))
        return nodes_names
    
    def es_esquina(self,i,j):
        """ Numeración de las esquinas 
            No es esquina = 0
            Esquina Arriba izquierda = 1
            Esquina arriba derecha = 2
            Esquina abajo derecha = 3
            Esquina abajo izquierda = 4
        
        """
        width1 = self.board_width
        height1 = self.board_height
        esEsquina = False
        if ((i is 0) and (j is 0)):
            esEsquina = True
            num_esquina = 1
        elif ((i is width1-1) and (j is 0)):
            esEsquina = True
            num_esquina = 2
        elif (i is width1-1) and (j is height1-1):
            esEsquina = True
            num_esquina = 3
        elif ((i is 0) and (j is height1-1)):
            esEsquina = True
            num_esquina = 4
        else:
            esEsquina = False
            num_esquina = 0

        return esEsquina, num_esquina
    
    def es_lateral(self,i,j):
        """ Numeración de los laterales 
            No es lateral = 0
            Lateral izquierdo = 1
            Lateral derecho = 2
            Techo = 3
            Suelo = 4
        
        """
        esLateral = False
        width1 = self.board_width
        height1 = self.board_height

        if i is 0:
            lateral = 1
            esLateral = True
        elif i is width1-1:
            lateral = 2
            esLateral = True
        elif j is 0:
            lateral = 3
            esLateral = True
        elif j is height1-1:
            lateral = 4
            esLateral = True
        else:
            esLateral = False
            lateral = 0

        return esLateral,lateral


    def neightbours_of_position(self,i,j):
        """
        Ayuda a encontrar los vecinos (casillas adyacentes) de una casilla dada
        """
        neightbours_of_position = []
        g = (j+1) + ((i+1) - 1) * self.board.board_width -1
        x = self.name_nodes()
        esEsquinaYCual = self.es_esquina(i,j)
        esLateralYCual = self.es_lateral(i,j)

        if not esEsquinaYCual[0] and not esLateralYCual[0]:
            neight_hori_izq = x[g-1] 
            neight_hori_dch = x[g+1] 
            width3 = self.board_width
            neight_ver_arr = x[g-width3]
            neight_ver_abj = x[g+width3]
            neight_diag_iz_arri = x[g-width3-1]
            neight_diag_iz_abaj = x[g+width3-1]
            neight_diag_dcha_arri = x[g-width3+1]
            neight_diag_dcha_abaj = x[g+width3+1]

            neightbours_of_position.append(neight_hori_dch)
            neightbours_of_position.append(neight_hori_izq)
            neightbours_of_position.append(neight_ver_abj)
            neightbours_of_position.append(neight_ver_arr)
            neightbours_of_position.append(neight_diag_iz_arri)
            neightbours_of_position.append(neight_diag_iz_abaj)
            neightbours_of_position.append(neight_diag_dcha_abaj)
            neightbours_of_position.append(neight_diag_dcha_arri)
            
        elif esEsquinaYCual[0]:
            width1 = self.board_width
            if esEsquinaYCual[1] is 1:
                neight_hori_dch = x[g+1]
                neight_ver_abj = x[g+width1]
                neight_diag_dcha_abaj = x[g+width1+1]
                neightbours_of_position.append(neight_hori_dch)
                neightbours_of_position.append(neight_ver_abj)
                neightbours_of_position.append(neight_diag_dcha_abaj)
            elif esEsquinaYCual[1] is 2:
                neight_hori_izq = x[g-width1]
                neight_ver_abj = x[g+1]
                neight_diag_iz_abaj = x[g-width1+1]
                neightbours_of_position.append(neight_hori_izq)
                neightbours_of_position.append(neight_ver_abj)
                neightbours_of_position.append(neight_diag_iz_abaj)
            elif esEsquinaYCual[1] is 3:
                neight_ver_arr = x[g-width1]
                neight_hori_dch = x[g-1]
                neight_diag_iz_arri = x[g-width1-1]
                neightbours_of_position.append(neight_ver_arr)
                neightbours_of_position.append(neight_hori_dch) 
                neightbours_of_position.append(neight_diag_iz_arri)
            else:
                neight_ver_arr = x[g+width1]
                neight_hori_izq = x[g-1]
                neight_diag_dcha_arri = x[g+width1-1]
                neightbours_of_position.append(neight_ver_arr)
                neightbours_of_position.append(neight_hori_izq)
                neightbours_of_position.append(neight_diag_dcha_arri)
        else:
            width2 = self.board_width
            if esLateralYCual[1] is 1:
                neight_ver_arr = x[g-1]
                neight_ver_abj = x[g+1]
                neight_hori_dch = x[g+width2]
                neight_diag_dcha_arri = x[g+width2-1]
                neight_diag_dcha_abaj = x[g+width2+1]
                neightbours_of_position.append(neight_ver_arr)
                neightbours_of_position.append(neight_ver_abj)
                neightbours_of_position.append(neight_hori_dch)
                neightbours_of_position.append(neight_diag_dcha_arri)
                neightbours_of_position.append(neight_diag_dcha_abaj)
            elif esLateralYCual[1] is 2:
                neight_ver_arr = x[g-width2]
                neight_ver_abj = x[g+1]
                neight_hori_izq = x[g-1]
                neight_diag_iz_arri = x[g-width2-1]
                neight_diag_iz_abaj = x[g-width2+1]
                neightbours_of_position.append(neight_ver_arr)
                neightbours_of_position.append(neight_ver_abj)
                neightbours_of_position.append(neight_hori_izq)
                neightbours_of_position.append(neight_diag_iz_arri)
                neightbours_of_position.append(neight_diag_iz_abaj)
            elif esLateralYCual[1] is 3:
                neight_hori_izq = x[g-width2]
                neight_hori_dch = x[g+1]
                neight_ver_abj = x[g+width2]
                neight_diag_iz_abaj = x[g-width2+1]
                neight_diag_dcha_abaj = x[g+width2+1]
                neightbours_of_position.append(neight_hori_izq)
                neightbours_of_position.append(neight_hori_dch)
                neightbours_of_position.append(neight_ver_abj)
                neightbours_of_position.append(neight_diag_iz_abaj)
                neightbours_of_position.append(neight_diag_dcha_abaj)
            else:
                neight_hori_izq = x[g-1]
                neight_hori_dch = x[g+width2]
                neight_ver_arr = x[g-width2]
                neight_diag_iz_arri = x[g-width2-1]
                neight_diag_dcha_arri = x[g+width2-1]
                neightbours_of_position.append(neight_hori_izq)
                neightbours_of_position.append(neight_hori_dch)
                neightbours_of_position.append(neight_ver_arr)
                neightbours_of_position.append(neight_diag_iz_arri)
                neightbours_of_position.append(neight_diag_dcha_arri)


        return neightbours_of_position

    def get_mine_map(self):
        """Get mine map."""
        return self.board.mine_map

    def end_game(self):
        """Settle the end game.

        TODO: some more expections..
        """
        if self.game_status == 0:
            print(" [ 💣 💣 💣 💣 💣 💣 ] ¡ HAS PERDIDO ! [ 💣 💣 💣 💣 💣 💣 ]")
        elif self.game_status == 1:
            print(" 🎉 🎉 🎉 🎉 🎉  TODAS LAS BOMBAS MARCADAS, HAS GANADO.  🎉 🎉 🎉 🎉 🎉  ")

    def parse_move(self, move_msg):
        """Parse a move from a string.

        Parameters
        ----------
        move_msg : string
            a valid message should be in:
            "[move type]: [X], [Y]"

        Returns
        -------
        """
        # TODO: some condition check
        type_idx = move_msg.index(":")
        move_type = move_msg[:type_idx]
        pos_idx = move_msg.index(",")
        move_x = int(move_msg[type_idx+1:pos_idx])
        move_y = int(move_msg[pos_idx+1:])

        return move_type, move_x, move_y

    def play_move_msg(self, move_msg):
        """Another play move function for move message.

        Parameters
        ----------
        move_msg : string
            a valid message should be in:
            "[move type]: [X], [Y]"
        """
        
        move_type, move_x, move_y = self.parse_move(move_msg)
        
        self.play_move(move_type, move_x, move_y)

    def mover_minas_alrededor(self,posi,posj):
        """
        Método que nos ayuda a tener un gran número de evidencias después del primer click al despejar la zona clickada 
        intentando maximizar el número de casillas libres.
        """
        if self.board.mine_map[posj,posi] == 1:
           self.mover_mina_a_esquina(posj,posi)

        vecinos = self.neightbours_of_position(posi,posj)
        for vecino in vecinos:
            i = int(vecino[1:2])
            j = int(vecino[2:3])
            if self.board.mine_map[j,i] == 1:
                self.mover_mina_a_esquina(j,i)


    def mover_mina_a_esquina(self,posx,posi):
        """
        Método auxiliar de mover_minas_alrededor, para intentar recolocar estas minas en esquinas vacías.
        """

        if self.board.mine_map[self.board.board_width-1,self.board.board_height-1] == 0:
            self.board.mine_map[posx,posi] = 0
            self.board.mine_map[self.board.board_width-1,self.board.board_height-1] = 1
        elif self.board.mine_map[0,0] == 0:
            self.board.mine_map[posx,posi] = 0
            self.board.mine_map[0,0] = 1
        elif self.board.mine_map[self.board.board_width-1,0] == 0:
            self.board.mine_map[posx,posi] = 0
            self.board.mine_map[self.board.board_width-1,0] = 1
        elif self.board.mine_map[0,self.board.board_height-1] == 0:
            self.board.mine_map[posx,posi] = 0
            self.board.mine_map[0,self.board.board_height-1] = 1