/*
Author: Vaddanak Seng
File: pebbles.cpp
Purpose: Determine probability of pebble color.
*/

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib> //strtol
#include <cctype> //isspace
#include <sstream>

//long int strtol(const char *nptr, char **endptr, int base);
// int isspace(int c);

/*
PURPOSE: Fn separate each number input in string, convert to int, and store
	them as elements in vector.
PRECOND: "numberList" holds number values separated by space. "storage" is
	allocated to hold int type.	
POSTCOND: "storage" contains int elements.
*/
void parse(const std::string& numberList, std::vector<int>& storage) {
	const char *p = numberList.c_str();
	std::stringstream ss;
	
	while(*p) {
		if(std::isspace(*p)) {
			++p;
			continue;
		}		
		ss.str("");
		for( ; *p && !std::isspace(*p); ++p)
			ss <<*p;		
		
		storage.push_back(int(std::strtol(ss.str().c_str(),0,10)));
	}	
}


static const int PREC = 2;

/*
PURPOSE: Program execution starts here.
PRECOND:
POSTCOND:
*/
int main(int argc, char **args) {
	std::string input;
	std::getline(std::cin, input); // get list of colors
	
	int index;
	std::cin >> index; // get index value

	std::vector<int> list;
	parse(input,list); // separate each value into separate int elements
	
	int sum = 0;
	for(size_t i = 0; i < list.size(); ++i)
		sum += list[i]; // add the int elements

	double probability = list[index-1] / double(sum); // calculate probability
	
	std::stringstream ss;
	ss <<probability <<"00"; // ensure at least 2 digits after decimal
	std::string result = ss.str();
	ss.str("");	
	
	const char *p = result.c_str(), *end = 0;
	while(*p && *p != '.') ss <<*p++; // store digits before decimal point
	
	end = p + PREC; // set pointer to second digit after decimal point
	ss<<*p++; // store decimal point
	for(; p <= end; ++p) ss<<*p; // store two digits after decimal point
	
	std::cout <<ss.str();

	return 0;
}

