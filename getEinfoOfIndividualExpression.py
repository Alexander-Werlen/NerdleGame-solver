import math
import itertools


def readData():
    with open("validSolutions8.txt", "r") as f:
        possibleSolutions = []

        for expression in f:
            possibleSolutions.append(expression[:-1])

    return possibleSolutions


def checkPattern(pattern, currentExpression, expression):

    for index, similitud in enumerate(pattern):
        if similitud == "0" and (currentExpression[index] in expression):
            return False
        elif similitud == "1" and (currentExpression[index] == expression[index] or currentExpression[index] not in expression):
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


def main():

    expression = input("Escribí la expression: ")

    numberOfTiles = 8  # HARDCODED

    patterns = []

    def foo(l, numberOfTiles):
        yield from itertools.product(*([l] * numberOfTiles))

    for x in foo("012", numberOfTiles):
        patterns.append(x)

    possibleSolutions = readData()

    print(expression, len(possibleSolutions), len(patterns))

    EinfoOfExpression = calculateInformationVariables(
        expression, possibleSolutions, patterns)

    print("For expression {} info: {}".format(expression, EinfoOfExpression))
    return


if __name__ == "__main__":
    main()
