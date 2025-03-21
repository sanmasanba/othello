import sys
import time
from typing import Tuple
import copy

from Board import Board
import CPU

class Othello:
    def __init__(self):
        self.ROW_LIST = ['0', '1', '2', '3', '4', '5', '6', '7']
        self.COL_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.board = Board()
        self.cpu = CPU.Random_CPU()
        self.minmax = CPU.MinMax_CPU()

    def change_player(self, crr_player: int) -> int:
        """手番の変更
        
        手番を変更します

        Args:
            crr_player (int): 現在のプレイヤー

        Returns:
            int: 変更後のプレイヤー
        """
        return (crr_player + 1) % 2

    def input_stone(self) -> Tuple[bool, str, str]:
        """_summary_

        Returns:
            Tuple[bool, str, str]: _description_
        """
        input_ = input()
        if len(input_) != 2:
            return False, 'x', 'x'
        input_ = input_.upper()
        return True, input_[0], input_[1]

    def check_input(self, r: str, c: str) -> bool:
        """
        Args:
            input_ (str): _description_

        Returns:
            bool: _description_
        """
        if r in self.ROW_LIST and c in self.COL_LIST:
            return True
        else:
            False

    def cpu_vs_cpu(self) -> None:
        player = 0

        # main loop
        while 1:    
            self.board.print_board(player)
            can_push_pos = []
            if player == 0:
                for r in range(8):
                    for c in range(8):
                        if self.board.board[r][c] == -1 and 0 < len(self.board._reversed_stones((r, c), player)):
                            can_push_pos.append((r, c))
                if not can_push_pos:
                    player = self.change_player(player)
                    continue
                r, c = self.cpu.random_choise(can_push_pos)
            else:
                for r in range(8):
                    for c in range(8):
                        if self.board.board[r][c] == -1 and 0 < len(self.board._reversed_stones((r, c), player)):
                            can_push_pos.append((r, c))
                if not can_push_pos:
                    player = self.change_player(player)
                    continue
                _, r, c = self.minmax.dfs(copy.deepcopy(self.board), player, 0)
            
            # put stone
            self.board.put_stone((r, c), player)
            # change player
            player = self.change_player(player)
            # if current player can't put a stone
            if not self.board.check_put_stone(player):
                # change player again
                player = self.change_player(player)
            
            # display
            sum_stones = self.board.print_board(player)

            # already put 64 stones
            if sum_stones == 64:
                self.board.print_result()
                return

    def play(self) -> None:
        player = 0

        # main loop
        while 1:    
            self.board.print_board(player)
            can_push_pos = []
            if player == 1:
                for r in range(8):
                    for c in range(8):
                        if self.board.board[r][c] == -1 and 0 < len(self.board._reversed_stones((r, c), player)):
                            can_push_pos.append((r, c))
                if not can_push_pos:
                    player = self.change_player(player)
                    continue
                r, c = self.cpu.random_choise(can_push_pos)
                self.board.put_stone((r, c), player)
                # change player
                player = self.change_player(player)
                # if current player can't put a stone
                if not self.board.check_put_stone(player):
                    # change player again
                    player = self.change_player(player)
            else:
                # input
                flg, r, c = self.input_stone()

                # checked input
                if not (flg and self.check_input(r, c)):
                    continue

                # put stone
                cursor = (int(r), self.COL_LIST.index(c))
                if self.board.put_stone(cursor, player):
                    # change player
                    player = self.change_player(player)
                    # if current player can't put a stone
                    if not self.board.check_put_stone(player):
                        # change player again
                        player = self.change_player(player)
                else:
                    continue
            
            # display
            sum_stones = self.board.print_board(player)

            # already put 64 stones
            if sum_stones == 64:
                self.board.print_result()
                return


def main() -> None:
    game = Othello()
    # play with random
    # game.play()
    game.cpu_vs_cpu()
    return

if __name__ == '__main__':
    main()