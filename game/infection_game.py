# from random import random as random
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Dict, Optional, Iterable

import matplotlib.cm as cm

from model.game import Game
from model.map import TwoDimLocation
from model.player import CellPlayer2D
from service.player_evolve import generate_children_in_2d, get_new_id
from util.player_interaction_related import *
# Map related Const
from util.player_interaction_related import age_player, initialize_locations_in_rectangle, \
    LIFE_KEY

NUM_INITIAL_PLAYER = 8
MAP_SIZE = (50, 50)

# Player Related Const
INITIAL_LIFE_SPAN = 50
Infected_key = "Infected"
Infection_rate_key = "Infection Rate"
Recover_rate_key = "Recover Rate"
Birth_rate_key = "Birth Rate"
EFFECTIVE_INFECTION_DIST = 5.0
INITIAL_INFECTION_RATE = 0.5
Next_Children_Name_Key = 'Next Children Name'
default_player_state = {
    Next_Children_Name_Key: 'A',
    LIFE_KEY: INITIAL_LIFE_SPAN,
    Infected_key: False,
    Infection_rate_key: 0.3,
    Recover_rate_key: 0.1,
    Birth_rate_key: 0.05,
}


# TODO: we would like to have a immutable state, because there are likely to have lots of players
#  in the same state
@dataclass()
class InfectionPlayer(CellPlayer2D):

    def __init__(self, player_id, state, location, interact_player, evolve):
        if state is None:
            state = default_player_state
        self.id = player_id
        self.state = state
        self.location = location
        self.interact_player = interact_player
        self.evolve = evolve

    def infected(self):
        new = self.clone()
        new.state[Infected_key] = True
        return new

    def cure(self):
        new = self.clone()
        new.state[Infected_key] = False
        return new

    def clone(self):
        state = deepcopy(self.state)
        return InfectionPlayer(state=state, player_id=self.id, location=self.location,
                               interact_player=self.interact_player,
                               evolve=self.evolve)


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


infection_player_evolve = lambda x: age_player(cure_player_by_chance(x))


def new_player_born(player: InfectionPlayer, loc: TwoDimLocation) -> InfectionPlayer:
    if loc == player.location:
        raise ValueError("Location of the children is the same as parent")

    children = player.clone()
    children.id = get_new_id(player.id)
    children.location = loc
    children.state[LIFE_KEY] = INITIAL_LIFE_SPAN
    return children


def initialize_infection_players(names: Iterable[str], locations: List[TwoDimLocation],
                                 player_states: List[Optional[Dict]]) -> List[InfectionPlayer]:
    return [InfectionPlayer(player_id=name,
                            state=state,
                            location=loc,
                            evolve=infection_player_evolve,
                            interact_player=interact_infection_player)
            for name, loc, state in zip(names, locations, player_states)]


def give_born_new_infection_player(player: InfectionPlayer, rectangle_map: TwoDimLocation) -> Optional[InfectionPlayer]:
    if random.random() > player.state[Birth_rate_key]:
        return None
    new_children = generate_children_in_2d(player.location, rectangle_map,
                                           lambda loc: new_player_born(player, loc), )
    return new_children


def generate_new_players(players: [InfectionPlayer], map_size: TwoDimLocation) -> [InfectionPlayer]:
    new_players = [give_born_new_infection_player(player, map_size) for player in players]
    new_players_not_none = filter(lambda x: x is not None, new_players)
    new_players_non_covered = list(filter(lambda x: x not in players, new_players_not_none))
    return players + new_players_non_covered


class InfectionGame(Game):
    def __init__(self, rectangle_map=MAP_SIZE, players: [InfectionPlayer] = None):
        if players is None:
            players = []
        self.players: List[InfectionPlayer] = players
        self.rectangle_map = rectangle_map

    def next_turn(self):
        old_players_evolved = [player.evolve(player) for player in self.players]

        player_interacted = [interact_cell_players(player, old_players_evolved) for player in old_players_evolved]
        player_alive = list(filter(lambda x: x.state[LIFE_KEY] > 0, player_interacted))
        new_players = generate_new_players(player_alive, self.rectangle_map)
        self.players = new_players

    def get_current_turn_info(self):
        infection_count = sum(p.state.get(Infected_key) for p in self.players)
        infection_info = f"{infection_count} players are infected out of {len(self.players)} players"
        return infection_info

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
        z = self.get_graph_origin()
        my_plt.imshow(z, cm.get_cmap("Greys"), interpolation='nearest')


def init_infection_game(rectangle_map=MAP_SIZE, number_of_player: int = NUM_INITIAL_PLAYER):
    i, j = rectangle_map
    players_locs = initialize_locations_in_rectangle(i, j, number_of_player)
    players = initialize_infection_players(names=[str(i) for i in range(len(players_locs))], locations=players_locs,
                                           player_states=[None for _ in range(number_of_player)])
    players = init_infected_player(players)
    return InfectionGame(rectangle_map=rectangle_map, players=players)
