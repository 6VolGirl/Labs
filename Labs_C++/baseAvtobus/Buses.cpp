#include "Buses.h"
#include <fstream>
#include <iostream>
#include <regex>
//#include <codecvt>

void Buses::addBus(Bus b)
{
	mapBus[b.number] = b;
}

void Buses::deleteBus(int num)
{
	mapBus.erase(num);
}

vector<vector<wstring>> Buses::outStrings()
{
	vector<vector<wstring>> out;

	for (auto iter1:mapBus)                                //(auto iter1 = ...begin(); iter1 != ...end(); iter1++)
	{
		vector<wstring> element;
		element.push_back(to_wstring(iter1.second.number));
		element.push_back(iter1.second.beggining);
		element.push_back(iter1.second.finishing);
		element.push_back(iter1.second.type);
		element.push_back(to_wstring(iter1.second.base));

		out.push_back(element);
	}
	return out;
}

void Buses::openFile(wstring fileName)
{
    wifstream fileBus;

    fileBus.open(fileName);
    if (!fileBus.is_open())
    {
        cout << "The file is not open" << endl;
    }
    else
    {
        wstring info;
        wregex r = wregex(LR"((\d+),\s*([a-zA-Z]+),\s*([a-zA-Z]+),\s*([a-zA-Z]+),\s*(\d+))");       // проверка вида 
        while (getline(fileBus, info))
        {
            if (info.empty())
                break;
            wsmatch match;                               // сюда будет считывается часть строки, которая совпала с r
            regex_search(info, match, r);
            wstring test = match[0];
            if (!(test.empty()))
            {
                Bus element;
                element.number = stoi(match[1]);
                element.beggining = match[2];
                element.finishing = match[3];
                element.type = match[4];
                element.base = stoi(match[5]);
                addBus(element);
            }
        }
    }
    fileBus.close();
}

void Buses::saveFile(wstring fileName)
{
    wofstream fileBus;

    fileBus.open(fileName);
    if (!fileBus.is_open())
    {
        cout << "The file is not open" << endl;
    }
    else
    {
        for (auto iter = mapBus.begin(); iter != mapBus.end(); iter++)
        {
            fileBus << iter->second.number << L", " << iter->second.beggining << L", " << iter->second.finishing << L", " << iter->second.type << L", " << iter->second.base << endl;
        }
    }
    fileBus.close();
}

void Buses::newBase()
{
    mapBus.clear();
}

vector<wstring> Buses::findRoute(int numb)
{
    vector<wstring> route;
    route.push_back(mapBus[numb].beggining);
    route.push_back(mapBus[numb].finishing);
    return route;
}

vector<wstring> Buses::identicalStops(wstring stop)
{
    vector<wstring> count;
    for (auto iter = mapBus.begin(); iter != mapBus.end(); iter++)
    {
        if (iter->second.beggining == stop || iter->second.finishing == stop)
        {
            count.push_back(to_wstring(iter->second.number));
        }
    }
    return count;
}

vector<pair<wstring, wstring>> Buses::routeOfBase(int base)
{
    vector<pair<wstring, wstring>> list;
    for (auto iter = mapBus.begin(); iter != mapBus.end(); iter++)
    {
        if (iter->second.base == base)
        {
            pair<wstring, wstring > element = { iter->second.beggining, iter->second.finishing };
            list.push_back(element);
        }
    }
    return list;
}

void Buses::clearMap()
{
    mapBus.clear();
}
