# OOPS Solver Algorithm
# Rules of this version
# Same as normal, however the stack can only move when touched by the wizzard
# → Less possible outcomes lighter algorithm could be used
# 90 represents hat, 81 wizard

import numpy as np
import copy


def GiveCopyOfBoard(board):
    global listWithInstructions
    if board is not None:
        originalBoard = copy.deepcopy(board)
        CalculateSolution(board, originalBoard)
        instructions = GiveInstructionsCorrectRotation(listWithInstructions)
        return instructions


def CalculateSolution(a_board, originalBoard):
    if a_board is not None:
        # print(a_board)
        for x in range(len(a_board)):
            for y in range(len(a_board[0])):
                if 81 <= a_board[x][y] <= 89:
                    # This is the wizard piece
                    # Check which direction he can move to
                    stackSize = a_board[x][y] - 80
                    # Check whether there is an other piece in range of the stackSize
                    PrintBoard(a_board)
                    a_board = CalculateMove(a_board, stackSize, x, y, originalBoard)
                    # print("We geven dees bord als original mee" + str(originalBoard))

                    if not CheckGameFinished(a_board):
                        CalculateSolution(a_board, originalBoard)
                        return
                    else:
                        return a_board


def CheckGameFinished(a_board):
    if a_board is not None:
        amountOfPiecesFound = 0
        for x in range(len(board)):
            for y in range(len(board[0])):
                if a_board[x][y] != 0:
                    amountOfPiecesFound += 1
        if amountOfPiecesFound <= 1:
            gameFinished = True
            return True
        else:
            return False


def CalculateMove(a_board, moves, x, y, originalBoard):
    global listWithInstructions
    #global listWithStackSize
    hatStep = False
    for x1 in range(len(a_board)):
        for y1 in range(len(a_board[0])):
            if (x != x1 or y != y1) and a_board[x1][y1] != 90 and a_board[x1][y1] != 0:
                distance = abs(x - x1) + abs(y - y1)
                for extraMoves in range(0, 20, 2):
                    if (distance + extraMoves) == moves:
                        # we got a match
                        a_board[x1][y1] += (moves + 80)
                        a_board[x][y] = 0
                        print("Move stack from position " + str(x) + "," + str(y) + " To position " + str(
                            x1) + ", " + str(y1) + " The stacksize is " + str(moves))
                        listWithInstructions.append([x,y])
                        listWithInstructions.append([x1,y1])
                        listWithStackSize.append(moves)

                        return a_board
            elif a_board[x1][y1] == 90:
                hatx = x1
                haty = y1
                hatStep = True

    if hatStep:
        # For the last move into the hat
        distance = abs(x - hatx) + abs(y - haty)
        for extraMoves in range(0, 20, 2):
            if (distance + extraMoves) == moves:
                # we got a match
                a_board[hatx][haty] += (moves + 80)
                a_board[x][y] = 0
                print("Move stack from position " + str(x) + "," + str(y) + " To position " + str(hatx) + ", " + str(
                    haty) + " The stacksize is " + str(moves) + " excluding the wizard.")
                listWithInstructions.append([x,y])
                listWithInstructions.append([hatx,haty])
                listWithStackSize.append(moves)
                return a_board

        # For the last move into the hat

    print("error:no match found")
    # If no solution was found → we must try again after rotating the matrix 90 degrees

    RotateMatrix(originalBoard)


def RotateMatrix(originalBoard):
    global listWithInstructions
    global rotation
    global timesRotated
    global  listWithStackSize
    if timesRotated <= 4:
        listWithInstructions = []
        listWithStackSize = []
        rotation +=1
        boardToRotate = copy.deepcopy(originalBoard)
        # print("This is the matrix we are going to rotate")
        # PrintBoard(boardToRotate)
        print("-" * 30)
        print("No solution was found therefore we will rotate matrix and try again.")
        print("This is the " + str(timesRotated) + "th time the matrix is rotated.")
        rotatedBoard = np.asarray(boardToRotate)
        # PrintBoard(rotatedBoard)
        for counter in range(3):
            rotatedBoard = np.rot90(rotatedBoard)
        PrintBoard(rotatedBoard)
        GiveCopyOfBoard(rotatedBoard)
        timesRotated +=1
    else:
        print("The matrix was rotated for " + str(timesRotated) + " times, but no solution was found.")
        print("Check if board isn't faulty.")


def PrintBoard(a_board):
    print("#" * 30)
    for x in range(len(a_board)):
        print(a_board[x])
    print("#" * 30)

def GiveInstructionsCorrectRotation(instructions):
    global rotation
    cx = 2
    cy = 2
    #print("Unrotated Instructions " + str(instructions))
    for degree in range(rotation):
        for x in instructions:
            #print(x)
            dx = x[0]-cx
            dy = x[1] - cy
            x[0] = cx - dy
            x[1] = cy + dx

    return instructions

def MatrixToSolution(board):
    instructions = GiveCopyOfBoard(board)
    print("These are the instructions")
    print(instructions)
    listWithStackSize.append(90)
    print("These are the stacksizes")
    print(listWithStackSize)
    #Combine stacksize with the other instructions
    for x in range(0,((len(listWithStackSize)-1)*2),2):
        if listWithStackSize[int((x/2)+1)] != 90:
            instructions[x].append(listWithStackSize[int(x/2)])
            instructions[x+1].append(listWithStackSize[int((x/2)+1)]-listWithStackSize[int((x/2))])
        else:
            instructions[x].append(listWithStackSize[int(x/2)])
            instructions[x+1].append(90)
    print("The final instructions in format [xcoor,ycoor,stacksizeOfTarget] are")
    print(instructions)
    return instructions


if __name__ == '__main__':
    gameFinished = False
    gameStarted = False
    global listWithInstructions

    listWithInstructions = []
    global rotation
    rotation = 0
    global timesRotated
    timesRotated = 0
    global listWithStackSize
    listWithStackSize = []
    
    board = [[1, 0, 0, 1, 81], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [90, 0, 0, 0, 0]]
    if not gameStarted:
        MatrixToSolution(board)
        gameStarted = True
