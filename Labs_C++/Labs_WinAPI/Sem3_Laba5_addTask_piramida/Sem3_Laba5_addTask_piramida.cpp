// Sem3_Laba5_addTask_piramida.cpp : Определяет точку входа для приложения.
//
/*Разработайте приложение на WinAPI для визуализации трёхмерной пирамиды (тетраэдра) с изометрической проекцией и рекурсивным разбиением граней.
Реализуйте удаление невидимых граней через проверку нормали, сортировку треугольников по удалённости и заливку с градацией яркости в зависимости от угла к наблюдателю.
Организуйте чтение координат вершин из файла и отрисовку сцены через GDI в ответ на сообщение WM_PAINT.*/

#include <windows.h>
#include <cmath>
#include <vector>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;




class Point3
{
    double x, y, z;

public:
    Point3()
    {
        x = 0;
        y = 0;
        z = 0;
    }
    Point3(double a, double b, double c)
    {
        x = a;
        y = b;
        z = c;
    }

    double getX() { return x; }
    double getY() { return y; }
    double getZ() { return z; }

    Point3 operator- (Point3 n2)
    {
        Point3 result;
        result.x = x - n2.x;
        result.y = y - n2.y;
        result.z = z - n2.z;
        return result;
    }

    friend Point3 operator*(double n1, Point3 n2)
    {
        Point3 result;
        result.x = n1 * n2.x;
        result.y = n1 * n2.y;
        result.z = n1 * n2.z;
        return result;
    }

    friend istream& operator>> (istream& in, Point3& element)
    {
        in >> element.x;
        in >> element.y;
        in >> element.z;
        return in;
    }
    friend ostream& operator<<(ostream& out, const Point3& element)
    {
        return out << element.x << " " << element.y << " " << element.z << " " << endl;
    }

    ~Point3() {};
};
struct Triangle3
{
    Point3 p1, p2, p3, normal;
};
struct Triangle
{
    POINT p1, p2, p3;
    Point3 normal;
};
static vector<Triangle3> trian3;
static vector<Triangle> trian;
static Point3 major;

Point3 normalVec(Point3 vec1, Point3  vec2, Point3 p, Point3 pOut);

vector<Point3> getCoordinatesFile(string fileName)
{
    bool flag;
    //string fileName = "C:\\Users\\6anna\\source\\repos\\Sem3_Laba3_addTask_vectors\\Result.txt";
    ifstream in;
    in.open(fileName);
    if (in.is_open())
        flag = true;
    else
        flag = false;

    string info;
    getline(in, info);


    vector<Point3> tops(4);
    in >> tops[0];
    in >> tops[1];
    in >> tops[2];
    in >> tops[3];

    in.close();

    return tops;
}
vector<POINT> transformateCoords(vector<Point3> tops, int centerX, int centerY, int numTop)
{
    double sqrt2 = sqrt(2);
    vector<POINT> newTops(numTop);

    for (int i = 0; i < numTop; i++)
    {
        newTops[i].x = centerX + 3.8 * (tops[i].getX() + tops[i].getZ() / sqrt2);
        newTops[i].y = centerY - 3.8 * (tops[i].getY() + tops[i].getZ() / sqrt2);
    }
    return newTops;
}

void transformateTrian(int centerX, int centerY)
{
    double sqrt2 = sqrt(2);

    for (auto iter{ trian3.begin() }; iter != trian3.end(); ++iter)
    {
        vector<Point3> tops(4);
        tops[0] = (*iter).p1;
        tops[1] = (*iter).p2;
        tops[2] = (*iter).p3;
        tops[3] = (*iter).normal;

        vector<POINT>  pHelp = transformateCoords(tops, centerX, centerY, 3);
        Triangle trHelp{ pHelp[0], pHelp[1],pHelp[2],tops[3] };
        trian.push_back(trHelp);
    }
}

void drawPiramid(HDC hdc, vector<POINT> tops)
{
    //Рисуем тетраэдр
    POINT mas[3];
    //OAC
    mas[0] = tops[0];
    mas[1] = tops[1];
    mas[2] = tops[3];
    Polygon(hdc, mas, 3);
    //OAB
    mas[2] = tops[2];
    Polygon(hdc, mas, 3);
    //OBC
    mas[1] = tops[2];
    mas[2] = tops[3];
    Polygon(hdc, mas, 3);
}

double distance(Point3 p)
{
    return sqrt(pow(major.getX() - p.getX(), 2) + pow(major.getY() - p.getY(), 2) + pow(major.getZ() - p.getZ(), 2));
}

bool comparator(Triangle3 a, Triangle3 b)
{
    return distance(a.p1) > distance(b.p1);
}

void sortTriangles()
{
    sort(trian3.begin(), trian3.end(), comparator);
}

void DrawTriangle(HDC hdc, POINT p1, POINT p2, POINT p3) {
    POINT vertices[] = { {p1.x, p1.y}, {p2.x, p2.y}, {p3.x, p3.y} };
    Polygon(hdc, vertices, 3);
}

void SubdivideTriangle(HDC hdc, Point3 p1, Point3 p2, Point3 p3, int depth, Point3 pOut) 
{
    if (depth <= 0) 
    {
        Triangle3 tr = { p1, p2, p3, normalVec(p3-p1, p3-p2, p1, pOut)};
        trian3.push_back(tr);
        return;
    }

    Point3 mid1 = { (p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2, (p1.getZ() + p2.getZ()) / 2 };
    Point3 mid2 = { (p2.getX() + p3.getX()) / 2, (p2.getY() + p3.getY()) / 2, (p2.getZ() + p3.getZ()) / 2 };
    Point3 mid3 = { (p3.getX() + p1.getX()) / 2, (p3.getY() + p1.getY()) / 2 ,(p3.getZ() + p1.getZ()) / 2 };

    // Рекурсивно разбиваем каждый из 4-х новых треугольников
    SubdivideTriangle(hdc, p1, mid1, mid3, depth - 1, pOut);
    SubdivideTriangle(hdc, mid1, p2, mid2, depth - 1, pOut);
    SubdivideTriangle(hdc, mid3, mid2, p3, depth - 1, pOut);
    SubdivideTriangle(hdc, mid1, mid2, mid3, depth - 1, pOut);
}

//true, если угол острый
bool scalarProduct(Point3 vec1, Point3  vec2)
{
    bool flag;
    double fl = (vec1.getX() * vec2.getX() + vec1.getY() * vec2.getY() + vec1.getZ() * vec2.getZ());
    if (fl > 0)
        flag = true;
    else
        flag = false;
    return flag;
}
double scalarProd(Point3 vec1, Point3  vec2)
{
    return (vec1.getX() * vec2.getX() + vec1.getY() * vec2.getY() + vec1.getZ() * vec2.getZ());
}
double modul (Point3 vec1)
{
    return sqrt(vec1.getX() * vec1.getX() + vec1.getY() * vec1.getY() + vec1.getZ() * vec1.getZ());
}


Point3 normalVec(Point3 vec1, Point3  vec2, Point3 p, Point3 pOut)
{
    double cofA = vec1.getY() * vec2.getZ() - vec1.getZ() * vec2.getY();
    double cofB = vec1.getZ() * vec2.getX() - vec1.getX() * vec2.getZ();
    double cofC = vec1.getX() * vec2.getY() - vec1.getY() * vec2.getX();
    double cofD = -(p.getX() * cofA + p.getY() * cofB + p.getZ() * cofC);
    Point3 normal{ cofA,cofB, cofC };
    if (!scalarProduct(normal, p - pOut)) // нормаль смотрит вне тетрайдэра
    {
        normal = (-1) * normal;
    }
    return normal;
}

//true рисуем грань
bool checkSide(Point3 vec1, Point3 vec2, Point3 p, Point3 pOut)
{
    Point3 normal = normalVec(vec1, vec2, p, pOut);
    //if (!scalarProduct(normal, p - pOut)) // нормаль смотрит вне тетрайдэра
    //{
    //    normal = (- 1) * normal;
    //}
    if (scalarProduct(normal, major))
        return true;       
    else
        return false;
}

void paintTriangles(HDC hdc)
{
    double color = 0;
    double bul = 255;
    for (auto iter{trian.begin()}; iter != trian.end(); ++iter)
    {
        POINT mas[3];
        mas[0] = (*iter).p1;
        mas[1] = (*iter).p2;
        mas[2] = (*iter).p3;

        //cos считается через скалярное проиведение
        color = 500* pow(scalarProd((*iter).normal, major)/(modul((*iter).normal)*modul(major)),2) ;
        if (color > 255)
            break;

        HBRUSH hBrush = CreateSolidBrush(RGB(color, 0, bul));
        SelectObject(hdc, hBrush);

        Polygon(hdc, mas, 3);
        DeleteObject(hBrush);



        
    }
}

void paintPiramid(HDC hdc, int maxX, int maxY, string fileName)
{
    int centerX = maxX / 2;
    int centerY = maxY / 2;

    //Рисуем оси
    HPEN hPen = CreatePen(PS_SOLID, 1, RGB(0, 0, 0)); 
    SelectObject(hdc, hPen);
    MoveToEx(hdc, centerX, centerY, NULL);
    LineTo(hdc, centerX, centerY - maxY); 
    MoveToEx(hdc, centerX, centerY, NULL); 
    LineTo(hdc, centerX - maxX, centerY + maxX); 
    MoveToEx(hdc, centerX, centerY, NULL);
    LineTo(hdc, centerX + maxX, centerY);

    int tickSpacing = 20;
    int tickLength = 10;

    for (int x = centerX; x < maxX; x += tickSpacing) 
    {
        MoveToEx(hdc, x, centerY - tickLength / 2, NULL);
        LineTo(hdc, x, centerY + tickLength / 2);
    }
    for (int y = centerY; y > 0; y -= tickSpacing) 
    {
        MoveToEx(hdc, centerX - tickLength / 2, y, NULL);
        LineTo(hdc, centerX + tickLength / 2, y);
    }
    for (int x = centerX, y = centerY; x > -maxX; x -= tickSpacing, y += tickSpacing)
    {
        MoveToEx(hdc, x, y - tickLength / 2, NULL);
        LineTo(hdc, x, y + tickLength / 2);
    }
    DeleteObject(hPen);

    vector<Point3> tops = getCoordinatesFile(fileName);
    vector<POINT> nTops = transformateCoords(tops, centerX, centerY, 4);
    drawPiramid(hdc, nTops);

    int depth = 3;

    if (checkSide(tops[1], tops[2], tops[0], tops[3]))
        SubdivideTriangle(hdc, tops[0], tops[1], tops[2], depth, tops[3]);
    if (checkSide(tops[1], tops[3], tops[0], tops[2]))
        SubdivideTriangle(hdc, tops[0], tops[1], tops[3], depth, tops[2]);
    if (checkSide(tops[2], tops[3], tops[0], tops[1]))
        SubdivideTriangle(hdc, tops[0], tops[2], tops[3], depth, tops[1]);
    if (checkSide(tops[3]- tops[1], tops[3] - tops[2], tops[1], tops[0]))
        SubdivideTriangle(hdc, tops[1], tops[2], tops[3], depth, tops[0]);
 
    sortTriangles();
    transformateTrian(centerX, centerY);
    paintTriangles(hdc);

    POINT major2;
    major2.x = centerX + 3.8 * (major.getX() + major.getZ() / sqrt(2));
    major2.y = centerY - 3.8 * (major.getY() + major.getZ() / sqrt(2));
    //HBRUSH hBrush = CreateSolidBrush(RGB(0, 0, 0));
    //SelectObject(hdc, hBrush);
    //Ellipse(hdc, major2.x - 5, major2.y - 5, major2.x + 5, major2.y + 5);
    //DeleteObject(hBrush);

}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_CREATE:
    {

    }break;
    case WM_PAINT:
    {
        string fileName = "C:\\Users\\6anna\\source\\repos\\Sem3_Laba3_addTask_vectors\\Result.txt";

        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        RECT rect;
        GetClientRect(hwnd, &rect);

        major = { 0,0,-100 };
        paintPiramid(hdc, rect.right, rect.bottom, fileName);

    } break;
    case WM_CLOSE:
        DestroyWindow(hwnd);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, message, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    MSG msg;
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"MainWnd";

    RegisterClass(&wc);
    HWND hwnd = CreateWindowA("MainWnd", "Tetrahedron", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return (int)msg.wParam;
}