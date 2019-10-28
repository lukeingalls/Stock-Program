#ifndef STOCK
#define STOCK

#include <string>
#include <fstream>
#include <iostream>
#include <list>
#include <stdlib.h>

struct date {
	int y;
	int d;
	int m;
};

class Stock
{
public:
	std::list<date> t_stamp;
	std::list<float> open;
	std::list<float> high;
	std::list<float> low;
	std::list<float> close;
	std::list<float> adj_close;
	std::list<unsigned int> volume;
	int items;

	Stock(std::string);
	~Stock();
	void generate_plot();
private:
};

#endif