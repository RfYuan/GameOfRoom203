class Game:
    def initialize_game(self):
        pass

    def next_turn(self, ):
        pass

    def show(self, my_plt):
        pass

    def get_current_turn_info(self) -> str:
        return "Current turn info"

    def next_turn_and_show(self, i, my_plt):
        self.next_turn()
        print(i, "turn")
        print(self.get_current_turn_info())
        self.show(my_plt)
