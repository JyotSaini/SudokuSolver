import numpy as py
import copy

unsolved_sudoku = [[8,0,0,0,0,0,0,0,0],
                   [0,0,3,6,0,0,0,0,0],
                   [0,7,0,0,9,0,2,0,0],
                   [0,5,0,0,0,7,0,0,0],
                   [0,0,0,0,4,5,7,0,0],
                   [0,0,0,1,0,0,0,3,0],
                   [0,0,1,0,0,0,0,6,8],
                   [0,0,8,5,0,0,0,1,0],
                   [0,9,0,0,0,0,4,0,0]]

possibles = [[[[] for i in range(9)] for i in range(9)] for i in range(9)] # First two dimensions denote row and column respectively, and the last one denotes the 9 possible values for the sudoku cell
numOfPossibles = [[[] for i in range(9)] for i in range(9)] # A list to store the number of possible values for each element of the sudoku

def initPossiblesList():
    for row in range(9):
        for col in range(9):
            for possible in range(9):
                if unsolved_sudoku[row][col] is not 0:
                    possibles[row][col][possible] = 0
                else:
                    possibles[row][col][possible] = 1

    for row in range(9):
        for col in range(9):
            tallyNumOfPossibles(row, col)

def shortlistPossible():
    for row in range(9):
        for col in range(9):
            eliminateObviousValues(row, col)

def combinePossibleLists(comb1, comb2):
    combinedPossibles = [0,0,0,0,0,0,0,0,0]

    for possible in range(9):
        if (comb1[possible] is 1) or (comb2[possible] is 1):
            combinedPossibles[possible] = 1

    return combinedPossibles

def combineMultiplePossibilitiesForSudoku():
    combineMultiplePossibilitiesForRows()
    combineMultiplePossibilitiesForCols()
    combineMultiplePossibilitiesForBoxes()

def combineMultiplePossibilitiesForRow(currRow, possibilitiesForRow, numOfPossibilities):
    unsolvedElemsInRow = 0
    unsolvedElemsInRowLocation = []
    # print(currRow, py.matrix(possibilitiesForRow), numOfPossibilities)

    for col in range(9):
        if numOfPossibilities[col] > 1:
            unsolvedElemsInRow += 1
            unsolvedElemsInRowLocation.append(col)

    if unsolvedElemsInRow < 3:
        processedRow = [currRow, possibilitiesForRow, numOfPossibilities]
        return processedRow

    combs = getAllCombinationsOfUnsolvedElems(unsolvedElemsInRowLocation)

    for combCounter in range(len(combs)):
        currCombination = possibilitiesForRow[combs[combCounter][0]]
        for elemCounter in range(1, len(combs[combCounter])):
            currCombination = combinePossibleLists(currCombination, possibilitiesForRow[combs[combCounter][elemCounter]])

        currCombinationSize = 0

        for n in range(9):
            if currCombination[n] is 1:
                currCombinationSize += 1

        if currCombinationSize == len(combs[combCounter]):
            currCombinationInverse = unsolvedElemsInRowLocation.copy()
            for elem in combs[combCounter]:
                currCombinationInverse.remove(elem)

            for inverseElem in currCombinationInverse:
                for possibility in range(9):
                    if currCombination[possibility] is 1:
                        possibilitiesForRow[inverseElem][possibility] = 0

            for unsolvedElem in unsolvedElemsInRowLocation:
                numOfPossiblesForCurrElem = 0
                for possibility in range(9):
                    if possibilitiesForRow[unsolvedElem][possibility] is 1:
                        numOfPossiblesForCurrElem += 1
                numOfPossibilities[unsolvedElem] = numOfPossiblesForCurrElem

    for col in range(9):
        if numOfPossibilities[col] is 1:
            for possible in range(9):
                if possibilitiesForRow[col][possible] is 1:
                    currRow[col] = possible + 1
                    possibilitiesForRow[col][possible] = 0
                    numOfPossibilities[col] = 0

    processedRow = [currRow, possibilitiesForRow, numOfPossibilities]

    return processedRow

def getAllCombinationsOfUnsolvedElems(unsolvedElems):
    combs = getAllCombinationsOfUnsolvedElemsHelper(len(unsolvedElems))

    for combCounter in range(len(combs)):
        for elemCounter in range(len(combs[combCounter])):
            combs[combCounter][elemCounter] = unsolvedElems[combs[combCounter][elemCounter]]

    return combs

def getAllCombinationsOfUnsolvedElemsHelper(unsolvedElemsLen):
    if unsolvedElemsLen <= 2:
        return []

    combs = [[]]

    for size in range(unsolvedElemsLen):
        combs.append([])

    for leftAnchor in range(unsolvedElemsLen - 1):                      # (Base Case) When size is 2
        for rightAnchor in range(leftAnchor + 1, unsolvedElemsLen):
            temp = [leftAnchor, rightAnchor]
            combs[2].append(temp)

    for size in range(3, unsolvedElemsLen):                             # Using Induction to build on base case for 2 < size < unsolvedElemsLen
        for leftAnchorCounter in range(len(combs[size - 1]) - 1):
            currComb = combs[size - 1][leftAnchorCounter].copy()
            leftAnchor = combs[size - 1][leftAnchorCounter][size - 2]
            for rightAnchorCounter in range(len(combs[size - 1])):
                currComb = combs[size - 1][leftAnchorCounter].copy()
                if leftAnchor == unsolvedElemsLen - 1:
                    break
                elif combs[size - 1][rightAnchorCounter][size - 3] == leftAnchor:
                    rightAnchor = combs[size - 1][rightAnchorCounter][size - 2]
                    currComb.append(rightAnchor)
                    combs[size].append(currComb)
                    if rightAnchor == unsolvedElemsLen - 1:
                        break
    
    formattedCombs = []

    for size in range(2, unsolvedElemsLen):
        formattedCombs.extend(combs[size])

    return formattedCombs

def calculatePossibleCombs(size):
    possibleCombsTotal = 0
    for i in range(size):
        possibleCombsTotal += i
    return possibleCombsTotal

def combineMultiplePossibilitiesForRows():
    for row in range(9):
        processedRow = combineMultiplePossibilitiesForRow(unsolved_sudoku[row], possibles[row], numOfPossibles[row])

        unsolved_sudoku[row] = processedRow[0]
        possibles[row] = processedRow[1]
        numOfPossibles[row] = processedRow[2]

def combineMultiplePossibilitiesForCols():
    for col in range(9):
        morphedCol = []
        morphedPossiblesForCol = []
        morphedNumOfPossiblesForCol = []

        for row in range(9):
            morphedCol.append(unsolved_sudoku[row][col])
            morphedPossiblesForCol.append(possibles[row][col])
            morphedNumOfPossiblesForCol.append(numOfPossibles[row][col])

        processedCol = combineMultiplePossibilitiesForRow(morphedCol, morphedPossiblesForCol, morphedNumOfPossiblesForCol)

        for row in range(9):
            unsolved_sudoku[row][col] = processedCol[0][row]
            possibles[row][col] = processedCol[1][row]
            numOfPossibles[row][col] = processedCol[2][row]

def combineMultiplePossibilitiesForBoxes():
    for boxRow in range(3):
        for boxCol in range(3):
            morphedBox = []
            morphedPossiblesForBox = []
            morphedNumOfPossiblesForBox = []

            for row in range(3):
                for col in range(3):
                    morphedBox.append(unsolved_sudoku[(boxRow * 3) + row][(boxCol * 3) + col])
                    morphedPossiblesForBox.append(possibles[(boxRow * 3) + row][(boxCol * 3) + col])
                    morphedNumOfPossiblesForBox.append(numOfPossibles[(boxRow * 3) + row][(boxCol * 3) + col])

            processedBox = combineMultiplePossibilitiesForRow(morphedBox, morphedPossiblesForBox, morphedNumOfPossiblesForBox)

            for row in range(3):
                for col in range(3):
                    unsolved_sudoku[(boxRow * 3) + row][(boxCol * 3) + col] = processedBox[0][(row * 3) + col]
                    possibles[(boxRow * 3) + row][(boxCol * 3) + col] = processedBox[1][(row * 3) + col]
                    numOfPossibles[(boxRow * 3) + row][(boxCol * 3) + col] = processedBox[2][(row * 3) + col]

def updateSudoku():
    for row in range(9):
        for col in range(9):
            if numOfPossibles[row][col] is 1:
                for possible in range(9):
                    if possibles[row][col][possible] is 1:
                        unsolved_sudoku[row][col] = possible + 1
                        possibles[row][col][possible] = 0
                        tallyNumOfPossibles(row, col)

def tallyNumOfPossibles(rowNum, colNum):
    totalForElement = 0
    for possible in range(9):
        totalForElement += possibles[rowNum][colNum][possible]
    numOfPossibles[rowNum][colNum] = totalForElement

def sudokuHasZeroes(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] is 0:
                return True

    return False

def sudokuIsNotVerified(sudoku):
    for row in sudoku:
        elemsTally = [1,1,1,1,1,1,1,1,1]

        for elem in row:
            elemsTally[elem - 1] = 0

        for elem in elemsTally:
            if elem == 1:
                return True
                
    for col in range(9):
        elemsTally = [1,1,1,1,1,1,1,1,1]

        for row in range(9):
            elemsTally[sudoku[row][col] - 1] = 0

        for elem in elemsTally:
            if elem == 1:
                return True
                
    for boxRow in range(3):
        for boxCol in range(3):
            elemsTally = [1,1,1,1,1,1,1,1,1]

            for row in range(boxRow * 3, (boxRow * 3) + 3):
                for col in range(boxCol * 3, (boxCol * 3) + 3):
                    elemsTally[sudoku[row][col] - 1] = 0

            for elem in elemsTally:
                if elem == 1:
                    return True
    return False

def sudokuIsMaxedOut(origSudoku, sudoku):
    maxSudoku = [[9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,9]]

    for row in range(9):
        for col in range(9):
            if origSudoku[row][col] > 0:
                maxSudoku[row][col] = origSudoku[row][col]

    if sudoku == maxSudoku:
        return True

    return False

def eliminateFromRow(rowNum):
    impossibles = []

    for col in range(9):
        if unsolved_sudoku[rowNum][col] is not 0:
            impossibles.append(unsolved_sudoku[rowNum][col] - 1)

    return impossibles

def eliminateFromColumn(colNum):
    impossibles = []

    for row in range(9):
        if unsolved_sudoku[row][colNum] is not 0:
            impossibles.append(unsolved_sudoku[row][colNum] - 1)

    return impossibles

def eliminateFromSameBox(rowNum, colNum):
    impossibles = []

    boxRow = rowNum // 3
    boxCol = colNum // 3

    for boxRowElem in range(boxRow * 3, (boxRow * 3) + 3):
        for boxColElem in range(boxCol * 3, (boxCol * 3) + 3):
            if unsolved_sudoku[boxRowElem][boxColElem] is not 0:
                impossibles.append(unsolved_sudoku[boxRowElem][boxColElem] - 1)

    return impossibles

def eliminateObviousValues(rowNum, colNum):
    if unsolved_sudoku[rowNum][colNum] is not 0:
        return

    impossiblesForElement = eliminateFromRow(rowNum)
    impossiblesForElement.extend(eliminateFromColumn(colNum))
    impossiblesForElement.extend(eliminateFromSameBox(rowNum, colNum))

    for impossible in impossiblesForElement:
        possibles[rowNum][colNum][impossible] = 0

    tallyNumOfPossibles(rowNum, colNum)

def printSudoku():
    print(py.matrix(unsolved_sudoku))

def verifyLastElemHelper(row, col, box, lastElem):
    for elem in row:
        if elem == lastElem:
            return False

    for elem in col:
        if elem == lastElem:
            return False

    for boxRow in box:
        for elem in boxRow:
            if elem == lastElem:
                return False

    return True

def verifyLastElem(sudoku, rowNum, colNum):
    row = [0,0,0,0,0,0,0,0,0]
    col = [0,0,0,0,0,0,0,0,0]
    box = [[0,0,0],[0,0,0],[0,0,0]]
    elem = sudoku[rowNum][colNum]

    for rowElemCounter in range(9):
        row[rowElemCounter] = sudoku[rowNum][rowElemCounter]

    for colElemCounter in range(9):
        col[colElemCounter] = sudoku[colElemCounter][colNum]

    for boxRowElemCounter in range((rowNum // 3) * 3, ((rowNum // 3) * 3) + 3):
        for boxColElemCounter in range((colNum // 3) * 3, ((colNum // 3) * 3) + 3):
            box[boxRowElemCounter % 3][boxColElemCounter % 3] = sudoku[boxRowElemCounter][boxColElemCounter]

    row[colNum] = 0
    col[rowNum] = 0
    box[rowNum % 3][colNum % 3] = 0

    return verifyLastElemHelper(row, col, box, elem)

def increaseElem(row, col):
    col += 1
    if col > 8:
        row += 1
        col = 0

    return [row, col]

def decreaseElem(row, col):
    col -= 1
    if col < 0:
        row -= 1
        col = 8

    return [row, col]

def bruteforceSolution(origSudoku, sudoku):
    currSudoku = copy.deepcopy(sudoku)
    origSudokuLocs = copy.deepcopy(origSudoku)

    for row in range(9):
        for col in range(9):
            if origSudokuLocs[row][col] > 0:
                origSudokuLocs[row][col] = True
            else:
                origSudokuLocs[row][col] = False

    row = 0
    col = 0

    while sudokuIsNotVerified(currSudoku):
        if sudokuIsMaxedOut(origSudoku, currSudoku):
            return False

        if not origSudokuLocs[row][col]:
            currSudoku[row][col] += 1
            if currSudoku[row][col] > 9:
                currSudoku[row][col] = 0
                row = decreaseElem(row, col)[0]
                col = decreaseElem(row, col)[1]
                while origSudokuLocs[row][col]:
                    row = decreaseElem(row, col)[0]
                    col = decreaseElem(row, col)[1]
            elif verifyLastElem(currSudoku, row, col):
                row = increaseElem(row, col)[0]
                col = increaseElem(row, col)[1]
        else:
            row = increaseElem(row, col)[0]
            col = increaseElem(row, col)[1]

    return currSudoku

def tamperLastElemInSudoku(origSudoku, sudoku):
    currSudoku = copy.deepcopy(sudoku)
    origSudokuLocs = copy.deepcopy(origSudoku)

    for row in range(9):
        for col in range(9):
            if origSudokuLocs[row][col] > 0:
                origSudokuLocs[row][col] = True
            else:
                origSudokuLocs[row][col] = False

    if sudokuIsMaxedOut(origSudoku, currSudoku):
        return False

    for row in reversed(range(9)):
        for col in reversed(range(9)):
            if not origSudokuLocs[row][col]:
                currSudoku[row][col] += 1
                if currSudoku[row][col] > 9:
                    currSudoku[row][col] = 0
                else:
                    break

    return currSudoku

def nBruteforceSolutions(origSudoku, n):
    sols = []
    solution = bruteforceSolution(origSudoku, origSudoku)

    while len(sols) < n:
        sols.append(solution)
        tamperedSolution = tamperLastElemInSudoku(origSudoku, solution)

        if tamperedSolution is False:
            break
        
        solution = bruteforceSolution(origSudoku, tamperedSolution)

        if solution is False:
            break

    for solution in sols:
        print(py.matrix(solution))


def main():
    initPossiblesList()

    while sudokuHasZeroes(unsolved_sudoku):
        temp_sudoku = copy.deepcopy(unsolved_sudoku)

        shortlistPossible()
        updateSudoku()
        combineMultiplePossibilitiesForSudoku()
        
        if temp_sudoku == unsolved_sudoku:
            print("Handcrafted Algorithm failing at finding solution, attempting bruteforce instead")
            break

    print(py.matrix(bruteforceSolution(unsolved_sudoku, unsolved_sudoku)))

main()
