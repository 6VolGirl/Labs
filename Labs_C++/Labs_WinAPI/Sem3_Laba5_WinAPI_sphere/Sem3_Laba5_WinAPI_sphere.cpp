// Sem3_Laba5_WinAPI_sphere.cpp : Определяет точку входа для приложения.
//
/*Разработайте приложение на WinAPI для визуализации трёхмерной сферы с использованием сферических координат и изометрической проекции.
Реализуйте отрисовку меридианов и параллелей в виде каркасной модели, а также координатных осей для ориентации в пространстве.
Обеспечьте обработку сообщений окна и корректную отрисовку графики через GDI*/

#include <windows.h>
#include <cmath>
#include <Vector>

using namespace std;

struct Point3
{
    double x, y, z;
};

struct Triangle
{
    Point3 a,b,c;
};

const double pi = 3.1415;
const double  dphi = pi / 20;
const double deta = pi / 20;

void DrawSphere(HDC hdc, int centerX, int centerY, double radius) 
{
    const double pi = 3.14159265358979323846;
    const double dPhi = pi / 20;
    const double deta = pi / 20;
    const double sqrt2 = sqrt(2);
    
    vector<vector<Point3>> points_r(21, vector<Point3>(41));
    vector<Triangle> triangles;

    //for (double a = 0, i=0; a <= pi; a += deta, i++) 
    //{
    //    for (double phi = 0, j=0; phi <= 2 * pi; phi += dPhi, j++) 
    //    {
    //        Point3 p;
    //        p.x = static_cast<int>(centerX +  radius * cos(phi) * sin(eta));
    //        p.y = radius * sin(phi) * sin(eta);
    //        p.z = radius * cos(eta);
    //        points_r[i][j] = p;                        
    //        static_cast<int>(centerX + (triangles[j].a.x + triangles[j].a.z / sqrt2));

    //        int n = points_r.size();
    //    }
    //}


    for (int i = 0; i < 20; i++)        
    {
        //итерируемся по горизонтали
        for (int j = 0; j < 40; j++)       
        { 
            Triangle tr1;
            tr1.a = points_r[i][j];
            tr1.b = points_r[i][j + 1];
            tr1.c = points_r[i+1][j];

            Triangle tr2;
            tr2.a = points_r[i+1][j];
            tr2.b = points_r[i+1][j+1];
            tr2.c = points_r[i][j+1];


            triangles.push_back(tr1);
            triangles.push_back(tr2); 
        }
    }

    int n = triangles.size();

        for (int j = 0; j < n; j++)        
        {
            POINT pon1, pon2, pon3;
            pon1.x = static_cast<int>(centerX + (triangles[j].a.x + triangles[j].a.z / sqrt2));
            pon1.y = static_cast<int>(centerY - (triangles[j].a.y + triangles[j].a.z / sqrt2));

            pon2.x = static_cast<int>(centerX + (triangles[j].b.x + triangles[j].b.z / sqrt2));
            pon2.y = static_cast<int>(centerY - (triangles[j].b.y + triangles[j].b.z / sqrt2));

            pon3.x = static_cast<int>(centerX + (triangles[j].c.x + triangles[j].c.z / sqrt2));
            pon3.y = static_cast<int>(centerY - (triangles[j].c.y + triangles[j].c.z / sqrt2));

            POINT mas[3];
            mas[0] = pon1;
            mas[1] = pon2;
            mas[2] = pon3;

            Polygon(hdc, mas, 3);
        }
}


LPSIZE* Y_X = 0;
double MaxsizeX = 0;
double MaxsizeY = 0;
double k = 100;

int XtoDisplayx(double x, double z)
{
    double DX;
    DX = k * (x + z / sqrt(2)) + MaxsizeX / 2;
    if (DX - double(int(DX)) >= 0.5) {
        return int(DX) + 1;
    }
    else
    {
        return int(DX);
    }
}

int YtoDisplayy(double y, double z)
{

    double DY;
    DY = -k * (y + z / sqrt(2)) + MaxsizeY / 2;
    if (DY - double(int(DY)) > 0.5) {
        return int(DY) + 1;
    }
    else
    {
        return int(DY);
    }
}

void meridian(HDC& hdc, double& phi, double& R) 
{
    double deta = pi / 20;
    MoveToEx(hdc, XtoDisplayx(0, 0), YtoDisplayy(R, 0), NULL);
    for (double eta = 0; eta <= 2 * pi; eta += deta) {
        LineTo(hdc, XtoDisplayx(R * sin(eta) * cos(phi - pi / 4), R * sin(eta) * sin(phi)), YtoDisplayy(R * cos(eta), R * sin(eta) * sin(phi + pi / 2)));
    }
}

void parallel(HDC& hdc, double& eta, double& R) {
    double dphi = pi / 20;
    MoveToEx(hdc, XtoDisplayx(R * sin(eta), 0), YtoDisplayy(R * cos(eta), 0), NULL);
    for (double phi = 0; phi <= 2 * pi; phi += dphi)
    {
        LineTo(hdc, XtoDisplayx(R * sin(eta) * cos(phi), R * sin(eta) * sin(phi)), YtoDisplayy(R * cos(eta), R * sin(eta) * sin(phi)));
    }
}

void cords(HDC& hdc) {

    HPEN pen;
    pen = CreatePen(1, 2, RGB(150, 0, 0));
    MoveToEx(hdc, 0, MaxsizeY / 2, NULL);
    LineTo(hdc, MaxsizeX, MaxsizeY / 2);
    MoveToEx(hdc, MaxsizeX / 2, 0, NULL);
    LineTo(hdc, MaxsizeX / 2, MaxsizeY);
    MoveToEx(hdc, MaxsizeY / 2 + MaxsizeX / 2, 0, NULL);
    LineTo(hdc, 0, MaxsizeY / 2 + MaxsizeX / (2));

}





LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) 
{
    static double R = 2;

    switch (msg) 
    {
        case WM_CREATE: 
        {
            //CreateWindow(TEXT("EDIT"), TEXT("3"), WS_CHILD | WS_VISIBLE | WS_BORDER, 50, 50, 100, 20, hwnd, (HMENU)1, NULL, NULL);
            //CreateWindow(TEXT("BUTTON"), TEXT("Change"), WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 50, 80, 100, 30, hwnd, (HMENU)2, NULL, NULL);
            //return 0;
        }
        case WM_COMMAND:
        {
            if (LOWORD(wParam) == 2) 
            {
                char buffer[256];
                GetWindowTextA(GetDlgItem(hwnd, 1), buffer, 256);
                R = atof(buffer)*3.8*10;
                InvalidateRect(hwnd, NULL, TRUE);
                InvalidateRect(hwnd, NULL, TRUE); 
        }
        return 0;
    }
    case WM_PAINT: 
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);

        RECT rect = { 0 };

        GetWindowRect(hwnd, &rect);
        MaxsizeY = rect.bottom - rect.top - 60;
        MaxsizeX = rect.right - rect.left;

        HPEN pen;
        cords(hdc);
        pen = CreatePen(PS_SOLID, 1, RGB(0, 0, 0));
        SelectObject(hdc, pen);
        MoveToEx(hdc, XtoDisplayx(0, 0), YtoDisplayy(R, 0), NULL);
        for (double eta = 0; eta <= pi; eta += deta * 3)
        {
            parallel(hdc, eta, R);
        }
        for (double phi = 0; phi <= pi; phi += dphi * 5)
        {
            meridian(hdc, phi, R);
        }
        double phi = pi / 2;

        pen = CreatePen(PS_SOLID, 1, RGB(255, 0, 0));
        SelectObject(hdc, pen);
        meridian(hdc, phi, R);

        EndPaint(hwnd, &ps);
    }
        break;
    case WM_CLOSE:
        DestroyWindow(hwnd);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    WNDCLASSEX wc;
    HWND hwnd;
    MSG Msg;

    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = L"myWindowClass";
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc)) 
    {
        MessageBox(NULL, L"Window Registration Failed!", L"Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    hwnd = CreateWindowEx(WS_EX_CLIENTEDGE, L"myWindowClass", L"Отрисовка сферы", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);

    if (hwnd == NULL) 
    {
        MessageBox(NULL, L"Window Creation Failed!", L"Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&Msg, NULL, 0, 0) > 0) 
    {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }
    return Msg.wParam;
}