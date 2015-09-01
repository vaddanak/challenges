/******************************************************************************
*  File: permutations.h
*  Author:  Vaddanak Seng
*  Purpose: This header file contains function template headers and 
*     implementations.  The primary function "outputPermutations(..)" 
*     will output all unique permutations of the passed-in array.  
*     The function "outputArray(..)" will output the elements of the 
*     passed-in array on the same line and separated using a space.  
*     The function "factorial(..)" will return the factorial of the 
*     passed-in value.          
******************************************************************************/

#ifndef PERMUTATIONS_H_
#  define PERMUTATIONS_H_

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <new>

//function template prototypes; please see comments on each function
//preceding the respective function implementation below
template <class T>
void outputArray(T* items, const int& size, std::ostream& out);

template <class T>
void outputPermutations(T* items, const int& size, std::ostream& out);

template <class T>
void nextSrcPosition( T* destArr, T* srcArr, const int& size,
                      int inUseSrcIndex, std::ostream& out, 
                      int totalPermutations, T** permutationsArr);
                      
template <class T>
void nextDestPosition(  T* destArr, T* srcArr, const int& size, 
                        int inUseSrcIndex, int inUseDestIndex,
                        std::ostream& out, 
                        int totalPermutations, T** permutationsArr); 
                        
template <class T>
void fillArray( T* destArr, T* srcArr, const int& size, int inUseSrcIndex,
                int inUseDestIndex, int srcIndex, int destIndex);    
                
template <class T>
bool isArraySame(T* arr1, T* arr2, const int& size);

template <class T>
bool isArrayUnique( T* targetArr, T** permutationsArr, const int& size,
                    int totalPermutations, int& availableIndex);
                        
template <class T>
void cleanup(T** arrPermutations, const int& numberOfPermutations);

template <class T>
void printArrayPermutations( T** arrPermutations,
                             const int& numberOfPermutations, 
                             const int& sizeOfPermutation,
                             std::ostream& out);
                           
template <class T>
void permutateArraySizeTwo( T* arrOriginalItems, const int& arrOriginalSize,
                            const int& arrSubsetSize, const int& currentIndex,
                            const int& maxPermutations,
                            T** arrUniquePermutations, std::ostream& out);          
                     
template <class T>
void permutateArraySizeVarious( T* arrOriginalItems,
                                const int& arrOriginalSize,
                                const int& arrSubsetSize, 
                                const int& currentIndex,
                                const int& totalPermutations, 
                                const int& currentPermutation,
                                T*** prevArrPermutations, 
                                const int& maxPermutations,
                                T** arrUniquePermutations, std::ostream& out);  
                     
template <class T>
void insertUniqueArray( T* destArr, const int& size,                          
                        int totalPermutations, T** permutationsArr);
                        
template <class T>
void copyArray(T* dest, T* src, const int& size);      

template <class T>
void initialize(T** arrays, const int& numArrays);                  
                        
//non-function template prototype                        
long factorial(const int& n);


/**
* Purpose: Function template outputs array content on same line and each 
*     element is separated by a space.   
* Precondition: Array "items" is provided that has "size" number of 
*     elements of type "T".
* Postcondition: Each element of array is output to "out".  The elements 
*     of array "items" will appear on the same line with a space between 
*     the elements.
*/
template <class T>
void outputArray(T* items, const int& size, std::ostream& out) {
   for(int i = 0; i < size; ++i)
      out << *(items+i) <<" ";
   //out <<std::endl;    
}


/**
* Purpose: Function calculates factorial of a value n, 
*     ie n! = n*(n-1)*(n-2)*...*2*1. 
* Precondition: A value n is passed to function.
* Postcondition: The factorial of n (n!) is calculated and returned.
*/
long factorial(const int& n) {
   if( n < 2 ) 
      return 1;
   return n * factorial(n-1);   
}

/**
* Purpose: Function template outputs all unique permutations of array "items" . 
* Precondition: Array "items" contain "size" number of elements.
* Postcondition: All unique permutations of array "items" is output to "out".
*/
template <class T>
void outputPermutations(T* items, const int& size, std::ostream& out) {
   const int MINIMUM_ARRAY_SIZE = 1;
   
   if( size < MINIMUM_ARRAY_SIZE ) {
      std::cerr <<"Array size is not valid!  size: " <<size <<std::endl;
      return;
   }  
   
   if(size == MINIMUM_ARRAY_SIZE) {
      out <<"Unique permutations of array { " ;
      outputArray<T>(items, size, out);
      out <<"} is ..." <<std::endl;
      outputArray<T>(items, size, out);
      out <<std::endl;
      return;        
   }     
   
   const int SUBSET_SIZE = 2;
   const int CURRENT_INDEX = 1;   
   
   int maxPermutations = factorial(size);//all possible permutations count
   //holds all arrays which represent all possible permutations; 
   //each array is size "size"      
   T** arrUniquePermutations = new(std::nothrow) T*[maxPermutations];      
   initialize<T>(arrUniquePermutations, maxPermutations);                                 
                                      
   //creates 2 permutations based on the first 2 elements in array "items"
   permutateArraySizeTwo<T>( items, size, SUBSET_SIZE, CURRENT_INDEX, 
                             maxPermutations, arrUniquePermutations, out);                   
   
   out <<"Unique permutations of array { " ;
   outputArray<T>(items, size, out);
   out <<"} are ..." <<std::endl;
   printArrayPermutations<T>(arrUniquePermutations,maxPermutations,size,out);
   
   cleanup<T>(arrUniquePermutations, maxPermutations);     
}

/**
* Purpose: Function template provides index of current element, which is
*     used to insert in all positions of a given destination array "destArr". 
* Precondition: Index "inUseSrcIndex" points to current element in array
*     "srcArr".  Array "destArr" holds a permutation with element at index
*     "inUseSrcIndex" in the same position in both arrays.  Both arrays have
*     "size" number of elements.
* Postcondition: Each recursive function call moves the index "inUseSrcIndex"
*     one position to the right.
*/
template <class T>
void nextSrcPosition( T* destArr, T* srcArr, const int& size,
                      int inUseSrcIndex, std::ostream& out, 
                      int totalPermutations, T** permutationsArr) 
{   
   if(inUseSrcIndex < size) {
      const int START_INDEX = 0;      
      nextDestPosition<T>( destArr, srcArr, size, inUseSrcIndex,
                           START_INDEX, out, totalPermutations,
                           permutationsArr);
      nextSrcPosition<T>( destArr, srcArr, size, ++inUseSrcIndex, out, 
                          totalPermutations, permutationsArr);
   }
}

/**
* Purpose: Function template inserts an element as indicated by "srcArr" 
*     index "inUseSrcIndex" in different positions of array "destArr".
*     Thus, each recursive function call represents a different permutation
*     of "destArr".
* Precondition: Index "inUseSrcIndex" points to current element in array
*     "srcArr".  Array "destArr" holds a permutation with element at index
*     "inUseSrcIndex" in the same position in both arrays.  Both arrays have
*     "size" number of elements.
* Postcondition: Each recursive function call results in element at index
*     "inUseSrcIndex" to be inserted in array "destArr" at index
*     "inUseDestIndex".  Each call moves the index "inUseDestIndex"
*     one position to the right.  Each unique permutation of "destArr"
*     is stored in "permutationsArr".
*/
template <class T>
void nextDestPosition(  T* destArr, T* srcArr, const int& size, 
                        int inUseSrcIndex, int inUseDestIndex,
                        std::ostream& out, int totalPermutations,
                        T** permutationsArr) 
{   
   if(inUseDestIndex < size) {
      const int START_INDEX = 0;      
      destArr[inUseDestIndex] = srcArr[inUseSrcIndex];
      fillArray<T>( destArr, srcArr, size, inUseSrcIndex, inUseDestIndex,
                    START_INDEX,START_INDEX);
            
      insertUniqueArray<T>( destArr, size, totalPermutations,
                            permutationsArr);
      
      nextDestPosition<T>( destArr, srcArr, size, inUseSrcIndex,
                           ++inUseDestIndex, out, totalPermutations,
                           permutationsArr);
   }
}

/**
* Purpose: Function template inserts unique array "destArr" in array
*     "permutationsArr".
* Precondition: Array "destArr" represents a permutation.
* Postcondition: If array "destArr" is unique, then it is inserted in
*     array "permutationsArr".
*/
template <class T>
void insertUniqueArray( T* destArr, const int& size,                          
                        int totalPermutations, T** permutationsArr) 
{
   int availableIndex = 0;
   if( isArrayUnique( destArr, permutationsArr, size, totalPermutations,
                      availableIndex) ) 
   {                      
      if( !*(permutationsArr+availableIndex) ) {         
         *(permutationsArr+availableIndex) = new(std::nothrow) T[size];
         if( !*(permutationsArr+availableIndex) ) {
            std::cerr <<"Failed to allocate array!" <<std::endl;
            std::exit(EXIT_FAILURE);
         }
      }
      
      copyArray<T>( *(permutationsArr+availableIndex), destArr, size );
   }
}

/**
* Purpose: Function template fills positions around index "inUseDestIndex"
*     in array "destArr" with remaining elements in their same order
*     relative to each other.
* Precondition: Array "destArr" contains element at index "inUseDestIndex".
* Postcondition: Positions before and after index "inUseDestIndex" in array
*     "destArr" are filled with remaining elements in the same order
*     relative to each other.
*/
template <class T>
void fillArray( T* destArr, T* srcArr, const int& size, int inUseSrcIndex,
                int inUseDestIndex, int srcIndex, int destIndex) 
{
   if(inUseDestIndex == destIndex)
      ++destIndex;
   if(inUseSrcIndex == srcIndex)
      ++srcIndex;
   if(srcIndex < size) {
      destArr[destIndex++] = srcArr[srcIndex++];
      fillArray<T>( destArr, srcArr, size, inUseSrcIndex, inUseDestIndex,
                    srcIndex,destIndex );
   }            
}

/**
* Purpose: Function template determines if 2 arrays are the same based on
*     the first "size" number of elements.
* Precondition: Two arrays have at least "size" number of elements.
* Postcondition: Function returns true if both arrays are the same based
*     on the first "size" number of elements; otherwise, it returns false.
*/
template <class T>
bool isArraySame(T* arr1, T* arr2, const int& size) {   
   for(int i = 0; i < size; ++i)
      if(arr1[i] != arr2[i])
         return false;
   return true;         
}

/**
* Purpose: Function template determines if array "targetArr" is unique
*     among the arrays contained in "permutationsArr".
* Precondition: Array "targetArr" has "size" elements.  Array
*     "permutationsArr" can hold "totalPermutations" number of arrays.
*     Parameter "availableIndex" is index available in "permutationsArr",
*     where a unique array can be stored.
* Postcondition: Function returns true if array "targetArr" does not exist
*     in array container "permutationsArr" and sets "availableIndex" to
*     indicate position in container where new array will be stored.
*     It returns false if "targetArr" is found in "permutationsArr" and
*     sets "availableIndex" to -1.
*/
template <class T>
bool isArrayUnique( T* targetArr, T** permutationsArr, const int& size,
                    int totalPermutations, int& availableIndex) 
{
   bool uniqueStatus = true;    
   int i = 0;
   for(; i < totalPermutations && *permutationsArr; ++i, ++permutationsArr) {
      if( isArraySame<T>(targetArr, *permutationsArr, size) ) {
         uniqueStatus = false;           
         break;  
      }         
   }  
   
   if(i < totalPermutations)
      availableIndex = i;
   else {
      availableIndex = -1;   
      uniqueStatus = false;  
   }                
   
   return uniqueStatus;
}

/**
* Purpose: Function template frees allocated resources.
* Precondition: Array container "arrPermutations" has at most
*     "numberOfPermutations" arrays, which occupies heap memory.
* Postcondition: Function frees allocated heap memory so it can be resused.
*/
template <class T>
void cleanup(T** arrPermutations, const int& numberOfPermutations) {
   if(arrPermutations) {
      for(int i = 0; i < numberOfPermutations; ++i) 
         if( *(arrPermutations+i) )
            delete[] *(arrPermutations+i);
      
      delete[] arrPermutations;  
   }
}

/**
* Purpose: Function template outputs all arrays in array container
*     "arrPermutations" to "out".
* Precondition: Array container "arrPermutations" contains at most
*     "numberOfPermutations" arrays, and each array has "sizeOfPermutation"
*     elements.
* Postcondition: Function outputs all arrays in "arrPermutations" to "out".
*/
template <class T>
void printArrayPermutations( T** arrPermutations,
                             const int& numberOfPermutations, 
                             const int& sizeOfPermutation,
                             std::ostream& out) 
{
   if(arrPermutations) 
      for(int i = 0; i < numberOfPermutations; ++i)
         if( *(arrPermutations+i) ) {
            outputArray<T>( *(arrPermutations+i), sizeOfPermutation, out );  
            out <<std::endl;  
         }                
}

/**
* Purpose: Function template generates 2 possible permutations based on the
*     first 2 elements in array "arrOriginalItems" and calls function
*     "permutateArraySizeVarious" to create permutations based on the
*     rest of the elements.
* Precondition: Array "arrOriginalItems" is the original array passed-in by
*     the user and has "arrOriginalSize" elements.  "arrSubsetSize" is the
*     number of array elements used to determine permutations, which is 2.
*     "currentIndex" is 1, points to second element.  Array container
*     "arrUniquePermutations" can hold "maxPermutations" arrays.
* Postcondition: Function generates 2 permutations based on the first 2
*     elements of array "arrOriginalItems" and calls function
*     "permutateArraySizeVarious" to generate permutations based on the
*     remaining elements in the array.  Unique arrays of size
*     "arrOriginalSize" are stored in array container "arrUniquePermutations".
*/
template <class T>
void permutateArraySizeTwo( T* arrOriginalItems, const int& arrOriginalSize,
                            const int& arrSubsetSize, const int& currentIndex,
                            const int& maxPermutations,
                            T** arrUniquePermutations, std::ostream& out) 
{
   if( arrSubsetSize > arrOriginalSize) {
      std::cerr <<"Size arrSubsetSize is larger than original size!"
                <<std::endl;
      return;
   }           
   const int STEP = 1; 
   const int START = 0;
   const int BASE_SIZE = 2;                
   //expect currentIndex == 1          
   int numberOfPermutations = currentIndex + STEP;   
   //stores unique permutations     
      
   T** arrPermutations = new(std::nothrow) T*[numberOfPermutations];
   initialize<T>(arrPermutations,numberOfPermutations);
   
   T destArr[arrSubsetSize];//expect arrSubsetSize == 2
   T srcArr[arrSubsetSize];
      
   copyArray<T>(srcArr, arrOriginalItems, arrSubsetSize);
      
   nextSrcPosition<T>( destArr, srcArr, arrSubsetSize, START, 
                       out, numberOfPermutations, arrPermutations);
   
  
   permutateArraySizeVarious<T>( arrOriginalItems, arrOriginalSize,
                                 arrSubsetSize + STEP,
                                 currentIndex + STEP,
                                 numberOfPermutations, START, 
                                 &arrPermutations, maxPermutations,
                                 arrUniquePermutations, out);
                
   if(arrOriginalSize == BASE_SIZE) {      
      for(int i = 0; i < numberOfPermutations; ++i) {
         if( *(arrPermutations+i) ) 
            insertUniqueArray( *(arrPermutations+i), arrOriginalSize,                          
                               maxPermutations, arrUniquePermutations);
      }
   }                      
   
   cleanup<T>(arrPermutations, numberOfPermutations);
}

/**
* Purpose: Function template generates array permutations.
* Precondition: Array "arrOriginalItems" is the original array passed-in by
*     the user and has "arrOriginalSize" elements.  "arrSubsetSize" is the
*     number of array elements used to determine permutations, which starts
*     with 3.  "currentIndex" starts with 2, points to third element.  Array
*     at "prevArrPermutations" holds all the permutations based on
*     arrSubsetSize-1 elements in previous function call; it contains
*     "totalPermutations" arrays; and "currentPermutation" indicates current
*     array in container to use to generate next set of permutations.  Array
*     container "arrUniquePermutations" can store "maxPermutations" arrays.
* Postcondition: Function generates all possible permutations based on all
*     elements of array "arrOriginalItems".  Unique arrays of size
*     "arrOriginalSize" are stored in array container "arrUniquePermutations".
*/
template <class T>
void permutateArraySizeVarious( T* arrOriginalItems,
                                const int& arrOriginalSize,
                                const int& arrSubsetSize, 
                                const int& currentIndex,
                                const int& totalPermutations, 
                                const int& currentPermutation,
                                T*** prevArrPermutations, 
                                const int& maxPermutations,
                                T** arrUniquePermutations, std::ostream& out) 
{   
   if( arrSubsetSize > arrOriginalSize)
      return;
      
   const int STEP = 1; 
   const int START = 0;                          
   int numberOfPermutations = currentIndex + STEP;   
   
   //stores unique permutations        
   T** arrPermutations = new(std::nothrow) T*[numberOfPermutations];
   initialize<T>(arrPermutations, numberOfPermutations);

   if( *(*prevArrPermutations+currentPermutation) ) {
      T destArr[arrSubsetSize];
      T srcArr[arrSubsetSize];
      if(totalPermutations) {                     
            copyArray<T>(srcArr, *(*prevArrPermutations+currentPermutation),
                         arrSubsetSize-STEP);       
                  
            srcArr[arrSubsetSize-STEP] = arrOriginalItems[arrSubsetSize-STEP];                        
      }
      else         
         copyArray<T>(srcArr, arrOriginalItems, arrSubsetSize);
         
      nextSrcPosition<T>( destArr, srcArr, arrSubsetSize,
                          (currentIndex>STEP?currentIndex:START), 
                          out, numberOfPermutations, arrPermutations);
   }
   
   if(currentPermutation < totalPermutations - STEP)
      permutateArraySizeVarious<T>( arrOriginalItems, arrOriginalSize,
                                    arrSubsetSize, currentIndex,
                                    totalPermutations, 
                                    (totalPermutations ? 
                                       currentPermutation+STEP:START),
                                    prevArrPermutations, maxPermutations,
                                    arrUniquePermutations, out);
   
   permutateArraySizeVarious<T>( arrOriginalItems,
                                 arrOriginalSize, arrSubsetSize + STEP,
                                 currentIndex + STEP,
                                 numberOfPermutations, START,
                                 &arrPermutations, maxPermutations,
                                 arrUniquePermutations, out);
   
   if(arrSubsetSize == arrOriginalSize) {      
      for(int i = 0; i < numberOfPermutations; ++i) {
         if( *(arrPermutations+i) )
            insertUniqueArray<T>( *(arrPermutations+i), arrSubsetSize,                          
                                  maxPermutations, arrUniquePermutations);
      }
   }
   
   cleanup<T>(arrPermutations, numberOfPermutations);
}

/**
* Purpose: Function template copies arrays.
* Precondition: Both arrays "dest" and "src" have "size" elements.
* Postcondition: Function copies elements from array "src" to array
*     "dest" by calling each element's assignment operator.  So, element
*     type of array must have implemented proper assignment operator,
*     ie it is responsible for copying its allocated resources.
*/
template <class T>
void copyArray(T* dest, T* src, const int& size) {
   for(int i = 0; i < size; ++i)
      dest[i] = src[i];
}

/**
* Purpose: Function template initializes pointer-type elements in container
*     to NULL.
* Precondition: When "::operator new" is used to allocate an array of
*     pointers (T**), it does not initialize the elements to NULL.
* Postcondition: The pointer elements (T*) as pointed to by T** are each
*     initialized to NULL.
*/
template <class T>
void initialize(T** arrays, const int& numArrays) {
   if(arrays)
      for(int i = 0; i < numArrays; ++i)
         *(arrays+i) = NULL;            
}

#endif // PERMUTATIONS_H_
