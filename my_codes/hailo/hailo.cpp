/*
Author: Vaddanak Seng
File: hailo.cpp
Purpose: Sort odd numbers in increasing order and even number in decreasing
	order.
*/


#include <iostream>
#include <string>
#include <vector>
#include <algorithm>//std::sort
#include <sstream>//std::stringstream


extern "C" long int strtol (const char* str, char** endptr, int base);//stdlib.h
extern "C++" std::istream& getline (std::istream&  is, std::string& str);
extern "C" int isspace(int c);//ctype.h
//template <class RandomAccessIterator, class Compare>
//  void sort (RandomAccessIterator first, RandomAccessIterator last, Compare comp);

template <class T>
bool compare(T t1, T t2) {
	return t1 > t2; //use for reverse order
}

int main(int argc, char ** args) {

	std::string inputString; //hold user input
	std::vector<int> odds, evens;//
	std::vector<std::string> numbers;//hold each "word" in string
	
	std::getline(std::cin, inputString);//get user input
	
	const char *p1 = inputString.c_str(), *p2 = p1;//set both pointers to first char
	
	for( ; *p1 ; ) {
		for( ; *p1 && isspace(*p1); ++p1) ;//skip spaces
		
		for(p2 = p1; *p2 && !isspace(*p2); ++p2) ;//p2 goes to next space
	
		if(p2 > p1)
			numbers.push_back(std::string(p1, p2));//get word bounded by p1 and p2
		
		p1 = p2;//move p1 to p2 location
	}
	
	long int num;
	for(size_t i = 0; i < numbers.size(); ++i) {
		num = strtol(numbers[i].c_str(),0,10);//convert string to long int
		if(num%2) //condition for odds
			odds.push_back(num);//store odd number in vector called "odds"
		else //rest are evens
			evens.push_back(num);//store even number in vector called "evens"
	}
	
	std::stringstream ss;	
	
	if(odds.size()) {
		std::sort(odds.begin(), odds.end());//sort in increasing order				
		for(size_t i = 0; i < odds.size(); ++i)		
			ss <<odds[i] <<" ";
	}
	
	if(evens.size()) {
		std::sort(evens.begin(), evens.end(), compare<int>);//sort in decreasing order
		for(int *p1 = &evens.front(), *p2 = &evens.back(); p1 <= p2; ++p1)		
			ss <<*p1 <<" ";
	}

	std::string result = ss.str();
	if(result.size())
		*&result.at(result.size()-1) = '\0'; //remove last space
		
	//std::cout <<result;//Mooshak complains "Wrong Answer"!
	std::cout <<result.c_str();//Mooshak approves with "Accepted".  Weird!

	return 0;
}

















