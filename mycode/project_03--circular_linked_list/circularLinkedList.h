/******************************************************************************
*  File: circularLinkedList.h
*  Author:  Vaddanak Seng
*  Purpose: The header file contains List class template definition and
*     implementation.  The List class provides storage of data using
*     a circular, singly linked list.  The basic operations are also provided
*     to manipulate the list content.
******************************************************************************/

#ifndef CIRCULARLINKEDLIST_H_
#  define CIRCULARLINKEDLIST_H_

#include <iostream>
#include <new> //std::nothrow
#include <cstdlib> //std::rand, std::srand
#include <ctime> //std::time

//forward declaration for use in function declaration
template <class T> 
class List; 

//template function declaration
template <class T> 
std::ostream& operator<<(std::ostream& out, const List<T>& list);

//global variables that have file scope only (ie static)
static const int TWICE = 2;
static const int STEP = 1;
static const int START_INDEX = 0;
static bool debug = false; //turn on/off console messages for debugging

/**
* Purpose:  List class template stores data in a circular, singly linked list.
* How-to-use:
*     1)  An empty List object is created using default constructor List().
*     2)  A List object copy is created using List(const List&) or
*         operator=(const List&).
*     3)  New data is inserted using insert(const T&, const int&).
*     4)  Data is removed using remove(const int&).
*     5)  The number of data items is obtained using getSize().
*     6)  Whether a list is empty is determined using isEmpty().
*     7)  The list is displayed using display(ostream&) or operator<<(..).
*     8)  Function runJosephusAlgorithm() selects a random list item.
*/
template <class T>
class List {
   private:
      class Node {
         public:
            T data;
            Node * next;
      };
      
   public:
      List();
      List(const List&);
      
      ~List();
      
      int getSize() const;
      int getCapacity() const;
      
      bool isEmpty() const;
      bool insert(const T&, const int&);
      bool remove(const int&);
      
      T runJosephusAlgorithm();      
      
      const List& operator=(const List&);
      
      void display(std::ostream&) const;
      friend std::ostream& operator<< <>(std::ostream&, const List<T>&); 
      
   private:
      Node * _first; // pointer to the first element of the linked list
      
      void copyCircularLinkedList(const List& source);
      Node* findNodeBeforePosition(const int& position);
      void removeAllNodes();
};

/**
* Purpose: Non-member template function displays content of list.
* Precondition: "out" specifies output stream.  "list" specifies object
*     from which to extract content.
* Postcondition: "list" content is output to "out" stream.  Reference to
*     output stream is returned.
*/
template <class T>
std::ostream& operator<<(std::ostream& out, const List<T>& list) {
   if(!list.isEmpty()) {
      //must specify "class" or "typename" when using inner class type
      typename List<T>::Node * ptr = list._first;
      do {
         out <<(ptr->data) <<" ";
         ptr = ptr->next;
      }
      while(ptr != list._first);
   }
   return out;
}                             

/**
* Purpose: Default constructor initializes data member.
* Precondition: There is memory allocated for "this" list object.
* Postcondition: List object is empty. "_first" pointer is NULL.
*/
template <class T>
List<T>::List() : _first(NULL) {}

/**
* Purpose: Copy constructor copies "original" list content to its own list.
* Precondition: There is memory allocated for "this" list object.
* Postcondition: List object contains a circular, singly-linked list with
*     same content as "original" list. "_first" pointer points to starting
*     node of the circular list.
*/
template <class T>
List<T>::List(const List& original) : _first(NULL) {
   copyCircularLinkedList(original);
}

/**
* Purpose: Destructor releases allocated heap memory back to system.
* Precondition: List object is valid.
* Postcondition: All nodes in linked list are deleted.
*/
template <class T>
List<T>::~List() {
   if(_first)
      removeAllNodes();
}

/**
* Purpose: Helper method duplicates content of "source" list to "this" list.
*     It does not append "source" list to "this" list.
* Precondition: "source" list object is valid.
* Postcondition: "this" list has same data as "source" list and also stored
*     in its own, separate, circular, singly-linked list.
*/
template <class T>
void List<T>::copyCircularLinkedList(const List& source) {
   if(source.isEmpty()) { //checks if source list is empty
      removeAllNodes(); //delete all nodes in "this" list
      _first = NULL;
      return;
   }      
      
   Node* ptrSource = source._first; //use to walk source list
   Node* ptrDest = NULL; //use to walk destination list, which is "this"
   
   do {
      Node* ptr = new(std::nothrow) Node;
      if(!ptr) { //checks if memory allocation for new node is successful
         std::cerr <<"Fail to allocate memory!" <<std::endl;
         return;
      }
      //initialize new node
      ptr->data = ptrSource->data;
      ptr->next = NULL;           
      
      if(!_first) //"this" list is empty
         _first = ptr;                    
      else //"this" list is not empty
         ptrDest->next = ptr;           
                    
      ptrDest = ptr; //points to last node inserted
      ptrSource = ptrSource->next; //points to next node in source list
   }
   while(ptrSource != source._first); //checks if we reached last node

   ptrDest->next = _first; //ensures last node points back to first node
}

/**
* Purpose: Member function determines number of nodes in linked list.
* Precondition: List object is valid.
* Postcondition: Return value is the number of nodes in the linked list.
*/
template <class T>
int List<T>::getSize() const {
   int count = 0;
   if(!isEmpty()) {
      Node * ptr = _first;
      do {
         ++count;
         ptr = ptr->next;
      }
      while(ptr != _first);
   }
   return count;
}

/**
 * Purpose: Get the capacity of a list object.
 * 
 * Note that this function is only provided for compatability with other list
 * implementations.
 * 
 * Precondition: N/A
 * Postcondition: -1 is returned since a pointer based linked list has no
 *     predefined capacity
 * 
 * Copied from Dr. Kouri's provided pointerLinkedList.h file
 */
template <class T>
int List<T>::getCapacity() const {
   return -1;
}

/**
* Purpose: Member function determines if linked list is empty.
* Precondition: List object is valid.
* Postcondition: Return value is true if "_first" is NULL, which means no node
*     in the linked list; otherwise, it returns false.
*/
template <class T>
bool List<T>::isEmpty() const {
   return _first == NULL;
}

/**
* Purpose: Member function inserts node with data in linked list.
* Precondition: "item" is the data of node to insert into the list.
*     "position" is the location in the linked list to insert;
*     it starts with 0.
* Postcondition: Return value is true if insert operation is successful.
*/
template <class T>
bool List<T>::insert(const T& item, const int& position) {
   bool status = false;
   Node * newNode = new(std::nothrow) Node;
   if(!newNode) {
      std::cerr <<"Fail to allocate new node!" <<std::endl;
      return false;
   }
   newNode->data = item;
   newNode->next = NULL;
   
   if(!isEmpty()) {      
      Node * ptr = findNodeBeforePosition(position);
      if(ptr) {
         newNode->next = ptr->next;
         ptr->next = newNode;
         status = true;
         if(position==START_INDEX)
            _first = newNode;
      }  
      else
         delete newNode;       
   }
   else { //special case; insert first node
      _first = newNode;
      newNode->next = newNode;
      status = true;
   }
   return status;
}

/**
* Purpose: Helper function locates the node before specified position.
* Precondition: Linked list is assumed non-empty.  Position is location
*     of node in linked list; position numbering starts with 0.
* Postcondition: Return value is NULL if position value is invalid. Function
*     returns pointer to node whose location is position-1.
*/
template <class T>
typename List<T>::Node* List<T>::findNodeBeforePosition(const int& position) {
   int count = -1;
   
   if(position < START_INDEX)
      return NULL;
   
   Node * ptr = _first;
   bool isFound = false;
   do {
      ++count;
      if( (position==START_INDEX && ptr->next == _first) ||
          count == position-STEP)
      {
         isFound = true;
         break;
      }        
      ptr = ptr->next;        
   }
   while(ptr != _first);

   return isFound?ptr:NULL;
}

/**
* Purpose: Member function removes node at "position" from linked list.
* Precondition: "position" is the location of the node in the linked list
*     to remove; it starts with 0.
* Postcondition: Return value is true if remove operation is successful.
*/
template <class T>
bool List<T>::remove(const int& position) {
   if(isEmpty())
      return false; //nothing was removed bc list is empty
                    
   Node * ptr = findNodeBeforePosition(position);
   if(!ptr)
      return false; //invalid position
      
   if(position > START_INDEX && ptr->next == _first) { //invalid position
      return false;
   }
   else {   
      if(position == START_INDEX) //since first node is removed, so ...
         _first = _first->next; // ... set _first to next node
         
      if(ptr->next == ptr) //last node is removed
         _first = NULL;
                  
      Node * temp = ptr->next; //ptr refers to node before target node
      ptr->next = temp->next; //node before target points to node after target
      delete temp; //remove target node, ie node at position
   }        
   return true;         
}

/**
* Purpose: Helper function deletes all nodes in linked list.   
* Precondition: List object is valid.
* Postcondition: Linked list is empty.  "_first" is NULL.
*/
template <class T>
void List<T>::removeAllNodes() {
   if(isEmpty())
      return;
      
   Node * ptr = _first;   
   Node * temp = NULL;
   do {
      temp = ptr;      
      ptr = ptr->next;
      delete temp;
   }
   while(ptr != _first);
   _first = NULL;
}

/**
* Purpose: Member function copies "original" list to "this" list.
* Precondition: List object is valid.  "original" refers to source list.
* Postcondition: Linked list content in "original" is copied into "this"
*     list object.
*/
template <class T>
const List<T>& List<T>::operator=(const List<T>& original) {
   if(this != &original) {    
      if(_first) 
         removeAllNodes();
      copyCircularLinkedList(original);  
   }    
   return *this;
}

/**
* Purpose: Member function outputs list content to "out" stream.
* Precondition: List object is valid.  "out" is output stream.
* Postcondition: Linked list is output to "out" output stream.
*/
template <class T>
void List<T>::display(std::ostream& out) const {
   out <<*this <<std::endl;
}

/**
* Purpose: Member function randomly selects a soldier.
* Precondition: List object is valid.
* Postcondition: Each iteration removes a soldier from the list.  Each
*     iteration starts with a random counting value and a random starting
*     soldier from the remaining list.  The count starts with the random
*     start soldier until count reaches the random counting value and chosen
*     soldier is removed.  The last soldier that remains is returned.
*/
template <class T>
T List<T>::runJosephusAlgorithm() {
   if(isEmpty()) {          
      return T(); //this is garbage        
   }   
   
   List<T> myCopy(*this); //create copy using copy constructor
   std::srand(std::time(NULL));
   
   if(debug) { //for DEBUG
      std::cout <<"The original list content: "; //for DEBUG
      myCopy.display(std::cout); //for DEBUG
   }        
   
   while(myCopy._first != myCopy._first->next) {
      //get number of nodes(soldiers) remaining in "myCopy" list
      int listSize = myCopy.getSize();
      //get random soldier position from range 0 to listSize-1
      int soldierPosition = std::rand() % listSize;
      //get random count value from range 0 to 2*listSize
      int countTo = std::rand() % (listSize * TWICE + STEP);
      //get node before position "soldierPosition"
      Node* beforeSoldier = myCopy.findNodeBeforePosition(soldierPosition);
                  
      if(debug) { //for DEBUG
         std::cout <<"\nsoldierPosition: " <<soldierPosition //for DEBUG
                   <<"  countTo: " <<countTo //for DEBUG
                   <<"  soldiers: " <<myCopy <<std::endl;//for DEBUG
      }        
            
      while(--countTo > START_INDEX)       
         beforeSoldier = beforeSoldier->next; //walk to next soldier            
                
      Node* selectedSoldier = beforeSoldier->next; //selected soldier
                                    
      if(debug) { //for DEBUG        
         std::cout <<"remove soldier: " <<selectedSoldier->data //for DEBUG
                   <<std::endl; //for DEBUG
      }  
                   
      if(selectedSoldier == myCopy._first) //selected node is _first node
         myCopy._first = myCopy._first->next; //set _first node to next node
      //set node before selected node to point to node after selected node
      beforeSoldier->next = selectedSoldier->next;
      delete selectedSoldier;                   
   }       
   //when myCopy goes out of scope, its destructor called to remove last node
   return myCopy._first->data;
}

#endif //CIRCULARLINKEDLIST_H_
