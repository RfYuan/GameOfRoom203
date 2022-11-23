from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Location:
    pass


TwoDimLocation = Tuple[int, int]
MultiDimLocation = Tuple[int, ...]


# unused for now, as we dont have complicated cells
@dataclass
class GameRoom203Cell:
    # state had state(0-255,0-255,0-255)
    state: List[float] = field(default_factory=list)
    # def __init__(self, state, move_in, evolve_cell):
    #     self._state = state


# unused for now
@dataclass
class GameRoom203Map:
    cells: List[List[GameRoom203Cell]] = field(default_factory=list)

    # def plot(self, plotter: Plotter):
    #     n = len(self.cells)
    #     assert n > 0
    #     m = len(self.cells[0])
    #     for i in range(n):
    #         for j in range(m):
    #             color = visualization.get_color(self.cells[i][j])
    #             plotter.plot_by_input((i, j), color)
