class Board(object):
    """
    Board Black and white chess board, the size is 8*8, black is represented by X, white is represented by O, and . is used when no move is made.
    """

    def __init__(self):
        """
        Initialize the board state
        """
        self.empty = '.'  # Unplaced status
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]  # 规格：8*8
        self._board[3][4] = 'X'  # black chess piece
        self._board[4][3] = 'X'  # black chess piece
        self._board[3][3], self._board[4][4] = 'O', 'O'  # white chess piece

    def __getitem__(self, index):
        """
        Added Board[][] index syntax
        :param index: subscript index
        :return:
        """
        return self._board[index]

    def display(self, step_time=None, total_time=None):
        """
        print checkerboard
        :param step_time: The time-consuming of each step, such as: {"X":1,"O":0}, the default value is None
        :param total_time: total time, for example: {"X":1,"O":0}, the default value is None
        :return:
        """
        board = self._board
        # print(step_time,total_time)
        #print column names
        print(' ', ' '.join(list('ABCDEFGH')))
        # print row names and checkerboard
        for i in range(8):
            # print(board)
            print(str(i + 1), ' '.join(board[i]))
        if (not step_time) or (not total_time):
            # The time displayed when the board is initialized
            step_time = {"X": 0, "O": 0}
            total_time = {"X": 0, "O": 0}
            print("State: Total Pieces / Avg time for each step / Total time ")
            print("~   Black: " + str(self.count('X')) + ' / ' + str(step_time['X']) + ' / ' + str(
                total_time['X']))
            print("~   White: " + str(self.count('O')) + ' / ' + str(step_time['O']) + ' / ' + str(
                total_time['O']) + '\n')
        else:
            # Show time during the game
            print("State: Total Pieces / Avg time for each step / Total time ")
            print("~   Black: " + str(self.count('X')) + ' / ' + str(step_time['X']) + ' / ' + str(
                total_time['X']))
            print("~   White: " + str(self.count('O')) + ' / ' + str(step_time['O']) + ' / ' + str(
                total_time['O']) + '\n')

    def count(self, color):
        """
        Count the number of pieces on the color side. (O: White, X: Black, .: Unmoved state)
        :param color: [O,X,.] Represents different pieces on the board
        :return: Returns the total number of color pieces on the board
        """
        count = 0
        for y in range(8):
            for x in range(8):
                if self._board[x][y] == color:
                    count += 1
        return count

    def get_winner(self):
        """
        To judge the winning or losing of black and white flags, judge by the number of pieces
        :return: 0-black wins, 1-white flag wins, 2-means a draw, the number of black and white flags is equal
        """
        # Define the initial number of black and white chess pieces
        black_count, white_count = 0, 0
        for i in range(8):
            for j in range(8):
                # Count the number of black pieces
                if self._board[i][j] == 'X':
                    black_count += 1
                # Count the number of white pieces
                if self._board[i][j] == 'O':
                    white_count += 1
        if black_count > white_count:
            # Black Wins
            return 0, black_count - white_count
        elif black_count < white_count:
            # White Wins
            return 1, white_count - black_count
        elif black_count == white_count:
            # Indicates a tie, the number of black pieces is equal to the number of white
            return 2, 0

    def _move(self, action, color):
        """ 
        Move a pawn and get the coordinates of the reverse pawn
        :param action: The coordinates of the move can be D3 or (2,3)
        :param color: [O,X,.] Represents different pieces on the board
        :return: Returns the list of coordinates of the reversed pieces, or False if the move fails
        """
        # Determine whether the action is a string, and if so, convert it to digital coordinates
        if isinstance(action, str):
            action = self.board_num(action)

        fliped = self._can_fliped(action, color)

        if fliped:
            # If there is, reverse the coordinates of the opponent's chess piece
            for flip in fliped:
                x, y = self.board_num(flip)
                self._board[x][y] = color

            # drop coordinates
            x, y = action
            # Change the state at the action coordinate on the chessboard. After modification, the position belongs to three states such as color[X,O,.]
            self._board[x][y] = color
            return fliped
        else:
            # If there is no reverser, the move fails
            return False

    def backpropagation(self, action, flipped_pos, color):
        """
        backtracking
        :param: action: the coordinates of the drop point
        :param: flipped_pos: list of flipped pawn coordinates
        :param: color: The attributes of the pieces, [X,0,.] three cases
        :return
        """

        # Determine whether the action is a string, and if so, convert it to digital coordinates
        if isinstance(action, str):
            action = self.board_num(action)

        self._board[action[0]][action[1]] = self.empty
        # if color == 'X', then op_color = 'O'; else op_color = 'X'
        op_color = "O" if color == "X" else "X"

        for p in flipped_pos:
            # Determine whether the action is a string, and if so, convert it to digital coordinates
            if isinstance(p, str):
                p = self.board_num(p)
            self._board[p[0]][p[1]] = op_color

    def is_on_board(self, x, y):
        """
        Determine whether the coordinates are out of bounds
        :param x: row row coordinate
        :param y: col column coordinate
        :return: True or False
        """
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def _can_fliped(self, action, color):
        """
        Check whether the move is legal, if not, return False, otherwise return the coordinate list of the reversed move
        :param action: next child position
        :param color: [X,0,.] pawn status
        :return: False or Reverse the coordinate list of the opponent's pieces
        """
        # Determine whether the action is a string, and if so, convert it to digital coordinates
        if isinstance(action, str):
            action = self.board_num(action)
        xstart, ystart = action

        #Returns False if the position already has a pawn or is out of bounds
        if not self.is_on_board(xstart, ystart) or self._board[xstart][ystart] != self.empty:
            return False

        #Temporarily put color in the specified position
        self._board[xstart][ystart] = color
        # chess player
        op_color = "O" if color == "X" else "X"

        #pawn to be flipped
        flipped_pos = []
        flipped_pos_board = []

        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                                       [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            # If (x,y) is on the chessboard and it is the opponent's piece, continue in this direction, otherwise loop to the next angle.
            if self.is_on_board(x, y) and self._board[x][y] == op_color:
                x += xdirection
                y += ydirection
                # Further judge whether the point (x, y) is on the chessboard. If it is not on the chessboard, continue to loop the next angle. If it is on the chessboard, perform a while loop.
                if not self.is_on_board(x, y):
                    continue
                # Go all the way to a position that is out of bounds or is not the opponent's piece
                while self._board[x][y] == op_color:
                    #If it is always the opponent's pawn, the point (x, y) keeps looping until the point (x, y) is out of bounds or is not the opponent's pawn.
                    x += xdirection
                    y += ydirection
                    #Point (x,y) is out of bounds and is not an opponent's pawn
                    if not self.is_on_board(x, y):
                        break
                #Out of bounds, and no pawn to flip OXXXXX
                if not self.is_on_board(x, y):
                    continue

                # It's his own pawn OXXXXXXO
                if self._board[x][y] == color:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        # It ends when you return to the starting point
                        if x == xstart and y == ystart:
                            break
                        # Pieces to be flipped
                        flipped_pos.append([x, y])

        # Remove the chess pieces temporarily placed in front, that is, restore the chessboard
        self._board[xstart][ystart] = self.empty  # restore the empty space

        # If there are no pieces to be flipped, the move is illegal. return False
        if len(flipped_pos) == 0:
            return False

        for fp in flipped_pos:
            flipped_pos_board.append(self.num_board(fp))
        #The move is normal, return the chessboard coordinates of the flipped piece
        return flipped_pos_board

    def get_legal_actions(self, color):
        """
        Legal moves to obtain pieces according to the rules of Othello
        :param color: different colored pieces, X-black, O-white
        :return: Generate legal move coordinates, use list() method to get all legal coordinates
        """
        # Indicates the 8 different direction coordinates of the chessboard coordinate point, for example, the direction coordinate [0][1] means directly above the coordinate point.
        direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        op_color = "O" if color == "X" else "X"
        # Count the positions of the unsettled states adjacent to the op_color side
        op_color_near_points = []

        board = self._board
        for i in range(8):
            for j in range(8):
                if board[i][j] == op_color:
                    for dx, dy in direction:
                        x, y = i + dx, j + dy
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (
                                x, y) not in op_color_near_points:
                            op_color_near_points.append((x, y))
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        for p in op_color_near_points:
            if self._can_fliped(p, color):
                if p[0] in l and p[1] in l:
                    p = self.num_board(p)
                yield p

    def board_num(self, action):
        """
        Convert chessboard coordinates to digital coordinates
        :param action: chessboard coordinates, such as A1
        :return: numeric coordinates, such as A1 --->(0,0)
        """
        row, col = str(action[1]).upper(), str(action[0]).upper()
        if row in '12345678' and col in 'ABCDEFGH':
            # The coordinates are correct
            x, y = '12345678'.index(row), 'ABCDEFGH'.index(col)
            return x, y

    def num_board(self, action):
        """
        Converting digital coordinates to chessboard coordinates
        :param action: numeric coordinates, such as (0,0)
        :return: chessboard coordinates, such as (0,0) ---> A1
        """
        row, col = action
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        if col in l and row in l:
            return chr(ord('A') + col) + str(row + 1)
