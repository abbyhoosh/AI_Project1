# Abby and Alyssa's dots and boxes player
import os
from pathlib import Path
import time

goPath = Path("theDestroyer.go")

## look for .go files in directory

### if .go then our turn
### if .pass then skip our turn - 
    ## read other players move
    ## write in move file fake move: theDestroyer 0,0 0,0
### if end_game file created - it is the end of the game


## read move_file (if empty then first player)

## calculate move

## write to move file

## wait for change (added files) in directory

def main():
    ##im just trying to test and see if this might work
    print("here")
    time.sleep(4)
    print("done sleeping")
    if goPath.exists():
        print("found the file!!!!")


if __name__ == '__main__':
    main()