/******************************************************************************
*  File: main.cpp
*  Author:  Vaddanak Seng
*  Purpose: Test default constructor, parameterized constructor, 
*			   overloaded operators << and >>, rotate, and validation check of
*           class MagicSquare
******************************************************************************/

#include "magicSquare.h"

#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <cstdlib>

/**
* Purpose:  The main function tests the public functions of MagicSquare.
* Precondition:  MagicSquare definition provides constructors to create an 
*     instance and public functions to validate and rotate a magic square.
* Postcondition:  MagicSquare constructors created objects, and their contents 
*     are output to a file output.txt.  The objects are rotated 90 degrees 
*     and contents output to file output.txt.  A file called input.txt 
*     provides input data for several magic squares, and the member function 
*     isMagicSquare() checks if it is a magic square; a message is displayed 
*     on console to indicate result of each check.  
*/
int main(int argc, char **args) {

   //create file to store output
   std::ofstream outputFile( "output.txt", std::ios_base::out);      
   if(!outputFile) {
      std::cerr <<"Failed to open file output.txt" <<std::endl;
      std::exit(EXIT_FAILURE);
   }  
       
   //create magic square object using default constructor
   MagicSquare magicSquare;
   if(magicSquare.isMagicSquare())                                 
      outputFile <<magicSquare <<std::endl;
   else {
      std::cout <<"The following is not a valid magic square:" <<std::endl;
      std::cout <<magicSquare <<std::endl;
   }
   
   //create magic squares of sizes 7,9,11,13,15,17,19,21,23,25
   int sizes[] = {7, 9, 11, 13, 15, 17, 19, 21, 23, 25};
   for(size_t i = 0; i < sizeof(sizes)/sizeof(*sizes); ++i) {
      MagicSquare magicSquareVarious(sizes[i]);
      if(magicSquareVarious.isMagicSquare()) 
         outputFile <<magicSquareVarious <<std::endl;
      else {
         std::cout <<"The following is not a valid magic square:" <<std::endl;
         std::cout <<magicSquareVarious <<std::endl;
      }    
      //rotate magic square 90 degrees
      MagicSquare magicSquareRotate = magicSquareVarious.rotate();
      if(magicSquareRotate.isMagicSquare()) 
         outputFile <<magicSquareRotate <<std::endl;
      else {
         std::cout <<"The following is not a valid magic square:" <<std::endl;
         std::cout <<magicSquareRotate <<std::endl;
      }       
   }    
   
   outputFile.close();    
   
   //check if matrices in input.txt are magic squares
   std::ifstream inputFile("input.txt");
   if(!inputFile) {
      std::cerr <<"Failed to open file input.txt" <<std::endl;
      std::exit(EXIT_FAILURE);
   }
   int numberOfInstances = 0;   
   inputFile >> numberOfInstances;
   
   for(int i = 0; i < numberOfInstances; ++i) {      
      MagicSquare tempSquare;
      inputFile >> tempSquare;
      std::cout <<i <<": is " 
                <<(tempSquare.isMagicSquare()?"valid":"not valid") 
                <<std::endl;     
      //std::cout <<tempSquare <<std::endl; //display magic square              
   }

   inputFile.close();  

   //std::cout <<MagicSquare().rotate() <<std::endl;
   return 0;
}

























