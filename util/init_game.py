from model.map import GameRoom203Map, GameRoom203Cell

DEFAULT_SIZE = (6, 4)


def init_test_map(size=DEFAULT_SIZE):
    length, width = size
    return GameRoom203Map([[GameRoom203Cell() for i in range(length)] for j in range(width)])
