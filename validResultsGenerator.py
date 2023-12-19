import re
import os


def createTXTFile(validSolutions):
    if os.path.exists("validSolutions8.txt"):
        os.remove("validSolutions8.txt")

    with open("validSolutions8.txt", "a") as f:
        for expression in validSolutions:
            f.write(expression + "\n")

        pass


def readValidInputs():
    if os.path.exists("validInputs8.txt"):
        with open("validInputs8.txt", "r") as f:
            validInputs = [line[:-1] for line in f]
            pass
    else:
        raise Exception("No validInputs8.txt file found")

    return validInputs


def isValidSolution(expression, avoidedPatterns):

    if avoidedPatterns.search(expression):
        return False
    else:
        return True


def main():

    validInputs = readValidInputs()

    """ 
    Cases in which the eq is not a valid solution>
    1) ^[+*/-=0]
    2) [+-][+-]
    3) [=][-+/*]
    4) [+*/][+/]
    5) [+/*][*]
    6) [=][\d-]+[*+-/]
    7) [\D]0\d
    8) [\D]0[\D]

     """
    avoidedPatterns = re.compile(
        r'(^[-+*/=0]|[\D]0[\D]|[+-][+-]|[=][-+/*]|[+*/][-+/]|[+/*][*]|[=][\d-]+[*+-/]|[\D]0\d)')

    possibleSolutions = [
        expression for expression in validInputs if isValidSolution(expression, avoidedPatterns)]

    createTXTFile(possibleSolutions)


if __name__ == "__main__":
    main()
