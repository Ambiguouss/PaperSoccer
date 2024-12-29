class GameRules:
    @staticmethod
    def is_valid_move(board, move):
        next_ball=tuple(a + b for a, b in zip(board.ball, move))
        if (next_ball,board.ball) not in board.board_graph.edges:
            return False
        if board.board_graph.edges[(board.ball,next_ball)]['weight']!=0:
            return False
        if board.ball not in board.touched_fields:
            return False
        return next_ball
    
    @staticmethod
    def in_player1_goal(board):
        if board.ball in board.goalsfirst:
            return True
        
    @staticmethod
    def in_player2_goal(board):
        if board.ball in board.goalssecond:
            return True
    
    #might have a problem if there are a lot of valid moves
    @staticmethod
    def find_valid_moves(board,max_moves=None):
        valid_moves=[]
        if GameRules.in_player1_goal(board) or GameRules.in_player2_goal(board):
            return valid_moves
        for e in board.board_graph.edges(board.ball):
            if e[0]!=board.ball:
                raise "o Huj"
            e_direction = tuple(b -a for a, b in zip(e[0], e[1]))
            if GameRules.is_valid_move(board,e_direction) is False:
                continue
            if e[1] in board.touched_fields:
                board.board_graph.edges[e]["weight"]=-1
                board.ball=e[1]
                valid = GameRules.find_valid_moves(board,max_moves)
                for sublist in valid:
                    valid_moves.append([e_direction] + sublist)
                board.ball=e[0]
                board.board_graph.edges[e]["weight"]=0
            else:
                valid_moves.append([e_direction])
            if(max_moves is not None and len(valid_moves)>max_moves):
                break
        return valid_moves