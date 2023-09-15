# Connect 4 AI Project

Welcome to the Connect 4 AI project! Dive into the classic game with a twist — play against two of the most well-known AI algorithms: Minimax and Monte Carlo Tree Search (MCTS).

## Algorithms

### Minimax

- **How it Works**: The Minimax algorithm uses an evaluation function to evaluate the game board. It evaluates boards up to a certain depth (modifiable, default is 5).
  
- **Performance**: Minimax is fast and efficient. When it identifies a winning move or seeks to prevent a loss, it'll play instantly, giving it a more "reactive" feel.

### Monte Carlo Tree Search (MCTS)

- **How it Works**: MCTS operates differently from Minimax. Instead of using a heuristic evaluation, it uses simulations and probability scores to determine the best move. By default, it thinks for 5 seconds before making a move. This duration, however, ensures a more robust decision-making process.

- **Special Feature**: MCTS has an added advantage — it continues its simulations even when it's not its turn. This "thinking ahead" feature allows it to gather more data and make better moves over time.

- **Balance Factor**: The balance factor for MCTS is set at 1. It's a tunable parameter, so you can experiment with different values to potentially improve the AI's performance.

## Limitations

The algorithms are designed to be challenging, but they aren't infallible. While they will likely outplay average human players with ease, there's always room for improvement. A strategic mind might still find ways to outsmart the AI!

## How to Play

1. Launch the game in your terminal.
2. Enter either "minimax" or "mcts" to choose which algorithm you'd like to challenge.
3. Once the game starts, click anywhere on the screen to make a move in the chosen column.

**Tip**: It's all about strategy! Think ahead and try to outsmart the AI.

Enjoy the game and challenge yourself against the power of artificial intelligence!
