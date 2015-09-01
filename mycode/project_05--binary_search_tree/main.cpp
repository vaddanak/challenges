/******************************************************************************
*  File: main.cpp
*  Author:  Vaddanak Seng
*  Purpose: The main function is implemented to test BinarySearchTree
*     class template.      
******************************************************************************/

#include "bst.h"

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <typeinfo>
#include <exception>
#include <cstdlib>
 
//forward declaration
template <class T>
class Fun;
 
//function template prototypes
template <class T>
void tester(const BinarySearchTree<T>& bst, const T& data1, const T& data2);

template <class T>
std::ostream& operator<<(std::ostream& out, const Fun<T>& rhs);
 
/**
* Purpose:  Class Fun holds a single data member to test with
*     BinarySearchTree class.
* How-to-use:
*     1)  The default object is used to create a "garbage" object.
*     2)  Constructor with parameter type T holds argument value internally.
*     3)  The relational operators allow comparison between Fun objects.
*     4)  The Fun(const int&) was implemented, which converts int type
*         to Fun type, inorder for non-numeric types to work with provided
*         remove function,
*         particularly because of line "itemLocation->data = -1".
*     5)  This object type is displayed using operator<<(..).
*/
template <class T>
class Fun {
   public:
   Fun() {} //used to construct garbage object
   Fun(const T& d) { convert(d); }
    
   //convert int to this type; needed because of 
   //line "itemLocation->data = -1" in provided remove function
   Fun(const int& rhs) {
      std::stringstream ss;
      ss <<rhs;
      data = ss.str();     
   }
   
   bool operator==(const Fun& rhs) const { return data==rhs.data; }
   bool operator!=(const Fun& rhs) const { return !operator==(rhs); }
   bool operator<(const Fun& rhs) const { return data<rhs.data; }
   bool operator<=(const Fun& rhs) const { return data<=rhs.data; }
   bool operator>(const Fun& rhs) const { return data>rhs.data; }
   bool operator>=(const Fun& rhs) const { return data>=rhs.data; }   
      
   private:
   std::string data;      
   
   void convert(const T& input);
      
   friend std::ostream& operator<<(std::ostream& out, const Fun<T>& rhs) {
      return out <<rhs.data;
   }
};

/**
* Purpose: It converts generic T type to string, if possible.
* Precondition: T type is expected to be convertible to string type.
* Postcondition: Value of T type is represented as string.     
*/
template <class T>
void Fun<T>::convert(const T& input) {
   try {
      std::stringstream ss;
      ss <<input;
      data = ss.str();
   }
   catch(const std::exception ex) {
      if(debug)
         std::cerr <<"Failed to convert type " 
                   <<typeid(T).name() <<std::endl;
      std::exit(EXIT_FAILURE);                         
   }
}
 
/**
* Purpose: Function main tests BinarySearchTree class template. 
* Precondition: BinarySearchTree class template is defined and implemented.
* Postcondition: BinarySearchTree class was instantiated and member functions
*     performed respective tasks.  All public functions of the
*     BinarySearchTree are tested.  The destructor is executed and evident
*     as a result of a BinarySearchTree object going out of local scope and
*     no memory leak.     
*/
int main(int argc, char** args) {
   debug = true;
   
   //testing with int type; creating a simple tree
   std::cout <<"\n=================================================\n";
   std::cout <<"testing with int type; creating a simple tree\n";
   BinarySearchTree<int> bstInt;       
   bstInt.insert(5);
   bstInt.insert(3);
   bstInt.insert(6);
   bstInt.insert(2);
   bstInt.insert(4);
   bstInt.insert(8);
   bstInt.insert(7);   
   
   tester<int>(bstInt, 3, 9);

   //testing with int type; creating a balanced tree
   std::cout <<"\n\n=================================================\n";
   std::cout <<"testing with int type; creating a balanced tree\n";
   
   int arrInt[] = { 50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24 };
   BinarySearchTree<int> bstInt2;       
   
   for(size_t i = 0 ; i < sizeof(arrInt)/sizeof(*arrInt); ++i)
      bstInt2.insert(arrInt[i]);
   
   tester<int>(bstInt2, 60, 91);   
   
   //testing with user-defined type; creating a balanced tree
   std::cout <<"\n\n=================================================\n";
   std::cout <<"testing with user-defined type; creating a balanced tree\n";
   
   Fun<std::string> arr[] = { 
      Fun<std::string>("NY"), Fun<std::string>("IL"), Fun<std::string>("GA"),
      Fun<std::string>("RI"), Fun<std::string>("MA"), Fun<std::string>("PA"),
      Fun<std::string>("DE"), Fun<std::string>("IN"), Fun<std::string>("VT"),
      Fun<std::string>("TX"), Fun<std::string>("OH"), Fun<std::string>("WY") };
      
   Fun<std::string> MA("MA");
   Fun<std::string> FL("FL");
      
   BinarySearchTree<Fun<std::string> > bstStates;
   for(size_t i = 0 ; i < sizeof(arr)/sizeof(*arr) ; ++i)
      bstStates.insert(arr[i]);   
   
   tester<Fun<std::string> >(bstStates, MA, FL);
   
   //testing with user-defined type; creating a "linear" tree
   std::cout <<"\n\n=================================================\n";
   std::cout <<"testing with user-defined type; creating a \"linear\" tree\n";
   
   std::vector<Fun<std::string> > vStates(arr, arr+sizeof(arr)/sizeof(*arr));
   std::sort(vStates.begin(), vStates.end());
   
   BinarySearchTree<Fun<std::string> > bstStates2;
   std::vector<Fun<std::string> >::iterator iter = vStates.begin();
   for( ; iter != vStates.end() ; ++iter)
      bstStates2.insert(*iter);   
   
   tester<Fun<std::string> >(bstStates2, MA, FL);
  
   return 0;
}

/**
* Purpose: Function template "tester" allows generic data types of
*     BinarySearchTree to be tested with the same operations. 
* Precondition: BinarySearchTree class template is defined and implemented.
* Postcondition: BinarySearchTree class was instantiated and member functions
*     performed respective tasks, with results output to console.
*/
template <class T>
void tester(const BinarySearchTree<T>& bst, const T& data1, const T& data2) {
   
   std::cout <<"Display original tree:" <<std::endl;
   bst.displayGraphic(std::cout);
   
   std::cout <<"Tree is copied by assignment:" <<std::endl;
   BinarySearchTree<T> bstAssign;
   bstAssign = bst;
   bstAssign.displayGraphic(std::cout);
   
   std::cout <<"Tree is copied by copy-constructor:" <<std::endl;
   BinarySearchTree<T> bstCopy(bst);
   bstCopy.displayGraphic(std::cout);
   
   std::cout <<"Tree is empty:" <<std::endl;
   BinarySearchTree<T> bstEmpty;
   bstEmpty.displayGraphic(std::cout);      
   
   std::cout <<"bstEmpty isEmpty: " <<std::boolalpha <<bstEmpty.isEmpty()
             <<std::endl;
   std::cout <<"bst isEmpty: " <<std::boolalpha <<bst.isEmpty() <<std::endl;             
   std::cout <<"search for " <<data1 <<": " <<std::boolalpha 
             <<bst.search(data1) <<std::endl;
   std::cout <<"search for " <<data2 <<": " <<std::boolalpha 
             <<bst.search(data2) <<std::endl;
   std::cout <<"successor to " <<data1 <<": " <<bst.getSuccessor(data1) 
             <<std::endl;
   std::cout <<"predecessor to " <<data1 <<": " <<bst.getPredecessor(data1) 
             <<std::endl;
   std::cout <<"Minimum: " <<bst.getMinimum() <<std::endl;
   std::cout <<"Maximum: " <<bst.getMaximum() <<std::endl;
   std::cout <<"Height: " <<bst.getHeight() <<std::endl;   
   std::cout <<"Size: " <<bst.getSize() <<std::endl;
   
   std::cout <<"inorder : ";
   bst.inorder(std::cout); 
   std::cout <<std::endl;
   
   std::cout <<"postorder : ";
   bst.postorder(std::cout); 
   std::cout <<std::endl;
   
   std::cout <<"preorder : ";
   bst.preorder(std::cout); 
   std::cout <<std::endl;
   
   std::cout <<"before remove " <<data1 <<": " <<std::endl;
   bstCopy.displayGraphic(std::cout);
   bstCopy.remove(data1);
   std::cout <<"after remove " <<data1 <<": " <<std::endl;
   bstCopy.displayGraphic(std::cout);
   
   std::cout <<"before insert " <<data1 <<": " <<std::endl;
   bstCopy.displayGraphic(std::cout);
   bstCopy.insert(data1);
   std::cout <<"after insert " <<data1 <<": " <<std::endl;
   bstCopy.displayGraphic(std::cout);
}


