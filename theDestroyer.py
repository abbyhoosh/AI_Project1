# Abby and Alyssa's dots and boxes player

################# run with command: python3 referee.py theDestroyer theDestroyer --time_limit 10 & python3 theDestroyer.py &

import copy
import os
from pathlib import Path
import time

#_________________________________BOX CLASS AND FUNCTIONS____________________________________________
class Box:
    def __init__(self, boxnum):
        self.boxNumber = boxnum
        self.heldBy = "" #name of owner if all four lines filled
        self.leftline = 0 # 1 if filled
        self.topline = 0
        self.rightline = 0
        self.bottomline = 0
    #returns true if all the sides of the box are filled
    def isFullBox(self):
        if(self.leftline ==1 and self.topline == 1 and self.bottomline ==1 and self.rightline ==1):
            return True
        else:
            return False
    
goPath = Path("theDestroyer.go")
movePath = Path("move_file")
endPath = Path("end_game")
passPath = Path("theDestroyer.pass")
allBoxes = []
########################################################

#finds the box number(s) that a set of coordinates will map to 
def findBoxNumber(one, two, three, four):
    if(one == three): ##if horizontal line
        smallx, smally = getSmallerHorizCoord(one,two,three,four)
        if(one == 0 or one == 9): ##if edge line
            if(one == 0):
                bigBoxnum = 9*smallx + smally
                return -1, bigBoxnum, "h"

            else:
                smallBoxnum = 9*(smallx-1)+smally
                return smallBoxnum, -1, "h"
                
        else:
            bigBoxnum = 9*smallx + smally
            smallBoxnum = 9*(smallx-1)+smally
            return smallBoxnum, bigBoxnum, "h"
    else:
        smallx, smally = getSmallerVertCoord(one,two,three,four)
        if (two == 0 or two == 9):
            if(two==0):
                bigBoxnum = 9*smallx+smally
                return -1, bigBoxnum, "v"
            else:
                smallBoxnum = 9*smallx + (smally-1)
                return smallBoxnum, -1, "v"
        else:
            bigBoxnum = 9*smallx+smally
            smallBoxnum = 9*smallx + (smally-1)
            return smallBoxnum, bigBoxnum, "v"

#takes a box number and the side of the box that the line is on and 
#returns the coordinates of that line in a string
#for boxside:
# t = topline, b = bottomline, r = rightline, l = leftline
def convertBoxToLine(boxnumber, boxside):
    smallx = 0
    smally = 0
    bigx = 0
    bigy = 0
    if(boxside == "r" or boxside == "l"):
        smallx = boxnumber//9
        smally = boxnumber%9
        if(boxside == "r"):
            smally +=1
        bigx = smallx+1
        bigy = smally
    elif(boxside == "b" or boxside == "t"):
        if(boxside == "b"):
            boxnumber+=9
        smallx = boxnumber//9
        smally = boxnumber%9
        bigy = smally+1
        bigx = smallx
    coords = str(smallx) +","+str(smally)+" "+str(bigx)+","+str(bigy)
    return coords

 #checks if board is full
def isFullBoard(board):
    for box in board:
        if not(box.isFullBox()):
            return False
    return True

#__________________________________FINDING COORDINATES TO A MOVE_____________________________________

## cut off other teams name in their move
# returns just the player, and coordinates of the move
def splitMove(fullMove):
    space = fullMove.find(" ")
    onlyMove = fullMove[space+1:]
    justPlayer = fullMove[:space]
    return justPlayer, onlyMove

def individualCoords(move):
    space = move.find(" ")
    first = move[:space]
    second = move[space+1:]
    commaone = first.find(",")
    commatwo = second.find(",")
    one = int(first[0:commaone])
    two = int(first[commaone+1:])
    three = int(second[0:commatwo])
    four = int(second[commatwo+1:])
    return one,two,three,four

## check if valid move
    #move is just the coordinates string
def checkValidMove(coordmove):
    print("checking valid")
    one,two,three,four = individualCoords(coordmove)

    ##checking if outside the board
    if (one<0 or two<0 or three<0 or four<0):
        return False, "Outside of the board"
    if (one>9 or two>9 or three>9 or four>9):
        return False, "Outside of the board"

    ## checking if edges are next to each other
    #checking if more that 1 point away
    if (one != three +1 and one != three -1) and (one != three):
        return False, "edges not next to each other"
    if (two != four +1 and two != four -1) and (four != two):
        return False, "edges not next to each other"
    if (one == three and two == four):
        return False, "not a line, just a point"
    #check if both x and y are one away
    if (one == three+1 or one == three-1)and(two==four-1 or two ==four+1):
        return False, "edges not next to each other"
    
    #checking if move is already on the board
    smallBoxnum, bigBoxnum, horv = findBoxNumber(one,two,three,four)
    if(smallBoxnum != -1):
        if(horv == "h"):
            if(allBoxes[smallBoxnum].bottomline == 1):
                return False, "line already taken"
        else:
            if(allBoxes[smallBoxnum].rightline == 1):
                return False, "line already taken"
    elif(bigBoxnum != -1):
        if(horv == "h"):
            if(allBoxes[bigBoxnum].topline == 1):
                return False, "line already taken"
        else:
            if(allBoxes[bigBoxnum].leftline == 1):
                return False, "line already taken"

    return True, "all good"
    ## return true if valid move, false if not

#gets the smaller coordinate between two coordinates
def getSmallerHorizCoord(one,two,three,four):
    if (two<four):
        return one,two
    else:
        return three,four
#gets the smaller coordinate between two coordinates
def getSmallerVertCoord(one,two,three,four):
    if (one<three):
        return one,two
    else:
        return three,four
    
#_________________________________BOARD GAME UPDATES__________________________________________________

## move is the full move with the name of the player
def updateInternalGame(move):
    player, justmove = splitMove(move)
    one,two,three,four = individualCoords(justmove)
    
    smallBoxnum, bigBoxnum, horv = findBoxNumber(one,two,three,four)

    ##updated who holds the box if now a full box
    # update the lines that are now occupied
    if(bigBoxnum != -1):
        if(horv == "h"):
            allBoxes[bigBoxnum].topline = 1
        elif(horv == "v"):
            allBoxes[bigBoxnum].leftline = 1
        if(allBoxes[bigBoxnum].isFullBox()):
            allBoxes[bigBoxnum].heldBy = player
    if(smallBoxnum != -1):
        if(horv == "h"):
            allBoxes[smallBoxnum].bottomline = 1
        elif(horv == "v"):
            allBoxes[smallBoxnum].rightline = 1
        if(allBoxes[smallBoxnum].isFullBox()):
            allBoxes[smallBoxnum].heldBy = player
    
    ##to be implemented
    ##return true if successfully wrote move to board, false otherwise

## calculate move
def calculateMove():
    copyboard = copy.deepcopy(allBoxes)
    bestScore, bestBoxnum, bestSide = minimax2(0, copyboard, True, -10000, 10000, 2)
    coords = convertBoxToLine(bestBoxnum, bestSide)
    updateInternalGame("theDestroyer "+coords)
    writeToMoveFile(coords)
    ##return move that our player is making

## write to move file
## move is just the string of the coordinates of the move
def writeToMoveFile(move):
    moveFileWrite = open(movePath, "w")
    moveFileWrite.write("theDestroyer " + move)
    moveFileWrite.close()
    time.sleep(0.2)     ## need to account for time for the ref to see the change in file
## wait for change (added files) in directory

#protocol for when pass file is made in directory
def passMove():
    closedBoxFile= open(movePath, "r")
    closedBoxSpot = closedBoxFile.read()
    player, justTheirMove = splitMove(closedBoxSpot)
    isValid, reason = checkValidMove(justTheirMove)
    if(isValid):
        updateInternalGame(closedBoxSpot)
        closedBoxFile.close()
        writePassFile = open(movePath, "w")
        writePassFile.write("theDestroyer 0,0 0,0")
        writePassFile.close()
        time.sleep(0.2)
    else:
        print(player +" lost because of "+reason)
    
#__________________________MINIMAX AND ALPHABETA FUNCTIONS____________________________________________      

## Eval Function for if i go here how many points do i get
def evalFunction(copyBoard):
    aiPoints = 0
    opponent = 0
    for box in copyBoard:
        if(box.heldBy == "theDestroyer"):
            aiPoints+=1
        elif(box.heldBy != "" and box.heldBy != "theDestroyer"):
            opponent+=1
    score = aiPoints-opponent
    return score #return difference in points aipts-opponentpts

## Utility function that determines if ai has more than the other player in points for terminal moves
def utility(board):
    for box in board:
        aiPoints = 0
        if (box.heldBy == "theDestroyer"):
            aiPoints += 1
    opponentPoints = 81 - aiPoints
    score = aiPoints - opponentPoints
    return score 

def updateCopyGame(move, copyboard, num):
    #num is 0 or 1
        #0 if deleting move on copyboard
        #1 is adding move on copyboard
## move is the full move with the name of the player
    player, justmove = splitMove(move)
    one,two,three,four = individualCoords(justmove)
    
    smallBoxnum, bigBoxnum, horv = findBoxNumber(one,two,three,four)

    ##updated who holds the box if now a full box
    # update the lines that are now occupied
    if(bigBoxnum != -1):
        if(horv == "h"):
            copyboard[bigBoxnum].topline = num
        elif(horv == "v"):
            copyboard[bigBoxnum].leftline = num
        if(copyboard[bigBoxnum].isFullBox()):
            copyboard[bigBoxnum].heldBy = player
        else:
            copyboard[bigBoxnum].heldBy = ""
    if(smallBoxnum != -1):
        if(horv == "h"):
            copyboard[smallBoxnum].bottomline = num
        elif(horv == "v"):
            copyboard[smallBoxnum].rightline = num
        if(copyboard[smallBoxnum].isFullBox()):
            copyboard[smallBoxnum].heldBy = player
        else:
            copyboard[smallBoxnum].heldBy = ""
# MINIMAX with Alpha Beta Pruning
# state is a copy of the board
def minimax2(depth, state, isMax, alpha, beta, maxdepth):
    MAX = 10000
    MIN = -10000
    currSide = ""
    bestBox = -1
    bestSide = ""
    best = 0
    if(depth == maxdepth):
        return evalFunction(state), -1, ""
    if(isMax):
        best = MIN
        for box in state:
            if (not box.isFullBox()):
                if(box.leftline == 0):
                    coords = convertBoxToLine(box.boxNumber, "l")
                    fullmove = "theDestroyer "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "l"
                    val, bnum, cside = minimax2(depth+1, state, False, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val>best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = max(best, val)
                    alpha = max(best, alpha)
                    if(beta<=alpha):
                        break
                if(box.topline == 0):
                    coords = convertBoxToLine(box.boxNumber, "t")
                    fullmove = "theDestroyer "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "t"
                    val, bnum, cside = minimax2(depth+1, state, False, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val>best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = max(best, val)
                    alpha = max(best, alpha)
                    if(beta<=alpha):
                        break
                if(box.bottomline == 0):
                    coords = convertBoxToLine(box.boxNumber, "b")
                    fullmove = "theDestroyer "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "b"
                    val, bnum, cside = minimax2(depth+1, state, False, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val>best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = max(best, val)
                    alpha = max(best, alpha)
                    if(beta<=alpha):
                        break
                if(box.rightline == 0):
                    coords = convertBoxToLine(box.boxNumber, "r")
                    fullmove = "theDestroyer "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "r"
                    val, bnum, cside = minimax2(depth+1, state, False, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val>best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = max(best, val)
                    alpha = max(best, alpha)
                    if(beta<=alpha):
                        break
    else:
        best = MAX
        for box in state:
            if (not box.isFullBox()):
                if(box.leftline == 0):
                    coords = convertBoxToLine(box.boxNumber, "l")
                    fullmove = "opp "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "l"
                    val, bnum, cside = minimax2(depth+1, state, True, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val<best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = min(best, val)
                    beta = min(best, beta)
                    if(beta<=alpha):
                        break
                if(box.topline == 0):
                    coords = convertBoxToLine(box.boxNumber, "t")
                    fullmove = "opp "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "t"
                    val, bnum, cside = minimax2(depth+1, state, True, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val<best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = min(best, val)
                    beta = min(best, beta)
                    if(beta<=alpha):
                        break
                if(box.bottomline == 0):
                    coords = convertBoxToLine(box.boxNumber, "b")
                    fullmove = "opp "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "b"
                    val, bnum, cside = minimax2(depth+1, state, True, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val<best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = min(best, val)
                    beta = min(best, beta)
                    if(beta<=alpha):
                        break
                if(box.rightline == 0):
                    coords = convertBoxToLine(box.boxNumber, "r")
                    fullmove = "opp "+coords
                    updateCopyGame(fullmove, state, 1)
                    currSide = "r"
                    val, bnum, cside = minimax2(depth+1, state, True, alpha, beta, maxdepth)
                    updateCopyGame(fullmove, state, 0)
                    if(val<best):
                        bestBox = box.boxNumber
                        bestSide = currSide
                    best = min(best, val)
                    beta = min(best, beta)
                    if(beta<=alpha):
                        break
    return best, bestBox, bestSide


#_________________________________________MAIN IMPLEMENTATION________________________________________

def main():
    print("Starting up theDestroyer...")
    for i in range (0,81):
        allBoxes.append(Box(i))

    while not endPath.exists():
        while not goPath.exists():
            time.sleep(0.1)
            if passPath.exists() and movePath.exists():
                passMove()

        if (movePath.exists() and goPath.exists()):
            moveFile = open(movePath, "r") # can read the move file
            if (os.path.getsize(movePath) == 0): # if move file is empty
                moveFile.close()        # needs to close read only and open write only to overwrite
                calculateMove()
            else:
                theirMove = moveFile.read()
                moveFile.close()
                player, justTheirMove = splitMove(theirMove)
                if(player == "theDestroyer"):
                    time.sleep(0.2)
                else:
                    if(justTheirMove == "0,0 0,0"):
                        calculateMove()
                    else:
                        isValid, reason = checkValidMove(justTheirMove)
                        if(isValid):
                            updateInternalGame(theirMove)
                            calculateMove()
                        else:
                            print(player + " lost the game because "+ reason)
                            break
    print("Game Over")
    score = utility(allBoxes)
    if(score>0):
        print("theDestroyer wins!!")
    elif(score<0):
        print("the opponent wins")
    else:
        print("Tie!")


if __name__ == "__main__":
    main()