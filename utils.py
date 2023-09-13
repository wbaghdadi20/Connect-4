# players
EMPTY = 0
PLAYER = 1
AI = 2

# board dimensions
ROW = 6
COL = 7

# drop pieces in a board (only used for creating children)
def drop_piece(parent_state, action, player):
    row = get_next_open_row(parent_state, action)
    new_state = parent_state.copy()
    new_state[row][action] = player
    return new_state

# returns index of first available row in a given column
def get_next_open_row(parent_state, col):
    for i in range(ROW-1, -1, -1):
        if parent_state[i][col] == EMPTY:
            return i
    
        
def winning_move(state, player):
    # Check horizontal locations for win
    for c in range(COL-3):
        for r in range(ROW):
            if state[r][c] == player and state[r][c+1] == player and state[r][c+2] == player and state[r][c+3] == player:
                return True
    # Check vertical locations for win
    for c in range(COL):
        for r in range(ROW-3):
            if state[r][c] == player and state[r+1][c] == player and state[r+2][c] == player and state[r+3][c] == player:
                return True
    # Check negatively sloped diaganols
    for c in range(COL-3):
        for r in range(ROW-3):
            if state[r][c] == player and state[r+1][c+1] == player and state[r+2][c+2] == player and state[r+3][c+3] == player:
                return True
    # Check positively sloped diaganols
    for c in range(COL-3):
        for r in range(3, ROW):
            if state[r][c] == player and state[r-1][c+1] == player and state[r-2][c+2] == player and state[r-3][c+3] == player:
                return True
            
def get_available_actions(state):
    return [c for c in range(COL) if any(state[:, c] == 0)]

def eval_board(state):
    return score_position(state, AI) + score_position(state, PLAYER)

def evaluate_window(window, piece):
    score = 0
    if window.count(piece) == 4:
        score += float("inf")
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    return score

def score_position(state, player):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(state[:, COL // 2])]
        center_count = center_array.count(player)
        score += center_count * 3
        # Score horizontal
        for r in range(ROW):
            row_array = [int(i) for i in list(state[r, :])]
            for c in range(COL - 3):
                window = row_array[c : c + 4]
                score += evaluate_window(window, player)
        # Score vertical
        for c in range(COL):
            col_array = [int(i) for i in list(state[:, c])]
            for r in range(ROW - 3):
                window = col_array[r : r + 4]
                score += evaluate_window(window, player)
        # Score positively sloped diagonal
        for r in range(ROW - 3):
            for c in range(COL - 3):
                window = [state[r + i][c + i] for i in range(4)]
                score += evaluate_window(window, player)
        # Score negatively sloped diagonal
        for r in range(ROW - 3):
            for c in range(COL - 3):
                window = [state[r + 3 - i][c + i] for i in range(4)]
                score += evaluate_window(window, player)
        return score

def is_terminal_node(state, player):
    return winning_move(state, player) or len(get_available_actions(state)) == 0