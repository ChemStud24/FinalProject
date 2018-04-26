############################################################
# CIS 521: Homework 3a
############################################################

student_name = "William Johnson"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from random import choice


############################################################
# Section 1: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False]*cols]*rows)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = [b[:] for b in board]
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [b[:] for b in [[False]*self.cols]*self.rows]

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row + 1 < self.rows and col < self.cols:
                if row >= 0 and col >= 0:
                    return (not self.board[row][col]) & (not self.board[row+1][col])
            return False
        else:
            if row < self.rows and col + 1 < self.cols:
                if row >= 0 and col >= 0:
                    return (not self.board[row][col]) & (not self.board[row][col+1])
            return False

    def legal_moves(self, vertical):
        return ((r,c) for r in xrange(self.rows) for c in xrange(self.cols) if self.is_legal_move(r,c,vertical))  ############## XRANGE

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row,col,vertical):
            self.board[row][col] = True
            if vertical:
                self.board[row+1][col] = True
            else:
                self.board[row][col+1] = True
            return self

    def game_over(self, vertical):
        return len(list(self.legal_moves(vertical))) == 0

    def copy(self):
        return DominoesGame([b[:] for b in self.board])

    def successors(self, vertical):
        return (((r,c),self.copy().perform_move(r,c,vertical)) for (r,c) in self.legal_moves(vertical))

    def get_random_move(self, vertical):
        return choice(list(self.legal_moves(vertical)))

    # Required
    def get_best_move(self, vertical, limit):
        alpha = -float('inf')
        beta = float('inf')
        return self.max_value(vertical,limit,alpha,beta)

    def max_value(self,vertical,limit,alpha,beta):
        # print('MAX')
        # print('Limit?',limit,limit == 0)
        # print('Game Over?',self.game_over(vertical))
        # print('Limit or Game Over?',limit == 0 | self.game_over(vertical))
        if limit == 0 or self.game_over(vertical):
            return ((),self.utility(vertical),1)
        v = -float('inf')
        count = 0
        # print('# Successors:',len(list(self.successors(vertical))))
        for a,s in self.successors(vertical):
            (_,new_v,new_count) = s.min_value(not vertical,limit-1,alpha,beta)
            count += new_count
            # print(v,new_v)
            if new_v > v:
                v = new_v
                if v >= beta:
                    return ((),v,count)
                alpha = max(alpha,v)
                action = a
        return (action,v,count)
        # v = max(v,min_value(not vertical,limit-1,alpha,beta))

    def min_value(self,vertical,limit,alpha,beta):
        # print('MIN')
        # print('Limit?',limit,limit == 0)
        # print('Game Over?',self.game_over(vertical))
        # print('Limit or Game Over?',limit == 0 | self.game_over(vertical))
        if limit == 0 or self.game_over(vertical):
            return ((),self.utility(not vertical),1)
        v = float('inf')
        count = 0
        # print('# Successors:',len(list(self.successors(vertical))))
        for a,s in self.successors(vertical):
            (_,new_v,new_count) = s.max_value(not vertical,limit-1,alpha,beta)
            count += new_count
            if new_v < v:
                v = new_v
                if v <= alpha:
                    return ((),v,count)
                beta = min(beta,v)
                action = a
        return (action,v,count)
        # v = min(v,max_value(not vertical,limit-1,alpha,beta))

    def utility(self,vertical):
        return len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical)))

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent about 3 hours on this assignment.
"""

feedback_question_2 = """
The understanding the minimax algorithm and alpha-beta
pruning was the most challengine, but I really feel like
I have a good grasp on it now.
"""

feedback_question_3 = """
I like games, so I like that we got to play a game with an
AI we programmed.  I also find all the GUIs very helpful.
"""
