#minimum remaining value = Choose the variable with the fewest 
#legal values left

#degree heuristic = Choose the variable with the most constraints on remaining
#(unassigned) variables, or has the most number of unassigned
#neighbors.

#forward checking =  After a variable is assigned a value, 
#update the remaining legal values of its neighbors 
#(a neighbor is another variable that shares one or more 
#constraintswith the current variable.)

import copy

class HyperSudoku:
    def __init__(self):
        #change the name to the file u wanna input, and output
        self.fileName = "Input3.txt"
        self.outputName = "Output3.txt"
        self.board = self.read()

    def read(self): #read the file line by line and return a board
        board = []
        f = open(self.fileName,"r")
        lines = f.readlines()
        for line in lines:
            if line.strip().split():    
                board.append(line.strip().split())
        f.close()
        return board

    def assignDomains(self): #list all the possible domains in the form of a list
        new_board = copy.deepcopy(self.board)
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if self.board[i][k] == '0': #values are str format
                    new_board[i][k] = ["1","2","3","4","5","6","7","8","9"]
        return new_board #every unassigned value is in a form of a list

    def inBounds(self,x,y):
        if 0 <= x < len(self.board[0]) and 0 <= y < len(self.board):
            return True
        return False

    #below is all the forward checking being done (row,column,whitebox,greenbox)
    def updateColumn(self,curValue,x):
        for i in range(len(self.board)): #updating the column
            if type(self.board[i][x]) == list:
                if curValue in self.board[i][x] :
                    self.board[i][x].remove(curValue)
    
    def updateRow(self,curValue,y):
        for i in range(len(self.board[0])): #updating the row
            if type(self.board[y][i]) == list:
                if curValue in self.board[y][i]:
                    self.board[y][i].remove(curValue)
    
    def updateWhiteBox(self,curValue,x,y):
        boxX = x - x%3 
        boxY = y - y%3
        for y in range(boxY, boxY+3):
            for x in range(boxX, boxX+3):
                if type(self.board[y][x]) == list:
                    if curValue in self.board[y][x]:
                        self.board[y][x].remove(curValue)
    
    def updateGreenBox(self,curValue,x,y): #update greenbox
        if((0 < y < 4) and (0 < x < 4)): #upper left greenbox
            for i in range(1, 4): #y 
                for k in range(1, 4): #x
                    if type(self.board[i][k]) == list:
                        if curValue in self.board[i][k]:
                            self.board[i][k].remove(curValue)
        elif((4 < y < 8) and (0 < x < 4)): #bottom left greenbox
            for i in range(5, 8): #y
                for k in range(1, 4): #x
                    if type(self.board[i][k]) == list:
                        if curValue in self.board[i][k]:
                            self.board[i][k].remove(curValue)
        elif((0 < y < 4) and (4 < x < 8)): #upper rihgt greenbox
            for i in range(1, 4): #y
                for k in range(5, 8): #x
                    if type(self.board[i][k]) == list:
                        if curValue in self.board[i][k]:
                            self.board[i][k].remove(curValue)
        elif((4 < y < 8) and (4 < x < 8)): #bottom right grenbox
            for i in range(5, 8): #y
                for k in range(5, 8): #x
                    if type(self.board[i][k]) == list:
                        if curValue in self.board[i][k]:
                            self.board[i][k].remove(curValue)

    def updateDomain(self,x,y): #updates all the values on the board based on constraints
        curValue = self.board[y][x]
        self.updateColumn(curValue,x)
        self.updateRow(curValue,y)
        self.updateWhiteBox(curValue,x,y)
        self.updateGreenBox(curValue,x,y)

    def reduceDomains(self): #basically only called once in the beginning, initial forward check
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if type(self.board[y][x]) != list: #find existing value and change domains of neighbors
                    self.updateDomain(x,y)

    def minimumRemaining(self): #returns the length of the shortest list
        _min = 10
        res = []

        #find length of shortest list
        for i in range(len(self.board)):
            for k in range(len(self.board)):
                if type(self.board[i][k]) == list:
                    if len(self.board[i][k]) < _min:
                        _min = len(self.board[i][k])

        #find shortest lists based on length found above      
        for i in range(len(self.board)):
            for k in range(len(self.board)):
                if type(self.board[i][k]) == list:
                    if len(self.board[i][k]) == _min:
                        res.append([(k,i),self.board[i][k]]) #[(x,y), possible domains]
        return res  

    def degreeHeuristic(self,lst): #most # of unassigned neighbors 
        maximumNeighbors = 0
        selected = []
        moves = [(0,1),(0,-1),(1,0),(-1,0)] #up, down, left, and right
        for i in range(len(lst)):
            coords = lst[i][0] #format is [(x,y), possible domains]
            numNeighbors = 0
            for move in moves: #(0,1), etc..
                x,y = coords[0] + move[0], coords[1] + move[1]
                if self.inBounds(x,y): #checking if inbounds
                    if type(self.board[y][x]) == list:
                        numNeighbors += 1
            
            if numNeighbors >= maximumNeighbors:
                maximumNeighbors = numNeighbors
                selected = lst[i]
        return selected

    def selectUnassignedVariable(self):
        #minimum remaining value = Choose the variable with the fewest 
        #legal values left

        #degree heuristic = Choose the variable with the most constraints on remaining
        #(unassigned) variables, or has the most number of unassigned
        #neighbors.
        lst = self.minimumRemaining()
        selected = self.degreeHeuristic(lst)
        return selected

    def checkFinish(self):
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if type(self.board[i][k]) == list:
                    return False
        return True

    def display(self):
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if type(self.board[i][k]) == list:
                    print('0', end = ' ')
                else:
                    print(self.board[i][k], end = ' ')
            print('')
    
    def output(self):
        f = open(self.outputName,"w")
        for i in range(len(self.board)): #y
            for k in range(len(self.board)): #x
                f.write(self.board[i][k])
                f.write(" ")
            f.write("\n")
        f.close()

    def backtrack(self):
        selected = self.selectUnassignedVariable()
        if not selected:
            return True
        x,y = selected[0][0], selected[0][1]
        possible = selected[1]
        temp = copy.deepcopy(self.board)

        if self.checkFinish():
            return True
        for num in possible:
            self.board[y][x] = num #assign
            self.updateDomain(x,y)
            if self.backtrack():
                return True
            self.board = temp #if backtrack doesn't work, reset
        return False

    def main(self):
        self.board = self.assignDomains() 
        self.reduceDomains()
        self.backtrack()
        self.display()
        self.output()

if __name__ == '__main__':
    test = HyperSudoku()
    test.main()
