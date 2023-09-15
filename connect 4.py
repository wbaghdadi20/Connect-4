import Gameboard
import MiniMax
import MCTS

EMPTY = 0
PLAYER = 1
AI = 2

class Connect4:

    def main(self):
        while True:
            ais = ["minimax", "mcts"]
            ai = self.get_player_type(ais, "Select AI Type ('minimax', or 'mcts'): ")

            game_board = Gameboard.Gameboard(ai)
            game_board.draw_board()

            if ai == "minimax":
                MiniMax.MiniMax(game_board, AI)
            else:
                MCTS.MCTS(game_board, PLAYER)
                
            game_board.display_winner()

    def get_player_type(self, ais, prompt):
        while True:
            user_input = input(prompt)
            if user_input in ais:
                return user_input
            else:
                print(f"Invalid input. Please enter one of the following: {', '.join(ais)}.")

if __name__ == "__main__":
    game = Connect4()
    game.main()