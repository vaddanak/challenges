
### HINTS
# "cat .git/refs/heads/master" shows head of master branch, ie a commit id
edit:
	@sudo gedit --new-window Makefile \
		.git/config .git/info/exclude \		
		./src/string_operations.c \
		&#

vad:
	@gedit --new-window \
		Makefile \
		./resources/3to2 \
		.git/config .git/info/exclude \
		./src/string_operations.c \
		./my_codes/palindrome/problem_description.txt \
		./my_codes/palindrome/palindrome.py \
		./my_codes/palindrome/palindrome3.py \
		&#
		
# convert python3 to python2; original python3 file stored as pyfile.py.bak
# and python2 converted file stored as pyfile.py per the -w flag		
convert:
	@./resources/3to2	-w ./my_codes/palindrome/palindrome.py
		
		
file:
	@g++ -Wall -o ./src/a.out ./src/string_operations.c

run:
	@valgrind --leak-check=full ./src/a.out

