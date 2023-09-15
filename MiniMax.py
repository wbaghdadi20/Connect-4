import math
import random
import sys
import utils

# players
EMPTY = 0
PLAYER = 1
AI = 2

# board dimensions
ROW = 6
COL = 7

# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_GREY = (200, 200, 200)

class MiniMax():

    def __init__(self, game_board, p1, depth=5):
        self.game_board = game_board
        self.root_node_id = (0,)
        self.tree = {self.root_node_id: 
                        {"state": self.game_board.state, 
                         "player": None, 
                         "parent": None, 
                         "action": None, 
                         "children": []}
                    }
        self.p1 = p1
        self.depth = depth
        self.start_game(depth, maximize_player=AI)

    def start_game(self, depth, maximize_player):
        root_node_id = self.root_node_id
        current_node_id = root_node_id
        prev_player = self.tree[root_node_id]["player"]
        player = self.p1
        while not self.game_board.is_game_over():
            if self.game_board.close_window():
                sys.exit()
            if player == maximize_player:
                # AI's turn
                action = self.minimax(depth, current_node_id, maximize_player, player)[0]
                # Make the AI move
                col = (action,)
                row = self.game_board.get_next_open_row(col)
                self.game_board.drop_piece(row, col, player)
                current_node_id += (action,)
            else:
                while True:
                    if not self.tree[current_node_id]["children"]:
                        utils.generate_children(self, current_node_id, player)
                    exit, action = self.game_board.player_input()
                    if exit:
                        break
                current_node_id += (action,)
            prev_player = player
            player = AI if prev_player == PLAYER else PLAYER
        self.game_board.display_winner()

    def minimax(self, depth, current_node_id, maximize_player, player):
        current_state = self.tree[current_node_id]["state"]
        opp = AI if player == PLAYER else PLAYER
        is_terminal = utils.is_terminal_node(current_state, opp)

        if is_terminal:
            if utils.winning_move(current_state, player):
                return (None, math.inf)
            elif utils.winning_move(current_state, opp):
                return (None, -math.inf)
            else:
                return (None, 0)
        if depth == 0:
            return (None, utils.eval_board(current_state))
    
        if not self.tree[current_node_id]["children"]:
            utils.generate_children(self, current_node_id, player)

        if player == maximize_player:
            best_score = -math.inf
            child_score = -math.inf
            best_actions = {}
            for child_id in self.tree[current_node_id]["children"]:
                action = self.tree[child_id]["action"]
                child_state = self.tree[child_id]["state"]
                if utils.winning_move(child_state, player):
                    return (action, math.inf)
                child_score = self.minimax(depth-1, child_id, maximize_player, opp)[1]
                if child_score > best_score:
                    best_score = child_score
                    best_actions = {action: child_score}
                elif child_score == best_score:
                    best_actions[action] = child_score
            best_action = random.choice(list(best_actions.keys()))
            return (best_action, best_actions[best_action])
        else:
            best_score = math.inf
            child_score = math.inf
            best_actions = {}
            for child_id in self.tree[current_node_id]["children"]:
                action = self.tree[child_id]["action"]
                child_state = self.tree[child_id]["state"]
                if utils.winning_move(child_state, player):
                    return (action, -math.inf)
                child_score = self.minimax(depth-1, child_id, maximize_player, opp)[1]
                if child_score < best_score:
                    best_score = child_score
                    best_actions = {action: child_score}
                elif child_score == best_score:
                    best_actions[action] = child_score
            best_action = random.choice(list(best_actions.keys()))
            return (best_action, best_actions[best_action])