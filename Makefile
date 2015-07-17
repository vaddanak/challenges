
### VARIABLES
javabin = ./resources/javadir/jdk1.8.0_45/bin

### HINTS
# "cat .git/refs/heads/master" shows head of master branch, ie a commit id
gituser:
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
		./my_codes/right_triangle/*.java \
		./my_codes/right_triangle/*.cpp ./my_codes/right_triangle/*.h \
		./my_codes/hailo/*.txt \
		./my_codes/hailo/*.py ./my_codes/hailo/*.java \
		./my_codes/hailo/*.cpp ./my_codes/hailo/*.h \
		./my_codes/pebbles/*.txt \
		./my_codes/fibonacci/*.txt \
		./my_codes/reverse/*.txt \
		./my_codes/smoke_signals/*.txt \
		./my_codes/hello_coin/*.txt \
		./my_codes/knights_and_knaves/*.txt \
		./my_codes/hello_world/*.txt \
		& #
		
# convert python3 to python2; original python3 file stored as pyfile.py.bak
# and python2 converted file stored as pyfile.py per the -w flag		
convert:#convert python3 to python2
	@./resources/3to2	-w ./my_codes/palindrome/palindrome.py
	
py:# run python program
	@python ./my_codes/${id}/right_triangle.py
	
		
### VARIABLES	
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
	
### extract source code files on Gateway Laptop
# Cloudstack contains 5830 java files	
countJavaCloudFiles = $$(find ./resources/sourceCode/apache-cloudstack-4.5.1-src \
	-type f | grep --color -E '.*(.{1}java)$$' | wc -l)
javaCloudFiles = $$(find ./resources/sourceCode/apache-cloudstack-4.5.1-src \
	-type f | grep --color -E '.*(.{1}java)$$' | sed '1,20!d')
	#read?
# Cloudstack contains 341 python files	
countPythonCloudFiles = $$(find ./resources/sourceCode/apache-cloudstack-4.5.1-src \
	-type f | grep --color -E '.*(.{1}py)$$' | wc -l)
pythonCloudFiles = $$(find ./resources/sourceCode/apache-cloudstack-4.5.1-src \
	-type f | grep --color -E '.*(.{1}py)$$' | sed -n '1,20p')
	#read?
# MySQL Connector contains 322 java files
javaMysqlConnFiles = $$(find \
	./resources/sourceCode/mysql-connector-java-5.1.35 \
	-type f | grep --color -E '.*(.{1}java)$$' | sed '1,20!d')
	#read?
# MySQL Connector contains 107 python files
pythonMysqlConnFiles = $$(find \
	./resources/sourceCode/mysql-connector-python-2.0.4 \
	-type f | grep --color -E '.*(.{1}py)$$' | sed -n '1,20p')
	#read?
# MySQL Connector contains 195 C++ files
cppMysqlConnFiles = $$(find \
	./resources/sourceCode/mysql-connector-c++-1.1.6 \
	-type f | grep --color -E '.*(.cpp|.h|.c)$$' | sed '1,20!d')
	#read?
studyjava:
	#@echo ${countPythonFiles}	
	@gedit --new-window ${javaCloudFiles} & #read? AddIpToVmNicTest.java 
	@gedit --new-window ${javaMysqlConnFiles} & #read?
studypython:
	@gedit --new-window ${pythonCloudFiles} & #read?
	@gedit --new-window ${pythonMysqlConnFiles} & #read?
studycpp:
	@gedit --new-window ${cppMysqlConnFiles} & #read?
	
	























