"""Test script for the game board.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
from msgame import MSGame

game = MSGame(6, 6, 5)

# game.print_board()
# print(game.get_info_map())
# print(game.get_mine_map())
# print(game.get_nodes())
# print(game.name_nodes())
print ("esquinas --------")
print(game.neightbours_of_position(5,5))
print(game.neightbours_of_position(0,5))
print(game.neightbours_of_position(0,0))
print(game.neightbours_of_position(5,0))
print("centrales random -----------")
print(game.neightbours_of_position(2,2))
print(game.neightbours_of_position(3,3))
print(game.neightbours_of_position(1,3))
print("laterales -------------------")

print(game.neightbours_of_position(0,1))
print(game.neightbours_of_position(3,5))
print(game.neightbours_of_position(3,0))
print(game.neightbours_of_position(5,4))
# print(game.es_esquina(2,3))
# print(game.es_lateral(0,3))


# try:
#     input = raw_input
# except NameError:
#     pass

# while game.game_status == 2:
#     # play move

#     move = input("Move: ")
#     game.play_move_msg(move)
#     game.print_board()
#     print(game.get_info_map())
#     print(game.get_mine_map())
#     print(game.get_nodes())