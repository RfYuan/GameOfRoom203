import math
import random
from typing import Tuple

from model.player import CellPlayer, Player

AGE_SPEED_MAX = 3


def euclid_distance(p1: Player, p2: Player) -> float:
    # total_dist = math.sqrt(math.fsum([(p_i - q_i) ** 2 for p_i, q_i in zip(p1.location, p2.location)]))
    return math.sqrt(math.fsum([(p_i - q_i) ** 2 for p_i, q_i in zip(p1.location, p2.location)]))


def interact_cell_players(p1: CellPlayer, players: [CellPlayer]) -> CellPlayer:
    # p1 could be in players list, need to skip the effect
    result_player = p1.clone()
    for other_player in players:
        if p1 != other_player:
            result_player = result_player.interact_player(result_player, other_player)
    return result_player


def initialize_locations_in_rectangle(w, l, number_of_player):
    loc_list = []
    for i in range(number_of_player):
        i, j = random.randint(0, w - 1), random.randint(0, l - 1)
        while (i, j) in loc_list:
            i, j = random.randint(0, w - 1), random.randint(0, l - 1)
        loc_list.append((i, j))
    return loc_list


def generate_new_location_around_current(current: Tuple[int, ...], possibility_birth: float = 0.005) -> Tuple[int, ...]:
    p_not_birth = 1 - possibility_birth
    dim = len(current)
    p_not_birth_each_direction = (p_not_birth ** (1. / dim))
    p_birth_in_each_direction = (1 - p_not_birth_each_direction) / 2
    new_pos = list(current)
    for i in range(dim):
        dim_dice = random.random()
        if dim_dice < p_birth_in_each_direction:
            new_pos[i] -= 1
        elif dim_dice > 1 - p_birth_in_each_direction:
            new_pos[i] += 1
    new_pos = tuple(new_pos)
    return new_pos


