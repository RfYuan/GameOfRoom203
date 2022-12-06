import random
from typing import Callable, Optional

from model.map import TwoDimLocation
from model.player import Player, CellPlayer, CellPlayer2D
from util.game_state_keys import Birth_rate_key, LIFE_KEY
from util.location_related import generate_uniform_location_around, test_player_location_out_of_cube_bounds
from util.player_interaction_related import AGE_SPEED_MAX


def generate_children_in_2d(player_loc: TwoDimLocation, map_size: TwoDimLocation,
                            create_player: Callable[[TwoDimLocation], Player], k=1, ) -> Optional[Player]:
    new_loc = generate_uniform_location_around(player_loc, k)
    in_bound = test_player_location_out_of_cube_bounds(loc=new_loc, cube_size=map_size)
    if in_bound:
        return create_player(new_loc)
    return None


def get_new_id(player_name: str) -> str:
    return player_name + "NewPlayer"


def age_player(player: Player, max_age_speed=AGE_SPEED_MAX) -> Player:
    result = player.clone()
    age_speed = random.randint(1, max_age_speed + 1)
    result.state[LIFE_KEY] -= age_speed
    return result


def decrease_by_union_distribution(input_num: int, max_increase: int = AGE_SPEED_MAX) -> int:
    return input_num - random.randint(1, max_increase + 1)


def give_born_new_2d_player(player: CellPlayer2D, rectangle_map: TwoDimLocation) -> Optional[CellPlayer2D]:
    if random.random() > player.state[Birth_rate_key]:
        return None
    new_children = generate_children_in_2d(player.location, rectangle_map,
                                           lambda loc: clone_player_at_new_loc(player, loc), )
    return new_children


def clone_player_at_new_loc(player: CellPlayer, loc: TwoDimLocation) -> CellPlayer:
    if loc == player.location:
        raise ValueError("Location of the children is the same as parent")

    children = player.clone()
    children.id = get_new_id(player.id)
    children.location = loc
    return children


def update_age_of_player(player: Player, age: int):
    player.state[LIFE_KEY] = age
