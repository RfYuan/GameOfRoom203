from model.player import Player
import random

LIFE_KEY = "Life"
MAX_AGE = 100
AGE_SPEED_MAX = 2


def age_player(player: Player, ) -> None:
    state = player.state
    age_speed = random.randint(1, AGE_SPEED_MAX + 1)
    state[LIFE_KEY] -= age_speed


class BasicInfectionGame:
    pass
