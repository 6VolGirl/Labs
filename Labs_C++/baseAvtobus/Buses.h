#pragma once
#include <string>
#include <map>
#include <vector>

using namespace std;

struct Bus
{
	int number;
	wstring beggining;
	wstring finishing;
	wstring type;
	int base;
};

class Buses
{
	map<int, Bus> mapBus;
public: 
	void addBus(Bus b);
	void deleteBus(int num);
	vector<vector<wstring>> outStrings();
	void openFile(wstring fileName);
	void saveFile(wstring fileName); 
	void newBase();
	

	vector<wstring> findRoute(int numb);
	vector<wstring> identicalStops(wstring stop);
	vector<pair<wstring, wstring>> routeOfBase(int base);

	void clearMap();
};

