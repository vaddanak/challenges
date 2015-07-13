/*
Author:  Vaddanak Seng
File:  palindrome.cpp
Purpose:  Determine if user input is a palindrome.
*/

#include <iostream>
#include <string>
//#include "palindrome.h"
#include <sstream>


int main(int argc, char** args) {

	std::stringstream ss;
	size_t result = 0;
	std::string input;
	std::getline(std::cin, input);
	
	const char *start = input.c_str(), *p = start + input.size() - 1;
	
	for( ; p >= start; --p )
		ss <<*p;

	if(input == ss.str())
		result = 1;
	

	//std::cout <<result <<std::endl;
	std::cout <<result;
}
