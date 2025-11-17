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
    '''
    def updateVelocity(self):
        outOfBounds = False
        # run sequentially after self.failAcceleration()
        # unconditionally updates self.velocity based upon self.acceleration
        # add values in self.acceleration to self.velocity, ensuring self.velocity is within bounds
        # return outOfBounds = True if the attempted set was out of allowed bounds
        return outOfBounds
        '''
    '''
    def updatePosition(self):
        collisionOccurred = False
        # run sequentially after self.updateVelocity()
        # unconditionally updates self.position based upon self.velocity
        
        # add values in self.acceleration to self.position, iteratively checking for collisions (i.e., if velocity is (-4, 2), 
        # check each position (x - 1, y + 0), (x - 2, y + 1), (x - 3, y + 1), (x - 4, y + 2).. or something...). 
        # for every position tested that is not a collision, append it to the self.path array
        # if collision is detected, unconditionally update position to the previous tested position and move to next steps
        # (keeps moving until it's up against wall it collides with)
        
        # if no collision occurs, set new position accordingly. 
        
        # if collision occurs, set self.velocity = 0, add 1 to self.numberOfCrashes
        # if collision occurs, check self.crashReset Variable. If true, set position to start of track
        
        # return collisionOccurred = True if collision occurred
        return collisionOccurred
        '''
    # ---------------- END ACTION METHODS  ------------------

    # ************************** SHARED METHODS *******************************
    # ------------------------ DO MOVE ---------------------------------
    def makeMode(self, move):
        return
    # ------------------------ END DO MOVE ---------------------------------

    # ************************** END SHARED METHODS *******************************


    # ************************** VALUE ITERATION METHODS *******************************
    # ------------------------ DO VALUE ITERATION ---------------------------------
    def doValueIteration(self):
        return
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

































