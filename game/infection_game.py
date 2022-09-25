# from random import random as random
import random
from copy import deepcopy
from typing import Tuple, List

import matplotlib.cm as cm

from model.game import Game
from util.player_interaction import *

# Map related Const
NUM_PLAYER = 10
MAP_SIZE = (50, 50)

# Player Related Const
LIFE_KEY = "Life"
MAX_AGE = 100
AGE_SPEED_MAX = 2
Infected_key = "Infected"
Infection_rate_key = "Infection Rate"
Recover_rate_key = "Recover Rate"
EFFECTIVE_INFECTION_DIST = 5.0
default_player_state = {
    LIFE_KEY: 150,
    Infected_key: False,
    Infection_rate_key: 0.3,
    Recover_rate_key: 0.2,
}


def age_player(player: Player, max_age_speed=AGE_SPEED_MAX) -> Player:
    result = player.clone()
    age_speed = random.randint(1, max_age_speed + 1)
    result.state[LIFE_KEY] -= age_speed
    return result


def create_players(locations: [Tuple[int, int]], player_states: [{}]) -> [CellPlayer]:
    return [InfectionPlayer(location=loc, state=state) for loc, state in zip(locations, player_states)]


def interact_player_infection(p1: Player, p2: Player) -> Player:
    distance = euclid_distance(p1, p2)
    if distance > EFFECTIVE_INFECTION_DIST:
        return p1
    resulting_player = p1.clone()
    if p2.state[Infected_key]:
        infected_dice = random()
        if infected_dice > p1.state[Infection_rate_key] * (
                2 * EFFECTIVE_INFECTION_DIST + 1 - distance) / EFFECTIVE_INFECTION_DIST:
            resulting_player.state[Infected_key] = True
    return resulting_player


def initialize_player_loc_in_rectangle(w, l, number_of_player):
    loc_list = []
    for i in range(number_of_player):
        i, j = random.randint(0, w), random.randint(0, l)
        while (i, j) in loc_list:
            i, j = random.randint(0, w), random.randint(0, l)
        loc_list.append((i, j))
    return loc_list


def init_infection_game(rectangle_map=MAP_SIZE, number_of_player: int = NUM_PLAYER):
    i, j = rectangle_map
    players_locs = initialize_player_loc_in_rectangle(i, j, number_of_player)
    players = create_players(locations=players_locs, player_states=[None for _ in range(number_of_player)])
    return InfectionGame(rectangle_map=rectangle_map, players=players)


class InfectionPlayer(Player):
    def __init__(self, location, state=None, ):
        if state is None:
            state = default_player_state
        self.location = location
        self.interact_player = interact_player_infection
        self.evolve = age_player
        self.state = deepcopy(state)
        # self.


class InfectionGame(Game):
    # default_state = {
    #     Infected_key: False,
    #     Infection_rate_key: 0.5,
    #     Recover_rate_key: 0.7,
    # }

    def __init__(self, rectangle_map=MAP_SIZE, players=None):
        if players is None:
            players = []
        self.players: [CellPlayer] = players
        self.rectangle_map = rectangle_map

    def next_turn(self):
        old_players_evolved = [player.evolve(player) for player in self.players]
        result = [interact_players(player, old_players_evolved) for player in old_players_evolved]
        result = [player.evolve(player) for player in result]
        self.players = result

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
        my_plt.plot(Z, cm.get_cmap("Spectral"), interpolation='nearest')

    def next_turn_and_show(self,i, my_plt):
        self.next_turn()
        self.show(my_plt)
