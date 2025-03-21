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