/*
Author: Vaddanak Seng
File: hello_coin.cpp
Purpose: Calculate the probability of getting at most H heads.
Date: 2015/07/29
*/


#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <cstdio>

// size_type find( CharT ch, size_type pos = 0 ) const; //string
//  long int strtol(const char *nptr, char **endptr, int base); // cstdlib
//  double strtod(const char *nptr, char **endptr); // cstdlib
// double pow(double x, double y); // cmath

long int factorial(int num);

typedef long int (*foo)(int);

typedef struct data {
	int trials;
	int heads;
} data_type;


/*
PURPOSE: Program execution starts here!
PRECON:
POSTCON:
*/
int main(int argc, char **args) {
	foo fn = factorial;
	std::string input;
	
	std::getline(std::cin, input); //get number of cases
	int cases = std::strtol(input.c_str(), 0, 10); // convert to int type
	
	std::vector<data_type> store; //trials and heads for each case
	
	for(int i = 0; i < cases; ++i) { //loop and get data for each case		
		std::getline(std::cin, input);
		std::string::size_type pos = input.find(' ');		
		
		data_type dt = { //extract trials and heads and store in struct object
			int(std::strtol(std::string(input.begin(),input.begin()+pos).c_str(),
				0,10)), 
			int(std::strtol(std::string(input.begin()+pos, input.end()).c_str(),
				0,10)) };
				
		store.push_back(dt);
	}
	
	
	for(size_t i = 0; i < store.size(); ++i) { //loop for each case
		//std::cout <<store[i].trials <<" " <<store[i].heads <<std::endl;
		double sum = 0.0;
		for(int j = 0; j < store[i].heads+1; ++j) {//add prob for each head count
			sum += (fn(store[i].trials) / (fn(j) * fn(store[i].trials - j))) *
				std::pow(0.5,j) * std::pow(0.5, store[i].trials-j) ;
		
		}
		//std::cout <<sum <<std::endl;
		std::printf("%.4f\n", sum);
	}

	return 0;
}

/*
PURPOSE: Fn calculates factorial of num.  num!
PRECON: "num" is unsigned.
POSTCON: Fn returns num!
*/
long int factorial(int num) {
	if(num>1) {
		return num * factorial(num-1);
	}
	return 1;
}

















