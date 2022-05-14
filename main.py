from game import Game
from aiPlayer import AIPlayer
from randomPlayer import RandomPlayer
from humanPlayer import HumanPlayer

if __name__ == "__main__":
    # 4 false 135/150
    # 5 false 49/50
    # 5 10 40 
    # 8 6
    config_1 = {
    'search_depth': 6,
    'pre_search_flag': False,
    'pre_search_branch': 10,}
    try:
        x = int(input('Select game type:\n1: Human vs AI\n2: Random Player vs AI\n3: AI vs AI\n4: Random Player vs Human\n>> '))
    except ValueError:
        print('You must write a number!')
    except KeyboardInterrupt:
        print('Exiting...')
        exit(0)
    if x == 1:
        black_player = HumanPlayer("X")
        white_player = AIPlayer("O", config_1)
    elif x == 2:
        black_player = RandomPlayer("X")
        white_player = AIPlayer("O", config_1)       
    elif x == 3:
        black_player = AIPlayer("X", config_1) 
        white_player = AIPlayer("O", config_1)   
    elif x == 4:
        black_player = HumanPlayer("X")
        white_player = RandomPlayer("O")
    else:
        print('You can only write one of the numbers 1-4.')
    game = Game(black_player, white_player)
    game.run()
