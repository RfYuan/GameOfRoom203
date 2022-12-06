from itertools import combinations
from typing import List, Optional, Tuple

import matplotlib.cm as cm

from game.ecology_game.ecology_model import TripleEco, TripleEcoPlayer, TripleEcoPlayerState, get_plyaer_type
from game.ecology_game.model_utils import update_energy
from model.game import Game2D
from model.map import TwoDimLocation
from util.player_evolve import generate_children_in_2d

GRASS_INITIAL_LIFE_SPAN = 50
GRASS_INITIAL_ENERGY = 10

LAMB_INITIAL_LIFE_SPAN = 30
LAMB_INITIAL_ENERGY = 20

LION_INITIAL_LIFE_SPAN = 40
LION_INITIAL_ENERGY = 15

GRASS_DEFAULT_STATE = TripleEcoPlayerState(
    life=GRASS_INITIAL_LIFE_SPAN,
    energy=GRASS_INITIAL_ENERGY
)

LAMB_DEFAULT_STATE = TripleEcoPlayerState(
    life=LAMB_INITIAL_LIFE_SPAN,
    energy=LAMB_INITIAL_ENERGY
)

LION_DEFAULT_STATE = TripleEcoPlayerState(
    life=LION_INITIAL_LIFE_SPAN,
    energy=LION_INITIAL_ENERGY
)

GROWING_RADIUS = {
    TripleEco.Grass: 4,
    TripleEco.Lamb: 2,
    TripleEco.Lion: 1
}

GROWING_THRESHOLD = {
    TripleEco.Grass: 0,
    TripleEco.Lamb: 30,
    TripleEco.Lion: 40
}


def get_triple_eco_player_generation_range(p: TripleEcoPlayer) -> int:
    return GROWING_RADIUS.get(get_plyaer_type(p))


def get_triple_eco_player_generation_threshold(p: TripleEcoPlayer) -> int:
    return GROWING_THRESHOLD.get(get_plyaer_type(p))


ECO_PLAYER_CONSUME = {
    (TripleEco.Lamb, TripleEco.Grass): (3, -6),
    (TripleEco.Lion, TripleEco.Lamb): (10, -20),
}

ECO_PLAYER_CONSUME_PROB = {
    (TripleEco.Lamb, TripleEco.Grass): 1,
    (TripleEco.Lion, TripleEco.Lamb): 0.5,
}


def eco_player_with_praying(praying_range: int, praying_prob: float) -> bool:
    pass


def eco_player_interact_praying(p1: TripleEcoPlayer, p2: TripleEcoPlayer) -> None:
    if p1 == TripleEco.Lamb and p2 == TripleEco.Grass:
        pass
    elif p1 == TripleEco.Tiger and p2 == TripleEco.Lamb:
        pass


def interact_player(current_player: TripleEcoPlayer, other_player: TripleEcoPlayer, ) -> None:
    eco_player_interact_praying(current_player, other_player)


def interact_players_as_list(players: List[TripleEcoPlayer]) -> None:
    for p1, p2 in combinations(players, 2):
        interact_player(p1, p2)
        interact_player(p2, p1)


def generate_by_energy_threshold(current_player: TripleEcoPlayer, map_size: TwoDimLocation, threshold: int) -> \
        Optional[TripleEcoPlayer]:
    if current_player.state.energy >= threshold:
        new_player = generate_children_in_2d(current_player.location, map_size,
                                             lambda loc: TripleEcoPlayer(
                                                 player_state=get_default_state_by_type(current_player.type),
                                                 location=loc
                                             ), k=get_triple_eco_player_generation_range(current_player)
                                             )
        update_energy(current_player, current_player.state.energy - threshold)
        return new_player
    return None


def get_default_state_by_type(eco_type: TripleEco) -> TripleEcoPlayerState:
    if eco_type == TripleEco.Grass:
        return GRASS_DEFAULT_STATE
    elif eco_type == TripleEco.Lamb:
        return LAMB_DEFAULT_STATE
    else:
        return LION_DEFAULT_STATE


def evolve_player(p: TripleEcoPlayer) -> TripleEcoPlayer:
    pass


def born_player(p: TripleEcoPlayer) -> Optional[TripleEcoPlayer]:
    pass


def init_players(player_info: List[Tuple[TwoDimLocation, TripleEco]]) -> List[TripleEcoPlayer]:
    return [
        TripleEcoPlayer(
            player_state=get_default_state_by_type(eco_type),
            location=loc
        )
        for loc, eco_type in player_info
    ]


class TripleEcoGame(Game2D):
    def next_turn(self):
        pass

    def get_graph_origin(self) -> List[List[float]]:
        pass

    def show(self, my_plt):
        z = self.get_graph_origin()
        my_plt.imshow(z, cm.get_cmap("Greys"), interpolation='nearest')
