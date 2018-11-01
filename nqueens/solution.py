import os

class cell(object):
    def __init__(self):
        self.scooterCount = 0
        self.policePresent = False
        self.valid = 0

def calculateScore(board):
    totalSum = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j].policePresent == True:
                totalSum += board[i][j].scooterCount
    return totalSum


def updateInvalidPositions(board, row, col,pNumber):
    board[row][col].valid =-(pNumber)
    for i in range(len(board)):
        if board[row][i].valid == 0:
            board[row][i].valid = -(pNumber)
        if board[i][col].valid == 0:
            board[i][col].valid = -(pNumber)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if row + col == i + j or row - col == i - j:
                if board[i][j].valid == 0:
                    board[i][j].valid = -(pNumber)

def updateValidPositions(board, row,col,pNumber):
    board[row][col].valid = 0
    for i in range(len(board)):
        if board[row][i].valid == -(pNumber):
            board[row][i].valid = 0
        if board[i][col].valid == -(pNumber):
            board[i][col].valid = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if(row+col ==i+j or row-col == i-j):
                if board[i][j].valid== -(pNumber):
                    board[i][j].valid = 0
#for debugging only
def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print(str(board[i][j].valid)+ "  ")
        print()

def dfs(board, pNumber, row,allScores):
    if pNumber == 0:
        score = calculateScore(board)
        allScores.append(score)
        return score
    else:
        for i in range(row,len(board)):
            for j in range(len(board)):
                if(board[i][j].valid==0):
                    board[i][j].policePresent = True
                    updateInvalidPositions(board, i, j,pNumber)
                    dfs(board, pNumber - 1, i+1, allScores)
                    board[i][j].policePresent=False
                    #print(pNumber)
                    updateValidPositions(board,i,j,pNumber)

path=os.getcwd()
inputFileName=path+"/input.txt"
with open(inputFileName,'r') as ifp:
    n=int(ifp.readline())
    board=[[cell() for i in range(n)]for j in range(n)]
    pNumber=int(ifp.readline())
    sNumber=int(ifp.readline())
    count=12*sNumber
    maxScore = -1
    while(count):
        x,y=map(int,ifp.readline().rstrip().split(','))
        board[x][y].scooterCount+=1
        if board[x][y].scooterCount > maxScore:
            maxScore = board[x][y].scooterCount
        count-=1
    ifp.close()
    outputFilePath = os.getcwd() + "/output.txt"
    ofp = open(outputFilePath, 'w')
    if(pNumber==1):
        ofp.write(str(maxScore))
    elif pNumber == 0:
        ofp.write("0")
    else:
        allScores=[]
        score = dfs(board, pNumber, 0, allScores)
        ofp.write(str(max(allScores)))
