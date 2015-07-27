/*
Author: Vaddanak Seng
File: smoke_signals.cpp
Purpose: Complete a program which converts a binary sequence to ASCII.
Date: 2015/07/27
*/



#include <iostream>
#include <string>
#include <cstdlib> // long int strtol(const char*, char**, int)



int main(int argc, char **args) {


	std::string input;
	std::cin >>input;

	const int asciiBinaryLength = 7;

		
	for(const char *p = input.c_str(), *pp = p; 
		p < pp+input.size(); p+=asciiBinaryLength) 
		
		std::cout 
			<<char(std::strtol(std::string(p, p+asciiBinaryLength).c_str(),0,2));
	

	return 0;
}
