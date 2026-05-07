// Sem3_laba6_addTask_music.cpp : Определяет точку входа для приложения.
//

/*Разработайте приложение на WinAPI для воспроизведения мелодий через MIDI-устройства с использованием Windows Multimedia API.
Реализуйте чтение нот из файла в формате <нота> <длительность>, преобразование названий нот в MIDI-коды и последовательное воспроизведение с заданной громкостью.
Обеспечьте простой графический интерфейс с кнопкой запуска и корректную обработку сообщений окна.*/


#include <windows.h>
#include <mmsystem.h>
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <map>
#pragma comment(lib, "winmm.lib")
using namespace std;

struct Note
{
    string name; 
    int time;
};

vector<Note> getMelody(string fileName)
{
    bool flag;
    ifstream in;
    in.open(fileName);
    if (in.is_open())
        flag = true;
    else
        flag = false;


    vector<Note> notes;
    string a, b;
    Note help;
    while ( in>>a, in>>b) 
    {
        help.name = a;
        help.time = stoi(b);
        notes.push_back(help);
    }
    in.close();
    return notes;
}

int nameNoteToNum(string name)
{
    map<string, int> notesMyNum;
    notesMyNum["PP"] = 0;
    notesMyNum["C4"] = 60;
    notesMyNum["D4"] = 62;
    notesMyNum["E4"] = 64;
    notesMyNum["F4"] = 65;
    notesMyNum["G4"] = 67;
    notesMyNum["A4"] = 69;
    notesMyNum["H4"] = 71;
    return notesMyNum[name];
}

void playNote(HMIDIOUT hMidiDevice, int note, int time, int volume)
{
    if (note == 0) 
    {
        Sleep(time);
    }
    midiOutShortMsg(hMidiDevice, (volume << 16) | (note << 8) | 0x90);
    Sleep(time);
    midiOutShortMsg(hMidiDevice, (volume << 16) | (note << 8) | 0x80);
}

void playMusic(vector<Note> nts, int volume)
{
    HMIDIOUT hMidiDevice;   //дескриптор
    UINT deviceID = 0;

    MMRESULT result = midiOutOpen(&hMidiDevice, deviceID, 0, 0, CALLBACK_NULL);
    if (result != MMSYSERR_NOERROR)
    {
        MessageBox(NULL, L"Не удалось открыть MIDI-устройство", L"Error!", MB_ICONEXCLAMATION | MB_OK);
    }
    for (auto iter{ nts.begin() }; iter != nts.end(); ++iter)
    {
        playNote(hMidiDevice, nameNoteToNum((*iter).name), (*iter).time, volume);
    }
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch (msg)
    {
    case WM_CREATE:
    {
        CreateWindow(TEXT("BUTTON"), TEXT("PLAY"), WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 150, 235, 200, 30, hwnd, (HMENU)4, NULL, NULL);
        return 0;
    }
    case WM_COMMAND: {
        if (LOWORD(wParam) == 4)
        {
            string fileName = "Notes.txt";
            playMusic(getMelody(fileName),127);
        }
    }
    case WM_SIZE: {
        InvalidateRect(hwnd, NULL, TRUE);
        break;
    }
    case WM_CLOSE:
        DestroyWindow(hwnd);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
        return 0;
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    WNDCLASSEX wc = { 0 };
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
    if (!RegisterClassEx(&wc)) {
        MessageBox(NULL, L"Window Registration Failed!", L"Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    HWND hwnd = CreateWindowEx(WS_EX_CLIENTEDGE, L"myWindowClass", L"Music", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 500, 500, NULL, NULL, hInstance, NULL);

    if (hwnd == NULL) {
        MessageBox(NULL, L"Window сreation failed!", L"Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG Msg;
    while (GetMessage(&Msg, NULL, 0, 0) > 0)
    {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }
    return Msg.wParam;
}