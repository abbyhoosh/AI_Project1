# Abby and Alyssa's dots and boxes player

################# run with command: python3 referee.py theDestroyer theDestroyer --time_limit 10 & python3 theDestroyer.py &

import os
from pathlib import Path
import time

goPath = Path("theDestroyer.go")
movePath = Path("move_file")
endPath = Path("end_game")

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
def checkValidMove(move):
    ##to be implemented
    move
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

## calculate move
def calculateMove():
    calculate = 1
    moveFileWrite = open(movePath, "w")         #will delete these later
    moveFileWrite.write("theDestroyer 2,2 2,1")
    moveFileWrite.close()
    ##to be implemented
    ##return move that our player is making

## write to move file
## move is just the string of the coordinates of the move
def writeToMoveFile(move):
    moveFileWrite = open(movePath, "w")
    moveFileWrite.write("theDestroyer " + move)
    moveFileWrite.close()
## wait for change (added files) in directory

def main():
    print("here")
    while not endPath.exists():
        while not goPath.exists():
            time.sleep(0.1)

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