import numpy as np
from player import Player

default_config = {
    'search_depth': 4,
    'pre_search_flag': False,
    'pre_search_branch': 6,
}


class AIPlayer(Player):
    """
    AI player
    """

    def __init__(self, color, config=default_config):
        """
        Player initialization
        :param color: player, 'X' - black, 'O' - white
        """
        super().__init__(color)
        # add o
        self.opponent_color = 'O' if color == 'X' else 'X'
        # config
        self.search_depth = config['search_depth']
        self.pre_search_flag = config['pre_search_flag'] # pre-prone can increase search depth
        self.pre_search_branch = config['pre_search_branch']

        self.wmap = np.array([
                    [500,-25,10,5,5,10,-25,500],
                    [-25,-45,1,1,1,1,-45,-25],
                    [10,1,3,2,2,3,1,10],
                    [5,1,2,1,1,2,1,5],
                    [5,1,2,1,1,2,1,5],
                    [10,1,3,2,2,3,1,10],
                    [-25,-45,1,1,1,1,-45,-25],
                    [500,-25,10,5,5,10,-25,500],
        ])

    def get_move(self, board):
        """
        Get the best move position based on the current chessboard state
        :param board: board
        :return: action Best move position, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '[AI] Black'
        else:
            player_name = '[AI] White'
        print("Please wait a moment, the other {} ({}) is thinking...\n==============================\n".format(player_name, self.color))

        action = self.alpha_beta_search(board)

        return action

    def alpha_beta_search(self, state):
        '''
        state: board
        '''
        # TODO return an action maximize the utility
        # depth = 7 is the limitation
        utility, action = self.max_value(state, depth=self.search_depth, alpha=-float('inf'), beta=float('inf'), ab_depth=0)
        return action

    def max_value(self, state, depth, alpha, beta, ab_depth):
        # judge whether terminal or reach the max deep we can do
        if self.is_terminal(state) or depth == 0:
            return self.utility(state, ab_depth), None
        # find all possible action(one step)
        action_list = list(state.get_legal_actions(self.color))
        if len(action_list) == 0: # no legal action
            return self.utility(state, ab_depth), None
        val = -float('inf')
        best_action = None
        # add a pre-search self.pre_search_branch
        if self.pre_search_flag:
            pre_val = []
            for action in action_list:
                flipped_pos = state._move(action, self.color)
                if not flipped_pos:
                    continue
                state.backpropagation(action, flipped_pos, self.color)
                pre_val.append(self.utility(state, ab_depth))
            idx = np.argsort(pre_val)[::-1]
            action_list = [action_list[i] for i in idx[0:self.pre_search_branch]]
        # for each action
        # move one step and get state
        # compute utility and decide whether jump
        # update max uility alpha
        # go back the step
        for action in action_list:
            flipped_pos = state._move(action, self.color)
            if not flipped_pos:
                continue
            act_val, _ = self.min_value(state, depth-1, alpha, beta, ab_depth+1)
            state.backpropagation(action, flipped_pos, self.color)
            # act_val = self.min_value(state, depth-1, alpha, beta)
            if act_val > val:
                val = act_val
                best_action = action
            if val > beta:
                break
            alpha = max(alpha, val)
        return val, best_action

    def min_value(self, state, depth, alpha, beta, ab_depth):
        # judge whether terminal or reach the max deep we can do
        if self.is_terminal(state) or depth == 0:
            return self.utility(state, ab_depth), None
        # find all possible action(one step)
        action_list = list(state.get_legal_actions(self.opponent_color))
        if len(action_list) == 0: # no legal action
            return self.utility(state, ab_depth), None
        val = float('inf')
        best_action = None

        # add a pre-search self.pre_search_branch
        if self.pre_search_flag:
            pre_val = []
            for action in action_list:
                flipped_pos = state._move(action, self.color)
                if not flipped_pos:
                    continue
                state.backpropagation(action, flipped_pos, self.color)
                pre_val.append(self.utility(state, ab_depth))
            idx = np.argsort(pre_val)[::-1]
            action_list = [action_list[i] for i in idx[:self.pre_search_branch]]

        for action in action_list:
            flipped_pos = state._move(action, self.opponent_color)
            if not flipped_pos:
                continue
            act_val, _ = self.max_value(state, depth-1, alpha, beta, ab_depth+1)
            state.backpropagation(action, flipped_pos, self.opponent_color)
            if act_val < val:
                val = act_val
                best_action = action
            if val < alpha:
                break
            beta = min(beta, val)
        return val, best_action

    def utility(self, state, depth):
        '''
        depth: the depth of the node (to the root), absolute depth
        '''
        # transform board to a matrix
        def board2mat(board):
            board_mat = np.zeros((8, 8))
            # should not access variables in this way...
            for l in range(8):
                for c in range(8):
                    if board._board[l][c] == 'X':
                        board_mat[l, c] = 1
                    elif board._board[l][c] == 'O':
                        board_mat[l, c] = -1
            return board_mat
        # in the end, just use the board_score
        if depth > 60:
            return state.count(self.color) - state.count(self.opponent_color)
        # in the begining, just use the action score
        if depth < 10:
            return len(list(state.get_legal_actions(self.color))) - len(list(state.get_legal_actions(self.opponent_color)))
        # add weight 
        board_score = np.sum(np.multiply(board2mat(state), self.wmap))
        # add action sub
        action_score = len(list(state.get_legal_actions(self.color))) - len(list(state.get_legal_actions(self.opponent_color)))
        # TODO add stable chess
        return board_score+15*action_score
        # return state.count(self.color) - state.count(self.opponent_color)

    def is_terminal(self, state):
            if state.count('.') == 0:
                return True
            return False
