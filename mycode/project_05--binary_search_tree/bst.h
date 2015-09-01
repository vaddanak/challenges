/******************************************************************************
*  File: bst.h
*  Author:  Vaddanak Seng
*  Purpose: The header file contains BinarySearchTree class template definition
*     and implementation.  The data stored in this binary search tree are
*     expected to be unique and adhere to properties of a binary search tree:
*     for a given node, all left descendants are less than and all right
*     descendants are greater than.
*
*     NOTE:
*     User-defined T types MUST be able to convert "int" type to T type
*     as a result of the provided "remove" function, particularly line
*     "itemLocation->data = -1".  One could accomplish this by implementing
*     constructor T::T(const int&) or T::operator=(const int&).
******************************************************************************/

#ifndef BST_H_
#define BST_H_

#include <iostream>
#include <iomanip>

//global variables
const int INDENT_VALUE = 8;
static bool debug = false;

/**
 * Class to hold binary search trees
 * 
 * Note that this binary search requires that all items be unique
 */
template <class T>
class BinarySearchTree {
   private: //tree node
      class Node {
         public:
            T data;
            Node * left;
            Node * right;
            Node * parent;
            
            Node():left(NULL),right(NULL),parent(NULL) {}
            Node(const T& item) {
               data=item;
               left=NULL;
               right=NULL;
               parent=NULL;
            } 
      };
   public:
      BinarySearchTree();
      BinarySearchTree(const BinarySearchTree&);
      
      ~BinarySearchTree();
      
      bool isEmpty() const;
      bool search(const T&) const;
      
      T getSuccessor(const T&) const;
      T getPredecessor(const T&) const;
      T getMinimum() const;
      T getMaximum() const;
      int getHeight() const;
      int getSize() const;
      
      void inorder(std::ostream&) const;
      void postorder(std::ostream&) const;
      void preorder(std::ostream&) const;
      
      bool insert(const T&);
      bool remove(const T&);
      
      void displayGraphic(std::ostream&) const;
      
      BinarySearchTree& operator=(const BinarySearchTree& rhs);
   private:
      Node * _root;
      
      void searchHelper(const T&, Node *, Node * &) const;
      void searchParent(const T&, Node *, Node * &) const;
      void getMaximumHelper(Node *, Node * &) const;
      void getMinimumHelper(Node *, Node * &) const;
      
      void inorderHelper(std::ostream&, Node *) const;
      void preorderHelper(std::ostream&, Node *) const;
      void postorderHelper(std::ostream&, Node *) const;
      
      void displayGraphicHelper(std::ostream&, const int&, Node *) const;      
      
      void getSuccessorHelper(Node *, Node * &) const;
      void getPredecessorHelper(Node *, Node * &) const;
      
      void copyBinarySearchTree(Node *, Node * &);
      void deleteBinarySearchTree(Node * &);
      
      //additional helper functions
      void findHeight(Node * subtree, int& height) const;
      void findSize(Node * subtree, int& size) const;      
      void copyBinarySearchTree(Node*, Node*&, Node**);
};

/*****************************************************************************/
/********************** Constructors *****************************************/
/*****************************************************************************/

/**
 * Construct a Binary Search Tree Object
 * 
 * Precondition: None
 * Postcondition: An empty BST has been constructed
 * 
 * Worst-Case Time Complexity: O(1)
 */
template<class T>
BinarySearchTree<T>::BinarySearchTree() {
   _root = NULL;
}

/**
 * Copy constructor for a Binary Search Tree Object
 * 
 * Precondition: Original is a Binary Search Tree
 * Postcondition: An empty BST has been constructed
 * 
 * Worst-Case Time Complexity: O(1)
 */
template<class T>
BinarySearchTree<T>::BinarySearchTree(const BinarySearchTree& original) {   
   _root = NULL;
   copyBinarySearchTree(original._root, _root);
}

/*****************************************************************************/
/********************** Destructor *******************************************/
/*****************************************************************************/

/**
 * Destructor for a Binary Search Tree
 * 
 * Precondition: The life of the binary search tree is over
 * Postcondition: Memory used by the binary search tree is freed
 * 
 * Worst-Case Time Complexity: O(n)
 */
template<class T>
BinarySearchTree<T>::~BinarySearchTree() {
   deleteBinarySearchTree(_root);
}

/*****************************************************************************/
/********************** Accessors ********************************************/
/*****************************************************************************/

/**
 * Check if the Binary Search Tree is empty
 * 
 * Precondition: None
 * Postcondition: Return true if the Binary Search Tree is empty and false
 *    otherwise
 * 
 * Worst-Case Time Complexity
 */
template <class T>
bool BinarySearchTree<T>::isEmpty() const {
   return (_root==NULL);
}

/**
 * Search the binary search tree for an item
 * 
 * Precondition: None
 * Postcondition: Returns true if item found, and false otherwise
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
bool BinarySearchTree<T>::search(const T& item) const {
   bool found = false;
   Node * currentRoot = _root;
   while(currentRoot) {
      if(currentRoot->data == item) {
         found = true;
         break;
      }
      if(item < currentRoot->data)
         currentRoot = currentRoot->left;
      else
         currentRoot = currentRoot->right;         
   }
   return found;   
}

/**
 * Search the binary search tree for an item
 * 
 * Precondition: subtreePtr points to a subtree of this binary search tree
 * Postcondition: Set itemLocation to point to the item if it is found and to 
 *    NULL otherwise
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
void BinarySearchTree<T>::searchHelper(const T& item,
                                       Node * subtreePtr, 
                                       Node * &itemLocation) const {
   // if this is an empty binary search tree, return null 
   if (subtreePtr==NULL) {
      itemLocation = NULL;
      return;
   }
   
   // if this is the item we are looking for, return this item
   if (subtreePtr->data==item) {
      itemLocation = subtreePtr;
      return;
   }
   
   // look for the parent of the specified item
   Node * parent = NULL;
   searchParent(item, subtreePtr, parent);
      
   // return the appropriate child
   if (item < parent->data) {
      itemLocation = parent->left;
   } else {
      itemLocation = parent->right;
   }
}

/**
 * Search the binary tree for the parent for an item
 * 
 * Precondition: subtreePtr points to a subtree of this binary search tree
 * Postcondition: Sets itemLocation to point to the direct parent of the node 
 *    that contains item OR sets itemLocation to point to the node that will be
 *    the parent of a node that contains item if item is inserted into the tree
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
void BinarySearchTree<T>::searchParent(const T& item, 
                                       Node * subtreePtr, 
                                       Node * &parentLocation) const {
   // if this is an empty tree return NULL
   if (subtreePtr==NULL) {
      parentLocation = NULL;
      return;
   }
   
   // if we have found what we are looking for, then return
   if (item==subtreePtr->data) {
      parentLocation = subtreePtr->parent;
      return;
   }
   
   // holds a pointer to the next subtree that we will look at
   Node * nextSubtree = NULL;
   
   if (item < subtreePtr->data) { // smaller items in left subtree
      nextSubtree = subtreePtr->left;
   } else { // larger items in right subtree
      nextSubtree = subtreePtr->right;      
   }
   
   if (nextSubtree==NULL) {
      parentLocation = subtreePtr;
   } else {
      searchParent(item,nextSubtree, parentLocation);
   }
}

/**
 * Search the binary tree for the inorder successor of item. If the item is not 
 * present in the tree, then return a garbage value
 * 
 * Precondition: None
 * Postcondition: Returns the inorder successor of the node containing item.
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
T BinarySearchTree<T>::getSuccessor(const T& item) const {
   // find the item in the tree
   Node * location = NULL;
   searchHelper(item,_root,location);
   
   if (location == NULL) { // item not in BST      
      return T(); // garbage
   }
   
   Node * successor = NULL;
   getSuccessorHelper(location,successor);
   
   if (successor != NULL) {
      return successor->data;
   } else {      
      return T(); // garbage
   }
}

/**
 * Search the binary tree for the inorder successor of the node, item
 * 
 * Precondition: item points to a node in the binary search tree. 
 *    succLocation points to NULL
 * Postcondition: succLocation points to the inorder successor of item in the
 *    binary search tree
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
void BinarySearchTree<T>::getSuccessorHelper(Node * item, 
                                             Node * &succLocation) const {
   if (item->right==NULL) { // successor is an ancestor
      succLocation = item->parent;
      while (succLocation!=NULL && succLocation->data<item->data) {
         succLocation=succLocation->parent;
      }
   } else { // successor is a descendant
      getMinimumHelper(item->right,succLocation);
   }
}

/**
 * Search the binary tree for the inorder predecessor of item. If the item is 
 * not present in the tree, then return a garbage value
 * 
 * Precondition: None
 * Postcondition: Returns the inorder predecessor of item
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
T BinarySearchTree<T>::getPredecessor(const T& item) const {
   // find the item in the tree
   Node * location = NULL;
   searchHelper(item,_root,location);
   
   if (location == NULL) { // item not in BST      
      return T(); // garbage
   }
   
   Node * predecessor = NULL;
   getPredecessorHelper(location,predecessor);
   
   if (predecessor != NULL) {
      return predecessor->data;
   } else {      
      return T(); // garbage
   }
}

/**
 * Search the binary tree for the inorder predecessor of the node, item
 * 
 * Precondition: item points to a node in the binary search tree. 
 *    predLocation points to NULL
 * Postcondition: predLocation points to the inorder predecessor of item in the
 *    binary search tree
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
void BinarySearchTree<T>::getPredecessorHelper(Node * item, 
                                             Node * &predLocation) const {
   if (item->left==NULL) { // predecessor is an ancestor
      predLocation = item->parent;
      while (predLocation!=NULL && predLocation->data>item->data) {
         predLocation=predLocation->parent;
      }
   } else { // predecessor is a descendant
      getMaximumHelper(item->left,predLocation);
   }
}

/**
 * Determine the maximum item in the binary search tree
 * 
 * Precondition: None
 * Postcondition: Return the maximum value held in the binary search. If the
 *    tree is empty then a garbage value is returned
 * 
 * Worst-case time Complexity: O(h), where h is the height of the tree
 */
template <class T>
T BinarySearchTree<T>::getMaximum() const {
   if(_root == NULL)
      return T(); //garbage
   Node * maxLocation = NULL;
   getMaximumHelper(_root, maxLocation); //using non-empty subtree    
   return maxLocation->data;
}

/**
 * Determine the maximum item for the subtree rooted at subtreeRoot
 * 
 * Precondition: subtreeRoot is a node in the binary search tree.
 *    maxLocation points to null
 * Postcondition: maxLocation points to the maximum item in the subtree
 *    rooted at subtreeRoot (points to NULL for an empty subtree)
 * 
 * Worst-case time Complexity: O(h), where h is the height of the tree
 */
template <class T>
void BinarySearchTree<T>::getMaximumHelper(Node * subtreeRoot,
                                           Node * &maxLocation) const {
   maxLocation = subtreeRoot;
   if(maxLocation) // using non-empty subtree rooted at "subtreeRoot"
      while(maxLocation->right)
         maxLocation = maxLocation->right;
}

/**
 * Determine the minimum item in the binary search tree
 * 
 * Precondition: None
 * Postcondition: Return the minimum value held in the binary search. If the
 *    tree is empty then a garbage value is returned
 * 
 * Worst-case time Complexity: O(h), where h is the height of the tree
 */
template <class T>
T BinarySearchTree<T>::getMinimum() const {
   if(_root == NULL) //validating subtree
      return T(); // garbage
   Node * minLocation = NULL;
   getMinimumHelper(_root, minLocation); // using non-empty subtree
   return minLocation->data;
}

/**
 * Determine the minimum item for the subtree rooted at subtreeRoot
 * 
 * Precondition: subtreeRoot is a node in the binary seach tree.
 *    minLocation points to null
 * Postcondition: minLocation points to the minimum item in the subtree
 *    rooted at subtreeRoot (points to NULL for an empty subtree)
 * 
 * Worst-case time Complexity: O(h), where h is the height of the tree
 */
template <class T>
void BinarySearchTree<T>::getMinimumHelper(Node * subtreeRoot, 
                                           Node * &minLocation) const {
   minLocation = subtreeRoot;
   if(minLocation) //ensures using non-empty subtree rooted at subtreeRoot
      while(minLocation->left)
         minLocation = minLocation->left;
}

/**
 * Determine the number of levels in a binary search tree. For example,
 * a binary tree with a single node has height 1 and a binary tree
 * with a root and a single child has height 2
 * 
 * Precondition: none
 * Postcondition: Return the number of levels in this binary search tree
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
int BinarySearchTree<T>::getHeight() const {
   int height = 0;
   findHeight(_root, height);
   return height;
}

/**
 * Determine the number of levels in a binary search tree. For example,
 * a binary tree with a single node has height 1 and a binary tree
 * with a root and a single child has height 2
 * 
 * Precondition: Subtree rooted at "subtreeRoot".  Parameter "height" is
 *    storage to hold height data.      
 * Postcondition: Parameter "height" is modified with height of tree.
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::findHeight(Node * subtreeRoot, int& height) const {
   if(subtreeRoot) {
      static int counter = 0;
      ++counter;
      findHeight(subtreeRoot->left, height);
      findHeight(subtreeRoot->right, height);
      if(counter > height)
         height = counter;
      --counter;      
   }
}

/**
 * Determine the number of vertices in the binary search tree.
 * 
 * Precondition: none
 * Postcondition: Return the number of vertices in this binary search tree
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
int BinarySearchTree<T>::getSize() const {
   int size = 0;
   findSize(_root, size);
   return size;      
}

/**
 * Determine the number of vertices in the binary search tree.
 * 
 * Precondition: Subtree rooted at "subtreeRoot".  Parameter "size" is
 *    storage to hold size data.      
 * Postcondition: Parameter "size" is modified with number of vertices.
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::findSize(Node * subtreeRoot, int& size) const {
   if(subtreeRoot) {
      ++size;
      findSize(subtreeRoot->left, size);
      findSize(subtreeRoot->right, size);        
   }
}

/*****************************************************************************/
/********************** Traversals *******************************************/
/*****************************************************************************/

/**
 * Inorder traversal of Binary Search Tree
 * 
 * Precondition: ostream out is open
 * Postcondition: Binary Search Tree has been inorder traversed and values in 
 *    nodes have been output to out
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::inorder(std::ostream& out) const {
   inorderHelper(out, _root);   
}

/**
 * Inorder traversal helper function
 * 
 * Precondition: ostream out is open. subtreePtr points to a subtree of 
 *    this binary search tree
 * Postcondition: subtree with root pointed to by subtreePtr has been output
 *    to output
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::inorderHelper(std::ostream& out, 
                                        Node * subtreePtr) const {
   if(subtreePtr) {      
      inorderHelper(out, subtreePtr->left);
      out <<(subtreePtr->data) <<" ";
      inorderHelper(out, subtreePtr->right);
   }
}

/**
 * Preorder traversal of Binary Search Tree
 * 
 * Precondition: ostream out is open
 * Postcondition: Binary Search Tree has been preorder traversed and values in 
 *    nodes have been output to out
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::preorder(std::ostream& out) const {
   preorderHelper(out, _root);
}

/**
 * Preorder traversal helper function
 * 
 * Precondition: ostream out is open. subtreePtr points to a subtree of 
 *    this binary search tree
 * Postcondition: subtree with root pointed to by subtreePtr has been output
 *    to output
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::preorderHelper(std::ostream& out, 
                                        Node * subtreePtr) const {
   if(subtreePtr) {
      out <<(subtreePtr->data) <<" ";
      preorderHelper(out, subtreePtr->left);
      preorderHelper(out, subtreePtr->right);
   }   
}

/**
 * Postorder traversal of Binary Search Tree
 * 
 * Precondition: ostream out is open
 * Postcondition: Binary Search Tree has been postorder traversed and values in 
 *    nodes have been output to out
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::postorder(std::ostream& out) const {
   postorderHelper(out, _root);
}

/**
 * Postorder traversal helper function
 * 
 * Precondition: ostream out is open. subtreePtr points to a subtree of 
 *    this binary search tree
 * Postcondition: subtree with root pointed to by subtreePtr has been output
 *    to output
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::postorderHelper(std::ostream& out, 
                                        Node * subtreePtr) const {
   if(subtreePtr) {
      postorderHelper(out, subtreePtr->left);
      postorderHelper(out, subtreePtr->right);
      out <<(subtreePtr->data) <<" ";
   }
}

/*****************************************************************************/
/********************** Operations *******************************************/
/*****************************************************************************/

/**
 * Insert item into the binary search tree
 * 
 * Precondition: item is not present in the binary search tree
 * Postcondition: Binary search tree has been modified with the item inserted
 *    at the proper position to maintain the binary search tree property.
 *    Returns true if item is inserted into the tree and false otherwise
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
bool BinarySearchTree<T>::insert(const T& item) {
   // create a  new node
   Node * newNode = new Node(item);
   if(newNode==NULL) {
      if(debug)
         std::cerr <<"Failed to allocate memory!" <<std::endl;
      return false;
   }      
   
   // if we are inserting into an empty tree
   if (_root==NULL) {
      _root = newNode;
      return true;
   }
   
   // if the item is the root of the tree
   if (_root->data==item) {
      delete newNode;
      return false;
   }
  
   // find the parent of the item
   Node * parentLocation = NULL;
   searchParent(item,_root,parentLocation);
   
   // add the new node to the tree, if it is not already there
   if (item < parentLocation->data) { // left child
      if (parentLocation->left!=NULL) {
         delete newNode;
         return false;
      }
      parentLocation->left = newNode;
   } else { // right child
      if (parentLocation->right!=NULL) {
         delete newNode;
         return false;
      }
      parentLocation->right = newNode;
   }
   
   // set the parent of the new node
   newNode->parent = parentLocation;
   
   return true;
}

/**
 * Remove item from the binary search tree
 * 
 * Precondition: none
 * Postcondition: binary search tree has been modified with  the item
 *    removed, if present. binary search tree property is maintained.
 *    returns true if insertion is successful and false otherwise.
 * 
 * Worst-Case Time Complexity: O(h), where h is the height of the tree
 */
template <class T>
bool BinarySearchTree<T>::remove(const T& item) {
   // find the item in the binary search tree
   Node * itemLocation = NULL;
   searchHelper(item,_root,itemLocation);
   
   // determine the item is in the binary search tree
   if (itemLocation==NULL) {
      return false;
   }
   
   // get the parent of the item to be deleted
   Node * itemParent = itemLocation->parent;
   
   // The node containing item has 2 children
   if (itemLocation->left != NULL && itemLocation->right!=NULL) {      
      // Find the inorder successor node of item
      Node * itemSuccessor = NULL;
      getSuccessorHelper(itemLocation, itemSuccessor);
      
      // copy the data
      itemLocation->data = itemSuccessor->data;
      
      // redirect the itemLocation pointer to the successor
      // since that is now what will be deleted
      itemParent = itemSuccessor->parent;
      itemLocation = itemSuccessor;
      
      //itemLocation->data = -1; //original line
      itemLocation->data = T(); //change to work with generic data type
   }
   
   // We now know that the item being deleted has 0 or 1 children
   
   // determine which subtree, if any, has children
   Node * itemSubtree = itemLocation->left;
   if (itemSubtree == NULL) {
      itemSubtree = itemLocation->right;
   }
      
   if (itemParent == NULL) { // root being deleted
      _root = itemSubtree;
      if (_root!=NULL) {
         _root->parent=NULL;       
      }
   } else if (itemParent->left == itemLocation) { 
      itemParent->left = itemSubtree;
   } else {
      itemParent->right = itemSubtree;
   }
   
   if (itemSubtree!=NULL) {
      itemSubtree->parent = itemParent;
   }
      
   // free the memory for this item
   delete itemLocation;
      
   return true;
}

/*****************************************************************************/
/********************** Input/Output *****************************************/
/*****************************************************************************/

/**
 * Graphic output of binary search tree
 * 
 * Precondition: ostream out is open
 * Postcondition: Graphical representation of binary search tree has been 
 *    output to out.
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::displayGraphic(std::ostream& out) const {
   displayGraphicHelper(out,0,_root);
}

/**
 * Graphic output of binary search tree helper function
 * 
 * Precondition: ostream out is open. subtreePtr points to a subtree of 
 *    this binary search tree
 * Postcondition: Graphical representation of subtree with root pointed to
 *    by subtreePtr has been output to out, indented indent spaces.
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::displayGraphicHelper(std::ostream& out, 
                                               const int& indent,
                                               Node * subtreePtr) const {
   if (subtreePtr==NULL) {
      return;
   }
   
   displayGraphicHelper(out,indent+INDENT_VALUE, subtreePtr->right);
   out << std::setw(indent) << " " << subtreePtr->data << std::endl;
   displayGraphicHelper(out,indent+INDENT_VALUE, subtreePtr->left);
}

/*****************************************************************************/
/********************** Operators ********************************************/
/*****************************************************************************/

/**
 * Assign a copy of a binary search tree object to the current object
 * 
 * Preconditions: N/A
 * Postconditions: A copy of rhs has been assigned to this object. A non-const
 *    reference to this binary search tree is returned.
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
BinarySearchTree<T>& BinarySearchTree<T>::operator=(const BinarySearchTree& 
                                                          rhs) {
   if (this != &rhs) {          
      copyBinarySearchTree(rhs._root, _root);
   }
   return *this;
}

/*****************************************************************************/
/********************** Functions ********************************************/
/*****************************************************************************/

/**
 * Copy the Binary Search Tree rooted at original
 * 
 * Preconditions: original is a Binary Search Tree
 * Postcondition: copy holds a copy of the Binary Search Tree
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::copyBinarySearchTree(Node * original, Node * &copy) {
   // ensure that any memory allocated by the copy is properly freed
   deleteBinarySearchTree(copy);
   copyBinarySearchTree(original, copy, NULL);
}

/**
 * Copy the Binary Search Tree rooted at original
 * 
 * Preconditions: original is a Binary Search Tree.  "parent" refers to
 *    parent of current node.
 * Postcondition: copy holds a copy of the Binary Search Tree
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::copyBinarySearchTree( Node * original, Node*& copy,
                                                Node** parent) {
   if(original) {      
      copy = new Node(original->data);
      if(copy==NULL) {
         if(debug)
            std::cerr <<"Failed to allocate memory!" <<std::endl;
         return;            
      }        
      copy->parent = parent? (*parent) :NULL;
      copyBinarySearchTree(original->left, copy->left, &copy);
      copyBinarySearchTree(original->right, copy->right, &copy);
   }
}

/**
 * Delete the Binary Search Tree rooted at bstRoot
 * 
 * Preconditions: The life of the Binary Search Tree rooted at bstRoot is over
 * Postconditions: Memory used by the Binary Search Tree rooted at bstRoot is
 *    freed
 * 
 * Worst-Case Time Complexity: O(n)
 */
template <class T>
void BinarySearchTree<T>::deleteBinarySearchTree(Node * &bstRoot) {
   if(bstRoot) {
      deleteBinarySearchTree(bstRoot->left);
      deleteBinarySearchTree(bstRoot->right);
      delete bstRoot;
      bstRoot = NULL;
   }
}

#endif /* BST_H_ */
