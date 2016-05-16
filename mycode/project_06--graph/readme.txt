Steps to run the program...

step 1:  Put all the following files in the same directory:  

         Makefile, main.cpp, bunchofgraphs.cpp, bunchofgraphs.h,
         graph.cpp, graph.h, readme.txt and input.txt
         
step 2:  Before you re-compile, it is suggested to remove old object files
         before recompiling to create more recent ones.         
         
         make clean

step 3:  Type the following at the command prompt to compile, link, and create
         an executable file called "a.out":  
         
         make

step 4:  Type the following at the command prompt to run the program:  

         ./a.out

         The program should output the following to console based on
         the provided "input.txt" file:
   
         STARTING VERTEX: 0
		 Path by vertex index: 0 6 7 1 4 5 8 
		 Path by direction: S E N S E S


         STARTING VERTEX: 0
         Path by vertex index: 0 3 24 45 10 31 28 32 18 14 16 20 17 38 40 5 1 43 48 
         Path by direction: E S S N S W E N W E E W S E N W S E
         
   
         The program should also output to a file called "output.txt"  
         The content of file "output.txt" based on provided "input.txt" file is:
   
         S E N S E S

         E S S N S W E N W E E W S E N W S E

         

