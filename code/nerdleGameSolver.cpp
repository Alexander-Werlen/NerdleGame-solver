#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include <algorithm>

using namespace std;

string possibleSolutions8[17723];
map<string, int> PxAuxiliarMatchingTable; //key=Pattern+Expresion, value: numberOfMatchingExpressions

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

string generatePattern(int idxE1, int idxE2){
    string pattern="";
    for (int i = 0; i < 8; i++)
    {
        if(possibleSolutions8[idxE1]==possibleSolutions8[idxE2]) pattern+="2";
        else if(possibleSolutions8[idxE1].find(possibleSolutions8[idxE2][i]) != std::string::npos) pattern+="1";
        else pattern+="0";
    }
    return pattern;
}

void preComputePxAuxiliarTable() {
    for(int idxExpresionFija = 0; idxExpresionFija<17723; idxExpresionFija++){
        if(idxExpresionFija%500==0)cout<<idxExpresionFija<<"/17723"<<endl;
        for(int idxExpresionMovil = 0; idxExpresionMovil<17723; idxExpresionMovil++){
            string pattern = generatePattern(idxExpresionFija, idxExpresionMovil);
            PxAuxiliarMatchingTable[pattern+possibleSolutions8[idxExpresionFija]]++;
        }
    }
}

float calculatePx(string pattern, string currentExpression)
{
    if(PxAuxiliarMatchingTable.find(pattern+currentExpression)!=PxAuxiliarMatchingTable.end()) return (float)PxAuxiliarMatchingTable[pattern+currentExpression] / 17723;
    else return 0;
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
        float Px = calculatePx(patterns[i], expression);

        if (Px != 0.0f)
        {
            EinfoOfExpression += Px * log2(1 / Px);
        }
    }

    return EinfoOfExpression;
}

bool customSortFunc(string info1[2], string info2[2]){
    return true;
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
    MyReadFile.close();

    // Generating array of possible patterns
    for (int i = 0; i < 3; i++)
    {
        createPatternsRecursionFunction("", simbolosPatronSimilitud[i]);
    }

    cout<<"STARTED precomputing PxAuxiliarTable"<<endl; //LOGGING
    preComputePxAuxiliarTable();
    cout<<"FINISHED precomputing PxAuxiliarTable"<<endl;

    cout<<"STARTED computing Einfo of expressions"<<endl;
    // Calculating information given every equation
    vector<pair<float, int>> informationList; 

    for (int i = 0; i < 17723; i++)
    {
        if(i%500==0) cout<<i<<"/17723"<<endl; //LOGGING

        string expression = possibleSolutions8[i];
        float EInfoOfExpression = calculateInformationVariables(expression, possibleSolutions8, patterns);

        informationList.push_back({EInfoOfExpression, i});
    }

    sort(informationList.rbegin(), informationList.rend());

    //saving data in .txt
    ofstream OutputFile("GuessesEinfo8.txt");
    for (int i = 0; i < 17723; i++)
    {
        OutputFile<<possibleSolutions8[informationList[i].second]<<": "<<informationList[i].first<<endl;
    }
    OutputFile.close();
    
    return 0;
}