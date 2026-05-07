// Sem3_Laba3_addTask_vectors.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
/*Разработайте программу для проверки геометрических свойств трёх векторов в пространстве: коллинеарности и компланарности.
Реализуйте проверку корректности построения пирамиды по трём входным векторам и вычислите координаты её вершин и рёбер.
Организуйте чтение исходных данных из файла и запись результатов расчёта в выходной файл.*/

#include <iostream>
#include <fstream>
#include <vector>


using namespace std;

class Point
{
    double x, y, z;

public:
    Point()
    {
        x = 0;
        y = 0;
        z = 0;
    }
    Point(double a, double b, double c)
    {
        x = a;
        y = b;
        z = c;
    }

    friend ostream& operator<<(ostream& out, const Point& element)
    {
        return out << element.x << " " << element.y << " " << element.z << " " << endl;
    }

    ~Point() {};
};

class Vector
{
    double x, y, z;

public:
    Vector()
    {
        x = 0;
        y = 0;
        z = 0;
    }
    Vector(double a, double b, double c)
    {
        x = a;
        y = b;
        z = c;
    }
    double getX() { return x; }
    double getY() { return y; }
    double getZ() { return z; }

    Vector operator+ (Vector n2)
    {
        Vector result;
        result.x = x + n2.x;
        result.y = y + n2.y;
        result.z = z + n2.z;
        return result;
    }

    Vector operator- (Vector n2)
    {
        Vector result;
        result.x = x - n2.x;
        result.y = y - n2.y;
        result.z = z - n2.z;
        return result;
    }

    bool operator== (Vector n2)
    {
        if ((x == n2.x) && (y == n2.y) && (z == n2.z))
            return true;
        else
            return false;
    }

    friend istream& operator>> (istream& in, Vector& element)
    {
        in >> element.x;
        in >> element.y;
        in >> element.z;
        return in;
    }

    friend ostream& operator<<(ostream& out, const Vector& element)
    {
        return out << element.x << " " << element.y << " " << element.z << " " << endl;
    }
    ~Vector() {}
};

// true = коллинеарны
bool CheckCollinearity(Vector vec1, Vector vec2, Vector vec3)
{
    //определитель: 11*22*33+12*23*31+13*21*32-13*22*31-11*23*32-12*21*33
    double determinant = vec1.getX() * vec2.getY() * vec3.getZ() + vec1.getY() * vec2.getZ() * vec3.getX() + vec1.getZ() * vec2.getX() * vec3.getY() - vec1.getZ() * vec2.getY() * vec3.getX() - vec1.getX() * vec2.getZ() * vec3.getY() - vec1.getY() * vec2.getX() * vec3.getZ();
    if (determinant)
        return false;
    else
        return true;
}

// true = компланарны
bool CheckCoplanarity(Vector vec1, Vector vec2, Vector vec3)
{
    // смешанное произведение (считаем через определитель)
    //определитель: 11*22*33+12*23*31+13*21*32-13*22*31-11*23*32-12*21*33
    double determinant = vec1.getX() * vec2.getY() * vec3.getZ() + vec1.getY() * vec2.getZ() * vec3.getX() + vec1.getZ() * vec2.getX() * vec3.getY() - vec1.getZ() * vec2.getY() * vec3.getX() - vec1.getX() * vec2.getZ() * vec3.getY() - vec1.getY() * vec2.getX() * vec3.getZ();
    double chek = pow(10, -12);
    if ((determinant==0) || (abs(determinant) < pow(10,-12)) )
        return true;
    else
        return false;
}

bool CheckFacesPiramid(vector<Vector> vectors)
{
    bool flag;
    if (CheckCoplanarity(vectors[0], vectors[2], vectors[3]) && CheckCoplanarity(vectors[1], vectors[2], vectors[4]) && CheckCoplanarity(vectors[0], vectors[1], vectors[5]))
        flag = true;
    else
        return false;

    if ((vectors[0] + vectors[5] == vectors[1]) && (vectors[0] + vectors[3] == vectors[2]) && (vectors[1] + vectors[4] == vectors[2]))
        return flag;
    else
        return false;
}


int main()
{
    string fileName = "Vectors.txt";
    ifstream in;
    in.open(fileName);
    if (in.is_open())
    {
        cout << "File was opened successfully!" << endl;
    }
    else
    {
        cout << "File opening error!" << endl;
        return 0;
    }

    Vector vec1, vec2, vec3;
    in >> vec1;
    in >> vec2;
    in >> vec3;

    in.close();

  
    if (CheckCoplanarity(vec1, vec2, vec3))
    {
        cout << "Vectors are Coplanarity" << endl;
        return 0;
    }
    else
        cout << "Vectors aren't Coplanarity" << endl;

    vector<Point> poinsTopPyramid;
    Point o(0, 0, 0);
    Point a(vec1.getX(), vec1.getY(), vec1.getZ());
    Point b(vec2.getX(), vec2.getY(), vec2.getZ());
    Point c(vec3.getX(), vec3.getY(), vec3.getZ());
    poinsTopPyramid.push_back(o);
    poinsTopPyramid.push_back(a);
    poinsTopPyramid.push_back(b);
    poinsTopPyramid.push_back(c);
    
    vector<Vector> vectors;
    vectors.push_back(vec1);
    vectors.push_back(vec2);
    vectors.push_back(vec3);
    vectors.push_back(vec3-vec1);
    vectors.push_back(vec3-vec2);
    vectors.push_back(vec2-vec1);

    if (CheckFacesPiramid(vectors))
    {
        cout << "Correct piramid" << endl;
    }
    else
    {
        cout << "The calculations are wrong" << endl;
        return 0;
    }
    Vector vec_r0(0,0,0);

    ofstream out("Result.txt");

    out << "Coordinates top: " << endl;
    out << poinsTopPyramid[0];
    out << poinsTopPyramid[1];
    out << poinsTopPyramid[2];
    out << poinsTopPyramid[3];

    out << "r01: " << vec_r0;
    out << "r02: " << vec_r0;
    out << "r03: " << vec_r0;
    out << "r04: " << vec1;
    out << "r05: " << vec2;
    out << "r06: " << vec3;

    out << "a1: " << vectors[0];
    out << "a2: " << vectors[1];
    out << "a3: " << vectors[2];
    out << "a4: " << vectors[3];
    out << "a5: " << vectors[4];
    out << "a6: " << vectors[5];

    out.close();
}