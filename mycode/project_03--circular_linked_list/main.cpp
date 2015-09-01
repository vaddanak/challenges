/******************************************************************************
*  File: main.cpp
*  Author:  Vaddanak Seng
*  Purpose: The main() function is implemented to test List class template.      
******************************************************************************/

#include "circularLinkedList.h"
#include <iostream>
#include <string>

/**
* Purpose:  Class Test holds a single data member to test with List class.
* How-to-use:
*     1)  A Test object is created using constructor Test(string).
*     2)  It is displayed using operator<<(..).
*/
class Test {
   public:
   Test(const std::string& name="") : name(name) {}
   
   private:
   std::string name;
   friend std::ostream& operator<<(std::ostream& out, const Test& rhs) {
      return out <<rhs.name;       
   }  
};
     
/**
* Purpose: Function main tests List class template. 
* Precondition: List class template is defined and implemented.
* Postcondition: List class is instantiated and member functions are called.
*/
int main(int argc, char ** args) {   
   
   debug = true; //TURN ON DEBUG
   
   std::cout <<"Creating empty list..." <<std::endl;
   List<int> list;   
   std::cout <<"   size: " <<list.getSize() 
             <<"  isEmpty? " <<std::boolalpha <<list.isEmpty() 
             <<"  content: ";
   list.display(std::cout);
     
   std::cout <<"Inserting at consecutive positions..." <<std::endl;
   list.insert(3,0);
   list.insert(4,1);  
   list.insert(5,2);    
   list.insert(6,3);  
   list.insert(7,4);
   std::cout <<"   size: " <<list.getSize() 
             <<"  isEmpty? " <<std::boolalpha <<list.isEmpty()
             <<"  content: ";
   list.display(std::cout); 
   
   std::cout <<"Inserting at random positions..." <<std::endl;      
   list.insert(33,0); //at index 0 (position 0)
   list.insert(55,2);  
   list.insert(77,4);  
   list.insert(88,5);  
   list.insert(99,9); //at index 9 (position 9)
   list.insert(100,11);  //won't insert bc index 11 is "out of bounds"
   list.insert(99,-1);  //won't insert bc index -1 "out of bounds"
   std::cout <<"   size: " <<list.getSize()
             <<"  isEmpty? " <<std::boolalpha <<list.isEmpty()
             <<"  content: ";
   list.display(std::cout); 
   
   std::cout <<"Removing at random positions..." <<std::endl;     
   list.remove(0); //at index 0      
   list.remove(3); //at index 3   
   list.remove(7); //at index 7  
   list.remove(7);  //won't remove bc index 7 is "out of bounds"
   list.remove(-1);  //won't remove bc index -1 "out of bounds" 
   std::cout <<"   size: " <<list.getSize()
             <<"  isEmpty? " <<std::boolalpha <<list.isEmpty()
             <<"  content: ";
   list.display(std::cout); 
   
   std::cout <<"Create copy using copy constructor..." <<std::endl;
   List<int> copy1(list);
   std::cout <<"   size: " <<copy1.getSize() 
             <<"  isEmpty? " <<std::boolalpha <<copy1.isEmpty()
             <<"  content: ";
   copy1.display(std::cout);    
   
   std::cout <<"Create copy using assignment operator..." <<std::endl;
   List<int> copy2;
   copy2 = list;
   std::cout <<"   size: " <<copy2.getSize()
             <<"  isEmpty? " <<std::boolalpha <<copy2.isEmpty()
             <<"  content: ";
   copy2.display(std::cout);
   
   std::cout <<"Testing overloaded extraction operator..." <<std::endl;
   std::cout <<"   " <<copy1 <<std::endl;
   
   std::cout <<"Removing all items in list..." <<std::endl;
   while(list.getSize())
      list.remove(0);      
   std::cout <<"   size: " <<list.getSize()
             <<"  isEmpty? " <<std::boolalpha <<list.isEmpty()
             <<"  content: ";
   list.display(std::cout);
   
   std::cout <<"Creating list with user-defined type..." <<std::endl;
   List<Test> soldiers;
   soldiers.insert(Test("Mike"),0);
   soldiers.insert(Test("Mary"),1);
   soldiers.insert(Test("Jack"),2);
   soldiers.insert(Test("Jill"),3);
   soldiers.insert(Test("Pat"),4);
   std::cout <<"   size: " <<soldiers.getSize()
             <<"  isEmpty? " <<std::boolalpha <<soldiers.isEmpty()
             <<"  content: ";
   soldiers.display(std::cout);
    
   std::cout <<"=====================================" <<std::endl;
   std::cout <<"Testing runJosephusAlgorithm() using int list " <<std::endl;
   std::cout <<"\nlast soldier: " <<copy2.runJosephusAlgorithm() <<std::endl;
   
   std::cout <<"=====================================" <<std::endl;
   std::cout <<"Testing runJosephusAlgorithm() using user-defined list:\n";
   std::cout <<"\nlast soldier: "<<soldiers.runJosephusAlgorithm()<<std::endl;
   
   std::cout <<"=====================================" <<std::endl;
   std::cout <<"Displaying intact, original, user-defined list:\n   ";
   soldiers.display(std::cout);
      
   std::cout <<"=====================================" <<std::endl;
   std::cout <<"Removing all items from user-defined list:" <<std::endl;  
   while(soldiers.getSize())
      soldiers.remove(0);
   std::cout <<"   size: " <<soldiers.getSize()
             <<"  isEmpty? " <<std::boolalpha <<soldiers.isEmpty()
             <<"  content: ";
   soldiers.display(std::cout);
       
   std::cout <<"=====================================" <<std::endl;
   std::cout <<"Testing runJosephusAlgorithm() with empty user-defined "
             <<"list:" <<std::endl;
   std::cout <<"\nlast soldier: " <<soldiers.runJosephusAlgorithm()
             <<std::endl;
          
   return 0; 
}
