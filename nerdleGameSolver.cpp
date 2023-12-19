#include <iostream>
#include <fstream>
#include <cmath>
#include <string>

using namespace std;

string possibleSolutions8[17723];

char simbolosPatronSimilitud[3] = {'0', '1', '2'};
string patterns[6561];
int numberOfTiles = 8;
int indexOfPattern = 0;

void createPatternsRecursionFunction(string prevString, char simbol)
{
    string newString = prevString += simbol;
    if (newString.length() < ::numberOfTiles)
    {
        for (int i = 0; i < 3; i++)
        {
            createPatternsRecursionFunction(newString, simbolosPatronSimilitud[i]);
        }
    }
    else
    {
        ::patterns[::indexOfPattern] = newString;
        ::indexOfPattern += 1;
    }
}
bool checkPattern(string pattern, string currentExpression, string expression)
{
    for (int i = 0; i < 8; i++)
    {
        if (pattern[i] == '2' && (currentExpression[i] != expression[i]))
        {
            return false;
        }
        else if (pattern[i] == '0' && (expression.find(currentExpression[i]) != std::string::npos))
        {
            return false;
        }
        else if (pattern[i] == '1' && (currentExpression[i] == expression[i] || expression.find(currentExpression[i]) == std::string::npos))
        {
            return false;
        }
    }

    return true;
}
float calculatePx(string pattern, string currentExpression, string possibleSolutions[17723])
{
    int Nmatches = 0.0f;

    for (int i = 0; i < 17723; i++)
    {
        if (checkPattern(pattern, currentExpression, possibleSolutions[i]))
        {
            Nmatches++;
        }
    }

    return (float)Nmatches / 17723;
}

float calculateInformationVariables(string expression, string possibleSolutions[17723], string patterns[6561])
{
    /*
    E[i] = sumatoria(p(x)*log2(1/p(x)))
    Donde:
    x = patron de similitud
    p(x) = (N de eq posibles con el patron x dado) / (N total de eq)
     */

    float EinfoOfExpression = 0.0f;

    for (int i = 0; i < 6561; i++)
    {
        //cout << patterns[i] << "  Einfo: " << EinfoOfExpression << endl;
        float Px = calculatePx(patterns[i], expression, possibleSolutions);

        if (Px != 0.0f)
        {
            EinfoOfExpression += Px * log2(1 / Px);
        }
    }

    return EinfoOfExpression;
}

int main()
{
    // Reading possible solutions
    string solutionsText;

    ifstream MyReadFile("validSolutions8.txt");

    int indexOfSolutionReading = 0;
    while (getline(MyReadFile, solutionsText))
    {
        possibleSolutions8[indexOfSolutionReading] = solutionsText;
        indexOfSolutionReading++;
    }

    // Generating array of possible patterns
    for (int i = 0; i < 3; i++)
    {
        createPatternsRecursionFunction("", simbolosPatronSimilitud[i]);
    }

    // Calculating information given every equation

    string informationList[17723][2];

    for (int i = 0; i < 17723; i++)
    {
        string expression = possibleSolutions8[i];
        //cout << expression << endl; //###DEBUG
        float EInfoOfExpression = calculateInformationVariables(expression, possibleSolutions8, patterns);

        informationList[i][0] = expression;
        informationList[i][1] = to_string(EInfoOfExpression);

        //cout << expression << " Einfo: " << EInfoOfExpression << endl; //#DEBUG
    }
    return 0;
}