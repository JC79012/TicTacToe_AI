import turtle
import math
import random
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt

# epsilon = 0.7
# learning_rate = 0.7
# discount = 0.9
class QTable():
    def __init__(self,player):
        self.player = player
        self.qTable = {}
        self.EPSILON = 0.8
        self.GAMMA = 0.9
        self.ALPHA = 0.7
        self.Trackboard = [' ' for x in range(9)]
        ### changed this to track the last move made instead of all  prev moves
        self.movesMade = None 

    def availableActions(self,board):
        #  return self._board[pos] == ' '
         return [i for i in range(9) if board[i] == ' ']

    def GetqValues(self,state,action):
        #if there is no value, initialize the q value to 0 
        if self.qTable.get((state,action)) is None:
            self.qTable[(state,action)] = 0.0
        return self.qTable[(state,action)]

    def move(self, board):
        self.Trackboard = tuple(board)
        moves = self.availableActions(board)

        if random.random() < self.EPSILON:
            self.movesMade = random.choice(moves)
            return self.movesMade
        
        QVals = [self.GetqValues(self.Trackboard, x) for x in moves]
        maxQ = max(QVals)
        
        if QVals.count(maxQ) > 1:
            maxActions = [i for i in range(len(moves)) if QVals[i] == maxQ]
            bestMove = moves[random.choice(maxActions)]
        
        else:
            bestMove = moves[QVals.index(maxQ)]

        self.movesMade = bestMove
        return self.movesMade

    def updateQ(self, reward, board):
        if self.movesMade:
            ## gets the q value of the last move made
            prevQ = self.GetqValues(self.Trackboard, self.movesMade)

            allQ =[self.GetqValues(tuple(board), i) for i in self.availableActions(self.Trackboard)]
            maxQ = max(allQ)
            self.qTable[(self.Trackboard, self.movesMade)] += prevQ + self.ALPHA *((reward + self.GAMMA * maxQ)-prevQ)
    
    def printBoard(self, board):
        print('   |   |')
        print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
        print('   |   |')
    def Exploitmove(self, board):
        self.Trackboard = tuple(board)
        moves = self.availableActions(board)
        
        QVals = [self.GetqValues(self.Trackboard, a) for a in moves]
        maxQ = max(QVals)
        
        if QVals.count(maxQ) > 1:
            bestActions = [i for i in range(len(moves)) if QVals[i] == maxQ]
            bestMove = moves[random.choice(bestActions)]

        else:
            bestMove = moves[QVals.index(maxQ)]

        self.movesMade = bestMove
        return self.movesMade

class TicTacToe():
    def __init__(self,player1, player2):
        # self._board = board
        self.player1 = player1 
        self.player2 = player2 
        self._board = [' ' for x in range(9)]
        self.isX = random.choice([True,False])
    #     self.reset()
        
    # def reset(self):
    #     self._board = [' ' for x in range(9)]
    
    def insertLetter(self, letter, pos):
        self._board[pos] = letter

    def spaceIsFree(self, pos):
        return self._board[pos] == ' '
         
    def isWinner(self, players):
        for le in players:
            win =  (self._board[6] == le and self._board[7] == le and self._board[8] == le) or (self._board[3] == le and self._board[4] == le and self._board[5] == le) or(self._board[0] == le and self._board[1] == le and self._board[2] == le) or(self._board[0] == le and self._board[3] == le and self._board[6] == le) or(self._board[1] == le and self._board[4] == le and self._board[7] == le) or(self._board[2] == le and self._board[5] == le and self._board[8] == le) or(self._board[0] == le and self._board[4] == le and self._board[8] == le) or(self._board[2] == le and self._board[4] == le and self._board[6] == le)
            if win:
                return win, le
        if self.isBoardFull():
            return (True, None)
        else:
            return (False,None)

    # # def valid_actions(self):
    #     # actions = [0,1,2,3,4,5,6,7,8]

    #     # for i in actions:
    #     #     if not self.spaceIsFree(i):
    #     #         actions.remove(i)
    #     # return actions

    def isBoardFull(self):
        if self._board.count(' ') > 1:
            return False
        else:
            return True
    # def choose_move(self) :
    #     actions = self.valid_actions()
    #     choice = random.choice(actions)
    #     return choice

#### serves to train the AI without printing the board just the winner 
    def Train_Ai(self):
        # self.reset()
        winner = False

        while not winner:
            if self.isX: #the first player is X
                first_player = self.player1
                second_player = self.player2
                chars = ('X','O')

            else: # the first player isnt X
                first_player = self.player2
                second_player = self.player1
                chars = ('O','X')
                
            for i in chars:
                winner, winning_letter = self.isWinner(i)

                if winner:
                    if winning_letter == chars[0]:
                        print(chars[0], ' Won')
                        first_player.updateQ(10,self._board[:])
                        second_player.updateQ(-10,self._board[:])
                        return winning_letter

                    if winning_letter == chars[1]:
                        print(chars[1], ' Won')
                        second_player.updateQ(10,self._board[:])
                        first_player.updateQ(-10,self._board[:])
                        return winning_letter
                        
                    else:
                        print('Tie')
                        first_player.updateQ(5,self._board[:])
                        second_player.updateQ(5,self._board[:])
                        winning_letter = 'T'
                        return winning_letter
                    break
                else:
                    first_player.updateQ(-1,self._board[:])

            self.isX = not self.isX

            move = first_player.move(self._board)

            if not self.spaceIsFree(move):
                first_player.updateQ(-50,self._board[:])
                break
            
            self.insertLetter(chars[0],move)

#Works just like the TrainAI function except it prints the board 
    def final_game(self):
        winner = False

        while not winner:
            if self.isX: #the first player is X
                first_player = self.player1
                second_player = self.player2
                chars = ('X','O')

            else: # the first player isnt X
                first_player = self.player2
                second_player = self.player1
                chars = ('O','X')
                
            for i in chars:
                winner, winning_letter = self.isWinner(i)

                if winner:
                    if winning_letter == chars[0]:
                        first_player.printBoard(self._board[:])
                        print(chars[0], ' Won!')
                        first_player.updateQ(10,self._board[:])
                        second_player.updateQ(-10,self._board[:])
                        return winning_letter

                    if winning_letter == chars[1]:
                        first_player.printBoard(self._board[:])
                        print(chars[1], ' Won!')
                        second_player.updateQ(10,self._board[:])
                        first_player.updateQ(-10,self._board[:])
                        return winning_letter
                        
                    else:
                        first_player.printBoard(self._board[:])
                        print('Tie')
                        first_player.updateQ(5,self._board[:])
                        second_player.updateQ(5,self._board[:])
                        winning_letter = 'T'
                        return winning_letter
                    break
                else:
                    first_player.updateQ(-1,self._board[:])

            self.isX = not self.isX

            move = first_player.Exploitmove(self._board)

            if not self.spaceIsFree(move):
                first_player.updateQ(-50,self._board[:])
                break
            
            self.insertLetter(chars[0],move)


                
def main():
    Epoch = 20000
    x_won = 0 
    o_won = 0 
    tie = 0
    
    player1 = QTable('player1')
    player2 = QTable('player2')
    print('Begin training cycles')
 

    for i in range(Epoch):
        train = TicTacToe(player1,player2)
        print('Training Cycle: ',i, "/", Epoch)
        letter = train.Train_Ai()
        if letter == 'X':
            x_won += 1
        if letter == 'O':
            o_won += 1
        if letter == 'T':
            tie += 1
    x = 0
    o = 0
    t = 0 
    exploit_games = 100
    print("Training ended")
    for y in range(exploit_games):
        final_show = TicTacToe(player1,player2)
        le = final_show.final_game()
        if le == 'X':
            x += 1
        if le == 'O':
            o += 1
        if le == 'T':
            t += 1
    print("Training Stats: ")
    print('X won: ',x_won, ' O won: ', o_won,' Tie: ',tie)
    print('X won:',(x_won/Epoch)*100,'%', ' O won:', (o_won/Epoch)*100,'%',' Tie:',(tie/Epoch)*100,'%')

    print('\n')
    print("After Training:")
    print('X won: ',x, ' O won: ', o,' Tie: ',t)
    print('X won:',(x/exploit_games)*100,'%', ' O won:', (o/exploit_games)*100,'%',' Tie:',(t/exploit_games)*100,'%')
main()



#####
# win = self._board[6] == le and self._board[7] == le and self._board[8] == le 
#             if win:
#                 return win, le

# win = self._board[6] == le and self._board[7] == le and self._board[8] == le 
# if win:
#   return win, le
# win = self._board[3] == le and self._board[4] == le and self._board[5] == le
# if win:
#   return win, le
# win = self._board[0] == le and self._board[1] == le and self._board[2] == le
# win = self._board[0] == le and self._board[3] == le and self._board[6] == le
# win = self._board[1] == le and self._board[4] == le and self._board[7] == le 
# win = self._board[2] == le and self._board[5] == le and self._board[8] == le 
# win = self._board[0] == le and self._board[4] == le and self._board[8] == le 
# win = self._board[2] == le and self._board[4] == le and self._board[6] == le

# def calcQ(self,move):
    #     reward = self.move(move)

    #     if self.isX:
    #         old_state = self.getQ1(move)
    #         self.q1[move] += learning_rate * ((reward + discount) - old_state)
    #     else:
    #         old_state = self.getQ2(move)
    #         self.q2[move] +=  learning_rate * ((reward + discount) - old_state)
