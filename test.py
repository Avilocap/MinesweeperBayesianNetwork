from __future__ import print_function
import minesweeperGen as board

borad = board.MinesweeperBoard(10,10,5)
borad.print_board()
print(borad.info_map)
print(borad.mine_map)