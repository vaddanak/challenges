
### 
edit:
	@sudo gedit \
		.git/config .git/info/exclude \
		Makefile \
		string.c \
		&#

file:
	@g++ -Wall string.c

run:
	@valgrind --leak-check=full ./a.out
