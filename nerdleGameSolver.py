""" 
Before running there must be a txt file containing all the valid Inputs. This file is created by 
running "possibleInputGenerator.py" and "validInputsGenerator.py".
"""

import math
import itertools
import os


def createInfoTxt(infoList):
    if os.path.exists("infoList8.txt"):
        os.remove("infoList8.txt")

    with open("infoList8.txt", "a") as f:
        for expression in infoList:
            f.write("{} {}\n".format(expression[0], expression[1]))

        pass
    return


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

    # Parsing the .txt's into a lists

    # voy a tomar como que las unicas valid inputs son las posibles soluciones. Me veo obligado a esto ya que si no achico el set de posibles opciones se apaga el sol antes de que termine de computar todos los valores
    with open("validSolutions8.txt", "r") as f:
        validInputs = []

        for expression in f:
            # Esto porque como la leo de un txt termina con un /n para el salto de linea. lo cual es indeseable
            validInputs.append(expression[:-1])

        pass

    with open("validSolutions8.txt", "r") as f:
        possibleSolutions = []

        for expression in f:
            possibleSolutions.append(expression[:-1])

    # Calculating possible patterns of similitud
    """ 
    Simbolos de patron de similitud
    0: if sign not in eq
    1: if sign in eq but not in that place
    2: if sign in eq in that place
    """
    numberOfTiles = 8  # HARDCODED

    patterns = []

    def foo(l, numberOfTiles):
        yield from itertools.product(*([l] * numberOfTiles))

    for x in foo("012", numberOfTiles):
        patterns.append(x)

    # Calculating information given by every variable
    informationList = []

    total = len(validInputs)  # DEBUGING

    for expression in validInputs:
        print(round(len(informationList)/total, 3) * 100)  # DEBUGING

        EinfoOfExpression = calculateInformationVariables(
            expression, possibleSolutions, patterns)

        print("{} info: {}".format(expression, EinfoOfExpression))

        informationList.append((expression, EinfoOfExpression))

    # Sorting list

    def sortingKey(e):
        return e[1]

    informationList.sort(key=sortingKey)

    createInfoTxt(informationList)

    return


if __name__ == "__main__":
    main()
