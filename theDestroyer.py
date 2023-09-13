# Abby and Alyssa's dots and boxes player
import os
from pathlib import Path
import time

goPath = Path("theDestroyer.go")
movePath = Path("move_file")

## look for .go files in directory

### if .go then our turn
### if .pass then skip our turn - 
    ## read other players move
    ## write in move file fake move: theDestroyer 0,0 0,0
### if end_game file created - it is the end of the game


## read move_file (if empty then first player)

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

## calculate move
def calculateMove():
    calculate = 1
    ##to be implemented
    ##return move that our player is making

## write to move file

## wait for change (added files) in directory

def main():
    print("here")
    while not goPath.exists():
        time.sleep(0.1)

    if movePath.exists():
        moveFile = open(movePath, "r+") ##can read and write to the move file
        if (os.movePath.getsize() == 0):
            ### first player
            ##for testing purposes below line
            moveFile.write("theDestroyer 1,3 2,3")
            ourMove = calculateMove()
        else:
            theirMove = moveFile.read()
            isValid = checkValidMove(theirMove)



if __name__ == "__main__":
    main()