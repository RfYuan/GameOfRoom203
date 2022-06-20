from dataclasses import dataclass, field


@dataclass
class GameRoom203Cell:
    state: list[float] = field(default_factory=list)
    # def __init__(self, state, move_in, evolve_cell):
    #     self._state = state


@dataclass
class GameRoom203Map:
    cells: list[list[GameRoom203Cell]] = field(default_factory=list)
