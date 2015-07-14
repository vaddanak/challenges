
### VARIABLES
javabin = ./resources/javadir/jdk1.8.0_45/bin

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
		./my_codes/palindrome/*.py \
		./my_codes/palindrome/*.java \
		./my_codes/palindrome/*.cpp ./my_codes/palindrome/*.h \
		./my_codes/right_triangle/problem_description.txt \
		./my_codes/right_triangle/*.py \
		./my_codes/right_triangle/*.cpp ./my_codes/right_triangle/*.h \
		./my_codes/right_triangle/*.java \
		& #
		
# convert python3 to python2; original python3 file stored as pyfile.py.bak
# and python2 converted file stored as pyfile.py per the -w flag		
convert:#convert python3 to python2
	@./resources/3to2	-w ./my_codes/palindrome/palindrome.py
	
py:
	@python ./my_codes/right_triangle/right_triangle.py
	
		
### 	
id = right_triangle
cc:# compile c++ source files
	#@g++ -Wall -o ./src/a.out ./src/string_operations.c
	#@g++ -Wall -o ./my_codes/palindrome/a.out ./my_codes/palindrome/palindrome.cpp
	@g++ -Wall -o ./my_codes/${id}/a.out ./my_codes/${id}/${id}.cpp

rc:# run c++ executable
	#@valgrind --leak-check=full ./src/a.out
	#@valgrind --leak-check=full ./my_codes/palindrome/a.out	
	@valgrind --leak-check=full ./my_codes/${id}/a.out

#example:  @${javabin}/javac ./my_codes/palindrome/palindrome.java
#java doc:  google-chrome ./resources/javadir/jdk1.8.0_45/docs/index.html &
cjava:#compile java
	@${javabin}/javac -help
	#@${javabin}/javac ./my_codes/palindrome/palindrome.java
	@${javabin}/javac ./my_codes/right_triangle/right_triangle.java

#example:  @${javabin}/java -classpath ./my_codes/palindrome: palindrome
rjava:#run java	
	@${javabin}/java -help
	#@${javabin}/java -classpath ./my_codes/palindrome: palindrome
	@${javabin}/java -classpath ./my_codes/right_triangle: right_triangle
	

	
	

