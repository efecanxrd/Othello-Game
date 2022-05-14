class Player(object):
#Player base class

    def __init__(self, color=None):
        """
        Get current player state
        :param color: If color=='X', it means black is on the side; color=='O', it means white.
        """
        self.color = color

    def get_move(self, board):
        """
        Obtain the coordinates of the best move position based on the current chessboard
        :param board: current board
        :return: position coordinates of the move
        """
        pass

    def move(self, board, action):
        """
        Drop a chess piece, the coordinates of the chess piece dropped by the root piece get the coordinate list of the reverse chess piece
        :param board: board
        :param action: the coordinates of the dropped piece
        :return: Reverse the list of pawn coordinates
        """
        flipped_pos = board._move(action, self.color)
        return flipped_pos
