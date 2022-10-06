# from random import random as random
import random
from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple, List

import matplotlib.cm as cm

from model.game import Game
from util.player_interaction import *

# Map related Const
NUM_PLAYER = 50
MAP_SIZE = (50, 50)

# Player Related Const
LIFE_KEY = "Life"
MAX_AGE = 100
AGE_SPEED_MAX = 3
Infected_key = "Infected"
Infection_rate_key = "Infection Rate"
Recover_rate_key = "Recover Rate"
Birth_rate_key = "Birth Rate"
EFFECTIVE_INFECTION_DIST = 10.0
INITIAL_INFECTION_RATE = 0.5
default_player_state = {
    LIFE_KEY: 50,
    Infected_key: False,
    Infection_rate_key: 0.7,
    Recover_rate_key: 0.2,
    Birth_rate_key: 0.05,
}


def age_player(player: Player, max_age_speed=AGE_SPEED_MAX) -> Player:
    result = player.clone()
    age_speed = random.randint(1, max_age_speed + 1)
    result.state[LIFE_KEY] -= age_speed
    return result


def initialize_locations_in_rectangle(w, l, number_of_player):
    loc_list = []
    for i in range(number_of_player):
        i, j = random.randint(0, w - 1), random.randint(0, l - 1)
        while (i, j) in loc_list:
            i, j = random.randint(0, w - 1), random.randint(0, l - 1)
        loc_list.append((i, j))
    return loc_list


def test_player_location_out_of_cube_bounds(cube_size: Tuple[int, ...], loc: Tuple[int, ...]) -> bool:
    return all(0 <= i < b for i, b in zip(loc, cube_size))


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


# Immutable
@dataclass()
class InfectionPlayer(CellPlayer):

    def __init__(self, state, location, interact_player, evolve):
        if state is None:
            state = default_player_state
        self.state = state
        self.location = location
        self.interact_player = interact_player
        self.evolve = evolve

    def infected(self):
        new = self.clone()
        new.state[Infected_key] = 1
        return new

    def cure(self):
        new = self.clone()
        new.state[Infected_key] = 0
        return new

    def clone(self):
        state = deepcopy(self.state)
        return InfectionPlayer(state, self.location, self.interact_player, self.evolve)


def init_infected_player(players: [InfectionPlayer], inital_infection_rate: float = INITIAL_INFECTION_RATE):
    return [p.infected() if (random.random() > inital_infection_rate) else p for p in players]


def interact_infection_player(p1: InfectionPlayer, p2: InfectionPlayer) -> InfectionPlayer:
    distance = euclid_distance(p1, p2)
    if distance > EFFECTIVE_INFECTION_DIST:
        return p1
    resulting_player = p1.clone()
    if p2.state[Infected_key]:
        infected_dice = random.random()
        if infected_dice > p1.state[Infection_rate_key] * (
                2 * EFFECTIVE_INFECTION_DIST + 1 - distance) / EFFECTIVE_INFECTION_DIST:
            resulting_player.state[Infected_key] = True
    return resulting_player


def cure_player_by_chance(player: InfectionPlayer) -> InfectionPlayer:
    infected_dice = random.random()
    if infected_dice < player.state[Recover_rate_key]:
        return player.cure()
    else:
        return player


def create_infection_player(locations: [Tuple[int, int]], player_states: [{}]) -> [InfectionPlayer]:
    return [InfectionPlayer(state=state,
                            location=loc,
                            evolve=lambda x: age_player(cure_player_by_chance(x)),
                            interact_player=interact_infection_player)
            for loc, state in zip(locations, player_states)]


def generate_new_players(players: [InfectionPlayer], map_size: Tuple[int, ...]) -> [InfectionPlayer]:
    player_locs = [i.location for i in players]
    new_locs = [generate_new_location_around_current(player.location, player.state[Birth_rate_key]) for player in
                players]
    new_locs_filter_out_of_bounds = filter(lambda loc: test_player_location_out_of_cube_bounds(
        map_size, loc), new_locs)
    new_locs_not_overlap = list(filter(lambda x: x not in player_locs, new_locs_filter_out_of_bounds))

    new_players = create_infection_player(new_locs_not_overlap, [None for _ in range(len(new_locs_not_overlap))])
    return players + new_players


class InfectionGame(Game):
    def __init__(self, rectangle_map=MAP_SIZE, players: [InfectionPlayer] = None):
        if players is None:
            players = []
        self.players: [InfectionPlayer] = players
        self.rectangle_map = rectangle_map

    def next_turn(self):
        old_players_evolved = [player.evolve(player) for player in self.players]
        player_interacted = [interact_players(player, old_players_evolved) for player in old_players_evolved]
        player_alive = list(filter(lambda x: x.state[LIFE_KEY] > 0, player_interacted))
        new_players = generate_new_players(player_alive, self.rectangle_map)
        self.players = new_players

    def get_graph_origin(self) -> List[List[float]]:
        length, width = self.rectangle_map
        result = [[0.0 for _ in range(length)] for _ in range(width)]
        for player in self.players:
            player_state = player.state
            i, j = player.location

            if player_state.get(Infected_key):
                result[i][j] = 1
            else:
                result[i][j] = 0.5
        return result

    def show(self, my_plt):
        Z = self.get_graph_origin()
        my_plt.imshow(Z, cm.get_cmap("Spectral"), interpolation='nearest')

    def next_turn_and_show(self, i, my_plt):
        self.next_turn()
        print(i, "turn")
        self.show(my_plt)


def init_infection_game(rectangle_map=MAP_SIZE, number_of_player: int = NUM_PLAYER):
    i, j = rectangle_map
    players_locs = initialize_locations_in_rectangle(i, j, number_of_player)
    players = create_infection_player(locations=players_locs, player_states=[None for _ in range(number_of_player)])
    players = init_infected_player(players)
    return InfectionGame(rectangle_map=rectangle_map, players=players)
