from Players.Player import Player
from Enviroment.GameRules import GameRules

class HumanPlayer(Player):

    def make_mini_move(self,board):
        compass = input()
        return GameRules.compass_to_dir[compass]

    def make_moves(self,board,last_move):
        
        moves = []
        while True:
            board.draw()
            mini_move = self.make_mini_move(board)
            if mini_move not in GameRules.find_valid_minimoves(board):
                return moves
            moves.append(mini_move)
            my_turn = board.fast_make_move(mini_move)
            if not my_turn:
                return moves