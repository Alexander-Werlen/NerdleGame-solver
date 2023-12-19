import math
import itertools
from nerdleGameSolver import calculatePx, checkPattern
import matplotlib.pyplot as plt


def calculateInformationVariables(expression, possibleSolutions, patterns):
    """ 
    E[i] = sumatoria(p(x)*log2(1/p(x))) 
    Donde:
    x = patron de similitud
    p(x) = (N de eq posibles con el patron x dado) / (N total de eq) 
    """
    patternsInfo = []

    EinfoOfExpression = 0

    for pattern in patterns:
        Px = calculatePx(pattern, expression, possibleSolutions)
        if Px != 0:  # Avoiding division by 0
            EinfoOfExpression += Px*math.log((1/Px), 2)
            patternsInfo.append((pattern, Px, Px*math.log((1/Px), 2)))
        else:
            patternsInfo.append((pattern, 0, 0))

    return EinfoOfExpression, patternsInfo


def main():
    with open("validSolutions.txt", "r") as f:
        possibleSolutions = []

        for expression in f:
            possibleSolutions.append(expression[:-1])

    numberOfTiles = 6  # HARDCODED

    patterns = []

    def foo(l, numberOfTiles):
        yield from itertools.product(*([l] * numberOfTiles))

    for x in foo("012", numberOfTiles):
        patterns.append(x)

    ####
    expression = "12-8=4"
    Einfo, patternsInfo = calculateInformationVariables(
        expression, possibleSolutions, patterns)

    def sortingKey(e):
        return e[2]

    patternsInfo.sort(reverse=True, key=sortingKey)

    # Plotting
    plt.plot([pattern[2]
              for pattern in patternsInfo])
    plt.title('Einfo of {} for: {}'.format(str(round(Einfo, 3)), expression))
    plt.show()

    return


if __name__ == "__main__":
    main()
