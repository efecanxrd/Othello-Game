from func_timeout import func_timeout, FunctionTimedOut
import datetime
from board import Board
from copy import deepcopy


class Game(object):
    def __init__(self, black_player, white_player):
        self.board = Board()  
        
        self.current_player = None
        self.black_player = black_player  
        self.white_player = white_player  
        self.black_player.color = "X"
        self.white_player.color = "O"

    def switch_player(self, black_player, white_player):
        """
        Switch palyer 
        :param black_player: black player
        :param white_player: white player
        :return: current player
        """

        if self.current_player is None:
            return black_player
        else:
            if self.current_player == self.black_player:
                return white_player
            else:
                return black_player

    def print_winner(self, winner):
        """
        :param winner: code from [0,1,2], 0: black players wins; 1: white player wins; 3: draw.
        :return: None
        """
        print(['Black Player Wins!', 'White Player Wins!', 'There is a Draw!'][winner])

    def force_loss(self, is_timeout=False, is_board=False, is_legal=False):
        """
         If you place 3 pieces that do not meet the rules and time out, the game will end, and modifying the board is also a loser.
        :param is_timeout: Whether the time has timed out, the default is not timed out
        :param is_board: whether to modify the board
        :param is_legal: whether the move is legal
        :return: winner (0,1), pawn difference 0
        """

        if self.current_player == self.black_player:
            win_color = 'White (O)'
            loss_color = 'Black (X)'
            winner = 1
        else:
            win_color = 'Black (X)'
            loss_color = 'White (O)'
            winner = 0

        if is_timeout:
            print('\n{} Think more than 60s, {} Wins!'.format(loss_color, win_color))
        if is_legal:
            print('\nThe {} move 3 times does not meet the rules, so {} wins'.format(loss_color, win_color))
        if is_board:
            print('\n{} Unauthorized changes to the chessboard are judged to be lost, so {} wins'.format(loss_color, win_color))

        diff = 0

        return winner, diff

    def run(self):
        """
        run game
        :return:
        """
        # Define and count the playing time of both sides
        total_time = {"X": 0, "O": 0}
        #Define the time for each move of both sides
        step_time = {"X": 0, "O": 0}
        #Initialize the result of winning and losing and the difference between the pieces
        winner = None
        diff = -1

        # Games start
        print('\n========Start========\n')
        # Checkerboard initialization
        self.board.display(step_time, total_time)
        while True:
            # Switch the current player, if the current player is None or white white_player, return black black_player;
            # Otherwise return white_player.
            self.current_player = self.switch_player(self.black_player, self.white_player)
            start_time = datetime.datetime.now()
            # After the current player thinks about the board, get the position of the move
            # Determine the current chess player
            color = "X" if self.current_player == self.black_player else "O"
            # Get the legal position of the current player
            legal_actions = list(self.board.get_legal_actions(color))
            if len(legal_actions) == 0:
                # Determine if the game is over
                if self.game_over():
                    # The game is over and neither side has a legal position
                    winner, diff = self.board.get_winner() 
                    break
                else:
                    # The other side has a legal position, switch the player
                    continue

            board = deepcopy(self.board._board)

            #Legal actions not equal to 0 means the current player has a legal move
            try:
                for i in range(0, 3):
                    # Get the move position
                    action = func_timeout(60, self.current_player.get_move,
                                          kwargs={'board': self.board})

                    #If action is Q then the human wants to end the game
                    if action == "Q":
                        #It shows that humans want to end the game, that is, to win or lose according to the number of pieces.
                        break
                    if action not in legal_actions:
                        #Determine whether the current player's move is legal. If it is not legal, the opponent needs to re-enter
                        print("Invalid location, Please relocate")
                        continue
                    else:
                        #If the move is legal, break directly
                        break
                else:
                    #It's illegal to make 3 moves, end the game!
                    winner, diff = self.force_loss(is_legal=True)
                    print("3 consective invalid locations, game ends!")
                    break
            except FunctionTimedOut:
                # Time out, end the game
                winner, diff = self.force_loss(is_timeout=True)
                print("The operation times out, the game ends!")
                break

            end_time = datetime.datetime.now()
            if board != self.board._board:
                #Modify the board and end the game!
                winner, diff = self.force_loss(is_board=True)
                break
            if action == "Q":
                #It shows that humans want to end the game, that is, to win or lose according to the number of pieces.
                winner, diff = self.board.get_winner()
                break

            if action is None:
                continue
            else:
                # Count the time spent in one step
                es_time = (end_time - start_time).seconds
                if es_time > 60:
                    #If this step exceeds 60 seconds, the game is over.
                    print('\n{}, think more than 60s'.format(self.current_player))
                    winner, diff = self.force_loss(is_timeout=True)
                    break

                #Current player color, update the game
                self.board._move(action, color)
                #Count the total time spent playing chess for each type of chess piece
                if self.current_player == self.black_player:
                    #The current player is the black side
                    step_time["X"] = es_time
                    total_time["X"] += es_time
                else:
                    step_time["O"] = es_time
                    total_time["O"] += es_time
                #Show the current board
                self.board.display(step_time, total_time)

                #Determine if the game is over
                if self.game_over():
                    #game over
                    winner, diff = self.board.get_winner()  # 得到赢家 0,1,2
                    break

        print('\n==========GAME OVER==========\n')
        self.board.display(step_time, total_time)
        self.print_winner(winner)

        # Return black win','white win','draw', the difference in the number of pieces
        if winner is not None and diff > -1:
            result = {0: 'Black Player Wins!', 1: 'White Player Wins!', 2: 'There is a draw!'}[winner]

            # return result,diff

    def game_over(self):
        """
        Determine if the game is over
        :return: True/False game over/game not over
        """
        # According to the current chessboard, determine whether the chess game is terminated
        # If the current player does not have a legal position to play chess, switch players; if another player does not have a legal position to play chess, the game stops.
        b_list = list(self.board.get_legal_actions('X'))
        w_list = list(self.board.get_legal_actions('O'))

        is_over = len(b_list) == 0 and len(w_list) == 0  # return value True/False

        return is_over
