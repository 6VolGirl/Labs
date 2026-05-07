// Sem3_laba3_WinAPI_File.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
/*Разработайте программу, записывающую побитовое представление числа `double` (IEEE 754) в файл.  
  Выведите в консоль и файл отдельные поля: знак, экспоненту и мантиссу.  
  Проверьте корректность работы на тестовых значениях.*/

#include <iostream>
#include <fstream>
#include <windows.h>
#include <stdio.h>


using namespace std;


void WriteCharArrayToFile(const char* fileName, double num) {
    HANDLE hFile = CreateFileA(fileName, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

    if (hFile == INVALID_HANDLE_VALUE) {
        printf("Error create file.\n");
        return;
    }
    int size_bits = sizeof(num);

    unsigned char* ptr = (unsigned char*)&num;
    char data[33];
    int schetchic = 0;
    for (int i = size_bits - 1; i >= 0; i--)
    {
        for (int j = 7; j >= 0; j--) 
        {
            char byte = (ptr[i] >> j)   & 1;
            printf("%u", byte);
            data[schetchic] = byte;
            schetchic++;
        }
    }
    puts("");

    data[32] = '\0';
    char buff[256];
    sprintf_s(buff, "Bits of the number : %s", data);

    DWORD written;
    BOOL result = WriteFile(hFile, buff, strlen(buff), &written, NULL);



    CloseHandle(hFile);
}

typedef union {
    double value;
    struct {
        unsigned long long  mantissa : 52;
        unsigned long long exponent : 11;
        unsigned long long  sign : 1;
    } bits;
} FloatUnion;

string binaryStructure(unsigned long long number, int bits) {
    string buff;
    for (int i = bits - 1; i >= 0; i--) {
        printf("%u", (number >> i) & 1);
        buff += (((number >> i) & 1)?'1':'0');
    }
    puts("");
    return buff;
}


void BitsOfNumberWriteToFile(const char* filename, double num) {
    ofstream out;
    out.open(filename);
    FloatUnion f{};
    f.value = num;
    string buffer;
    buffer = binaryStructure(f.bits.sign, 1);
    out << "Sing: " << buffer << endl;
    buffer.clear();

    buffer = binaryStructure(f.bits.exponent, 11);
    out << "Exponent: " << buffer << endl;
    buffer.clear();

    buffer = binaryStructure(f.bits.sign, 52);
    out << "Mantisa: " << buffer << endl;
    buffer.clear();


    out.close();


}

int main()
{
    const char* filename = "bum.txt";
    double number = -1.5;
    BitsOfNumberWriteToFile(filename, number);

    return 0;
}