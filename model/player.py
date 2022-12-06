from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Callable, Dict, Union, NamedTuple, Any

# TODO: make player immutable
from model.map import MultiDimLocation, TwoDimLocation

DataClassType = Any
PlayerState = Union[DataClassType, NamedTuple, Dict[str, Union[list, str, bool, float, int]]]


@dataclass(frozen=False)
class Player:
    location: MultiDimLocation
    state: PlayerState = field(repr=False, default=None, compare=True)
    interact_player: Callable[[Player, Player], Player] = field(repr=False, default=None)
    evolve: Callable[[Player], Player] = field(repr=False, default=None)
    id: str = field(default="")

    def clone(self):
        pass


# class such that each player in same cell are identical (we wanted to allow at most one player per cell)
class CellPlayer(Player):
    # location: MultiDimLocation = field(compare=True)

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.location == other.location
        return False


class CellPlayer2D1(CellPlayer):
    location: TwoDimLocation


class CellPlayer2D(Player):
    location: TwoDimLocation = field(compare=True)


a_player = CellPlayer(location=(0, 1), state={"A": 0})
b_player = CellPlayer2D1(location=(0, 1), state={"A": 1})
c_player = CellPlayer2D(location=(0, 1), state={"A": 2})
d_player = Player(location=(0, 1), state={"A": 2})
d_player1 = Player(location=(0, 1), state={"A": 0})

# print("dataclass with inherited eq")
# print(b_player == a_player)
# print(b_player == c_player)
# print(b_player == d_player)
# print()
#
# print("dataclass with override field eq")
# print(c_player == a_player)
# print(c_player == b_player)
# print(c_player == d_player)
# print()

print("original dataclass")
print(d_player == a_player)
print(d_player == b_player)
print(d_player == c_player)
print(d_player == d_player1)
print()

print(inspect.getsource(a_player.__eq__))
print(inspect.getsource(b_player.__eq__))
print(inspect.getsource(PlayerState.__eq__))
# print(d_player.state == a_player.state)
# print( inspect.getsource(d_player.__eq__) )
# print(str(d_player.__eq__.func_code))
