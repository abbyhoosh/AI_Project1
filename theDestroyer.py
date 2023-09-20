# Abby and Alyssa's dots and boxes player

################# run with command: python3 referee.py theDestroyer theDestroyer --time_limit 10 & python3 theDestroyer.py &

import copy
import os
from pathlib import Path
import time
import numpy as np
import math

class Box:
    def __init__(self, boxnum):
        self.boxNumber = boxnum
        self.heldBy = "" #name of owner if all four lines filled
        self.leftline = 0 # 1 if filled
        self.topline = 0
        self.rightline = 0
        self.bottomline = 0
        self.filledCount = 0 #should be the same number as returned by countFilledSides
    #returns true if all the sides of the box are filled
    def isFullBox(self):
        if(self.leftline ==1 and self.topline == 1 and self.bottomline ==1 and self.rightline ==1):
            return True
        else:
            return False
    # returns the number of sides that contain a line/are filled
    def countFilledSides(self):
        count = 0
        if(self.leftline ==1):
            count +=1
        if(self.rightline == 1):
            count +=1
        if(self.bottomline ==1):
            count +=1
        if(self.topline ==1):
            count+=1
        return count
goPath = Path("theDestroyer.go")
movePath = Path("move_file")
endPath = Path("end_game")
passPath = Path("theDestroyer.pass")
gameBoard = np.full((9,9), 0)
allBoxes = []
threeLineBoxes = []
#make an array for boxes that have 3 lines filled
#maybe just order the array based of of that factor?? 3 first then 1 then 0 then 2?
#i'm thinking 3 separate arrays might be easier for sorting purposes
########################################################

def addToBoxArr(boxnum):
    count = allBoxes[boxnum].countFilledSides()
    if(count == 3):
        threeLineBoxes.append(allBoxes[boxnum])
        print("three line boxes:")
        for box in threeLineBoxes:
            print(box.boxNumber)
        print("end")
    elif(count == 4):
        idx = 0
        for box in threeLineBoxes:
            if box.boxNumber == boxnum:
                break
            idx +=1
        threeLineBoxes.pop(idx)
        print("fullbox")


 #checks if board is full
def isFullBoard(board):
    for box in board:
        if not(box.isFullBox()):
            return False
    return True
#copyBoard is a copy of the board to go through testing a new move
#if i go here how many points do i get
def evalFunction(copyBoard):
    #count points for us if we hold a box
    aiPoints = 0
    opponent = 0
    for box in allBoxes:
        if(box.heldBy == "theDestroyer"):
            aiPoints+=1
        elif(box.heldBy != ""):
            opponent+=1
    score = aiPoints-opponent
    #count points for them if they hold a box
    return score
    #return difference in points aipts-opponentpts

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
    one = int(first[:commaone])
    two = int(first[commaone+1:])
    three = int(second[:commatwo])
    four = int(second[commatwo+1:])
    return one,two,three,four

## check if valid move
    #move is just the coordinates string
def checkValidMove(coordmove):
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

## write moves to our game board
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
            allBoxes[bigBoxnum].filledCount +=1
        elif(horv == "v"):
            allBoxes[bigBoxnum].leftline = 1
            allBoxes[bigBoxnum].filledCount +=1
        if(allBoxes[bigBoxnum].isFullBox()):
            allBoxes[bigBoxnum].heldBy = player
        addToBoxArr(bigBoxnum)
    if(smallBoxnum != -1):
        if(horv == "h"):
            allBoxes[smallBoxnum].bottomline = 1
            allBoxes[smallBoxnum].filledCount +=1
        elif(horv == "v"):
            allBoxes[smallBoxnum].rightline = 1
            allBoxes[smallBoxnum].filledCount +=1
        if(allBoxes[smallBoxnum].isFullBox()):
            allBoxes[smallBoxnum].heldBy = player
        addToBoxArr(smallBoxnum)
    

    ##to be implemented
    ##return true if successfully wrote move to board, false otherwise

## calculates move for when we are first
def calculateFirstMove():
    moveFileWrite = open(movePath, "w")
    moveFileWrite.write("theDestroyer 1,3 2,3")
    moveFileWrite.close()
    time.sleep(0.8)

## calculate move
def calculateMove():
    copyboard = copy.deepcopy(allBoxes)
    bestScore, bestBoxnum, bestSide = minimax2(4, copyboard, True, -10000, 10000, 7)
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
        writePassFile.write("theDestoyer 0,0 0,0")
        writePassFile.close()
        time.sleep(0.1)
    else:
        print(player +" lost because of "+reason)
    

# minimax algorithim implementation
# state is the current state of the board being looked into
# isMax says whether this is a max or min layer
# 4 layers to start
def minimax(state, depth, isMax):
    print("uphere")
    #makes a copy of the current board state to manipulate
    copyOfBoard = allBoxes.copy()

    if (isMax):
        bestMove = (-10000, None)
    else:
        bestMove = (10000, None)

    if (depth==0): # add check that all moves are taken somewhere
        print("depth = 0 true")
        return evalFunction(state) # this will return the possible score of this route
    if (isFullBoard(state)):
        print("isfullboardtrue")
        return utility(state) #returns what the final score would be
    print("in here")
    
    #goes through and checks if the box is full, if not it finds the first available side to start on
    for box in copyOfBoard:
        # checks if box if sull (bc then we don't need to check it)
        if (not box.isFullBox()):
            #checks each side of box to see if full and gos down first come first serve type beat
            if (box.leftline == 0):
                #if it's empty make it full
                box.leftline = 1 
                #recursivley call function with new cope of the game board to keep going down
                # when evalFunction is returned it decides is that is better than the current best move
                # replaces it with either new move or samve move and continues
                bestMove = compare(minimax(copyOfBoard, depth-1, not isMax), bestMove, isMax)
            elif (box.topline == 0):
                box.topline = 1
                bestMove = compare(minimax(copyOfBoard, depth-1, not isMax), bestMove, isMax)
            elif (box.rightline == 0):
                box.rightline = 1
                bestMove = compare(minimax(copyOfBoard, depth-1, not isMax), bestMove, isMax)
            elif (box.bottomline == 0):
                box.bottomline = 1
                bestMove = compare(minimax(copyOfBoard, depth-1, not isMax), bestMove, isMax)
    
    # Question--> we only need the number for most of this but need to return coordinates
    # for the last one is there a way to get coordinates from the boxes so just bestMove can be returned
    # with the move? idk if that makes sense.
    print("Bestmove:")
    print(bestMove[0])
    return bestMove[0]

# based on what kayer compares best move accordingly
def compare(score, bestMove, isMax):
    if (isMax):
        if (score > bestMove[0]):
            bestMove[0] = score
            return bestMove
            # add thing to account for coordinates of move
    else:
        if( score < bestMove[0]):
            bestMove[0] = score
            return bestMove


## utility function that determines if ai has more than the other player in points for temrinal moves
def utility(board):
    for box in board:
        aiPoints = 0
        if (box.heldBy == "theDestroyer"):
            aiPoints += 1
    opponentPoints = 81 - aiPoints
    score = aiPoints - opponentPoints
    return score 


#state is a copy of the board
def minimax2(depth, state, isMax, alpha, beta, maxdepth):
    MAX = 10000
    MIN = -10000
    currSide = ""
    bestBox = -1
    bestSide = ""
    if(depth == maxdepth):
        return evalFunction(state), -1, ""
    if(isMax):
        best = MIN
        for box in state:
            if (not box.isFullBox()):
                if(box.leftline == 0):
                    box.leftline = 1
                    currSide = "l"
                elif(box.topline == 0):
                    box.topline = 1
                    currSide = "t"
                elif(box.bottomline == 0):
                    box.bottomline = 1
                    currSide = "b"
                else:
                    box.rightline = 1
                    currSide = "r"
                val, bnum, cside = minimax2(depth+1, state, False, alpha, beta, maxdepth)
                #print(best, val, box.boxNumber)
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
                    box.leftline = 1
                    currSide = "l"
                elif(box.topline == 0):
                    box.topline = 1
                    currSide = "t"
                elif(box.bottomline == 0):
                    box.bottomline = 1
                    currSide = "b"
                else:
                    box.rightline = 1
                    currSide = "r"
                val, bnum, cside = minimax2(depth+1, state, True, alpha, beta, maxdepth)
                #print(best, val, box.boxNumber)
                if(val<best):
                    bestBox = box.boxNumber
                    bestSide = currSide
                best = min(best, val)
                bestBox = box.boxNumber
                beta = min(best, beta)
                if(beta<=alpha):
                    break
    return best, bestBox, bestSide

#takes a box number and the side of the box that the line is on and 
#returns the coordinates of that line in a string
#for boxside:
# t = topline, b = bottomline, r = rightline, l = leftline
def convertBoxToLine(boxnumber, boxside):
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


def main():
    print("Starting up theDestroyer...")
    for i in range (0,81):
        allBoxes.append(Box(i))

    print(convertBoxToLine(80, "t"))
    print(convertBoxToLine(80, "b"))
    print(convertBoxToLine(80, "r"))
    print(convertBoxToLine(80, "l"))

    while not endPath.exists():
        while not goPath.exists():
            time.sleep(0.1)
            if passPath.exists():
                passMove()

        if passPath.exists() and movePath.exists():
            passMove()
        elif (movePath.exists() and goPath.exists()):
            moveFile = open(movePath, "r") ##can read the move file
            if (os.path.getsize(movePath) == 0): ## if move file is empty
                moveFile.close()        ##needs to close read only and open write only to overwrite
                ourMove = calculateFirstMove()
            else:
                theirMove = moveFile.read()
                moveFile.close()
                player, justTheirMove = splitMove(theirMove)
                if(player == "theDestroyer"):
                    time.sleep(0.1)
                    print(player)
                    print("sleeping...")
                else:
                    print(player)
                    print(justTheirMove)
                    print("their move")
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


if __name__ == "__main__":
    main()