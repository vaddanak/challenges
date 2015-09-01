/******************************************************************************
*  File: main.cpp
*  Author:  Vaddanak Seng
*  Purpose: The "main" function will call "outputPermutations(..)" to display 
*     all unique permutations of the passed-in array; it uses various helper 
*     functions to perform the operation.
******************************************************************************/

#include "permutations.h"

#include <iostream>
#include <new>
#include <string>

/**
* Purpose: Test class is a simple definition so I can test
*     outputPermutations(..) using user-defined type.
* How-to-use:
*     1) You create an instance by calling the constructor with arguments
*        for firstname, lastname, age, and weight.
*     2) Overloaded operators == and != are used to determine same objects.
*     3) Overloaded operator<< output string representation of object.
*/
class Test {
   public:
   Test( const char * firstname = "firstDefault",          
         const std::string& lastname = "lastDefault",
         int age = 0, double weight = 0.0) : 
         firstname(firstname), lastname(lastname), age(age), weight(weight) {}
         
   bool operator==(const Test& rhs) {
      if( weight==rhs.weight && age==rhs.age && 
          firstname==rhs.firstname && lastname==rhs.lastname) 
          return true;
      return false;
   }  
   
   bool operator!=(const Test& rhs) {
      return !operator==(rhs);
   }       
      
   friend std::ostream& operator<<(std::ostream& out, const Test& rhs) {
      out <<"[" <<rhs.firstname <<" " <<rhs.lastname 
          <<" " <<rhs.age <<" " <<rhs.weight <<"]";
      return out;
   }
   
   private:
   const char * firstname;   
   std::string lastname;
   int age;
   double weight;  
};

/**
* Purpose: Contact_t struct is a simple definition so I can test
*     outputPermutations(..) using user-defined type.
* How-to-use:
*     1) You create an instance by declaring and defining Contact_t type
*        and identifier and then assign values to member data firstname,
         lastname, and gender.
*     2) Overloaded operators == and != are used to determine same objects.
*     3) Overloaded operator<< output string representation of object.
*/
struct Contact_t {
   std::string firstname;
   std::string lastname;
   std::string gender;
   friend std::ostream& operator<<(std::ostream& out, const Contact_t& rhs) {
      return out<<"["<<rhs.firstname<<" "<<rhs.lastname<<" "<<rhs.gender<<"]";
   }
   bool operator==(const Contact_t rhs) {
      return firstname==rhs.firstname && lastname==rhs.lastname &&
             gender==rhs.gender;
   }
   bool operator!=(const Contact_t rhs) {
      return !operator==(rhs);
   }
};

/**
* Purpose: The "main" function will call "outputPermutations(..)" to display 
*     all unique permutations of the passed-in array.
* Precondition: The functions are implemented in header file permutations.h .
* Postcondition: Function "outputPermutations(..)" is called to display 
*     all unique combination of array elements; it uses various helper 
*     functions to perform the operation.
*/
int main(int argc, char ** args) {
  
   //sample arrays   
   const int SIZE = 3;
   int intArray[] = {0,1,2};  
   double doubleArray[] = {0.0, 1.1, 2.2, 3.3};   
      
   Test testArray[4];
   testArray[0] = Test("Mary","Lamb",20,120.5);
   testArray[1] = Test("Joe","Smoot",15,89.4);   
   testArray[2] = Test("Hero","Smith",45,349.1);
   testArray[3] = Test("Candace","Cat",30,120.45);
   
   
   Contact_t contacts[3];
   contacts[0].firstname = "Mary"; 
   contacts[0].lastname = "Lamb";
   contacts[0].gender = "female";
   contacts[1].firstname = "Joe"; 
   contacts[1].lastname = "Smoot";
   contacts[1].gender = "male";
   contacts[2].firstname = "Hero"; 
   contacts[2].lastname = "Smith";
   contacts[2].gender = "unknown";
                      
   //test function "outputArray(..)"
   std::cout <<"===== TESTING FUNCTION outputArray(..) =====" <<std::endl;
   outputArray<int>(intArray, SIZE, std::cout);
   std::cout <<std::endl;
   outputArray<double>(doubleArray, SIZE, std::cout);
   std::cout <<std::endl; 
   outputArray<Contact_t>(contacts, SIZE, std::cout);
   std::cout <<std::endl;
   outputArray<Test>(testArray, SIZE, std::cout);
   std::cout <<std::endl;           
   
   //test function "factorial(..)"
   std::cout <<"===== TESTING FUNCTION factorial(..) =====" <<std::endl;      
   const int num1 = 1, num2 = 6, num3 = 13;
   std::cout <<"1! = " <<factorial(num1) <<std::endl;
   std::cout <<"6! = " <<factorial(num2) <<std::endl;
   std::cout <<"13! = " <<factorial(num3) <<std::endl;

   //test function "outputPermutations(..)"
   std::cout <<"===== TESTING FUNCTION outputPermutations(..) ====="
             <<std::endl;  
   outputPermutations<int>(intArray, SIZE, std::cout);
   std::cout <<std::endl;   
   outputPermutations<double>(doubleArray, SIZE, std::cout);
   std::cout <<std::endl;
   outputPermutations<double>(doubleArray, 4, std::cout);
   std::cout <<std::endl;
   outputPermutations<Contact_t>(contacts, SIZE, std::cout);
   std::cout <<std::endl;
   outputPermutations<Test>(testArray, 1, std::cout);
   std::cout <<std::endl;
   outputPermutations<Test>(testArray, 2, std::cout);
   std::cout <<std::endl;
   outputPermutations<Test>(testArray, SIZE, std::cout);
   std::cout <<std::endl;  
     
   outputPermutations<Test>(testArray, 4, std::cout);                  
   return 0;
}
