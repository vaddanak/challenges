/******************************************************************************
*  File: functions.h
*  Author:  Vaddanak Seng
*  Purpose: Function getInfixExpression translates a valid postfix
*     expression to an infix expression.  Function radixSort sorts a
*     collection of numbers of some base between 2 to 36, in an increasing
*     order.
******************************************************************************/

#ifndef FUNCTIONS_H_
#  define FUNCTIONS_H_

#include <vector>
#include <string>
#include <queue>
#include <iostream>
#include <stack>
#include <cctype> //std::isdigit, std::isalpha, std::tolower

//global variable
static bool debug = false;
static const int LOWEST_RADIX = 2;
static const int HIGHEST_RADIX = 36;
static const int RADIX_10 = 10;
static const int RADIX_11 = 11;
static const int INCREMENT = 1;
static const char NULL_CHAR = '\0';
static const int INIT_INT = 0;
static const char CHAR_ZERO = '0';
static const char CHAR_A = 'a';
static const int INVALID_INT = -1;
static const int START_INDEX = 0;
static const int BINARY_OPERATION = 2;

//function prototypes
std::string getInfixExpression(const std::string& postfix);
bool isOperator(const char& operatorChar);
bool containsSpace(const std::string& postfixExpression);

void radixSort( std::vector<std::string>& numbers, const int& digitsPerNumber,
                const int& radix);
char getDigitAtPosition(const std::string& number, const int& digitPosition);
int getBucketIndex(const int& radix, const char& digit);
char getLargestDigit(const int& radix);
bool isValidDigit(const int& radix, const char& digit);

   
/**
* Purpose: Function converts postfix to infix expression.
* Precondition: Parameter "postfix" represents a postfix expression.
* Postcondition: Function returns a string object containing the infix
*     expression.
*/
std::string getInfixExpression(const std::string& postfix) {
   int operatorCount = INIT_INT;
   std::stack<std::string> strings;
   std::string result = postfix;
   bool hasSpace = containsSpace(result);
  
   for( std::string::iterator iter = result.begin();
        iter != result.end(); ++iter )
   {
      //skip to next non-space char
      while(iter!=result.end() && std::isspace(*iter))
         ++iter;
         
      if(iter==result.end()) {
         --iter;
         continue;
      }         
      //If spacing is used in postfix expression, then output will also
      //include spacing. 
      //Negative signed operands will also be correctly displayed.
      //Positive signed operands are displayed without the sign.
      if( isOperator(*iter) && 
          (((iter+INCREMENT)==result.end()) || 
          (hasSpace?std::isspace(*(iter+INCREMENT)):true)) ) 
      {
         ++operatorCount;
         if(strings.size()>= static_cast<size_t>(BINARY_OPERATION)) {
            std::string str1 = strings.top();
            strings.pop();
            std::string str2 = strings.top();
            strings.pop();
            std::string str3 = "(" + str2 + (hasSpace?" ":"") + *iter
                                 + (hasSpace?" ":"") + str1 + ")";
            strings.push(str3);
         }
      }
      else 
         if(!hasSpace) { //for postfix expression without spacing
            if(std::isalnum(*iter)){
               std::string temp;
               temp = *iter;
               strings.push(temp);
            }   
         }                  
         else { //for postfix expression with spacing
            std::string tempNum;                     
            //read all char until next space            
            while(iter!=result.end() && !std::isspace(*iter) ) {
               if(isOperator(*iter) && *iter!='-') {
                  //do nothing                                    
               }
               else 
                  tempNum += *iter;                 
                                 
               ++iter;
            }  
            
            if(tempNum.size())                                   
               strings.push(tempNum);                                           
               
            --iter; 
         }        
   }//end... for-loop        

   int size = strings.size();    
   
   if(size == INCREMENT) {
      result = strings.top();
      strings.pop(); 
      
      if(operatorCount == INCREMENT) 
          result = std::string(result.begin()+INCREMENT, 
                  result.end()-INCREMENT);
   }                        
   
   return result;
}

/**
* Purpose: Helper function determines if space is used in postfix expression
*     separate the operands and operators.
* Precondition: Parameter "postfixExpression" represents a postfix expression.
* Postcondition: Function returns a true if spacing is used to separate
*     the operands and operators; otherwise, it returns false.
*/
bool containsSpace(const std::string& postfixExpression) {
   std::string temp = postfixExpression;
   std::string::iterator iter = temp.begin();
   bool status = false;
   while(iter != temp.end() && std::isspace(*iter))//skip initial space
      ++iter;
   for(; iter != temp.end(); ++iter)
      if(std::isspace(*iter)) {
         status = true;
         break;
      }
   return status;      
}

/**
* Purpose: Helper function determines if argument is an arithmetic operator.
* Precondition: Parameter "operatorChar" is a char.
* Postcondition: Function returns true if the char argument is either
*     +, -, *, or /; otherwise, it returns false.
*/
bool isOperator(const char& operatorChar) {
   bool status = false;   
   switch(operatorChar) {
      case '+':
      case '-':
      case '*':
      case '/':
         status = true;
         break;                  
   }
   return status;
}

/**
* Purpose: Function sorts a collection of numbers.
* Precondition: Parameter "numbers" is a collection of numbers with base
*     "radix".  Parameter "digitsPerNumber" is the largest number of digits for
*     some number in the collection.
* Postcondition: The collection of numbers is sorted in increasing order.
*/
void radixSort( std::vector<std::string>& numbers, const int& digitsPerNumber,
                const int& radix)
{
   std::vector<std::queue<std::string> > buckets(radix);
   std::vector<std::queue<std::string> >::iterator bucketsIter;
   std::vector<std::string>::iterator numbersIter;
   
   //digitPosition 0 is at right-most digit of a number
   for( int digitPosition = INIT_INT, index = INIT_INT; 
        digitPosition < digitsPerNumber; ++digitPosition)
   {
      bucketsIter = buckets.begin();
      numbersIter = numbers.begin();
      
      //put numbers vector in buckets queue
      for( ; numbersIter != numbers.end() ; ++numbersIter) {
         char digit = getDigitAtPosition(*numbersIter, digitPosition);
         index = ((index = getBucketIndex(radix,digit)) > INVALID_INT)?
                  index:START_INDEX;
         (bucketsIter+index)->push(*numbersIter);
      }                   
      
      //retrieve items in buckets queue and put in numbers vector
      for( numbersIter = numbers.begin(); numbersIter != numbers.end() &&
           bucketsIter != buckets.end() ; ++bucketsIter )
      {
         while(!bucketsIter->empty()) {
            *numbersIter = bucketsIter->front();
            bucketsIter->pop();
            ++numbersIter;     
         }
      }
   } 
}   

/**
* Purpose: Helper function gets the character in string "number" at position
*     "digitPosition".
* Precondition: Parameter "number" is a string representing a number with a
*     sequence of 1 or more digits.  Parameter "digitPosition" is the index
*     of the digit.  The rightmost digit is 0.  Position of digits range
*     from 0 to string.size()-1.
* Postcondition: The digit at position "digitPosition" in "number", with
*     right-most digit in position 0, is returned as a char.  If position
*     argument is invalid, a NULL char is returned.
*/
char getDigitAtPosition(const std::string& number1, const int& digitPosition){
   std::string number = number1;
   int stringLength = number.size();
   if(digitPosition < START_INDEX || digitPosition >= stringLength) {
      if(debug)
         std::cerr <<"Digit position " <<digitPosition
                   <<" is out of bounds!" <<std::endl;
      return NULL_CHAR;
   }      
   //position 0 is at rightmost digit      
   int position = stringLength - digitPosition - INCREMENT;
   return number[position];
}  

/**
* Purpose: Helper function determines the index of a bucket; a bucket is a
*     queue object stored in a vector.
* Precondition: Parameter radix is a base between 2 and 36.  Parameter digit
*     is a single digit (a char) that makes up a whole number.
* Postcondition: Bucket index ranges from 0 to radix-1.  Index of an object
*     (bucket) stored in a vector is returned.  Otherwise, an invalid integer
*     flag -1 is returned to indicate either invalid radix, digit, or both.
*/
int getBucketIndex(const int& radix, const char& digit) {
   if(!isValidDigit(radix, digit)) {
      if(debug) 
         std::cerr <<"Radix " <<radix <<" contains invalid digit "
                   <<digit <<std::endl;
      return INVALID_INT; //invalid condition
   }
   
   if(std::isdigit(digit))
      return digit - '0';
      
   return (std::tolower(digit) - 'a') + RADIX_10;
}

/**
* Purpose: Helper function determines the largest digit for a given radix.
* Precondition: Parameter radix is assumed to be between 2 to 36.
* Postcondition: The highest digit for radix is returned as char.  If radix
*     argument is not between 2 and 36, then it is invalid and function
*     returns a NULL char, '\0' as a flag.
*/
char getLargestDigit(const int& radix) {
   if( radix < LOWEST_RADIX || radix > HIGHEST_RADIX) {
      if(debug)
         std::cerr <<"Radix " <<radix <<" is an invalid base!" <<std::endl;
      return NULL_CHAR; //flag for invalid result
   }      
      
   if( radix <= RADIX_10 )
      return (radix - INCREMENT) + '0';
            
   return (radix - RADIX_11) + 'a';
}

/**
* Purpose: Helper function validates a digit for a given radix.
* Precondition: Parameter radix is a base between 2 to 36.  Parameter digit
*     is a single digit of number using radix.
* Postcondition: True is returned if digit is a valid digit for radix;
*     otherwise, it returns false.
*/
bool isValidDigit(const int& radix, const char& digit) {
   char ch = getLargestDigit(radix);
   if(!ch) //validates radix
      return false;
      
   if(!std::isalnum(digit)) //validates digit is a number or letter
      return false;      
   //validates radix 2 to 10 has a number not greater than ch
   if(radix < RADIX_11) { 
      if(!std::isdigit(digit) || digit>ch)
         return false;  
   }         
   else //validates radix 11 to 36 has a letter not greater than ch
      if(std::isalpha(digit) && std::tolower(digit)>ch)
         return false;
         
   return true;     
}

#endif //FUNCTIONS_H_
