
#include <iostream>
#include <cstdlib>
#include <wchar.h>

wchar_t *my_wstrchr(wchar_t *ws, wchar_t wc) {
	return 0;
}


const char * something(const char * msg = "None") {

	return "hello folks";
}

char * my_strcpy(char *t, char *s) {

	return t;
}

size_t stash(const char * const p) {
	return 0;
}

const char * my_strcat(char * dest, const char * source) {

	return "None";
}


//visible only with wchar_support branch
/* wide character strlen function */
size_t my_wstrlen(const wchar_t *s) {

	return 0;
}



int main(int argc, char** argv) {


	std::cout <<something() <<std::endl;

	return 0;
}
//hi home

