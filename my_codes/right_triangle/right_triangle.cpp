/*
Author: Vaddanak Seng
File: right_triangle.cpp
Purpose: Given any two edge lengths of a right triangle, find the missing third.
*/

#include <cmath>
#include <iostream>
#include <cstdio>
#include <string>
#include <sstream>
#include <cctype>
#include <vector>
#include <cstdlib>

//#include "right_triangle.h"

template <class T>
T add(T a, T b) {
	return a + b;
}


#ifndef __RIGHT_TRIANGLE_H__
enum LEGS { SIDE1 = 1, SIDE2 = 2, HYPOTENUSE = 4};

double calculateLegLength( double side1, double side2, double hypotenuse,
						   size_t givenLegs);
#endif							


int main(int argc, char ** args) {

	
	std::string input;
	std::getline(std::cin, input);//read line of user input

	//split line into words	
	std::vector<std::string> list;//holds 3 side inputs
	std::stringstream ss;
	for(const char *p = input.c_str(); *p; ++p) {
		if(std::isspace(*p)) continue; //skip space
		while(*p && !std::isspace(*p)) {//accepts non-null and not space
			ss <<*p++;
		}
		if( ss.str().size() ) {	//contains a side input	
			list.push_back(ss.str());//store a side input
			ss.str("");	//reset stringstream content to empty
		}
		if(!*p) //prevents segmentation fault
			--p;	
	}
	
	size_t givenLegs = 0;
	double side1 = 0.0, side2 = 0.0, hypotenuse = 0.0, result = 0.0;
		
	if(list[0]!="_") {
		side1 = std::strtod(list[0].c_str(),0);//convert to double
		givenLegs |= SIDE1;//set flag for side1
	}	
	if(list[1]!="_") {
		side2 = std::strtod(list[1].c_str(),0);
		givenLegs |= SIDE2;
	}
	if(list[2]!="_") {
		hypotenuse = std::strtod(list[2].c_str(),0);
		givenLegs |= HYPOTENUSE;
	}	
	
	result = calculateLegLength(side1, side2, hypotenuse, givenLegs);

	//std::cout <<result <<std::endl;
	std::printf("%.3f", result); //it also rounds!
	std::cout <<add<double>(1.1, 2.2) <<std::endl;

	return 0;
}

/*
PURPOSE: Determine length of missing leg of a right triangle when the other
	two legs are given.
PRECON: Parameter givenLegs is bitwise OR of given legs.  For example, if
	side1 and hypotenuse are given, then 
	givenLegs = SIDE1 | HYPOTENUSE
POSTCON: Fn returns side length of unknown leg.
*/
double calculateLegLength( double side1, double side2, double hypotenuse,
							size_t givenLegs)
{
	double result = 0.0;
	
	if( !(givenLegs&SIDE1) ) //side1 is unknown
		result = std::pow(std::pow(hypotenuse,2) - std::pow(side2,2), 0.5);
	else if( !(givenLegs&SIDE2) ) //side2 is unknown
		result = std::pow(std::pow(hypotenuse,2) - std::pow(side1,2), 0.5);
	else if( !(givenLegs&HYPOTENUSE) ) //hypotenuse is unknown
		result = std::pow(std::pow(side1,2) + std::pow(side2,2), 0.5);
		
	return result;
}							










