#include "Stock.hpp"

// This will simply read in the company code and take that file in to this stock instance.
Stock::Stock(std::string company_code) {
	std::ifstream file;
	file.open(company_code + ".csv");
	if (file.is_open()) {
		while (getline(file, company_code, ',') && items++) {
			date d;
			d.m = stoi(company_code.substr(0, company_code.find('-')));
			company_code.erase(0, company_code.find('-') + 1);
			d.d = stoi(company_code.substr(0, company_code.find('-')));
			d.y = stoi(company_code.substr(company_code.length() - 4, company_code.length()));
			getline(file, company_code, ',');
			open.push_front(stof(company_code));
			getline(file, company_code, ',');
			high.push_front(stoi(company_code));
			getline(file, company_code, ',');
			low.push_front(stoi(company_code));
			getline(file, company_code, ',');
			close.push_front(stoi(company_code));
			getline(file, company_code, ',');
			adj_close.push_front(stoi(company_code));
			getline(file, company_code);
			volume.push_front(stoul(company_code));
		}
		file.close();
	} else {
		std::cout << "The file " << company_code << ".csv failed to open. Please try another." << std::endl;
	}
}

Stock::~Stock() {}

void Stock::generate_plot() {
	std::ofstream plot_data;
	plot_data.open("temp.txt");
	int i = 1;
	int i_factor = 0;
	for (std::list<float>::const_iterator iterator = high.begin(), end = high.end(); iterator != end; iterator++, i++) {
		if ((i_factor * 5) + 1 == i) {
			// plot_data << i_factor++ + 1 << " " << *iterator << "\n";
		}
		plot_data << i << " " << *iterator << "\n";
	}
	plot_data.close();
	std::system("gnuplot -p -e \"plot 'temp.txt' using 1:2\"");
}
