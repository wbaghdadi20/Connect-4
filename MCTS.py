import math
import random
import sys
import time
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

BALANCE_FACTOR = math.sqrt(2)

class MCTS:

    def __init__(self, game_board):
        self.game_board = game_board
        self.root_node_id = (0,)
        self.tree = {self.root_node_id: 
                        {"state": self.game_board.state, 
                         "player": None, 
                         "parent": None, 
                         "action": None, 
                         "children": [],
                         "wins": 0,
                         "visits": 0
                         }
                    }
        self.time_limit = 5
        self.total_visits = 0
        self.p1 = PLAYER # random.randint(PLAYER, AI)
        self.start_game()

    def start_game(self):
        root_node_id = self.root_node_id
        current_node_id = root_node_id
        prev_player = self.tree[root_node_id]["player"] 
        player = self.p1
        while not self.game_board.is_game_over():
            if player == AI:
                # AI's turn
                t0 = time.time()
                i = 0

                while time.time() - t0 < self.time_limit:
                    selected_node_id = self.selection(current_node_id)
                    expanded_node = self.expansion(selected_node_id, player)
                    winner = self.simulation(expanded_node)
                    self.backpropagation(expanded_node, winner)
                    i += 1

                children = self.tree[current_node_id]["children"]
                if not children:
                    self.generate_children(current_node_id, player)
                total_visits = -math.inf
                for child_id in children:
                    action = self.tree[child_id]["action"]
                    visits = self.tree[child_id]["visits"]
                    if visits > total_visits:
                        total_visits = visits
                        best_action = action
                col = (best_action,)
                row = self.game_board.get_next_open_row(col)
                self.game_board.drop_piece(row, col, player)
                # new_key = current_node_id + (best_action,)
                current_node_id += (best_action,)
            else:
                while True:
                    if not self.tree[current_node_id]["children"]:
                        self.generate_children(current_node_id, player)
                    exit, action = self.game_board.player_input()
                    if exit:
                        break
                current_node_id += (action,)
            prev_player = player
            player = AI if prev_player == PLAYER else PLAYER
        # draw
        if not self.game_board.empty_spaces():
            self.game_board.display("Draw !!", 100, 10, LIGHT_GREY)
        elif self.game_board.winning_move(AI):
            self.game_board.display("AI Wins !!", 120, 10, YELLOW)
        else:
            self.game_board.display("Player Wins !!", 30, 10, RED)

    def uct(self, node_id):
        if not self.total_visits: # node_id is root doesnt have parent
            return math.inf
        parent_id = self.tree[node_id]["parent"]
        parent_visits = self.tree[parent_id]["visits"]
        wins = self.tree[node_id]["wins"]
        visits = self.tree[node_id]["visits"]
        small_value = sys.float_info.epsilon
        exploitation = wins / (visits + small_value)
        exploration = math.sqrt(math.log(parent_visits + small_value) / (visits + small_value))
        return exploitation + BALANCE_FACTOR * exploration

    def selection(self, current_node_id):
        is_terminal = False
        leaf_node_id = current_node_id
        while not is_terminal:
            num_children = len(self.tree[leaf_node_id]['children'])
            if not num_children:
                is_terminal = True
            else:
                best_score = -math.inf
                child_score = -math.inf
                best_actions = {}
                for child_id in self.tree[leaf_node_id]["children"]:
                    action = self.tree[child_id]["action"]
                    child_score = self.uct(child_id)
                    if child_score > best_score:
                        best_score = child_score
                        best_actions = {action: child_score}
                    elif child_score == best_score:
                        best_actions[action] = child_score
                best_action = random.choice(list(best_actions.keys()))
                leaf_node_id += (best_action,)
        return leaf_node_id
    
    def expansion(self, selected_node_id, player):
        state = self.tree[selected_node_id]["state"]
        if selected_node_id != self.root_node_id:
            opp = self.tree[selected_node_id]["player"]
            player = AI if opp == PLAYER else PLAYER
        else:
            opp = PLAYER
        is_terminal_node = utils.is_terminal_node(state, opp)

        if not is_terminal_node:
            self.generate_children(selected_node_id, player)

        if not self.tree[selected_node_id]["children"]: # lead node
            return selected_node_id
        
        best_actions = []
        for child_id in self.tree[selected_node_id]["children"]:
            action = self.tree[child_id]["action"]
            child_state = self.tree[child_id]["state"]
            if utils.winning_move(child_state, player):
                return selected_node_id + (action,)
            best_actions.append(action)

        return selected_node_id + (random.choice(best_actions),)

    def simulation(self, expanded_node_id):
        self.total_visits += 1
        node_id = expanded_node_id
        state = self.tree[node_id]["state"]
        opp = self.tree[node_id]["player"]
        player = AI if opp == PLAYER else PLAYER
        is_terminal = utils.is_terminal_node(state, opp)
        count = 0

        while not is_terminal and count < 10:
            actions_available = utils.get_available_actions(state)
            if not len(actions_available):
                return None # its a draw
            else:
                count += 1
                actions = []
                for action in actions_available:
                    # simulate dropping a piece
                    child_state = utils.drop_piece(state, action, player)
                    if utils.winning_move(child_state, player):
                        return player
                    actions.append(action)
                # to move to next state
                action = random.choice(actions)
                state = utils.drop_piece(state, action, player)
            opp = player
            player = AI if player == PLAYER else PLAYER

        return opp # default in case expanded node is terminal
    
    def backpropagation(self, node_id, winner):
        player = self.tree[node_id]["player"]
        opp = AI if player == PLAYER else PLAYER
        self.tree[node_id]["visits"] += 1

        if winner == player:
            self.tree[node_id]["wins"] += 1
        elif winner == opp:
            self.tree[node_id]["wins"] -= 10

        if node_id != self.root_node_id:
            self.backpropagation(self.tree[node_id]["parent"], winner)

    def generate_children(self, parent_node_id, player):
        # get available locations
        parent_state = self.tree[parent_node_id]["state"]
        actions_available = utils.get_available_actions(parent_state)
        for action in actions_available:
            # create new child node and add it to tree
            child_id = parent_node_id + (action,)
            child_state = utils.drop_piece(parent_state, action, player)
            # Initialize the child node in the tree
            self.tree[child_id] = {
                "state": child_state,
                "player": player,
                "parent": parent_node_id,
                "action": action,
                "children": [],
                "wins": 0,
                "visits": 0
            }
            self.tree[parent_node_id]["children"].append(child_id)