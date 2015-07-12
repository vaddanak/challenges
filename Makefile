
### HINTS
# "cat .git/refs/heads/master" shows head of master branch, ie a commit id
edit:
	@sudo gedit --new-window \
		.git/config .git/info/exclude \
		Makefile \
		string.c \
		&#

vad:
	@gedit --new-window \
		Makefile \
		./resources/3to2 \
		.git/config .git/info/exclude \
		string_operations.c \
		./palindrome/problem_description.txt \
		./palindrome/palindrome.py \
		./palindrome/palindrome3.py \
		&#
		
# convert python3 to python2; original python3 file stored as pyfile.py.bak
# and python2 converted file stored as pyfile.py per the -w flag		
convert:
	@./resources/3to2	-w ./palindrome/palindrome.py
		
		
file:
	@g++ -Wall -o ./src/a.out ./src/string_operations.c

run:
	@valgrind --leak-check=full ./src/a.out

