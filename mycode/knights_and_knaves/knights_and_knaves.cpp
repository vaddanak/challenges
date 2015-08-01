/*
Author: Vaddanak Seng
File: knights_and_knaves.cpp
Purpose: Determine which person is telling the truth.
Date: 2015/08/01
*/

#include <string>
#include <iostream>
#include <cstdio>

// int scanf(const char *format, ...); //stdio.h
// int sscanf(const char *str, const char *format, ...);

typedef struct {
	char speaker;
	int mTruthCode;
	int vTruthCode;
} dataType;

static const char m = 'm';
static const char v = 'v';

void processData(dataType *data);

/*
PURPOSE: Program execution starts here.
PRECOND:
POSTCOND:
*/
int main(int argc, char **args) {

	std::string line;	
	
	dataType data1 = {'z', 99, 99}, data2 = data1;
	
	std::getline(std::cin, line);
	std::sscanf(line.c_str(), "%c:m%dv%d", &data1.speaker, &data1.mTruthCode,
		&data1.vTruthCode);
				
	//std::cout <<line<<std::endl;
	//std::cout <<data1.speaker <<" " <<data1.mTruthCode <<" " <<data1.vTruthCode
	//	<<std::endl;
			
	processData(&data1);	
	//std::cout <<data1.speaker <<" " <<data1.mTruthCode <<" " <<data1.vTruthCode
	//	<<std::endl;		
				
	std::getline(std::cin, line);
	std::sscanf(line.c_str(), "%c:m%dv%d", &data2.speaker, &data2.mTruthCode,
		&data2.vTruthCode);	
	
	//std::cout <<line<<std::endl;
	//std::cout <<data2.speaker <<" " <<data2.mTruthCode <<" " <<data2.vTruthCode
	//	<<std::endl;
			
	processData(&data2);	
	//std::cout <<data2.speaker <<" " <<data2.mTruthCode <<" " <<data2.vTruthCode
	//	<<std::endl;	
	
	
	if( data1.mTruthCode&data2.mTruthCode && // m1=m2=1 and v1=v2=0
		!(data1.vTruthCode&data2.vTruthCode) &&
		!(data1.vTruthCode^data2.vTruthCode) )
		std::cout <<"m";
	
	else if( data1.vTruthCode&data2.vTruthCode && // v1=v2=1 and m1=m2=0
		!(data1.mTruthCode&data2.mTruthCode) &&
		!(data1.mTruthCode^data2.mTruthCode) )
		std::cout <<"v";
	else
		std::cout <<"u";
	
	return 0;
}

/*
PURPOSE: Fn adjusts data based on liar response.  The speaker tells whether
	the other person is a liar or truthteller.  If speaker announces to be a
	liar, then the other person's "truth code" is the opposite.
PRECOND: "data" holds original input data.  struct object contains members
	speaker, mTruthCode, and vTruthCode.
POSTCOND: "data" member values may be modified.
*/
void processData(dataType *data) {
	if(data->speaker == m) { 
		if(data->mTruthCode == 0) 
			data->vTruthCode = data->vTruthCode?0:1;
	}		
	else if(data->speaker == v) 
		if(!data->vTruthCode)
			data->mTruthCode = data->mTruthCode?0:1;
}






