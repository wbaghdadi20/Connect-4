import Gameboard
import MiniMax
import MCTS

def main():
    while True:
        ais = ["minimax", "mcts"]
        print(f"AI types: {ais[0]:<2}, {ais[1]}.")

        while True:
            user_input = input("Select AI Type (0, 1, 'minimax', or 'mcts'): ")

            if user_input in ["0", "1"]:
                ai_type = ais[int(user_input)]
                break  # Exit the loop if a valid input is provided
            elif user_input in ais:
                ai_type = user_input
                break  # Exit the loop if a valid input is provided
            else:
                print("Invalid input. Please enter 0, 1, 'minimax', or 'mcts'.")

        game_board = Gameboard.Gameboard()
        game_board.draw_board()

        if ai_type == "minimax":
            MiniMax.MiniMax(game_board)
        else:
            MCTS.MCTS(game_board)

main()