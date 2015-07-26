/*
Author: Vaddanak Seng
File: fibonacci.cpp
Purpose: Print out the first N numbers in the Fibonacci sequence.
Date: 2015/07/25
*/


#include <vector>
#include <iostream>




/*
PURPOSE: Fn generates sequence of fibonacci numbers.
PRECON: "N" is number of values in the fibonacci sequence.  "storage" is
	container that will hold the sequence of numbers.
POSTCOND: "storage" contains N number of values of fibonacci numbers.
*/
void fibo(int N, std::vector<int>& storage) {
	if(N>0) {
		size_t len = storage.size();
		if(len == 0)
			storage.push_back(0);
		else if(len == 1)
			storage.push_back(1);
		else
			storage.push_back(storage[len-1] + storage[len-2]);
	
		fibo(N-1, storage);
	}
}


/*
PURPOSE: Program execution starts here!
PRECON:
POSTCOND:
*/
int main(int argc, char **args) {
	
	int N;
	std::cin >>N;

	std::vector<int> storage;
	fibo(N, storage);
	
	for(size_t i=0, len = storage.size(); i < len; ++i) {
		std::cout <<storage[i];
		if(i < len-1)
			std::cout <<" ";	
	}

	return 0;
}





















