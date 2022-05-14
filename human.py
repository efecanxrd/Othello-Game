from player import Player

class HumanPlayer(Player):

    def __init__(self, color):
        """
        Inherit the base class, the player initializes
        :param color: player, 'X' - black, 'O' - white
        """
        super().__init__(color)

    def get_move(self, board):
        """
        Enter the legal position of human beings based on the current chessboard
        :param board: board
        :return: The position of the human chess move
        """
        # If self.color is black "X", then player is "black", otherwise "white"
        if self.color == "X":
            player = "[H] BLACK"
        else:
            player = "[H] WHITE"

        # The human player enters the move position, if 'Q' is entered, it returns 'Q' and ends the game.
        # If a human player enters a board position, e.g. 'A1',
        # First judge whether the input is correct, and then judge whether it conforms to the position of Othello rules
        while True:
            action = input("Please enter a valid coordinate for the '{} ({})' | e.g. 'D3' (Enter 'Q' to end the game)\n>> ".format(player, self.color))
            # If the human player types Q to end the game
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                #Check if human input is correct
                if row in '12345678' and col in 'ABCDEFGH':
                    #Checks if human input is a valid drop position
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("Your input is invalid, please try again!")
