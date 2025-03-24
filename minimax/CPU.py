import copy
import random
from typing import Tuple, List, Any

from Board import Board

class RandomCPU:

    def __init__(self):
        pass

    def random_choice(self, can_push_pos: List[Tuple[int, int]]) -> Tuple[int, int]:
        pushed_pos = random.choice(can_push_pos)
        return pushed_pos 


class MiniMaxCPU:

    def __init__(self):
        pass

    def evaluate(self, board: Board, player: int, crr_player: int) -> float:
        p1_score = board.p1_stone
        p2_score = board.p2_stone
        total_stones = p1_score + p2_score

        if total_stones < 20:
            weight = 1.2
        elif total_stones < 50:
            weight = 1.5
        else:
            weight = 2.0

        # 一致するなら1、一致しないなら-1
        if player == crr_player:
            a = 1
        else:
            a = -1
        return a * (p1_score * weight - p2_score)**3


    def dfs(self, board: Board, player: int, crr_player: int, depth: int = 0) -> Tuple[bool, Tuple[int, int]]:
        # 末端
        if 3 <= depth or board.sum_stone == 64:
            score = self.evaluate(board, player, crr_player)
            return  (score, -1, -1)

        # 候補点のサーチ
        candidate_pos = []
        for r in range(8):
            for c in range(8):
                if board.board[r][c] == -1 and board._reversed_stones((r, c), crr_player):
                    candidate_pos.append((r, c))

        # 置く場所がないとき、あるいは少し先まで読んだとき
        # 現在の石の数をそのまま返す
        if not candidate_pos:
            crr_player = (crr_player + 1) % 2
            return (self.dfs(board, player, (crr_player+1)%2, depth+1))
    
        score_rc = []
        for r, c in candidate_pos:
            board.snapshot()
            board.put_stone((r, c), crr_player)
            score, _, _ = self.dfs(board, player, (crr_player+1)%2, depth+1)
            board.undo()
            score_rc.append((score, r, c))

        return max(score_rc)
    
class AlphaBetaCPU:

    def __init__(self):
        pass

    def evaluate(self, board: Board, player: int, crr_player: int) -> float:
        p1_score = board.p1_stone
        p2_score = board.p2_stone
        total_stones = p1_score + p2_score

        if total_stones < 20:
            weight = 1.2
        elif total_stones < 50:
            weight = 1.5
        else:
            weight = 2.0

        # 一致するなら1、一致しないなら-1
        if player == crr_player:
            a = 1
        else:
            a = -1
        return a * (p1_score * weight - p2_score)**3


    def dfs(self, board: Board, player: int, crr_player: int, depth: int = 0) -> Tuple[bool, Tuple[int, int]]:
        # 末端
        if 3 <= depth or board.sum_stone == 64:
            score = self.evaluate(board, player, crr_player)
            return  (score, -1, -1)

        # 候補点の列挙
        candidate_pos = []
        for r in range(8):
            for c in range(8):
                if board.board[r][c] == -1 and board._reversed_stones((r, c), crr_player):
                    candidate_pos.append((r, c))

        # 設置不可の場合パス
        if not candidate_pos:
            crr_player = (crr_player + 1) % 2
            return (self.dfs(board, player, (crr_player+1)%2, depth+1))
    
        # 深さ優先探索
        score_rc = []
        for r, c in candidate_pos:
            board.snapshot()
            board.put_stone((r, c), crr_player)
            score, _, _ = self.dfs(board, player, (crr_player+1)%2, depth+1)
            board.undo()
            score_rc.append((score, r, c))

        return max(score_rc)

