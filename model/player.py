from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Union

# TODO: make player immutable
from model.map import MultiDimLocation, TwoDimLocation


@dataclass()
class Player:
    state: Dict[str, Union[list, str, bool, float, int]]
    location: MultiDimLocation
    interact_player: Callable[[Player, Player], Player]
    evolve: Callable[[Player], Player]
    id: str

    def clone(self):
        pass


class CellPlayer(Player):
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.location == other.location
        return False


class CellPlayer2D(CellPlayer):
    location: TwoDimLocation
