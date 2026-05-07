// Sem 2, lab 2, vectors.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
/*Разработайте программу, которая считывает координаты точек в формате [x-I*y] и сохраняет их в вектор структур Point.
Вычислите евклидовы расстояния от последней введённой точки до всех остальных и отсортируйте их по возрастанию расстояния.
Определите необходимый размер квадратной координатной плоскости, отобрази ось и точки на плоскости.*/

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <regex>
#include <sstream>

using namespace std;

struct Point
{
    double x;
    double y;
};

bool compare(const pair<int, double>& left, const pair<int, double>& right)
{
    return left.second < right.second;
}

int main()
{
   
    vector<Point> points;

    cout << "Enter coordinates 3 points [x-I*y]  ";
    string fulEnter;
    //hjg[9jh -I* 97] d[8-I*4] [7-I*4] kj[2-I*1] [7+I*4]
    //[3-I*20] [4-I*4] [7-I*1] [5-I*2] [-7-I*6] [1-I*1]



    string part;
    regex r(".*\\[(-?\\d+)-I\\*(-?\\d+)\\].*");  // проверка вида 
    while (getline(cin, fulEnter))
    {
        if (fulEnter.empty())
            break;
        istringstream iss(fulEnter);                 //считыватель
        while (iss >> part)                       // пока есть данные
        {
            smatch match;                               // сюда будет считывается часть строки, которая совпала с r
            if (regex_match(part, match, r))
            {
                Point p;
                p.x = stod(match[1]);
                p.y = stod(match[2]);
                points.push_back(p);
            }
            else
            {
                cout << "Input error " << part << endl;
            }
        }
    }
    
    vector<pair<int, double>> dis;
    Point pLast = points.back();                     // последняя введётнная точка
    for (int i = 0; i < points.size() - 1; i++)                 
    {
        Point p1 = points.at(i);              //точка по счёту 
        double distance = sqrt(pow(pLast.x - p1.x, 2) + pow(pLast.y - p1.y, 2));
        dis.push_back(make_pair(i, distance));                          //вектор со значением номера пары и расстояния
        cout << "Distance between the last point and " << i + 1 << " point: " << distance << endl;
    }
 
    sort(dis.begin(), dis.end(), compare);
    cout << "\nDistance has already sorted by distance: " << endl;
    for (const auto pair : dis)
        //(vector<pair<int, double>>::iterator iter = dis.begin(); iter != dis.end(); iter++)            //вывод отсортерованного массива 
    {
        //cout << endl << typeid(iter).name() << endl;
        //cout << typeid(iter).name();
        cout << " Number of pair " << pair.first << " point: " << pair.second << endl;
    }

    //Расчёт размера координатной плоскости
    int n;
    int x_max = 0;
    for (const auto& Point : points)           //проходим по всем элементам вектора points c доступлм к элементам Point
    {
        if (x_max < abs(Point.x))
        {
            x_max = Point.x;
        }
    }

    int y_max = 0;
    for (const auto& Point : points)           //проходим по всем элементам вектора points c доступлм к элементам Point
    {
        if (y_max < abs(Point.x))
        {
            y_max = Point.y;
        }
    }
    
    if (x_max >= abs(y_max))
    {
        n = 2*x_max +4;
    }
    else
    {
        n = 2*y_max + 4;
    }
    
    //n = 100;
    //if (n % 2)                   // делаю n - чётным
    //    n++;


    
    //Вывод координатной плоскости
    char** coordinatePlane = new char* [n];
    for (int i = 0; i < n; i++) 
    {
        coordinatePlane[i] = new char[n];
    }

    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            coordinatePlane[i][j] = ' ';
        }
    }

    for (int j = 0; j < n; j++)
    {
        coordinatePlane[n/2][j] = '|';
    }

    for (int i = 0; i < n; i++)
    {
        coordinatePlane[i][n / 2] = '-';
    }

    for (const auto& Point : points)           //проходим по всем элементам вектора points c доступлм к элементам Point
    {
        int i = Point.x + (n / 2);
        int j = (n / 2) - Point.y;
        coordinatePlane[i][j] = '*';
    }

    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            cout << coordinatePlane[j][i] << " ";
        }
        cout << endl;
    }


    for (int i = 0; i < n; i++) 
    {
        delete[] coordinatePlane[i];
    }
    delete[] coordinatePlane;
    
}

