# Abby and Alyssa's dots and boxes player

################# run with command: python3 referee.py theDestroyer theDestroyer --time_limit 10 & python3 theDestroyer.py &

import os
from pathlib import Path
import time
import numpy as np

goPath = Path("theDestroyer.go")
movePath = Path("move_file")
endPath = Path("end_game")
passPath = Path("theDestroyer.pass")
gameBoard = np.full((10,10), 0)

## look for .go files in directory

### if .go then our turn
### if .pass then skip our turn - 
    ## read other players move
    ## write in move file fake move: theDestroyer 0,0 0,0
### if end_game file created - it is the end of the game


## read move_file (if empty then first player)

## cut off other teams name in their move
#     returns just the coordinates of the move
def justMove(fullMove):
    space = fullMove.find(" ")
    onlyMove = fullMove[space+1:]
    return onlyMove

## check if valid move
    #move is just the coordinates string
def checkValidMove(move):
    ##to be implemented
    space = move.find(" ")
    first = move[:space]
    second = move[space+1:]
    commaone = first.find(",")
    commatwo = second.find(",")
    one = int(first[:commaone])
    two = int(first[commaone+1:])
    three = int(second[:commatwo])
    four = int(second[commatwo+1:])

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
    ###################
    #still need to check whether move has already been made on the board

    return True, "all good"
    
    ## return true if valid move, false if not

## write moves to our game board
def internalGame(move):
    move
    ##to be implemented
    ##return true if successfully wrote move to board, false otherwise

## calculates move for when we are first
def calculateFirstMove():
    moveFileWrite = open(movePath, "w")
    moveFileWrite.write("theDestroyer 1,3 2,3")
    moveFileWrite.close()
    time.sleep(0.1)

## calculate move
def calculateMove():
    calculate = 1
    moveFileWrite = open(movePath, "w")         #will delete these later
    moveFileWrite.write("theDestroyer 2,2 2,1")
    moveFileWrite.close()
    time.sleep(0.1)
    ##to be implemented
    ##return move that our player is making

## write to move file
## move is just the string of the coordinates of the move
def writeToMoveFile(move):
    moveFileWrite = open(movePath, "w")
    moveFileWrite.write("theDestroyer " + move)
    moveFileWrite.close()
    time.sleep(0.1)     ## need to account for time for the ref to see the change in file
## wait for change (added files) in directory

def passMove():
    closedBoxFile= open(movePath, "r")
    closedBoxSpot = closedBoxFile.read()
    internalGame(closedBoxSpot)
    closedBoxFile.close()
    writePassFile = open(movePath, "w")
    writePassFile.write("theDestoyer 0,0 0,0")
    writePassFile.close()
    time.sleep(0.1)

def main():
    print("here")
    check = checkValidMove("1,2 3,4") #false        
    print(check)
    print(checkValidMove("-1,1 2,1"))   #false
    print(checkValidMove("0,1 2,1")) #false
    print(checkValidMove("8,8 8,9")) #true
    print(checkValidMove("8,10 8,9")) #false
    print(checkValidMove("6,8 8,9")) #false 
    print(checkValidMove("1,1 2,2")) #false

    while not endPath.exists():
        while not goPath.exists():
            time.sleep(0.1)
            if passPath.exists():
                passMove()


        if movePath.exists() and goPath.exists():
            moveFile = open(movePath, "r") ##can read the move file
            if (os.path.getsize(movePath) == 0): ## if move file is empty
                moveFile.close()        ##needs to close read only and open write only to overwrite
                ourMove = calculateFirstMove()
            else:
                theirMove = moveFile.read()
                moveFile.close()
                justTheirMove = justMove(theirMove)
                print(justTheirMove)
                isValid = checkValidMove(justTheirMove)
                calculateMove()


if __name__ == "__main__":
    main()