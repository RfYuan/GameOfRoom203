import random
from typing import Tuple

from model.map import TwoDimLocation


def generate_uniform_location_around(my_loc: TwoDimLocation, k=1) -> TwoDimLocation:
    if k <= 0:
        raise ValueError("can not generate location with distance {}".format(k))
    i, j = my_loc
    possibility = 1.0 / ((2 * k + 1) ** 2 - 1)
    new_locs = [(p, q) for p in range(i - k, i + k + 1) for q in range(j - k, j + k + 1)]
    new_locs_prob = [possibility if ele != (i, j) else 0 for ele in new_locs]
    return random.choices(new_locs, new_locs_prob)[0]


def test_player_location_out_of_cube_bounds(cube_size: Tuple[int, ...], loc: Tuple[int, ...]) -> bool:
    return all(0 <= i < b for i, b in zip(loc, cube_size))
