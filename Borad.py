from typing import List, Dict, Tuple, Set
import os, sys

class Board:
    def __init__(self):
        self.h: int = 8
        self.w: int = 8
        self.board: List[int] = [[-1]*8 for _ in range(8)]
        self.i2c:Dict[int, str] = {-1:'□', 0:'○', 1:'●'}
        self.p1_stone = 2
        self.p2_stone = 2
        
        self._board_init()        
    
    def _board_init(self):
        """盤面の初期化
        
        最初に石を配置します
        """
        self.board[3][3] = 0
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 0
    
    def _is_out_of_range(self, h: int, w: int) -> bool:
        """範囲チェック
        
        (h, w)が盤面の外に出ていないかを判定

        Args:
            h (int): 縦方向
            w (int): 横方向

        Returns:
            bool: 範囲内におさまっているか(0:範囲内、1:範囲外)
        """
        return not (0 <= h < 8 and 0 <= w < 8)
    
    def _check_stones(self, cursor: Tuple[int, int], directions: List[Tuple[int, int]], player: int) -> Set[Tuple[int, int]]:
        """石の反転チェック

        石を配置した際に反転する石の列挙を行う

        Args:
            cursor (Tuple[int, int]): カーソルの現在地
            directions (List[Tuple[int, int]]): カーソルの位置からチェックを行う方向
            player (int): 操作中のプレイヤー

        Returns:
            Set[Tuple[int, int]]: 反転する石の集合
        """
        h, w = cursor
        reversed_stones = set()
        
        for dh, dw in directions:
            nh = h + dh
            nw = w + dw
            tmp_reversed_stones = []
            while not self._is_out_of_range(nh, nw) and -1 < self.board[nh][nw] and self.board[nh][nw] ^ player:                
                tmp_reversed_stones.append((nh, nw))   
                nh += dh
                nw += dw
            if not self._is_out_of_range(nh, nw) and not (self.board[nh][nw] ^ player):
                    reversed_stones.update(tmp_reversed_stones) 
        
        return reversed_stones      
   
    def _reversed_stones(self, cursor: Tuple[int, int], player: int) -> Set[Tuple[int, int]]:
        """石の列挙
        
        カーソルを起点として、裏返しが可能な石を列挙する

        Args:
            cursor (Tuple[int, int]): カーソルの現在位置
            player (int): 操作中のプレイヤー

        Returns:
            int: 裏返した石の集合
        """
        
        reversed_stones = set()
        # 縦の判定
        reversed_stones.update(self._check_stones(cursor, [(1, 0), (-1, 0)],player))
        # 横の判定
        reversed_stones.update(self._check_stones(cursor, [(0, 1), (0, -1)], player))
        # 斜めの判定
        reversed_stones.update(self._check_stones(cursor, [(1, 1), (1, -1), (-1, 1), (-1,-1)], player))

        return reversed_stones

    def _calc_stones(self, stone_cnt: int, player: int):
        """石の数
        
        石の数を計算しておく

        Args:
            stone_cnt (int): 変化があった石の数
            player (int): 操作しているプレイヤー
        """
        if player:
            self.p1_stone += stone_cnt + 1
            self.p2_stone -= stone_cnt
        else:
            self.p1_stone -= stone_cnt 
            self.p2_stone += stone_cnt + 1
            
    def check_put_stone(self, player: int) -> bool:
        """配置チェック

        現在のプレイヤーが石を配置可能であるかを調べます

        Args:
            player (int): 現在のプレイヤー

        Returns:
            bool: 配置が可能か(True: 可能, Flase: 不可能)
        """

        for h in range(8):
            for w in range(8):
                if self.board[h][w] == -1:
                    if 0 < len(self._reversed_stones((h, w), player)):
                        return True
        return False
    
    def put_stone(self, cursor: Tuple[int, int], player: int) -> bool:
        """石を配置する

        カーソルの現在地に、今のプレイヤーの石を置きます

        Args:
            cursor (Tuple[int, int]): カーソルの現在地
            player (int): 操作中のプレイヤー
        
        Returns:
            bool: 石の設置ができたかどうか
        """
        h, w = cursor
        
        if self.board[h][w] == -1:
            reversed_stone = self._reversed_stones(cursor, player)
            if 0 < len(reversed_stone):
                for th, tw in reversed_stone:
                    self.board[th][tw] = player
                self._calc_stones(len(reversed_stone), player)
                self.board[h][w] = 1 if player else 0
                return True
        return False
        
    def print_board(self, cursor: Tuple[int, int], cursor_switch: bool, player: int) -> int:
        """盤面の出力
        
        ターミナルをクリアしたのちに、盤面を出力します

        Args:
            cursor (Tuple[int, int]): カーソルの現在地
            cursor_switch (bool): カーソルを点滅させる
            player (int): 操作中のプレイヤー
            
        Returns:
            int : 現在置かれている石の総数
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        cursor_h, cursor_w = cursor
        for i in range(8):
                row = [self.i2c[c] for c in self.board[i]]
                if cursor_switch and i == cursor_h:
                    row[cursor_w] = ' '
                print(*row)
        sys.stdout.flush()
        print(f'現在はP{player + 1}のターンです。')
        print(f'現在の石の数 : P1:{self.p1_stone:03} P2:{self.p2_stone:03}') 
        
        return self.p1_stone + self.p2_stone

    def print_result(self):
        """結果出力
        
        リザルトを出力します
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(8):
                row = [self.i2c[c] for c in self.board[i]]
                print(*row)
        sys.stdout.flush()
        print(f'石の数 : P1:{self.p1_stone:03} P2:{self.p2_stone:03}') 
        result_flg = self.p2_stone < self.p1_stone
        print(f'石の数が{self.p1_stone if result_flg else self.p2_stone}でP{1 if result_flg else 2}の勝利です')