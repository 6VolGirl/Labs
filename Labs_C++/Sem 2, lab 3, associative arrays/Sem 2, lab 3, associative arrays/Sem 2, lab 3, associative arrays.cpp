// Sem 2, lab 3, associative arrays.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
/*Разработайте программу, которая считывает текстовый файл и подсчитывает частоту встречаемости букв латинского алфавита (без учёта регистра).
Реализуйте вывод количество каждой буквы и построение гистограммы, где высота столбцов пропорциональна количеству вхождений каждой буквы.
Организуйте меню для работы с файлами: создание нового файла, открытие существующего для анализа или редактирования (добавление/замена содержимого).*/


#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include<vector>
#include <sstream>

using namespace std;

void readingInformation(vector<string>& text)
{
    ifstream file1;

    file1.open("text1.txt");
    if (!file1.is_open())
    {
        cout << "The file is not open" << endl;

    }
    else
    {
        int iter = 0;
        while (!file1.eof())
        {
            string textLine;
            getline(file1, textLine);
            text.push_back(textLine);
            iter++;
        }
    }
    file1.close();
}

void frequencyOccurrenceLetters(vector<string>& text, map<char, int>& numberLetters)
{
    int n = text.size();
    cout << "Size of text: " << n << endl;

    for (int i = 0; i < 26; i++)
    {
        numberLetters.emplace(65 + i, 0);
    }

    for (int i = 0; i < n; i++)
    {
        string line = text[i];
        for (int j = 0; j < line.size(); j++)
        {
            if (line[j] > 64 && line[j] < 91)
            {
                numberLetters[line[j]] = numberLetters[line[j]] + 1;
            }
            if (line[j] > 96 && line[j] < 123)
            {
                numberLetters[line[j] - 32] = numberLetters[line[j] - 32] + 1;
            }
        }
    }
}

void arrayOutput(map<char, int>& numberLetters)
{
    for (auto iter = numberLetters.begin(); iter != numberLetters.end(); ++iter)                  // map<string, int>::iterator iter;
    {
        cout << iter->first << ": " << iter->second << '\n';
    }
}

void calculationOneDivision(map<char, int>& numberLetters, int size_of_columns, int mas[])
{
    for (int i = 0; i < 26; i++)
    {
        mas[i] = numberLetters[65 + i];
    }


    // расчёт размера одного деления
    int one_division;                 //одно деление
    int max = mas[0];
    for (int i = 0; i < 26; i++)
    {
        if (max < mas[i])
        {
            max = mas[i];
        }
    }

    if (max > size_of_columns)
    {
        one_division = max / size_of_columns + 1;
        for (int i = 0; i < 26; i++)
        {
            mas[i] = mas[i] / one_division;
        }
    }
    else
    {
        one_division = 1;
        size_of_columns = max + 1;
    }
    cout << "The value of one division:" << one_division;
}

void outputHistogram(int size_of_columns, int mas[])                   //Вывод координатной плоскости
{

    char** coordinatePlane = new char* [size_of_columns + 2];
    for (int i = 0; i < size_of_columns + 2; i++)
    {
        coordinatePlane[i] = new char[26];
    }

    for (int i = 0; i < size_of_columns + 2; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            coordinatePlane[i][j] = ' ';
        }
    }

    for (int j = 0; j < 26; j++)
    {
        coordinatePlane[size_of_columns][j] = '-';
        coordinatePlane[size_of_columns + 1][j] = 65 + j;
    }

    for (int j = 0; j < 26; j++)
    {
        for (int i = 0; i < mas[j]; i++)
        {
            coordinatePlane[size_of_columns - 1 - i][j] = '|';
        }
    }


    for (int i = 0; i < size_of_columns + 2; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            cout << coordinatePlane[i][j] << " ";
        }
        cout << endl;
    }


    for (int i = 0; i < size_of_columns + 2; i++)
    {
        delete[] coordinatePlane[i];
    }
    delete[] coordinatePlane;
}

void result_in_file(map<char, int>& numberLetters)
{
    ofstream result;
    if (!result.is_open())
    {
        cout << "File opening error!" << endl;
    }
    else
    {
        cout << "File is opened! " << endl;
        for (auto iter = numberLetters.begin(); iter != numberLetters.end(); ++iter)                  // map<string, int>::iterator iter;
        {
            result << iter->first << ": " << iter->second << '\n';
        }
        result.close();
    }
}

void opening_and_program(string nameFile)
{
    ifstream filePerson;
    filePerson.open(nameFile);
    if (!filePerson.is_open())
    {
        cout << "This file is missing" << endl;
    }
    else
    {
        cout << "File is opened! " << endl;

        vector<string> text;
        map<char, int> numberLetters;
        int iter = 0;
        while (!filePerson.eof())
        {
            string textLine;
            getline(filePerson, textLine);
            text.push_back(textLine);
            iter++;
        }
        frequencyOccurrenceLetters(text, numberLetters);
        arrayOutput(numberLetters);
        cout << "Size of hight of histogram: ";
        int size_of_columns;         // размер высоты выводимого поля
        cin >> size_of_columns;
        int mas[26];
        calculationOneDivision(numberLetters, size_of_columns, mas);
        outputHistogram(size_of_columns, mas);
        filePerson.close();
        result_in_file(numberLetters);
    }
}


void eding(string nameFile)
{
    ifstream filePerson;
    filePerson.open(nameFile);
    if (!filePerson.is_open())
    {
        cout << "This file is missing" << endl;
    }
    else
    {
        cout << "What do you want to add to the file?" << endl;
        vector<string> userInput;
        string informationUser;
        cin.ignore();
        while (getline(cin, informationUser))
        {
            if (informationUser.empty())
                break;
            userInput.push_back(informationUser);
        }
        cout << "If you want to save: ADD or to REPLACE or don't save?" << "\n ADD - A" << "\n REPLACE - R" << "\n No save - N";
        char ans;
        cin >> ans;

        switch (ans)
        {
        case'A':
        {
            ofstream filePerson;
            filePerson.open(nameFile, ios::app);
            if (!filePerson.is_open())
            {
                cout << "File opening error" << endl;
            }
            else
            {
                cout << "File is opened! " << endl;
                for (auto iter : userInput)
                {
                    filePerson << iter << endl;
                }
                filePerson.close();
            }
        }
        case'R':
        {
            ofstream filePerson;
            filePerson.open(nameFile);
            if (!filePerson.is_open())
            {
                cout << "File opening error" << endl;
            }
            else
            {
                cout << "File is opened! " << endl;
                for (auto iter : userInput)
                {
                    filePerson << iter << endl;
                }
                filePerson.close();
            }
        }
        case'N':
        {
            break;
        }
        default:
            cout << "Try again!" << endl;
            break;
        }
    }

    


    
    
}

void create(string nameFile)
{
    ifstream filePerson;
    filePerson.open(nameFile);
    if (!filePerson.is_open())
    {
        cout << "This file is missing" << endl;
    }
    else
    {
        filePerson.close();
        cout << "File is opened! " << endl;
        cout << "What do you want to add to the file?" << endl;
        vector<string> userInput;
        string informationUser;
        cin.ignore();
        while (getline(cin, informationUser))
        {
            if (informationUser.empty())
                break;
            userInput.push_back(informationUser);
        }
        ofstream filePerson;
        filePerson.open(nameFile);
        if (!filePerson.is_open())
        {
            cout << "File opening error" << endl;
        }
        for (auto iter : userInput)
        {
            filePerson << iter << endl;
        }
        filePerson.close();
    }
}



int main()
{

    //vector<string> text;
    //map<char, int> numberLetters;
    //readingInformation(text);
    //frequencyOccurrenceLetters(text, numberLetters);
    //arrayOutput(numberLetters);
    //cout << "Size of hight of histogram: ";
    //int size_of_columns;         // размер высоты выводимого поля
    //cin >> size_of_columns;
    //int mas[26];
    //calculationOneDivision(numberLetters, size_of_columns, mas);
    //outputHistogram(size_of_columns, mas);


    bool flag = true;
    while (flag)
    {
        cout << "What do you want to do?\n" << "Nothing. Goodbye - N\n" << "Open - O\n" << "Create a file - C\n";
        char action;
        cin >> action;
        switch (action)
        {
        case 'N':
            cout << "Thanks for your attention!" << endl;
            return 0;
        case'O':
        {
            cout << "Enter name of file (with .txt): ";
            string nameFile;
            cin >> nameFile;
            cout << "What do you want to do then?\n" << "Start the programm - P\n" << "Edit a file - E\n" << endl;
            char answer;
            cin >> answer;

            switch (answer)
            {
            case 'P':
            {
                ifstream filePerson;
                opening_and_program(nameFile);
                break;
            }
            case'E':
            {
                eding(nameFile);
                break;
            }
            default:
                cout << "Try again!" << endl;
                break;
            }
            break;
        }
        case 'C':
        {
            cout << "Enter name of file (with .txt): ";
            string nameFile;
            cin >> nameFile;
            create(nameFile);
            break;

        }
        default:
            cout << "Try again!" << endl;
            break;
        }

    }
}




