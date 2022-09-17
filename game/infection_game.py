from copy import deepcopy
from typing import Tuple, List

from model.game import Game
from model.player import Player, CellPlayer
import random
from random import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from util.player_interaction import *

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


def create_player(loc: Tuple[int, int]) -> CellPlayer:
    pass


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


class InfectionPlayer(Player):
    def __init__(self, location, state=None, ):
        if state is None:
            state = default_player_state
        self.interact_player = interact_player_infection
        self.evolve = age_player
        self.state = deepcopy(state)
        # self.


class BasicInfectionGame(Game):
    default_state = {
        Infected_key: False,
        Infection_rate_key: 0.5,
        Recover_rate_key: 0.7,
    }

    def __init__(self, rectangle_map=(100, 100), players=None):
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
        result = [[0.0 for i in range(length)] for j in range(width)]
        for player in self.players:
            player_state = player.state
            i, j = player.location

            if player_state.get(Infected_key):
                result[i][j] = 1
            else:
                result[i][j] = 0.5
        return result

    def show(self):
        Z = self.get_graph_origin()
        plt.imshow(Z, cm.get_cmap("Spectral"), interpolation='nearest')
        return plt
