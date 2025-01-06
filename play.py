import keyboard
import sys
import time
from typing import Tuple

from Borad import Board

FPS = 60
board = Board()

def cursor_move(cursor: Tuple[int, int], key=str) -> Tuple[int, int]:
    """カーソルの移動
    
    入力されたキーに合わせて、カーソルの位置を変更します

    Args:
        cursor (Tuple[int, int]): 現在のカーソル位置
        key (str): 現在の入力キー

    Returns:
        Tuple[int, int]: 移動後のカーソル位置
    """
    dh, dw = {"LEFT": [0, -1], "RIGHT": [0, 1], "UP": [-1, 0], "DOWN": [1, 0]}[key]
    currnet_cursor_h, currnet_cursor_w = cursor
    return ((currnet_cursor_h+dh)%8, (currnet_cursor_w+dw)%8)

def read_key() -> str:
        """キーの読み込み
        
        キーの入力に合わせて、文字列を返します

        Returns:
            str: 入力キーを表す文字列
        """
        if keyboard.is_pressed("d"):
            key = "RIGHT"
        elif keyboard.is_pressed("a"):
            key = "LEFT"
        elif keyboard.is_pressed("w"):
            key = "UP"
        elif keyboard.is_pressed("s"):
            key = "DOWN"
        elif keyboard.is_pressed("e"):
            key = "ENTER"
        else:
            key = None
        
        return key

def change_player(crr_player: int) -> int:
    """手番の変更
    
    手番を変更します

    Args:
        crr_player (int): 現在のプレイヤー

    Returns:
        int: 変更後のプレイヤー
    """
    return (crr_player + 1) % 2

def main():
    cursor: Tuple[int, int] = (3, 3)
    frame = 0
    pre_key = None
    player = 0
    while 1:    
        # pre_process
        cursor_switch = frame < 12
        
        # cursor
        key = read_key()
        
        # put stone
        if pre_key != key and key == "ENTER":
            if board.put_stone(cursor, player):
                # change player
                player = change_player(player)
                # if current player can't put a stone
                if not board.check_put_stone(player):
                    # change player again
                    player = change_player(player)
            
        # move a cusor
        if pre_key != key and key in ("RIGHT", "LEFT", "UP", "DOWN"):
            cursor = cursor_move(cursor, key)
        
        # display
        sum_stones = board.print_board(cursor, cursor_switch, player)
        # already put 64 stones
        if sum_stones == 64:
            board.print_result()
            time.sleep(5)
            sys.exit(0)
        
        # update 
        frame += 1
        frame %= 24
        pre_key = key
        time.sleep(1/24)
    
if __name__ == '__main__':
    main()