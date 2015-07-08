
### HINTS
# "cat .git/refs/heads/master" shows head of master branch, ie a commit id
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

vad:
	@gedit Makefile .git/config .git/info/exclude &
