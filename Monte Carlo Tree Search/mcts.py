import math
import random

# Tree node class definition
class TreeNode:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}
        self.is_terminal = board.is_win() or board.is_draw()
        self.is_fully_expanded = self.is_terminal

# MCTS class definition
class MCTS:
    def search(self, initial_state):
        self.root = TreeNode(initial_state)

        for _ in range(1000):
            node = self.select(self.root)
            score = self.rollout(node.board)
            self.backpropagate(node, score)

        return self.get_best_move(self.root, exploration_constant=0)

    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, exploration_constant=2)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        for state in node.board.generate_states():
            key = str(state.position)
            if key not in node.children:
                new_node = TreeNode(state, parent=node)
                node.children[key] = new_node
                if len(node.children) == len(node.board.generate_states()):
                    node.is_fully_expanded = True
                return new_node
        raise RuntimeError("No more children to expand, but node is not marked fully expanded.")

    def rollout(self, board):
        while not board.is_win():
            try:
                board = random.choice(board.generate_states())
            except IndexError:
                return 0  # draw
        return 1 if board.player_2 == 'x' else -1

    def backpropagate(self, node, score):
        while node:
            node.visits += 1
            node.score += score
            node = node.parent

    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_nodes = []

        for child in node.children.values():
            current_player = 1 if child.board.player_2 == 'x' else -1
            exploitation = current_player * (child.score / child.visits)
            exploration = exploration_constant * math.sqrt(math.log(node.visits) / child.visits)
            ucb1_score = exploitation + exploration

            if ucb1_score > best_score:
                best_score = ucb1_score
                best_nodes = [child]
            elif ucb1_score == best_score:
                best_nodes.append(child)

        return random.choice(best_nodes)
