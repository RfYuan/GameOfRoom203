from dataclasses import dataclass, field
from typing import List

from model.plotter import Plotter
from util import visualization


@dataclass
class GameRoom203Cell:
    # state had state(0-255,0-255,0-255)
    state: List[float] = field(default_factory=list)
    # def __init__(self, state, move_in, evolve_cell):
    #     self._state = state


@dataclass
class GameRoom203Map:
    cells: List[List[GameRoom203Cell]] = field(default_factory=list)

    def plot(self, plotter: Plotter):
        n = len(self.cells)
        assert n > 0
        m = len(self.cells[0])
        for i in range(n):
            for j in range(m):
                color = visualization.get_color(self.cells[i][j])
                plotter.plot_by_input((i, j), color)
