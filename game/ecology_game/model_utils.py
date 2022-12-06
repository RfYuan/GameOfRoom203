from dataclasses import replace

from game.ecology_game.ecology_model import TripleEcoPlayer


def update_energy(player: TripleEcoPlayer, new_value: int):
    if player.state.energy == new_value:
        return player
    else:
        player.state = replace(player.state, energy=new_value)


def update_life(player: TripleEcoPlayer, new_value: int):
    if player.state.life == new_value:
        return player
    else:
        player.state = replace(player.state, life=new_value)
