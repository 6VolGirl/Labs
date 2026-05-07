// Sem3_laba4_WinAPI_firstWindow.cpp : Определяет точку входа для приложения.
//
/*Разработайте приложение на WinAPI с двумя окнами: главное для ввода параметров (радиус, расстояние, скорости) и отображения модели упругого соударения двух дисков, и второе — для вывода графика зависимости.
Реализуйте расчёт скоростей после удара, отрисовку векторов (до/после) и их проекций с использованием GDI-функций, а также интерактивное обновление сцены при изменении параметров.
Обеспечьте обработку сообщений окон, корректную очистку ресурсов и визуализацию физического процесса в реальном времени.*/
#include <windows.h>
#include <cmath>
#include <string>
#include <stdio.h>

static double radius = 114;
static double distance = 152;
static double speed1 = 76;
static double speed2 = - 76;
static double DX = 200;
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
LRESULT CALLBACK GraphWndProc(HWND, UINT, WPARAM, LPARAM);

void DrawDisk(HDC hdc, int x, int y, int radius) 
{
    for (int dy = -radius; dy <= radius; dy++) 
    {
        int dx = (int)sqrt(radius * radius - dy * dy);
        MoveToEx(hdc, x - dx, y + dy, NULL);
        LineTo(hdc, x + dx + 1, y + dy);
    }
}

void DrawVectorsAndCollisionDetails(HDC hdc, double x1, double x2, double y1, double y2, double dx1, double dy1, double dx2, double dy2, double dx_x1, double dx_y1, double dx_x2, double dx_y2, double dy_x1, double dy_y1, double dy_x2, double dy_y2, int R)
{
    POINT center1 = { (double)x1, (double)(300 + y1) };
    POINT center2 = { (double)x2, (double)(300 + y2) };

    DrawDisk(hdc, center1.x, center1.y, R);
    DrawDisk(hdc, center2.x, center2.y, R);

    HPEN hPenGreen = CreatePen(PS_SOLID, 1, RGB(0, 255, 0)); //Зеленый
    SelectObject(hdc, hPenGreen);
    MoveToEx(hdc, center1.x, center1.y, NULL);
    LineTo(hdc, center2.x, center2.y);

    // Скорости после соударения
    HPEN hPen1 = CreatePen(PS_SOLID, 2, RGB(0, 0, 255)); // Синий             
    HPEN hPen2 = CreatePen(PS_SOLID, 2, RGB(255, 0, 0)); // Красный
    SelectObject(hdc, hPen1);
    MoveToEx(hdc, center1.x, center1.y, NULL);
    LineTo(hdc, center1.x - dx1, center1.y-dy1);     

    SelectObject(hdc, hPen2);
    MoveToEx(hdc, center2.x, center2.y, NULL);
    LineTo(hdc, center2.x - dx2, center2.y - dy2);

    // Пунктиром рисуем проекции скоростей до соударения
    HPEN hPen3 = CreatePen(PS_DOT, 1, RGB(0, 0, 255));   
    HPEN hPen4 = CreatePen(PS_DOT, 1, RGB(255, 0, 0));
    SelectObject(hdc, hPen3);
    MoveToEx(hdc, center1.x, center1.y, NULL);
    LineTo(hdc, center1.x + dx_x1, center1.y + dx_y1);    //

    SelectObject(hdc, hPen4);
    MoveToEx(hdc, center2.x, center2.y, NULL);
    LineTo(hdc, center2.x + dx_x2, center2.y + dx_y2);    

    SelectObject(hdc, hPen3);
    MoveToEx(hdc, center1.x, center1.y, NULL);
    LineTo(hdc, center1.x + dy_x1, center1.y - dy_y1);

    SelectObject(hdc, hPen4);
    MoveToEx(hdc, center2.x, center2.y, NULL);
    LineTo(hdc, center2.x + dy_x2, center2.y - dy_y2);   //

    // Рисуем скорости до соударения
    HPEN hPen5 = CreatePen(PS_SOLID, 1, RGB(0, 0, 255)); // Синий             
    HPEN hPen6 = CreatePen(PS_SOLID, 1, RGB(255, 0, 0)); // Красный
    SelectObject(hdc, hPen5);
    MoveToEx(hdc, center1.x, center1.y, NULL);
    LineTo(hdc, center1.x + speed1, center1.y);

    SelectObject(hdc, hPen6);
    MoveToEx(hdc, center2.x, center2.y, NULL);
    LineTo(hdc, center2.x + speed2, center2.y);

    DeleteObject(hPenGreen);
    DeleteObject(hPen1);
    DeleteObject(hPen2);
    DeleteObject(hPen3);
    DeleteObject(hPen4);
    DeleteObject(hPen5);
    DeleteObject(hPen6);
}

void CalculateAndDrawCollision(HDC hdc, HDC hdcGraph, double R) 
{
    double x1 = -DX / 2 + 400, x2 = DX / 2 + 400;
    double y1 = -distance / 2, y2 = distance / 2;
    double v1 = speed1, v2 = speed2;
    double t = 0, dt = 0.01;
    double test = distance / (2 * (double)R);
    double angle = asin(distance / (2 * (double)R));
    double dx1 = v1 * cos(2 * angle);
    double dy1 = v1 * sin(2 * angle);
    double dx2 = v2 * cos(2 * angle);
    double dy2 = v2 * sin(2 * angle);
    
    double dx_x1 = v1 * cos(angle) * cos(angle);
    double dx_y1 = v1 * cos(angle) * sin(angle);
    double dx_x2 = v2 * cos(angle) * cos(angle);
    double dx_y2 = v2 * cos(angle) * sin(angle);

    double dy_x1 = v1 * sin(angle) * sin(angle);
    double dy_y1 = v1 * sin(angle) * cos(angle);
    double dy_x2 = v2 * sin(angle) * sin(angle);
    double dy_y2 = v2 * sin(angle) * cos(angle);

    if (distance >= 2 * R)
    {
        x1 = 400;
        x2 = 400;
        POINT center1 = { (double)x1, (double)(300 + y1) };
        POINT center2 = { (double)x2, (double)(300 + y2) };

        DrawDisk(hdc, center1.x, center1.y, R);
        DrawDisk(hdc, center2.x, center2.y, R);
        HPEN hPenGreen = CreatePen(PS_SOLID, 1, RGB(0, 255, 0)); //Зеленый
        SelectObject(hdc, hPenGreen);
        MoveToEx(hdc, center1.x, center1.y, NULL);
        LineTo(hdc, center2.x, center2.y);
        HPEN hPen5 = CreatePen(PS_SOLID, 1, RGB(0, 0, 255)); // Синий             
        HPEN hPen6 = CreatePen(PS_SOLID, 1, RGB(255, 0, 0)); // Красный
        SelectObject(hdc, hPen5);
        MoveToEx(hdc, center1.x, center1.y, NULL);
        LineTo(hdc, center1.x + speed1, center1.y);

        SelectObject(hdc, hPen6);
        MoveToEx(hdc, center2.x, center2.y, NULL);
        LineTo(hdc, center2.x - speed2, center2.y);

        DeleteObject(hPenGreen);
        DeleteObject(hPen5);
        DeleteObject(hPen6);
        MessageBox(NULL, L"Расстояние равно или больше двух радиусов. Скорости не изменились", L"Информация", MB_OK | MB_ICONINFORMATION);
        return ;
    }
    while (fabs(sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))) > 2 * R) 
    {
        x1 += v1 * dt;
        x2 += v2 * dt;
        t += dt;
    }

    DrawVectorsAndCollisionDetails(hdc, x1, x2, y1, y2, dx1, dy1, dx2, dy2, dx_x1, dx_y1, dx_x2, dx_y2, dy_x1, dy_y1, dy_x2, dy_y2, R);
}

void DrawGraph(HDC hdc, int centerX, int centerY, double d, int R)
{
    double r = R;
    double step = 0.1;
    double xMax1 = 500;
    double xMax2 = sqrt(4 * r * r - d * d);

    for (double x = 400; x > xMax2; x -= step)
    {
        double y = sqrt(x * x + d * d);
        SetPixel(hdc, centerX + (int)(x), centerY - (int)(y)+2 * R, RGB(0, 0, 255));
    }

    for (double x = xMax2; x < xMax1; x += step)
    {
        double y = x / cos(asin(d / (2 * r)));
        SetPixel(hdc, centerX + (int)(x), centerY - (int)(y)+2 * R, RGB(0, 255, 0));
    }
}

void DrawTicks(HDC hdc, int centerX, int centerY, int tickLength, int tickSpacing) 
{
    HPEN hPen = CreatePen(PS_SOLID, 1, RGB(0, 0, 0));
    SelectObject(hdc, hPen);

    //// Горизонтальные отметки
    //for (int x = centerX; x < 600; x += tickSpacing) {
    //    MoveToEx(hdc, x, centerY - tickLength / 2, NULL);
    //    LineTo(hdc, x, centerY + tickLength / 2);
    //}
    //for (int x = centerX; x > 0; x -= tickSpacing) {
    //    MoveToEx(hdc, x, centerY - tickLength / 2, NULL);
    //    LineTo(hdc, x, centerY + tickLength / 2);
    //}

    //// Вертикальные отметки
    //for (int y = centerY; y < 600; y += tickSpacing) {
    //    MoveToEx(hdc, centerX - tickLength / 2, y, NULL);
    //    LineTo(hdc, centerX + tickLength / 2, y);
    //}
    //for (int y = centerY; y > 0; y -= tickSpacing) {
    //    MoveToEx(hdc, centerX - tickLength / 2, y, NULL);
    //    LineTo(hdc, centerX + tickLength / 2, y);
    //}

    MoveToEx(hdc, centerX+ tickSpacing, centerY - tickLength / 2, NULL);
    LineTo(hdc, centerX + tickSpacing, centerY + tickLength / 2);

    MoveToEx(hdc, centerX - tickLength / 2, centerY - tickSpacing, NULL);
    LineTo(hdc, centerX + tickLength / 2, centerY - tickSpacing);

    DeleteObject(hPen);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) 
{
    MSG msg;
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"MainWnd";

    RegisterClass(&wc);
    HWND hwnd = CreateWindowA("MainWnd", "Collision Simulation", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    wc.lpfnWndProc = GraphWndProc;
    wc.lpszClassName = L"GraphWnd";
    RegisterClass(&wc);
    HWND hwndGraph = CreateWindowA("GraphWnd", "Graph", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 600, 600, NULL, NULL, hInstance, NULL);
    ShowWindow(hwndGraph, nCmdShow);
    UpdateWindow(hwndGraph);

    while (GetMessage(&msg, NULL, 0, 0)) 
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

HWND hwndGr;

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    static HWND hwndGraph;
    HWND hEdit;
    switch (message) 
    {
    case WM_CREATE:
    {
        CreateWindow(L"STATIC", L"Radius, cm    ", WS_VISIBLE | WS_CHILD, 20, 50, 90, 20, hwnd, NULL, GetModuleHandle(NULL), NULL);
        CreateWindow(L"STATIC", L"Distance, cm  ", WS_VISIBLE | WS_CHILD, 20, 70, 90, 20, hwnd, NULL, GetModuleHandle(NULL), NULL);
        CreateWindow(L"STATIC", L"Speed1, cm/c  ", WS_VISIBLE | WS_CHILD, 20, 90, 90, 20, hwnd, NULL, GetModuleHandle(NULL), NULL);
        CreateWindow(L"STATIC", L"Speed2, cm/c  ", WS_VISIBLE | WS_CHILD, 20, 110, 90, 20, hwnd, NULL, GetModuleHandle(NULL), NULL);
        CreateWindow(TEXT("EDIT"), TEXT("3"), WS_CHILD | WS_VISIBLE | WS_BORDER, 110, 50, 50, 20, hwnd, (HMENU)2, NULL, NULL);
        CreateWindow(TEXT("EDIT"), TEXT("4"), WS_CHILD | WS_VISIBLE | WS_BORDER, 110, 70, 50, 20, hwnd, (HMENU)3, NULL, NULL);
        CreateWindow(TEXT("EDIT"), TEXT("2"), WS_CHILD | WS_VISIBLE | WS_BORDER, 110, 90, 50, 20, hwnd, (HMENU)4, NULL, NULL);
        CreateWindow(TEXT("EDIT"), TEXT("3"), WS_CHILD | WS_VISIBLE | WS_BORDER, 110, 110, 50, 20, hwnd, (HMENU)5, NULL, NULL);
        CreateWindow(TEXT("BUTTON"), TEXT("Change"), WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 60, 140, 60, 30, hwnd, (HMENU)1, NULL, NULL);
        hwndGraph = FindWindow(L"GraphWnd", NULL);
        return 0;
    }
    case WM_COMMAND:
    {
        if (LOWORD(wParam) == 1)
        {
            char buffer[256];
            GetWindowTextA(GetDlgItem(hwnd, 2), buffer, 256);
            radius = atof(buffer) * 3.8 * 10;
            GetWindowTextA(GetDlgItem(hwnd, 3), buffer, 256);
            distance = atof(buffer) * 3.8 * 10;
            GetWindowTextA(GetDlgItem(hwnd, 4), buffer, 256);
            speed1 = atof(buffer) * 3.8 * 10;
            GetWindowTextA(GetDlgItem(hwnd, 5), buffer, 256);
            speed2 = - atof(buffer) * 3.8 * 10;
            InvalidateRect(hwnd, NULL, TRUE);
            InvalidateRect(hwndGr, NULL, TRUE);
        }
        return 0;
    }

    case WM_PAINT: 
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        HDC hdcGraph = GetDC(hwndGraph);
        FillRect(hdc, &ps.rcPaint, (HBRUSH)(COLOR_WINDOW + 1)); // Очистка фона
        CalculateAndDrawCollision(hdc, hdcGraph,radius);
        EndPaint(hwnd, &ps);
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

LRESULT CALLBACK GraphWndProc(HWND hwndGr, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message) 
    {
    case WM_CREATE:
    {
        CreateWindow(L"STATIC", L"1 cm", WS_VISIBLE | WS_CHILD, 25, 500, 50, 20, hwndGr, NULL, GetModuleHandle(NULL), NULL);
        CreateWindow(L"STATIC", L"1 c", WS_VISIBLE | WS_CHILD, 35, 525, 50, 20, hwndGr, NULL, GetModuleHandle(NULL), NULL);
        return 0;
    }
    case WM_PAINT: 
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwndGr, &ps);
        RECT rect;
        FillRect(hdc, &ps.rcPaint, (HBRUSH)(COLOR_WINDOW + 1));   // Очистка фона
        GetClientRect(hwndGr, &rect);
        int centerX = 10;
        int centerY = rect.bottom-10;
        // Оси графика
        MoveToEx(hdc, 0, centerY, NULL);
        LineTo(hdc, rect.right, centerY);
        MoveToEx(hdc, centerX, 0, NULL);
        LineTo(hdc, centerX, rect.bottom);
        DrawGraph(hdc, centerX, centerY, distance, radius);
        DrawTicks(hdc, centerX, centerY, 10, 38);
        EndPaint(hwndGr, &ps);
    } break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwndGr, message, wParam, lParam);
    }
    return 0;
}

