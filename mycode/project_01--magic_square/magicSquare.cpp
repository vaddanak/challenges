/******************************************************************************
*  File: magicSquare.cpp
*  Author:  Vaddanak Seng
*  Purpose: The implementation file for the MagicSquare class definition 
*           provides functions to generate a n x n square where side length 
*           n is odd, to accept user input data for a magic square, to rotate 
*           a mgic square, and to check for correct magic square.
******************************************************************************/

#include "magicSquare.h"

#include <cstdlib>
#include <cmath>
#include <iomanip>
#include <cassert>

/**
* Purpose:  The default constructor initializes the member data.
* Precondition:  When MagicSquare type is declared and before constructor is
*     called, compiler allocates enough memory to hold member data but content
*     contains garbage data.
* Postcondition:  After constructor is executed, allocated memory contains 
*     relevant data.  Variable numberPerSide is the count of numbers along 
*     each side of a square matrix; it is initialized to 5.  Variable matrix 
*     is a pointer to arrays; it is initialized to NULL.  The matrix represents
*     a 5x5 square.  The function generateMagicSquare is called to allocate 
*     memory for the arrays and populate the elements with values from 1 to 25.
*/
MagicSquare::MagicSquare() : numberPerSide(5), matrix(NULL) 
{  
   generateMagicSquare();
}

/**
* Purpose:  The parameterized constructor allows user to specify an odd size.  
* Precondition:  Compiler allocates enough memory to hold member data.
* Postcondition:  Constructor call with odd integer argument initializes 
*     variable numberPerSide to the passed-in argument and matrix pointer 
*     to NULL.  Function generateMagicSquare allocates memory to hold magic 
*     square values and populate magic square elements with values 1 to 
*     numberPerSide x numberPerSide.
*/
MagicSquare::MagicSquare(const int& numberPerSide) : 
   numberPerSide(numberPerSide), matrix(NULL) 
{   
   //validate magic square size is positive odd integer
   if(!(numberPerSide%2) || numberPerSide<1) {
      std::cerr <<"Size MUST be positive odd integer!" <<std::endl;
      std::exit(EXIT_FAILURE);
   }
   generateMagicSquare();
}

/**
* Purpose:  Copy constructor creates an instance of the class and copies 
*     the contents of the MagicSquare type argument to the newly created object.
* Precondition:  Compiler allocates memory to hold member data.
* Postcondition:  Constructor call copies variable numberPerSide to 
*     this numberPerSide and sets matrix pointer to NULL.  Function 
*     createEmptyMatrix creates an empty 2D array with numberPerSide rows 
*     and numberPerSide columns.  Function copyMatrix copies contents from 
*     matrix of argument object to this matrix.
*/
MagicSquare::MagicSquare(const MagicSquare& rValue) 
   : numberPerSide(rValue.numberPerSide), matrix(NULL)
{  
   createEmptyMatrix();
   copyMatrix(matrix, rValue.matrix, numberPerSide);
}

/**
* Purpose:  Assignment operator copies state of passed-in argument to a 
*     left-value object that exists.
* Precondition:  The target object exists and reflects current state.
* Postcondition:  The assignment operator copies state of argument object 
*     to left-hand-side target object, so this object will have same state 
*     as argument object.  Function returns reference to left-hand-side object.
*/
MagicSquare& MagicSquare::operator=(const MagicSquare& rValue) {   
   if(this != &rValue) {//avoids self-reference
      //sizes are different, so remove old resources and reallocate
      if(numberPerSide != rValue.numberPerSide) {     
         cleanup();
         numberPerSide = rValue.numberPerSide;
         createEmptyMatrix();         
      }
      copyMatrix(matrix,rValue.matrix,numberPerSide);//copy matrix contents
   }
   return *this;
}

/**
* Purpose:  Destructor frees allocated resources.
* Precondition:  Heap memory are allocated to maintain this object's state.
* Postcondition:  Heap memory will be freed and available to other programs.
*/
MagicSquare::~MagicSquare() 
{  
   cleanup();
}

/**
* Purpose:  This helper function can be used to free allocated memory.
* Precondition:  Memory is allocated and reserved to hold object data.
* Postcondition:  Memory is released and becomes available to rest of system.
*/
void MagicSquare::cleanup() {
   if(matrix) { //deallocate memory
      for(int i = 0; i < numberPerSide; ++i)
         std::free( *(matrix+i) );//frees array of int
      std::free(matrix);//frees array of pointers (int*)         
   }
}

/**
* Purpose:  This helper function copies source matrix srcMatrix, which is 
*     length in size, to destination matrix destMatrix of the same size.
* Precondition:  There are two matrices which may contain different data.
* Postcondition:  The two matrices contain the same data.
*/
void MagicSquare::copyMatrix(int** destMatrix, int** srcMatrix, int length) {
   for(int row = 0; row < length; ++row)
      for(int column = 0; column < length; ++column)
         *(*(destMatrix+row)+column) = *(*(srcMatrix+row)+column);//copy
}

/**
* Purpose:  This helper function creates a magic square (2 dimensional array)
*     with side length numberPerSide and populates the array elements with 
*     values from 1 to numberPerSide x numberPerSide based on magic square 
*     rule.
* Precondition:  Current object has matrix pointer which is NULL; that is, 
*     matrix does not point to anything.
* Postcondition:  Current object matrix pointer points to allocated and 
*     populated memory that represents a numberPerSide x numberPerSide magic 
*     square.
*/
void MagicSquare::generateMagicSquare() 
{
   createEmptyMatrix();   
   //fill matrix with "magic" integers from 1 to (n x n)
   int maxValueInSquare = numberPerSide * numberPerSide;
   int row = 0, column = numberPerSide/2;//index coordinate of first value
   int rightMostSquareIndex = numberPerSide - 1;
   int topMostSquareIndex = 0;
   int nextRow = row, nextColumn = column;
   
   *(*matrix+(column)) = 1;//assign first value in magic square   
   
   for(int value = 2; value <= maxValueInSquare; ++value) {
      if( row==topMostSquareIndex && column==rightMostSquareIndex ) 
         ++nextRow;//at top-right corner, so go down one row
      else {//go up one row; if at top row, go to bottom row           
         nextRow = (row?row:numberPerSide) - 1;         
         nextColumn = (column+1) % numberPerSide;//go right 1 column
      }      
     
      while( *(*(matrix+nextRow)+nextColumn) )  
      { //square already filled
         nextRow = (row+1)%numberPerSide;//go down 1 row, wrap if needed  
         nextColumn = column;//same column             
      }                              
      
      *(*(matrix+nextRow)+nextColumn) = value;//set empty cell
      row = nextRow;
      column = nextColumn;   
   }      
}

/**
* Purpose:  This helper function creates an empty 2 dimensional array.
* Precondition:  Matrix pointer points to NULL.
* Postcondition:  Matrix pointer points to an array of pointers to int; this 
*     represents an empty magic square.
*/
void MagicSquare::createEmptyMatrix() 
{
   //allocate and initialize n x n matrix to hold magic square numbers   
   matrix = static_cast<int**>(std::calloc(numberPerSide, sizeof(*matrix)));
   if(!matrix) {//check rows
      std::cerr <<"Failed to allocate row!" <<std::endl;
      std::exit(EXIT_FAILURE);
   }
   for(int i = 0; i < numberPerSide; ++i) {//columns
      *(matrix+i) = 
         static_cast<int*>(std::calloc(numberPerSide,sizeof(**matrix)));    
      if( !*(matrix+i) ) {//check columns
         std::cerr <<"Failed to allocate column!" <<std::endl;
         std::exit(EXIT_FAILURE);
      }                 
   }
}

/**
* Purpose:  Insertion operator is overloaded to recognize a MagicSquare class 
*     type and customized to display a magic square formatted to look like a 
*     square.
* Precondition:  Insertion operator does not recognize MagicSquare class when 
*     we make the statement "std::cout <<MagicSquare();".
* Postcondition:  Insertion operator will display a custom, formatted square 
*     when we make the statement "std::cout <<MagicSquare;".  Function returns 
*     reference to ostream.
*/
std::ostream& operator<<(std::ostream& out, const MagicSquare& magicSquareRef) 
{   
   int maxDigitsInSquare = magicSquareRef.determineMaxDigits() + 1;
   out <<std::setw(maxDigitsInSquare) <<magicSquareRef.numberPerSide 
       <<std::endl;   
   for(int row = 0; row < magicSquareRef.numberPerSide; ++row) {
      for(int column = 0; column < magicSquareRef.numberPerSide; ++column)
         out <<std::setw(maxDigitsInSquare) 
             <<*((*(magicSquareRef.matrix+row))+column);
      out <<std::endl;     
   }     
   return out;
}

/**
* Purpose:  This extraction operator overload allows MagicSquare type to be 
*     used as a target object and customizes input to be stored in the 
*     elements of the 2-dimensional array (magic square).
* Precondition:  Extraction operator does not recognize MagicSquare type.
* Postcondition:  Extraction operator recognizes MagicSquare type and stores 
*     user-input properly in the 2-dimensional array.  Function returns 
*     reference to istream.
*/
std::istream& operator>>(std::istream& inStream, MagicSquare& storeInputData)
{
   int magicSquareSideLength = 0;
   inStream >>magicSquareSideLength;
   //object size is different from user-desired size so we free resources 
   //and allocate the requested size
   if(magicSquareSideLength != storeInputData.numberPerSide) {
      storeInputData.cleanup();
      storeInputData.numberPerSide = magicSquareSideLength;
      storeInputData.createEmptyMatrix();
   }
      
   for(int row = 0; row < storeInputData.numberPerSide; ++row) 
      for(int column = 0; column < storeInputData.numberPerSide; ++column) 
         //expecting n x n input values and storing them in n x n 2D array
         inStream >> *(*(storeInputData.matrix+row)+column);
      
   return inStream;    
}

/**
* Purpose:  Helper function determines greatest digits an element holds.
* Precondition:  Greatest number of digits an element in the magic square 
*     array may have is unknown.  This information would be useful inorder 
*     to properly format an output of all the numbers to look like a square.
* Postcondition:  Each element in the 2D array is evaluated and the greatest 
*     number of digits of an element value is returned.
*/
int MagicSquare::determineMaxDigits() const 
{   
   int maxDigits = 0;   
   for(int row = 0; row < numberPerSide; ++row) 
      for(int column = 0, counter, value; column < numberPerSide; ++column) {
         counter = 1;
         value = *(*(matrix+row)+column);
         while(value /= 10)
            ++counter;
         if(counter > maxDigits)
            maxDigits = counter;
      }   
   
   return maxDigits;     
}

/**
* Purpose:  Function determines if the current object represents a magic 
*     square based on three criteria:  sum of main diagonals, sum of row 
*     and column, and uniqueness of each element.
* Precondition:  Current object holds n x n values in a 2D array, but it 
*     is unknown if this represents a magic square.
* Postcondition:  The sum of each main diagonals and the sum of the row 
*     and column intersecting on each element are checked if they are equal.  
*     Each element in the 2D array are checked if each is unique.  If the 
*     object passes all 3 tests, then it returns true.
*/
bool MagicSquare::isMagicSquare() const {

   //check diagonal sums for diagonals through center of square
   int sum1 = findNegativeSlopeDiagonalSum();
   int sum2 = findPositiveSlopeDiagonalSum();   
   if(sum1 != sum2)
      return false;
   
   //check vertical sum and horizontal sum at intersectng square
   int sum3, sum4;
   for(int row = 0; row < numberPerSide; ++row) {
      for(int column = 0; column < numberPerSide; ++column) {
         sum3 = findRowSumAtCoordinate(row,column);
         sum4 = findColumnSumAtCoordinate(row,column);
         if(sum1 != sum3 || sum1 != sum4)
            return false;
      }
   }
     
   //check that all values in each unit square is unique
   return containUniqueValues();   
}

/**
* Purpose:  Helper function determines sum of row that contains coordinate.
* Precondition:  Object contains n x n matrix, but row sum is unknown.
* Postcondition:  Sum of elements in row containing coordinate as provided 
*     by the argument is returned.
*/
int MagicSquare::findRowSumAtCoordinate(const int& rowIndex, 
   const int& columnIndex) const
{
   int temp = columnIndex, sum = 0; //column is various, row is constant
   do {     
      sum += *(*(matrix+rowIndex)+temp);
      temp = (temp + 1) % numberPerSide;//modulus allows wraparound        
   }
   while(temp != columnIndex);
  
   return sum;
}

/**
* Purpose:  Helper function determines sum of column that contains coordinate.
* Precondition:  Object contains n x n matrix, but column sum is unknown.
* Postcondition:  Sum of elements in column containing coordinate as provided 
*     by the argument is returned.
*/
int MagicSquare::findColumnSumAtCoordinate(const int& rowIndex, 
   const int& columnIndex) const
{
   int temp = rowIndex, sum = 0; //column is constant, row is various
   do {     
      sum += *(*(matrix+temp)+columnIndex);//modulus allows wraparound
      temp = (temp + 1) % numberPerSide;        
   }
   while(temp != rowIndex);
   
   return sum;
}   

/**
* Purpose:  Helper function determines sum of elements that lie on the 
*     positively-sloping main diagonals (bottom-left to top-right).
* Precondition: Object contains n x n matrix, but main diagonal sum is unknown.
* Postcondition: Sum of elements along main diagonal is added and returned.
*/
int MagicSquare::findPositiveSlopeDiagonalSum() const {
   int sum = 0;
   for(int column = numberPerSide - 1, row = 0; row < numberPerSide ;
       --column, ++row) 
   {   
      sum += *(*(matrix+row)+column);
   }
   
   return sum;
}

/**
* Purpose:  Helper function determines sum of elements that lie on the 
*     negatively-sloping main diagonals (top-left to bottom-right).
* Precondition: Object contains n x n matrix, but main diagonal sum is unknown.
* Postcondition: Sum of elements along main diagonal is added and returned.
*/
int MagicSquare::findNegativeSlopeDiagonalSum() const {
   int sum = 0;   
   for(int row = 0, column = 0; row < numberPerSide; ++row, ++column) 
   {     
      sum += *(*(matrix+row)+column);
   }
  
   return sum;
}

/**
* Purpose:  Helper function determines uniqueness of each element in 2D array.
* Precondition:  Object contains n x n matrix, but uniqueness of elements is 
*     unknown.
* Postcondition: If elements in 2D array are unique, function returns true.
*/
bool MagicSquare::containUniqueValues() const {
   int countOfElements = numberPerSide * numberPerSide;
   int * valueList = (int*)calloc(countOfElements, sizeof(*valueList));
   if(!valueList) {
      std::cerr <<"Fail to calloc in containUniqueValues()!" <<std::endl;
      std::exit(EXIT_FAILURE);
   }
   
   bool isUniqueValue = true;//uniqueness status of values in matrix   
   for(int row = 0; row < numberPerSide && isUniqueValue; ++row) 
      for(int column = 0; column < numberPerSide; ++column) {
         //for value in matrix at index idx, check if value already exists in
         //array valueList at index between index 0 to idx-1               
         int i = 0;
         for( ; i < row*numberPerSide+column; ++i) {
            if( valueList[i] == *(*(matrix+row)+column) ) {
               isUniqueValue = false;
               break;
            }
         }
         
         if(!isUniqueValue)             
            break;         
         else //log each value to check for duplicate in next iteration
            valueList[i] = *(*(matrix+row)+column);                   
      }
   
   free(valueList);   
   return isUniqueValue;
}

/**
* Purpose:  Function rotates elements in magic square by 90 degrees.
* Precondition:  The position of the elements are determined by input.
* Postcondition:  The position of the elements are rotated by 90 degrees 
*     compared to their previous location.  Function returns a new object 
*     with the rotated elements.
*/
MagicSquare MagicSquare::rotate() const {
   MagicSquare ms(numberPerSide);   
   
   for(int row = 0; row < numberPerSide; ++row) 
      for(int column = 0; column < numberPerSide; ++column) 
         //copy source value to destination matrix at location 90 degrees
         //to source value location.
         *(*(ms.matrix+column)+(numberPerSide-row-1))=*(*(matrix+row)+column);   
   
   //compiler seems to construct object at destination location,
   //thus, bypass call to copy-constructor
   return ms;
}

























