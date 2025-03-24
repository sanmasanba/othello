import sys
import time
from typing import Tuple
import copy

from Board import Board
import CPU

class Othello:
    def __init__(self, display: bool=True, result: bool=True):
        self.init(display, result)
    
    def init(self, display: bool=True, result: bool=True):
        self.ROW_LIST = ['0', '1', '2', '3', '4', '5', '6', '7']
        self.COL_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.board = Board()
        self.cpu = CPU.RandomCPU()
        self.minimax = CPU.MiniMaxCPU()
        self.is_display = display
        self.is_result = result       

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
            return False

    def print_board(self, player: int) -> None:
        if self.is_display:
            self.board.print_board(player)
            time.sleep(0.2)
    
    def print_result(self) -> int:
        return self.board.print_result(self.is_result)

    def cpu_vs_cpu(self) -> None:
        player = 0
        skip = 0
        # main loop
        while 1:                
            self.print_board(player)
            # check
            can_push_pos = []
            for r in range(8):
                for c in range(8):
                    if self.board.board[r][c] == -1 and 0 < len(self.board._reversed_stones((r, c), player)):
                        can_push_pos.append((r, c))
            if not can_push_pos:
                skip += 1
                if 2 <= skip:
                    return self.print_result()
                player = self.change_player(player)
                continue

            # action
            if player == 0:    
                r, c = self.cpu.random_choice(can_push_pos)
            else:
                _, r, c = self.minimax.dfs(self.board, player, player, 0)
            
            # put stone
            if not self.board.put_stone((r, c), player):
                continue
            skip = 0

            # change player
            player = self.change_player(player)
            # if current player can't put a stone
            if not self.board.check_put_stone(player):
                # change player again
                skip += 1
                if 2 <= skip:
                    return self.print_result()
                player = self.change_player(player)
            
            # display
            sum_stones = self.board.sum_stone()

            # already put 64 stones
            if sum_stones == 64:
                return self.print_result()

    def iter_play(self, iter: int = 10):
        p1_win, p2_win, draw = 0, 0, 0
        print(" i,   p1, draw,   p2")
        sum_time = 0
        for i in range(iter):
            self.init(display=False, result=False)
            s_time = time.time()
            result = self.cpu_vs_cpu()
            episode = time.time() -s_time
            sum_time += episode
            if result == 0:
                p1_win += 1
            elif result == 1:
                p2_win += 1
            else:
                draw += 1

            print(f"{i+1:02}, {p1_win:04}, {draw:04}, {p2_win:04}, {episode:2.2f}")
        
        # stats
        print('# results')
        print(f'sum iter: {i+1:02}')
        print(f'p1_win  :{p1_win:04}')
        print(f'draw    :{draw:04}')
        print(f'p2_win  :{p2_win:04}')
        print(f'ave time:{sum_time/iter:2.2f}')
        return [p1_win, draw, p2_win]
    
def main() -> None:
    game = Othello(display=False, result=False)
    (p1_win, draw, p2_win) = game.iter_play(1000)
    # game = Othello()
    # game.cpu_vs_cpu()

if __name__ == '__main__':
    main()