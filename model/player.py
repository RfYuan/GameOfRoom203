from dataclasses import dataclass
from typing import Callable, Dict, Union


@dataclass()
class Player:
    state: Dict[str, Union[list, float]]
    location: tuple[int, int]
    interact_player: Callable[[Player], None]
    evolve: Callable[[int], None]
