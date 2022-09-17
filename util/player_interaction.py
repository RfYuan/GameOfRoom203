import math

from model.player import CellPlayer, Player


def euclid_distance(p1: Player, p2: Player) -> float:
    return math.dist(p1.location, p2.location)


def interact_players(p1: CellPlayer, players: [CellPlayer]) -> CellPlayer:
    # p1 could be in players list, need to skip the effect
    result_player = p1.clone()
    for other_player in players:
        if p1 != other_player:
            result_player = result_player.interact_player(result_player, other_player)
    return result_player
