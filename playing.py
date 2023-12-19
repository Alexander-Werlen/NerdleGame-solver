import os
import random
import itertools
import math


def generateAllPatterns():
    # Calculating possible patterns of similitud
    """ 
    Simbolos de patron de similitud
    0: if sign not in eq
    1: if sign in eq but not in that place
    2: if sign in eq in that place
    """
    numberOfTiles = 6  # HARDCODED

    patterns = []

    def foo(l, numberOfTiles):
        yield from itertools.product(*([l] * numberOfTiles))

    for x in foo("012", numberOfTiles):
        patterns.append(x)

    return patterns


def readData():
    if os.path.exists("validInputs.txt"):
        with open("validInputs.txt", "r") as f:
            validInputs = [line[:-1] for line in f]
            pass
    else:
        raise Exception("No validInputs.txt file found")

    if os.path.exists("validSolutions.txt"):
        with open("validSolutions.txt", "r") as f:
            validSolutions = [line[:-1] for line in f]
            pass
    else:
        raise Exception("No validInputs.txt file found")

    return validInputs, validSolutions


def checkSimilitud(currentExpression, solution):
    # Function returns the pattern resulting between the real solution and the current expression
    pattern = []

    for index, char in enumerate(currentExpression):
        if char not in solution:
            pattern.append(0)
        elif char in solution and char != solution[index]:
            pattern.append(1)
        elif char == solution[index]:
            pattern.append(2)
        else:
            raise Exception("problemas con el checkeo de similitud")

    return pattern


def expressionIsPossibleGivenSimilitud(expression, currentExpression, similitud):
    for index, char in enumerate(currentExpression):
        if similitud[index] == 0:
            if char in expression:
                return False
        elif similitud[index] == 1:
            if char not in expression or char == expression[index]:
                return False
        elif similitud[index] == 2:
            if char != expression[index]:
                return False

    return True


def adjustPossibleSolutions(currentPossibleSolutions, currentExpression, similitud):
    return [expression for expression in currentPossibleSolutions if expressionIsPossibleGivenSimilitud(expression, currentExpression, similitud)]


def checkPattern(pattern, currentExpression, expression):

    for index, similitud in enumerate(pattern):
        if similitud == "0" and (currentExpression[index] in expression):
            return False
        elif similitud == "1" and (currentExpression[index] not in expression or currentExpression[index] == expression[index]):
            return False
        elif similitud == "2" and (currentExpression[index] != expression[index]):
            return False

    return True


def calculatePx(pattern, currentExpression, possibleSolutions):
    Nmatches = 0
    TotalPossibleExpressions = len(possibleSolutions)

    for expression in possibleSolutions:
        if checkPattern(pattern, currentExpression, expression):
            Nmatches += 1

    Px = Nmatches/TotalPossibleExpressions

    return Px


def calculateInformationVariables(expression, possibleSolutions, patterns):
    """ 
    E[i] = sumatoria(p(x)*log2(1/p(x))) 
    Donde:
    x = patron de similitud
    p(x) = (N de eq posibles con el patron x dado) / (N total de eq) 
    """

    EinfoOfExpression = 0

    for pattern in patterns:
        Px = calculatePx(pattern, expression, possibleSolutions)
        if Px != 0:  # Avoiding division by 0
            EinfoOfExpression += Px*math.log((1/Px), 2)

    return EinfoOfExpression


def findBestInput(validInputs, currentPossibleSolutions):
    global patterns

    currentBestInput = ["", 0]
    for expression in validInputs:
        EinfoOfExpression = calculateInformationVariables(
            expression, currentPossibleSolutions, patterns)

        if EinfoOfExpression > currentBestInput[1]:
            currentBestInput = [expression, EinfoOfExpression]

    return currentBestInput[0]


def playGame(opener, validInputs, validSolutions):
    solution = validSolutions[random.randint(0, len(validSolutions)-1)]
    print("Solution: {}".format(solution))
    currentTry = 1
    currentExpression = opener[:]
    currentPossibleSolutions = validSolutions[:]

    while currentTry < 7:
        print("Remaining: {} Try{}: {}".format(len(currentPossibleSolutions),
              currentTry, currentExpression))

        similitud = checkSimilitud(currentExpression, solution)
        if similitud == [2, 2, 2, 2, 2, 2]:  # HARDCODED
            return currentTry
        else:
            currentPossibleSolutions = adjustPossibleSolutions(
                currentPossibleSolutions, currentExpression, similitud)

            if len(currentPossibleSolutions) <= 2:
                currentExpression = currentPossibleSolutions[0]
            else:
                currentExpression = findBestInput(
                    validInputs, currentPossibleSolutions)
        currentTry += 1

    return 6  # En caso de que no la adivine en 6 intentos


def main():
    opener = "12-8=4"  # Se cambia a mano según que expresión se quiera ver
    Niterations = 1000
    global patterns
    patterns = generateAllPatterns()

    statistics = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
    validInputs, validSolutions = readData()

    for i in range(Niterations):
        print("{})".format(i))

        finishedAt = playGame(opener, validInputs, validSolutions)
        statistics[str(finishedAt)] += 1

    print(statistics)


if __name__ == "__main__":
    main()
