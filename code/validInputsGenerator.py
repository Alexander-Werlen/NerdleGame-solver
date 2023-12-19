import itertools
import os
import re


def isValidInput(expression, avoidedPatterns):
    """ 
    Cases in which the eq is not a valid input:
    0A) tiene más o menos de un =
    0B) el lado de la izquierda no da el resultado de la derecha
    1) ^[*/=]
    2) [=][/*]
    3) [+/][*/]
    4) [=][\d-+]+[*+-/]
     """

    split = expression.split("=")
    if len(split) != 2:
        return False

    try:
        if eval(split[0]) != eval(split[1]):
            return False

    except Exception:
        return False

    if avoidedPatterns.search(expression):
        return False
    else:
        return True


def getAllPossibleStrings(possibleCharacters, numberOfTiles):
    # Funtion creates a txt file with all possible strings written on it by line
    # Input possibleCharacters is a string with all the possible characters without any split Ex: "1234567890=+*-/"

    avoidedPatterns = re.compile(
        r'(^[*/=]|[=][/*]|[+/][*/]|[=][\d+-]+[*+-/])')

    if os.path.exists("possibleInputs8.txt"):
        os.remove("possibleInputs8.txt")

    with open("possibleInputs8.txt", "a") as f:

        def foo(l, numberOfTiles):
            yield from itertools.product(*([l] * numberOfTiles))

        for x in foo(possibleCharacters, numberOfTiles):
            expression = ''.join(x)

            if isValidInput(expression, avoidedPatterns):

                f.write(expression + "\n")

        pass

    return


def main():
    getAllPossibleStrings("0123456789+-*/=", 8)

    return


if __name__ == "__main__":
    main()
