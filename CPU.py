import copy
import random
from typing import Tuple, List, Any

from Board import Board

class Random_CPU:

    def __init__(self):
        self.rnd = random.randint(0, 7)

    def random_choise(self, can_push_pos: List[Tuple[int, int]]) -> Tuple[int, int]:
        pushed_pos = random.choice(can_push_pos)
        return pushed_pos 

class Node:
    def __init__(self, board):
        self.crr_board: Board = board


class MinMax_CPU:

    def __init__(self):
        pass

    def dfs(self, board: Board, player: int, crr_player: int, depth: int = 0) -> Tuple[bool, Tuple[int, int]]:
        
        # 候補点のサーチ
        candidate_pos = []
        for r in range(8):
            for c in range(8):
                if board.board[r][c] == -1 and board._reversed_stones((r, c), player):
                    candidate_pos.append((r, c))

        # 置く場所がないとき、あるいは少し先まで読んだとき
        # 現在の石の数をそのまま返す
        if candidate_pos:
            score_rc = []
            for r, c in candidate_pos:
                if depth < 3:
                    score, _r, _c = self.dfs(copy.deepcopy(board), player, (player+1)%2, depth+1)
                nxt_board = copy.deepcopy(board)
                nxt_board.put_stone((r, c), crr_player)
                if player == 0:
                    score = nxt_board.p1_stone
                elif player == 1:
                    score = nxt_board.p2_stone
                score_rc.append((score, r, c))
            score_rc.sort()
        else: 
            score_rc = [(board.p1_stone if player == 0 else board.p2_stone, -1, -1)]

        if player == crr_player:
            score, r, c = score_rc[-1]
            return (score, r, c)
        else:
            score, r, c = score_rc[0]
            return (score, r, c)
