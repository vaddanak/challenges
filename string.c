
#include <iostream>
#include <cstdlib>


const char * something(const char * msg = "None") {

	return "hello folks";
}

char * my_strcpy(char *t, char *s) {

	return t;
}


int main(int argc, char** argv) {


	std::cout <<something() <<std::endl;

	return 0;
}


