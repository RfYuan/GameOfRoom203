from typing import List, Tuple

from model.map import MultiDimLocation
from model.player import Player


class Game:
    def next_turn(self, ):
        pass

    def show(self, my_plt):
        pass

    def get_current_turn_info(self) -> str:
        return "Current turn info"

    def next_turn_and_show(self, i, my_plt):
        self.next_turn()
        print(i, "turn")
        print(self.get_current_turn_info())
        self.show(my_plt)


class Game2D:
    def __init__(self, rectangle_map: MultiDimLocation, players: List[Player] = None):
        if players is None:
            players = []
        self.players: List[Player] = players
        self.rectangle_map = rectangle_map
