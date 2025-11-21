import math
import numpy as np
import os
import random 
import sys
import re
import copy as cp

class Track:
    # ---------------- INSTANTIATION ------------------
    def __init__(self, track, crashReset, inputTextArray):
        self.track = track # numpy array representing raw track grid
        self.trackShape = track.shape
        # 1 is 'S' aka Start, 2 is 'F' aka Finish, 0 is '.' aka track, 3 is '#', or wall. 
        self.crashReset = crashReset # Boolean, True or False. True if crash means restart, false if crash means start from previous position
        # (with no velocity)
        self.velocity = np.zeros(2, dtype = int) # representing velocity in x and y directions, respectively. 
        # positive x is left-to-right, positive y is up-to-down (think reading directions).
        # both values must be between -5 and 5 (inclusive)
        self.position = np.zeros(2, dtype = int) # initialized as (0, 0), 
        # but must be in approprate starting position (any 1 in self.track) upon start
        # additionally, it must be within the bounds of walls. 
        self.acceleration = np.zeros(2, dtype = int) # both values must be between -1 and 1 (inclusive)
        self.previousAcceleration = np.zeros(2, dtype = int) # Stores actual previous acceleration. may be used to track failed attempts
        # (0.2 probability), or movement from previous position
        self.previousAccelerationAttempt = np.zeros(2, dtype = int) # Stores agent's attempted previous acceleration attempt. 
        # may be used to track failed attempts (0.2 probability)
        self.path = [] # array storing type 'np.zeros(2, dtype = int)'. Tracks every position of car way to finish line.
        self.moves = 0 # tracks number of moves our AI has made. 

        self.inputTextArray = inputTextArray # numpy of actual input text. On output, will be used to display best path taken by learning method. 
        # on output, we replace the cells that are part of the path taken with 'P'. So, some '.' will become 'P'.
        self.bestMoves = 9999 # tracks the number of moves associated with the best path taken. Will be printed to console on end of function.
        self.bestPath = [] # stores the best path found by the algorithm

        self.numberOfCrashes = 0 # tracks the number of crashes for debugging purposes

        self.trackSize = 0 # number of non-wall elements
        self.trackIDs = {} # stores a list of non-wall element locations [row, column], as ordered by sequential access of (row, column) index.
        self.trackLocs = {} # stores all sequential access non-wall indexes, keys being a string representing the [row, column]
        self.startingCells = [] # contains array of all starting cells. 
        # For value iteration, the best of self.valIterStates[startingCell][0][0][startingAccx][startingAccy] will be selected as our first position/move.
        # Then, we will greedily follow that gradient to the finish to obtain our optimal path.
        
        for row in range(self.trackShape[0]):
            for col in range(self.trackShape[1]):
                item = self.track[row][col]
                if (item == 1):
                    self.startingCells.append([row, col])
                    
                if ((item == 0) or (item == 1) or (item == 2)):
                    self.trackIDs.update({self.trackSize : [row, col]})
                    self.trackLocs.update({str([row, col]) : self.trackSize})
                    self.trackSize += 1
                    
        # array to contain the score for every possible state. The state is represented as:
        # trackID, x velocity, y velocity, x acceleration, y acceleration
        self.valIterStates = np.zeros((self.trackSize, 11, 11, 3, 3), dtype = float)
        self.resultingStates = np.zeros((self.trackSize, 11, 11, 3, 3, 3), dtype = int) # lookup table for resulting states from valIterStates
        
    # ---------------- END INSTANTIATION ------------------


    # ---------------- GET METHODS ------------------
    '''
    def getX(self):
        # sample get expression
        return self.X'''

    def getInputTextArray(self):
        # for output purposes
        return self.inputTextArray

    def getBestPath(self):
        # for output purposes
        return self.bestPath
    
    def getBestMoves(self):
        # for output purposes
        return self.bestMoves
        
    '''    
    def getIsStart(self, posiiton):
        isStart = False
        # takes in a position and checks if that location on the graph is a '1'. If it is a '1', return true. Otherwise, return false
        return isStart'''
    '''    
    def getIsFinish(self, posiiton):
        isFinish = False
        # takes in a position and checks if that location on the graph is a '2'. If it is a '2', return true. Otherwise, return false
        return isFinish'''
    '''
    def getIsWall(self, posiiton):
        isWall = False
        # takes in a position and checks if that location on the graph is a '3'. If it is a '3', return true. Otherwise, return false
        return isWall'''
    # ---------------- END GET METHODS ------------------

    # ---------------- ACTION METHODS  ------------------
    '''
    def getIsTrack(self, posiiton):
        isWall = False
        # takes in a position and checks if that location on the graph is a '0'. If it is a '0', return true. Otherwise, return false
        return isWall'''
    '''
    def updateAcceleration(self, newAcceleration):
        outOfBounds = False
        # unconditionally updates self.acceleration, with values within bounds -1 and 1. Takes in a 2-size np.zeros array.
        # always update self.previousAccelerationAttempt to this value. 
        # always update self.acceleration to this value. 

        # always append 1 to self.moves
        
        # return outOfBounds = True if the attempted set was out of allowed bounds
        return outOfBounds
        '''
    '''
    def failAcceleration(self):
        failed = False
        # run sequentially after self.updateAcceleration() (we can comment it's function calls out for consistency while
        # debugging algorithms, then un-comment as one of the final steps)
        # with probability 0.2, set failed to be True
        # if failed is True, update self.acceleration to (0, 0)
        # afterward, always update self.previousAcceleration to self.acceleration
        return failed
        '''
    def updateVelocity(self):
        outOfBounds = False
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        if (self.velocity[0] > 5):
            self.velocity[0] = 5
            outOfBounds = True
        if (self.velocity[1] > 5):
            self.velocity[1] = 5
            outOfBounds = True
        if (self.velocity[0] < -5):
            self.velocity[0] = -5
            outOfBounds = True
        if (self.velocity[1] < -5):
            self.velocity[1] = -5
            outOfBounds = True
        # run sequentially after self.failAcceleration()
        # unconditionally updates self.velocity based upon self.acceleration
        # add values in self.acceleration to self.velocity, ensuring self.velocity is within bounds
        # return outOfBounds = True if the attempted set was out of allowed bounds
        return outOfBounds
        
    def updatePosition(self):
        collisionOccurred = False
        # run sequentially after self.updateVelocity()
        # unconditionally updates self.position based upon self.velocity
        
        # add values in self.acceleration to self.position, iteratively checking for collisions (i.e., if velocity is (-4, 2), 
        # check each position (x - 1, y + 0), (x - 2, y + 1), (x - 3, y + 1), (x - 4, y + 2).. or something...). 
        # for every position tested that is not a collision, append it to the self.path array
        # if collision is detected, unconditionally update position to the previous tested position and move to next steps
        # (keeps moving until it's up against wall it collides with)
        # if finish line is encountered, stop it there. 
        xCounter = 0
        yCounter = 0
        for i in range(5):
            xCounter += self.velocity[0]
            yCounter += self.velocity[1]
            xPosition = int(xCounter / 5) + self.position[0]
            yPosition = int(yCounter / 5) + self.position[1]
            locType = self.track[xPosition][yPosition]
            if locType == 2:
                self.position[0] = xPosition
                self.position[1] = yPosition
                return collisionOccurred
            if locType == 3:
                collisionOccurred = True
                if not self.crashReset:
                    self.position[0] = int((xCounter - self.velocity[0]) / 5) + self.position[0]
                    self.position[1] = int((yCounter - self.velocity[1]) / 5) + self.position[1]
                    self.velocity[0] = 0
                    self.velocity[1] = 0
                    return collisionOccurred
                else:
                    self.position[0] = self.startingCells[0][0]
                    self.position[1] = self.startingCells[0][1]
                    self.velocity[0] = 0
                    self.velocity[1] = 0
                    return collisionOccurred
        
        # if no collision occurs, set new position accordingly. 
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        # if collision occurs, set self.velocity = 0, add 1 to self.numberOfCrashes
        # if collision occurs, check self.crashReset Variable. If true, set position to start of track
        
        # return collisionOccurred = True if collision occurred
        return collisionOccurred
    # ---------------- END ACTION METHODS  ------------------

    # ************************** SHARED METHODS *******************************
    # ------------------------ DO MOVE ---------------------------------
    def makeMove(self, move):
        self.position[0] = move[0]
        self.position[1] = move[1]
        self.velocity[0] = move[2]
        self.velocity[1] = move[3]
        self.acceleration[0] = move[4]
        self.acceleration[1] = move[5]
        self.updateVelocity()
        self.updatePosition()
        trackID = self.trackLocs[str([self.position[0], self.position[1]])]
        resultingState = [trackID, self.velocity[0], self.velocity[1], self.acceleration[0], self.acceleration[1]]
        return resultingState

    def attemptFinish(self, move): # checks if move touches or crosses finish line
        self.position[0] = move[0]
        self.position[1] = move[1]
        self.velocity[0] = move[2]
        self.velocity[1] = move[3]
        self.acceleration[0] = move[4]
        self.acceleration[1] = move[5]
        self.updateVelocity()
        self.updatePosition()
        Finishes = False
        oldTrackID = self.trackLocs[str([move[0], move[1]])]
        trackID = self.trackLocs[str([self.position[0], self.position[1]])]
        self.resultingStates[oldTrackID][move[2] + 5][move[3] + 5][move[4] + 1][move[5] + 1] = np.array([trackID, self.velocity[0] + 5, self.velocity[1] + 5])
        if (self.track[self.position[0]][self.position[1]] == 2):
            Finishes = True
        return Finishes # returns false if move does not complete the race.
    # ------------------------ END DO MOVE ---------------------------------

    # ************************** END SHARED METHODS *******************************


    # ************************** VALUE ITERATION METHODS *******************************
    # ------------------------ DO VALUE ITERATION ---------------------------------
    def doValueIteration(self):
        self.doIterationK0()
        self.doIterationK1()
        valueUpdated = True
        k = 2
        while valueUpdated and (k < 100):
            print("k: " + str(k))
            valueUpdated = self.doIterationKn(k)
            k += 1

        # next, find best starting conditions (use self.startingCells), then follow the gradient greedily to track path to finish line.
        # update self.moves and self.bestPath along the way
        # from the best starting cell, track best path deterministically to finish (we are just recording our findings, this is not 
        # an actual simulation)
        
        bestStart = [self.trackLocs[str(self.startingCells[0])], 0, 0]
        bestStartValue = -99999
        for cell in self.startingCells:
            startingID = self.trackLocs[str(cell)]
            for xaccIndex in range(3):
                for yaccIndex in range(3):
                    startValue = self.valIterStates[startingID][5][5][xaccIndex][yaccIndex]
                    if (startValue > bestStartValue):
                        bestStart = [startingID, xaccIndex, yaccIndex]
                        bestStartValue = startValue
                        
        startPosition = self.trackIDs[bestStart[0]]
        self.position[0] = startPosition[0]
        self.position[1] = startPosition[1]
        self.bestPath.append([self.position[0], self.position[1]])
        self.acceleration[0] = bestStart[1] - 1
        self.acceleration[1] = bestStart[2] - 1
        self.updateVelocity()
        self.updatePosition()
        self.bestMoves = 1
        self.bestPath.append([self.position[0], self.position[1]])
        
        while self.track[self.position[0]][self.position[1]] != 2:
            bestMoveValue = -99999
            bestMove = [0, 0]
            cellID = self.trackLocs[str([self.position[0], self.position[1]])]
            for xaccIndex in range(3):
                for yaccIndex in range(3):
                    moveValue = self.valIterStates[cellID][self.velocity[0] + 5][self.velocity[1] + 5][xaccIndex][yaccIndex]
                    if (moveValue > bestMoveValue):
                        bestMove = [xaccIndex - 1, yaccIndex - 1]
                        bestMoveValue =moveValue
            self.acceleration[0] = bestMove[0]
            self.acceleration[1] = bestMove[1]
            self.updateVelocity()
            self.updatePosition()
            self.bestMoves += 1
            self.bestPath.append([self.position[0], self.position[1]])
        
        return

    def doIterationK0(self):
        locIndex = 0
        for loc in self.valIterStates:
            xy = self.trackIDs[locIndex]
            xpos = xy[0]
            ypos = xy[1]
            if (self.track[xpos][ypos] != 2):   
                xVelIndex = 0
                for xvel in loc:
                    yVelIndex = 0
                    for yvel in xvel:
                        xAccIndex = 0
                        for xacc in yvel:
                            yAccIndex = 0
                            for yacc in xacc:
                                self.valIterStates[locIndex, xVelIndex, yVelIndex, xAccIndex, yAccIndex] = -1.0
                                yAccIndex += 1
                            xAccIndex += 1
                        yVelIndex += 1
                    xVelIndex += 1
            locIndex += 1
        return

    def doIterationK1(self):
        locIndex = 0
        for loc in self.valIterStates:
            xy = self.trackIDs[locIndex]
            xpos = xy[0]
            ypos = xy[1]
            xvelVal = -5
            for xvel in loc:
                xVelIndex = xvelVal + 5
                
                yvelVal = -5
                for yvel in xvel:
                    yVelIndex = yvelVal + 5
                    
                    xaccVal = -1
                    for xacc in yvel:
                        xAccIndex = xaccVal + 1
                        
                        yaccVal = -1
                        for yacc in xacc:
                            yAccIndex = yaccVal + 1
                            move = [xpos, ypos, xvelVal, yvelVal, xaccVal, yaccVal]
                            finishes = self.attemptFinish(move)
                            if not finishes:
                                self.valIterStates[locIndex, xVelIndex, yVelIndex, xAccIndex, yAccIndex] += -0.999 * 0.8
                            yaccVal += 1
                        xaccVal += 1
                    yvelVal += 1
                xvelVal += 1
            locIndex += 1
        # for 20% chance of failure
        locIndex = 0
        for loc in self.valIterStates:
            xy = self.trackIDs[locIndex]
            xpos = xy[0]
            ypos = xy[1]
            xvelVal = -5
            for xvel in loc:
                xVelIndex = xvelVal + 5
                
                yvelVal = -5
                for yvel in xvel:
                    yVelIndex = yvelVal + 5
                    
                    move = [xpos, ypos, xvelVal, yvelVal, 1, 1]
                    finishes = self.attemptFinish(move)
                    
                    xaccVal = -1
                    for xacc in yvel:
                        xAccIndex = xaccVal + 1
                        
                        yaccVal = -1
                        for yacc in xacc:
                            yAccIndex = yaccVal + 1
                            if not finishes: 
                                self.valIterStates[locIndex, xVelIndex, yVelIndex, xAccIndex, yAccIndex] += -0.999 * 0.2
                            yaccVal += 1
                        xaccVal += 1
                    yvelVal += 1
                xvelVal += 1
            locIndex += 1 
        return
        
    def doIterationKn(self, k):
        valueRemoved = -(0.999**k)
        kMinus2Value = 0
        for i in range(k - 1): # iterations start from 0, not 1. So i is already k - 1. So i - 1 is k - 2. Really is confusing, though...
            kMinus2Value += -(1 * (0.999**i))

        valueUpdated = False
        pathFound1 = False # will need to be corrected for non-deterministic
        pathFound2 = False # will need to be corrected for non-deterministic
        locIndex = 0
        for loc in self.valIterStates:
            #print("locIndex: " + str(locIndex))
            xy = self.trackIDs[locIndex]
            xpos = xy[0]
            ypos = xy[1]
            xvelVal = -5
            for xvel in loc:
                xVelIndex = xvelVal + 5
                
                yvelVal = -5
                for yvel in xvel:
                    yVelIndex = yvelVal + 5
                    
                    xaccVal = -1
                    for xacc in yvel:
                        xAccIndex = xaccVal + 1
                        
                        yaccVal = -1
                        for yacc in xacc:
                            yAccIndex = yaccVal + 1
                            # move = [xpos, ypos, xvelVal, yvelVal, xaccVal, yaccVal]
                            nextState = self.resultingStates[locIndex][xVelIndex][yVelIndex][xAccIndex][yAccIndex]
                            nextValue = np.max(self.valIterStates[nextState[0]][nextState[1]][nextState[2]][:][:])
                            improves = (nextValue >= kMinus2Value) # the .8 breaks this comparison, skip for now.
                            if not improves: 
                                self.valIterStates[locIndex, xVelIndex, yVelIndex, xAccIndex, yAccIndex] += valueRemoved * 0.8
                                valueUpdated = True
                            if (self.track[xpos][ypos] == 1) and improves and (xvelVal == 0) and (yvelVal == 0):
                                pathFound1 = True # will need to be corrected for non-deterministic
                            yaccVal += 1
                        xaccVal += 1
                    yvelVal += 1
                xvelVal += 1
            locIndex += 1
        # for 20% chance of failure
        locIndex = 0
        for loc in self.valIterStates:
            #print("locIndex: " + str(locIndex))
            xy = self.trackIDs[locIndex]
            xpos = xy[0]
            ypos = xy[1]
            xvelVal = -5
            for xvel in loc:
                xVelIndex = xvelVal + 5
                
                yvelVal = -5
                for yvel in xvel:
                    yVelIndex = yvelVal + 5

                    # move = [xpos, ypos, xvelVal, yvelVal, 1, 1]
                    nextState = self.resultingStates[locIndex][xVelIndex][yVelIndex][1][1]
                    nextValue = np.max(self.valIterStates[nextState[0]][nextState[1]][nextState[2]][:][:])
                    improves = (nextValue >= kMinus2Value) # the .8 breaks this comparison, skip for now.
                    if not improves: 
                        xaccVal = -1
                        for xacc in yvel:
                            xAccIndex = xaccVal + 1

                            yaccVal = -1
                            for yacc in xacc:
                                yAccIndex = yaccVal + 1
                                self.valIterStates[locIndex, xVelIndex, yVelIndex, xAccIndex, yAccIndex] += valueRemoved * 0.2
                                valueUpdated = True
                                yaccVal += 1
                            if (self.track[xpos][ypos] == 1) and improves and (xvelVal == 0) and (yvelVal == 0):
                                pathFound2 = True # will need to be corrected for non-deterministic
                            xaccVal += 1
                    yvelVal += 1
                xvelVal += 1
            locIndex += 1 
        if pathFound1 and pathFound2:
            valueUpdated = False
        return valueUpdated
        
    # ------------------------ END DO VALUE ITERATION ---------------------------------

    # ************************** END VALUE ITERATION METHODS *******************************


    # ************************** Q-LEARNING METHODS *******************************
    # ------------------------ DO Q-LEARNING ---------------------------------
    def doQLearning(self):
        return
    # ------------------------ END DO Q-LEARNING ---------------------------------

    # ************************** END Q-LEARNING METHODS *******************************


    # ************************** SARSA METHODS *******************************
    # ------------------------ DO SARSA ---------------------------------
    def doSARSA(self):
        return

    # ------------------------ END DO SARSA ---------------------------------

    # ************************** END SARSA METHODS *******************************

































