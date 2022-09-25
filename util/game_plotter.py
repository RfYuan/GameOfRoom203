from model.game import Game
from model.player import Player
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_game_anime(game: Game, interval=500, frames=20):
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, game.next_turn_and_show, fargs=(ax,), frames=frames, interval=interval, repeat=False)
    plt.show()
