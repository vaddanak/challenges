
### VARIABLES
javabin = ./resources/javadir/jdk1.8.0_45/bin

### HINTS
# "cat .git/refs/heads/master" shows head of master branch, ie a commit id
gituser:
	@gedit --new-window Makefile \
		.git/config .git/info/exclude \
		./src/string_operations.c \
		& #
		
mycodeDir = /home/vad/challenges/mycode
vad:
	@gedit --new-window \
		Makefile \
		./resources/3to2 \
		.git/config .git/info/exclude \
		./src/string_operations.c \
		${mycodeDir}/palindrome/problem_description.txt \
		${mycodeDir}/palindrome/*.py \
		${mycodeDir}/palindrome/*.java \
		${mycodeDir}/palindrome/*.cpp ${mycodeDir}/palindrome/*.h \
		${mycodeDir}/right_triangle/problem_description.txt \
		${mycodeDir}/right_triangle/*.py \
		${mycodeDir}/right_triangle/*.java \
		${mycodeDir}/right_triangle/*.cpp ${mycodeDir}/right_triangle/*.h \
		${mycodeDir}/hailo/*.txt \
		${mycodeDir}/hailo/*.py ${mycodeDir}/hailo/*.java \
		${mycodeDir}/hailo/*.cpp ${mycodeDir}/hailo/*.h \
		${mycodeDir}/pebbles/*.txt \
		${mycodeDir}/pebbles/*.py ${mycodeDir}/pebbles/*.java \
		${mycodeDir}/pebbles/*.cpp ${mycodeDir}/pebbles/*.h \
		$$(find ${mycodeDir}/fibonacci/ -type f | \
			grep -E '\.txt$$|\.py$$|\.java$$|\.cpp$$|\.h$$') \
		$$(find ${mycodeDir}/reverse/ -type f | \
			grep -E '\.txt$$|\.py$$|\.java$$|\.cpp$$|\.h$$') \
		$$(find ${mycodeDir}/smoke_signals/ -type f | \
			grep -E '\.txt$$|\.py$$|\.java$$|\.cpp$$|\.h$$') \
		$$(find ${mycodeDir}/hello_coin/ -type f | \
			grep -E '\.txt$$|\.py$$|\.java$$|\.cpp$$|\.h$$') \
		$$(find ${mycodeDir}/knights_and_knaves/ -type f | \
			grep -E '\.txt$$|\.py$$|\.java$$|\.cpp$$|\.h$$') \
		$$(find ${mycodeDir}/hello_world/ -type f | \
			grep -E '\.txt$$|\.py$$|\.java$$|\.cpp$$|\.h$$') \
		& #


		

### VARIABLES	
#problemName = palindrome
#problemName = right_triangle
#problemName = hailo
#problemName = pebbles
#problemName = fibonacci
#problemName = reverse
#problemName = smoke_signals
#problemName = hello_coin
#problemName = knights_and_knaves
problemName = hello_world
cc:# compile c++ source files
	@g++ -Wall -o ${mycodeDir}/${problemName}/a.out \
		${mycodeDir}/${problemName}/${problemName}.cpp

rc:# run c++ executable
	@valgrind --leak-check=full ${mycodeDir}/${problemName}/a.out

#example:  @${javabin}/javac ./my_codes/palindrome/palindrome.java
#java doc:  google-chrome ./resources/javadir/jdk1.8.0_45/docs/index.html &
cj:#compile java
	#@${javabin}/javac -help
	@${javabin}/javac ${mycodeDir}/${problemName}/${problemName}.java

#example:  @${javabin}/java -classpath ./my_codes/palindrome: palindrome
rj:#run java	
	#@${javabin}/java -help
	@${javabin}/java -classpath ${mycodeDir}/${problemName}: ${problemName}

# convert python3 to python2; original python3 file stored as pyfile.py.bak
# and python2 converted file stored as pyfile.py per the -w flag		
convert:#convert python3 to python2
	@./resources/3to2	-w ${mycodeDir}/palindrome/palindrome.py

# -B is also sys.dont_write_bytecode, ie .pyc or .pyo
# -3 warns if python 2 code has compatibility issue if run as python 3
py2:# run python program
	@python2 -3 -B ${mycodeDir}/${problemName}/${problemName}.py < \
		${mycodeDir}/${problemName}/data.txt	

py3:# run python program
	@python3 -B ${mycodeDir}/${problemName}/${problemName}.py < \
		${mycodeDir}/${problemName}/data.txt
		
		
	
	
	
### SOURCE CODE of external available files on Gateway Laptop
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
	@gedit --new-window ${javaCloudFiles} & #read? AddNetworkServiceProviderCmdTest.java 
	#@gedit --new-window ${javaMysqlConnFiles} & #read?
studypython:
	#@gedit --new-window ${pythonCloudFiles} & #read?
	@gedit --new-window ${pythonMysqlConnFiles} & #read?
src_pymysql:#pymysql module source code, 70 total files (include .pyc files)
	@gedit --new-window $$(find ./resources/pymysql/ -type f \
		| grep -Ev '\.pyc$$') & #read? ER.py 207
src_git:#git source code, 2809 total files (including .txt files)
	@gedit --new-window \
		$$(find ./resources/git-master -type f | grep -Ev '\.txt$$' | \
		sed -n '1,20p') \
		& #read?
studycpp:#C++ MySQL connector source code
	@gedit --new-window ${cppMysqlConnFiles} & #read?
	
	























