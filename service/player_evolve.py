from typing import Callable, Optional

from model.map import TwoDimLocation
from model.player import Player
from util.location_related import generate_uniform_location_around, test_player_location_out_of_cube_bounds


def generate_children_in_2d(player_loc: TwoDimLocation, map_size: TwoDimLocation,
                            create_player: Callable[[TwoDimLocation], Player], k=1, ) -> Optional[Player]:
    new_loc = generate_uniform_location_around(player_loc, k)
    out_of_bound = test_player_location_out_of_cube_bounds(new_loc, map_size)
    if not out_of_bound:
        return create_player(new_loc)
    return None


def get_new_id(player_name: str) -> str:
    return player_name + "NewPlayer"
