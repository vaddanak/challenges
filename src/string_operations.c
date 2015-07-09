
#include <iostream>
#include <cstdlib>


const char * something(const char * msg = "None") {

	return "hello folks";
}

char * my_strcpy(char *t, char *s) {

	return t;
}

size_t stash(const char * const p) {
	return 0;
}


int main(int argc, char** argv) {


	std::cout <<something() <<std::endl;

	return 0;
}


