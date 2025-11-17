import math
import numpy as np
import os
import random 
import sys
import re
import copy as cp
from Track import Track

def fileImport(fileName): # brings file into program as str numpy array
    inputText = ''
    with open(fileName, "r") as f:
        inputText = f.read()
    print(inputText)
    textRows = inputText.split('\n')
    dimTxt = textRows[0].split(',')

    numRows = int(dimTxt[0])
    numCols = int(dimTxt[1])

    inputTextArray = np.zeros((numRows, numCols), dtype = str)

    for row in range(numRows):
        # currentRow = textRows[row + 1].split()
        for col in range(numCols):
            inputTextArray[row][col] = textRows[row + 1][col]
            
    # print(inputTextArray)
    
    return inputTextArray

def createTrack(inputTextArray, CRASH_POS):
    rows = inputTextArray.shape[0]
    cols = inputTextArray.shape[1]

    trackIntegers = np.zeros((rows, cols), dtype = int)

    # 1 is 'S' aka Start, 2 is 'F' aka Finish, 0 is '.' aka track, 3 is '#', or wall. 
    for row in range(rows):
        for col in range(cols):
            character = inputTextArray[row][col]
            if (character == 'S'):
                trackIntegers[row][col] = 1
            if (character == 'F'):
                trackIntegers[row][col] = 2
            if (character == '#'):
                trackIntegers[row][col] = 3

    crashReset = False

    if (CRASH_POS == 'STRT'):
        crashReset = True
    elif (CRASH_POS != 'NRST'):
        print("CRASH_POS invalid, defaulting to NRST setting (nearest non-crash position)")
        
    track = Track(trackIntegers , crashReset, inputTextArray)
    
    return track

def saveOutput(GROUP_ID, ALGORITHM, TRACK_NAME, CRASH_POS, track): 
    # saves solved network reported variables to output file
    # Formatted name as: [GROUP_ID]_[ALGORITHM]_[TRACK_NAME]_[CRASH_POS].txt
    trackPathArr = TRACK_NAME.split('/')
    trackName = trackPathArr[-1]
    fileName = GROUP_ID + "_" + ALGORITHM + "_" + trackName[:-4] + "_" + CRASH_POS + ".txt"
    writeArray = track.getInputTextArray()
    path = track.getBestPath()
    writeString = ''

    for pos in path:
        writeArray[pos[0]][pos[1]] = 'P'

    for row in writeArray:
        for col in row:
            writeString += col
        writeString += '\n'
    
    with open(fileName, "w") as f:
        f.write(writeString)
        
    print("Best Path Taken: ")
    print(writeString)
    
    return

def main(GROUP_ID, ALGORITHM, TRACK_NAME, CRASH_POS): 

    inputTextArray = fileImport(TRACK_NAME)
    track = createTrack(inputTextArray, CRASH_POS)
    
    if (ALGORITHM == 'ValItr'):
        # code to run variable elimination
        # will be method on Network class
        print("run Value Iteration")
        track.doValueIteration()
        
    elif (ALGORITHM == 'QLrng'):
        # code to run gibbs sampling
        # will be method on Network class
        print("run Q-Learning")
        track.doQLearning()

    elif (ALGORITHM == 'SARSA'):
        # code to run gibbs sampling
        # will be method on Network class
        print("run State-Action-Reward-State-Action")
        track.doSARSA()
        
    else:
        print("Not a valid algorithm. Terminating...")
        sys.exit() # exit program

    print("Moves of Best Run: " + str(track.getBestMoves()))

    saveOutput(GROUP_ID, ALGORITHM, TRACK_NAME, CRASH_POS, track)
    