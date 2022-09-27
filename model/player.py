from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Union, Tuple


# TODO: make player immutable
@dataclass()
class Player:
    state: Dict[str, Union[list, str, bool]]
    location: Tuple[int, int]
    interact_player: Callable[[Player, Player], Player]
    evolve: Callable[[Player], Player]

    def clone(self):
        pass


class CellPlayer(Player):
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.location == other.location
        return False
