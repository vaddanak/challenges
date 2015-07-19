

#include <iostream>
#include <vector>


// g++ -Wall -std=c++11 -o my_codes/test my_codes/test.cpp
int main(int argc, char **args) {
	std::vector<int> nums = {1,2,3,4,5};
	
	for(auto&& i: nums) {//??move operation
		std::cout <<i <<" ";//1 2 3 4 5 
		//i = 88;
	}
	std::cout <<std::endl;
	
	for(auto b: nums) {
		std::cout <<b <<" ";//1 2 3 4 5
		//b = 99;
	}	
	std::cout <<std::endl;
	
	for(auto c: nums)
		std::cout <<c <<" ";//1 2 3 4 5
	std::cout <<std::endl;


	return 0;
}



