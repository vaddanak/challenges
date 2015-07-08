
#include <iostream>
#include <cstdlib>


const char * something() {

	return "hello folks";
}


int main(int argc, char** argv) {


	std::cout <<something() <<std::endl;

	return 0;
}


