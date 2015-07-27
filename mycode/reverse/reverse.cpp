/*
Author: Vaddanak Seng
File: reverse.cpp
Purpose: Given two positive integers, reverse them (58 = 85), add them together,
	then reverse the final answer.
Date: 2015/07/25
*/


#include <iostream>
#include <string>
#include <algorithm> // std::reverse
#include <cstdlib> // long int strtol(const char*, char**, int)
#include <sstream> // stringstream



int main(int argc, char **args) {

	std::string input1, input2;
	
	std::cin >>input1 >>input2; // get input
	
	//std::cout <<input1 <<" " <<input2 <<std::endl;

	std::reverse(input1.begin(), input1.end()); // reverse characters
	std::reverse(input2.begin(), input2.end());
	
	std::stringstream ss;
	// find sum
	ss <<(std::strtol(input1.c_str(),0,10) + std::strtol(input2.c_str(),0,10));
	
	std::string result = ss.str();
	std::reverse(result.begin(), result.end());
	
	std::cout <<result;


	return 0;
}
