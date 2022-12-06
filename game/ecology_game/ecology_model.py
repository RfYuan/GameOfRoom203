from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from model.player import CellPlayer2D
from util.game_state_keys import LIFE_KEY, Energy_Key

TripleEcoState = namedtuple('TripleEcoState', [LIFE_KEY, Energy_Key])


class TripleEco(Enum):
    Grass = auto()
    Lamb = auto()
    Tiger = auto()


# states are immutable
@dataclass(frozen=True, )
class TripleEcoPlayerState:
    life: int
    energy: int


# players are mutable
@dataclass()
class TripleEcoPlayer(CellPlayer2D):
    type: TripleEco = field(default=TripleEco.Grass, compare=True)
    state: TripleEcoPlayerState = field(repr=False, default=None, compare=True)
    neighbour: List["TripleEcoPlayer"] = field(repr=False, default_factory=list, compare=False)

    def __init__(self, player_state: TripleEcoPlayerState, location):
        self.state = player_state
        self.location = location


def get_plyaer_type(p: TripleEcoPlayer) -> TripleEco:
    return p.type
