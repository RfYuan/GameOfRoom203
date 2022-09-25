from game.infection_game import init_infection_game
from util.game_plotter import plot_game_anime

# map = init_test_map()
# print(map.cells)
#
#
# player1 = Player()

i_game = init_infection_game()
plot_game_anime(i_game)
