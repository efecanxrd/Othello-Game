import random
from player import Player

class RandomPlayer(Player):
    """
    RandomPlayer class, randomly returns a legal move position
    """

    def __init__(self, color):
        """
        Inherit the base class player, the player is initialized
        :param color: player, 'X' - black, 'O' - white
        """
        super().__init__(color)

    def random_choice(self, board):
        """
        Randomly choose a move position from the legal move positions
        :param board: board
        :return: random legal move position, e.g. 'A1'
        """
        # Use the list() method to get a list of all legal move positions
        action_list = list(board.get_legal_actions(self.color))
   
        # If action_list is empty, return None, otherwise select a random element from it, that is, legal move coordinates
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        """
        Get the best move position based on the current chessboard state
        :param board: board
        :return: action Best move position, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '[RP] BLACK'
        else:
            player_name = '[RP] WHITE'
        print("Please wait a moment, the other {} ({}) is thinking...\n==============================\n".format(player_name, self.color))
        action = self.random_choice(board)
        return action
