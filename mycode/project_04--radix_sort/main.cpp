/******************************************************************************
*  File: main.cpp
*  Author:  Vaddanak Seng
*  Purpose: Function main tests functions getInfixExpression and radixSort.
******************************************************************************/

#include "functions.h"

#include <iostream>
#include <string>
#include <vector>

//function prototype
void printArray(const std::vector<std::string>& nums);
 
/**
* Purpose: This function tests functions getInfixExpression and radixSort.
* Precondition: None.
* Postcondition: Functions getInfixExpression and radixSort fully tested.
*/
int main(int argc, char** args) {
 
   //turn ON debug
   //debug = true;   
   
   //testing getInfixExpression(postfixString)
   std::string postfix[] = 
   {
      "d", //hint: d  
      "ab+cd-*", //hint: ((a+b)*(c-d))
      "-a -b + -c -d - *", //hint: ((a + b) * (c - d))
      "ab+", //hint: a+b 
      "2 5 * 3 +", //hint: ((2*5)+3)
      "3 4 5 + *", //hint: (3 * (4 + 5)) 
      "345+*", //hint: (3*(4+5)) 
      "1 2 + 3 +", //hint: ((1+2)+3)   
      "1 -2 3 + +", //hint: (1+(2+3))   
      "1 2 - 3 + 4 + 5 + 6 + 7 +", //hint:  ((((((1-2)+3)+4)+5)+6)+7)
      "3 2 + 4 2 - * 8 7 + /",    //hint:  (((3+2)*(4-2))/(8+7))
      "300 23 + 43 21 - * 84 7 + /", //hint:  (300+23)*(43-21)/(84+7)
      //hint:  (-4 + -8888) * (6 - -5) / ((-3 - -2) * (-2 + 2))  
      "-4 -8888 + +6 -5 - * -3 -2 - -2 +2 + * /",  
      "5 1 2 + 4 * + 3 -",  //hint:  (5+((1+2)*4)−3)
      " x y * 3 z / + 4 *", //hint:  (x * y + 3 / z) * 4
      "2 3 + 6 X * * 7 - ", //hint:  ((2+3)*(6*X))-7
      "x y - z + w -", //hint:  ((x-y+z)-w
      "x 2 w + y z * - /", //hint:   x/((2+w)-(y*z))
      "2 x +  4 *" //hint:   (2+x)*4
   };  
          
   for(size_t i = 0; i < sizeof(postfix)/sizeof(*postfix); ++i)
      std::cout <<"postfix: " <<postfix[i] <<"   -->   infix: "
             <<getInfixExpression(postfix[i]) <<std::endl;
       
   //testing radixSort
   std::string radixString1[] = 
      {"329", "457", "657", "839", "436", "720", "355", "432", "909", "1",
        "3", "45", "12", "0", "9", "9", "720", "354"};
   std::vector<std::string> arr1(radixString1,
      radixString1+(sizeof(radixString1)/sizeof(*radixString1)));
   std::cout <<"\nBefore sort base 10:  ";
   printArray(arr1);              
   radixSort(arr1, 3, 10);    
   std::cout <<"After sort base 10:  ";      
   printArray(arr1);
   
   std::string radixString2[] = 
      { "0110", "1000", "1001", "0011", "0001", "1010", "0111", "10001",
        "11001", "10100", "1000110", "1001100", "11111", "11010", "100001"};
   std::vector<std::string> arr2(radixString2,
      radixString2+(sizeof(radixString2)/sizeof(*radixString2)));
   std::cout <<"\nBefore sort base 2:  ";      
   printArray(arr2);              
   radixSort(arr2, 7, 2);    
   std::cout <<"After sort base 2:  ";      
   printArray(arr2);
   
   std::string radixString3[] = 
      { "F0F8FF", "FAEBD7", "00FFFF", "7FFFD4", "F0FFFF", "F5F5DC", "FFE4C4",
        "000000", "FFEBCD", "0000FF", "8A2BE2", "A52A2A", "DEB887", "7FFF00"};
   std::vector<std::string> arr3(radixString3,
      radixString3+(sizeof(radixString3)/sizeof(*radixString3)));
   std::cout <<"\nBefore sort base 16:  ";      
   printArray(arr3);              
   radixSort(arr3, 6, 16);    
   std::cout <<"After sort base 16:  ";      
   printArray(arr3);
   
   std::string radixString4[] = 
      { "255S", "2S", "LFLS", "RYS", "GJDGXS", "Y", "A", "10001", "W", "VU",
        "11001", "AZ", "1000110", "U7", "T", "CRE66I9S", "11010", "GJDGXS"};
   std::vector<std::string> arr4(radixString4,
      radixString4+(sizeof(radixString4)/sizeof(*radixString4)));
   std::cout <<"\nBefore sort base 36:  ";      
   printArray(arr4);              
   radixSort(arr4, 8, 36);    
   std::cout <<"After sort base 36:  ";      
   printArray(arr4);   

   return 0;
}  
 
/**
* Purpose: Function prints content of a vector.
* Precondition: Parameter "num" is vector with content to print.
* Postcondition: The content of vector object is printed to console with
*     a space separating them.
*/
void printArray(const std::vector<std::string>& nums) {
   std::vector<std::string> num = nums;
   for( std::vector<std::string>::iterator iter = num.begin();
        iter != num.end(); ++iter )
      std::cout <<*iter <<"  ";
   std::cout <<std::endl;               
}

