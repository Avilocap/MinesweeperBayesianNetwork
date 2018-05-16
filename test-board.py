"""Test script for the game board.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
from msgame import MSGame

game = MSGame(5, 5, 5)

game.print_board()
print(game.get_info_map())
print(game.get_mine_map())

try:
    input = raw_input
except NameError:
    pass

while game.game_status == 2:
    # play move

    move = input("Move: ")
    game.play_move_msg(move)
    game.print_board()
    print(game.get_info_map())
    print(game.get_mine_map())