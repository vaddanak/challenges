/******************************************************************************
*  File: magicSquare.h
*  Author:  Vaddanak Seng
*  Purpose: The header file contains MagicSquare class definition.
******************************************************************************/

#ifndef MAGICSQUARE_H_
#	define MAGICSQUARE_H_

#include <iostream>

/**
* Purpose:  Class MagicSquare represents an n-by-n magic square where n is an 
*     odd integer.
* How-to-use:
*     1)  You can create a 5x5 magic square by using the default 
*         constructor MagicSquare().
*     2)  You can create your own magic square by using the constructor 
*         MagicSquare(int) but make sure the argument is an odd number.
*     3)  You can input either an odd or even square using the overloaded 
*         extraction operator, ie cin >> magicSquareObject.  The program 
*         requires that the first input must be a single number to indicate 
*         the side length (n) of your square.  Then, you must make sure that 
*         you provide n x n number of values (each value is separated by a 
*         space) to properly fill up the square.
*     4)  Once you have a magic square object, either from custom input or 
*         by calling a constructor, you can check if the object represents an 
*         actual magic square by calling its member function isMagicSquare(), 
*         which returns true if it is a magic square.
*     5)  Once you have a magic square object, you can rotate the elements by 
*         90 degrees by calling its member function rotate(), which will 
*         return a new object.
*     6)  You can display the contents of your magic square by calling the 
*         overloaded insertion operator, ie cout << magicSquareObject .      
*/
class MagicSquare {
   //overloaded insertion operator
	friend std::ostream& operator<<( std::ostream& out, 
	                                 const MagicSquare& dataForOutput);
   //overloaded extraction operator	                                 
   friend std::istream& operator>>( std::istream& inStream,
                                    MagicSquare& storeInputData);	                                 

   void generateMagicSquare();//populate each square with "magic" numbers
   void createEmptyMatrix();//create n x n squares; initialized to 0 per square
   int determineMaxDigits() const;//find max digits in square
   //given cell coordinate, find its row sum
   int findRowSumAtCoordinate(const int& rowIndex, 
                              const int& columnIndex) const;
   //given cell coordinate, find its column sum                              
   int findColumnSumAtCoordinate(const int& rowIndex, 
                                 const int& columnIndex) const;
   //find positive-slope diagonal sum that goes through center of square                                 
   int findPositiveSlopeDiagonalSum() const;
   //find negative-slope diagonal sum that goes through center of square
   int findNegativeSlopeDiagonalSum() const;
   //checks that each value in square is unique, assuming values used 
   //are 1,2,3,4,...,(n*n)
   bool containUniqueValues() const;
   
   int numberPerSide;//count of values per side of square
   int ** matrix;//holds all integers in magic square
   
   void cleanup();//free allocated memory
   void copyMatrix(int** destinationMatrix, //copy n x n matrix; n=sideLength
                   int** sourceMatrix, int sideLength);

   public:
   MagicSquare();//create 5x5 magic square
   MagicSquare(const int& numberPerSide);//numberPerSide x numberPerSide square
   MagicSquare(const MagicSquare& rValue);//copy constructor   
   MagicSquare& operator=(const MagicSquare& rValue);//assignment operator
   

   ~MagicSquare();//free allocated memory

   bool isMagicSquare() const;//checks if correct magic square
   MagicSquare rotate() const;//rotate square 90 degrees and return instance copy

};

#endif //MAGICSQUARE_H_






