/******************************************************************************
*  File: graph.cpp
*  Author:  Vaddanak Seng
*  Purpose: This is the implementation file for classes Graph, Node, Edge,
*     and MyBad.  Graph represents a graph instance.  Node or Vertex
*     represents each vertex in the graph.  Edge represents a directed arc
*     between a pair of vertices.  MyBad is a custom exception type used in
*     throw statement to indicate some kind of error.
******************************************************************************/

#include "graph.h"

#include <iostream>
#include <iomanip>
#include <sstream>
  
//file-scope variables 
static bool debug = false;
static const char * INFINITY = "\u221E";

/*======= class Graph implementation =======*/ 

/**
* Purpose: This creates a default object with data members properly
*     initialized.  It is mainly useful for containers.
* Precondition: Memory is allocated.
* Postcondition: Instance of Graph type is created with members initialized.     
*/
Graph::Graph() : width(NULL_ZERO), numberOfElements(NULL_ZERO),
                 dataStore(NULL),                 
                 adjacencyArraySize(NULL_ZERO), 
                 adjacencyList(adjacencyArraySize),
                 vertexSet(adjacencyArraySize)
{}
 
/**
* Purpose: This creates a Graph object with the specified dimension.  Graph
*     is expected to be a square.
* Precondition: Memory is allocatd.
* Postcondition: Instance of Graph type is created with members initialized.
*/
Graph::Graph(const int& width) : width(width), numberOfElements(width*width),
                                 dataStore(NULL),                                                              
                                 adjacencyArraySize(TWO*numberOfElements),
                                 adjacencyList(adjacencyArraySize),
                                 vertexSet(adjacencyArraySize) 
{
   createDataStore();        
   createAdjacencyList();
   populateVertexSet();
   populateEdgeSet();
}

/**
* Purpose: This creates a Graph object that is a copy of passed-in argument.
* Precondition: Memory is allocated.
* Postcondition: Copy of "rhs" is created.
*/
Graph::Graph(const Graph& rhs) : width(NULL_ZERO), numberOfElements(NULL_ZERO), 
                                 dataStore(NULL),                                                         
                                 adjacencyArraySize(NULL_ZERO),
                                 adjacencyList(adjacencyArraySize),
                                 vertexSet(adjacencyArraySize)
{
   operator=(rhs);
} 

/**
* Purpose: Destructor releases allocated memory.
* Precondition: Object is valid.
* Postcondition: Resources have been released.
*/
Graph::~Graph() {  
   removeDataStore();     
   removeAdjacencyList();
}
  
/**
* Purpose: This copies "rhs" content into "this" object content.
* Precondition: Object is valid.
* Postcondition: This object contains same content as "rhs".
*/
Graph& Graph::operator=(const Graph& rhs) {   
   if(this != &rhs) {
      removeDataStore();        
      removeAdjacencyList();        
    
      width = rhs.width;
      numberOfElements = rhs.numberOfElements; 
      adjacencyArraySize = rhs.adjacencyArraySize;  
      adjacencyList.resize(adjacencyArraySize);     
      vertexSet.resize(adjacencyArraySize);       
      
      createDataStore();
      copyDataStore(rhs.dataStore); 
            
      createAdjacencyList();
      populateVertexSet();
      populateEdgeSet();
   }
   return *this;
}

/**
* Purpose: This provides access to the set of vertices of this graph.
* Precondition: Graph object is valid.
* Postcondition: A set of vertices is returned.
*/
std::vector<Vertex>& Graph::getVertexSet() {
   return vertexSet; 
}

/**
* Purpose: This provides access to the set of directed arcs/edges between
*     pairs of vertices in this graph.
* Precondition: Graph object is valid.
* Postcondition: A set of arcs/edges is returned.
*/
const std::vector<Edge>& Graph::getEdgeSet() const {
   return edgeSet; 
}

/**
* Purpose: This provides the side length of the square graph.
* Precondition: Graph object is valid.
* Postcondition: The side length of the graph is returned.
*/
int Graph::getWidth() const { 
   return width; 
}

/**
* Purpose: This gives the number of elements in the adjacent list container,
*     which is 2*width*width.
* Precondition: Graph object is valid.
* Postcondition: The number of adjacent-list elements is returned.
*/
int Graph::getAdjacencySize() const { 
   return adjacencyArraySize; 
}

/**
* Purpose: This displays the graph data as obtained from input.txt file.
* Precondition: Graph object is valid.
* Postcondition: Graph data is displayed to console.
*/
void Graph::showDataStore() const {
   debug = true;
   const int WIDTH = 4;

   if(dataStore) {
      std::cout <<"\nGraph dataStore ..." <<std::endl;
      for(int i = 0; i < numberOfElements ; ) {
         std::cout <<std::setw(WIDTH) <<dataStore[i++];
         if( !(i%width) )
            std::cout <<std::endl;
      }
      std::cout <<std::endl;   
   }

}

/**
* Purpose: This allows access to graph data.
* Precondition: "index" is between 0 to width*width-1.
* Postcondition: A reference to graph data at "index" location is returned if
*     index is valid; otherwise, it throws MyBad.
*/
int& Graph::operator[](const int& index) {
   if(!dataStore) //array not available
      throw MyBad("Array dataStore is NULL");
   if(index < 0 || index >= numberOfElements) { //index is out of bounds
      std::stringstream ss;
      ss <<"Index is out of bounds. Must be between 0 and less than ";      
      ss << numberOfElements << ".";
      throw MyBad(ss.str());     
   }          
   return dataStore[index];
}

/**
* Purpose: This allows access to vertices contained in adjacency list.
* Precondition: "index" is between 0 to 2*width*width-1.
* Postcondition: If "index" is valid, pointer to a vertex at "index" location
*     is returned; otherwise, it returns NULL.
*/
const Node* Graph::operator()(int index) const {   
   if(!adjacencyList.size()) //array not available      
      return NULL;         
   if(index < 0 || index >= adjacencyArraySize) { //index is out of bounds      
      return NULL;
   }             
   return &adjacencyList[index];
}

/**
* Purpose: This allocates and initializes memory for graph data.
* Precondition: Graph object is valid.
* Postcondition: Memory has been allocated for dataStore and initialized.
*/
int* Graph::createDataStore() {   
   dataStore = new int[numberOfElements];
   if(!dataStore) { //make sure allocate is good
      std::cerr <<"Fail to allocate memory" <<std::endl;
   }
   //initialize array for graph elements
   for(int i = 0; i < numberOfElements; ++i)
      dataStore[i] = NULL_ZERO;
   
   return dataStore;
}

/**
* Purpose: This displays content of adjacency list to console.
* Precondition: Graph object is valid.
* Postcondition: Content of adjacency list is displayed to console.
*/
void Graph::showAdjacencyList() const {
   if(adjacencyList.size()) {
      std::cout <<"\nAdjacency list ..." <<std::endl;
      std::stringstream ss;
      for(size_t i = 0; i < adjacencyList.size(); ++i) {
         ss.str() = "";
         ss <<"[i=" <<adjacencyList[i].getId() 
            <<",d=" <<adjacencyList[i].getDistance()
            <<"] -> ";
         Node* temp = adjacencyList[i].next;
         while(temp) {            
            ss <<"[i=" <<temp->getId() <<",d="; 
            temp->getDistance() < DISTMAX ?
               ss <<temp->getDistance() : ss <<INFINITY;
            ss <<"] -> ";
            temp = temp->next;                      
         }   
         ss <<"NULL" <<std::endl;    
      }
      std::cout <<ss.str() <<std::endl;   
   }
}

/**
* Purpose: This copies graph data from "sourceData" into "this" dataStore.
* Precondition: "sourceData" is a pointer to source graph data location.
* Postcondition: Graph's "dataStore" is filled with a copy of "sourceData"
*/
void Graph::copyDataStore(const int* sourceData) {
   if(dataStore && sourceData)  
      for(int i = 0; i < numberOfElements ; ++i)
         dataStore[i] = sourceData[i];         
}

/**
* Purpose: This deletes memory allocated for "dataStore"
* Precondition: Graph object is valid.
* Postcondition: "dataStore" allocation has been deleted.
*/
void Graph::removeDataStore() {
   if(dataStore) {
      delete[] dataStore;
      dataStore = NULL;
   }       
}
   
/**
* Purpose: This creates the adjacency list.
* Precondition: Graph object is valid.
* Postcondition: Adjacency list is created containing vertices and associated
*     linked-list of adjacent vertices.
*/
void Graph::createAdjacencyList() {   
   //populate adjacencyList array with Node objects   
   int vSize = static_cast<int>(adjacencyList.size());
   for(int i = 0; i < vSize; ++i) {     
      adjacencyList[i].setId(i);
      adjacencyList[i].setDistance(dataStore[i%numberOfElements]);         
   }     
   
   //for each element at index 0 to n*n-1; horizontal/vertical part
   //check left, right, above, and below
   //if negative, check diagonals in diagonal part
   
   //populate linked-list per array element with adjacent Node objects
   for(int i = 0, index; i < vSize; ++i) {
      //leave the goal vertices alone
      if(i == numberOfElements - STEP || i == TWO*numberOfElements-STEP)
         continue;
         
      index = determineAdjacencyArrayIndex(i,WEST);
      if(index > ERR_VALUE) addNode(i,index);     
         
      index = determineAdjacencyArrayIndex(i,EAST);
      if(index > ERR_VALUE) addNode(i,index);       
      
      index = determineAdjacencyArrayIndex(i,NORTH);
      if(index > ERR_VALUE) addNode(i,index); 
      
      index = determineAdjacencyArrayIndex(i,SOUTH);
      if(index > ERR_VALUE) addNode(i,index);   
      
      index = determineAdjacencyArrayIndex(i,NORTHWEST);
      if(index > ERR_VALUE) addNode(i,index);
      
      index = determineAdjacencyArrayIndex(i,NORTHEAST);
      if(index > ERR_VALUE) addNode(i,index);
      
      index = determineAdjacencyArrayIndex(i,SOUTHWEST);
      if(index > ERR_VALUE) addNode(i,index);
      
      index = determineAdjacencyArrayIndex(i,SOUTHEAST);
      if(index > ERR_VALUE) addNode(i,index);         
   }     
}

/**
* Purpose: This gives the index of the vertex adjacent to current vertex.
* Precondition: "currentIndex" refers to the reference vertex.  "direction"
*     refers to W, E, N, S, NW, NE, SW, or SE direction of adjacent vertex
*     with respect to reference vertex.
* Postcondition: The index of the adjacent vertex that lies "direction"
*     of the reference vertex is returned.
*/
int Graph::determineAdjacencyArrayIndex( int currentIndex,  
                                         enum Direction direction) {      
   int index = ERR_VALUE;   
   int diagonalStartIndex = numberOfElements; 
   
   int row, column; // base on width x width array; so can be 0 to width-1
   if(currentIndex < diagonalStartIndex) {
      row = currentIndex / width;
      column = currentIndex % width;
   }
   else {
      row = (currentIndex - diagonalStartIndex) / width;
      column = (currentIndex - diagonalStartIndex) % width;
   }            
  
   int elementDistance = adjacencyList[currentIndex].getDistance();  
   switch(direction) {
      case WEST:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE; //cannot move horizontal/vertical
            }
            else { // for diagonal part
               column = column - elementDistance;               
               if(column < 0)
                  index = ERR_VALUE;
               else
                  index = row * width + column;                  
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               column = column - elementDistance;
               if(column < 0)
                  index = ERR_VALUE;
               else
                  index = row * width + column;                  
            }
            else { // for diagonal part
               index = ERR_VALUE;
            }         
         }
         break;
      case EAST:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE; //cannot move horizontal/vertical
            }
            else { // for diagonal part
               column = column + elementDistance;
               if(column < width) 
                  index = row * width + column;
               else
                  index = ERR_VALUE;             
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               column = column + elementDistance;
               if(column < width)
                  index = row * width + column;
               else
                  index = ERR_VALUE;
            }
            else { // for diagonal part
               index = ERR_VALUE;
            }         
         }
         break;
      case NORTH:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE; //cannot move horizontal/vertical
            }
            else { // for diagonal part
               row = row - elementDistance;
               if(row < 0) 
                  index = ERR_VALUE;
               else
                  index = row * width + column;             
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               row = row - elementDistance;
               if(row < 0)
                  index = ERR_VALUE;
               else
                  index = row * width + column;
            }
            else { // for diagonal part
               index = ERR_VALUE;
            }         
         }
         break;
      case SOUTH:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE; //cannot move horizontal/vertical
            }
            else { // for diagonal part
               row = row + elementDistance;
               if(row < width) 
                  index = row * width + column;
               else
                  index = ERR_VALUE;             
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               row = row + elementDistance;
               if(row < width)
                  index = row * width + column;
               else
                  index = ERR_VALUE;
            }
            else { // for diagonal part
               index = ERR_VALUE;
            }         
         }
         break;
      case NORTHWEST:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               row = row - elementDistance;
               column = column - elementDistance;
               if(row<0 || column<0)
                  index = ERR_VALUE;
               else
                  index = row * width + column + diagonalStartIndex;                  
            }
            else { // for diagonal part
               index = ERR_VALUE;          
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE;
            }
            else { // for diagonal part
               row = row - elementDistance;
               column = column - elementDistance;
               if(row<0 || column<0)
                  index = ERR_VALUE;
               else
                  index = row * width + column + diagonalStartIndex;                  
            }         
         }
         break;
      case NORTHEAST:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               row = row - elementDistance;
               column = column + elementDistance;
               if(row<0 || column>=width)
                  index = ERR_VALUE;
               else
                  index = row * width + column + diagonalStartIndex;                  
            }
            else { // for diagonal part
               index = ERR_VALUE;             
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE;
            }
            else { // for diagonal part
               row = row - elementDistance;
               column = column + elementDistance;
               if(row<0 || column>=width)
                  index = ERR_VALUE;
               else
                  index = row * width + column + diagonalStartIndex;                  
            }         
         }
         break;
      case SOUTHWEST:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               row = row + elementDistance;
               column = column - elementDistance;
               if(row>=width || column<0)
                  index = ERR_VALUE;
               else
                  index = row * width + column + diagonalStartIndex;                  
            }
            else { // for diagonal part
               index = ERR_VALUE;             
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE;
            }
            else { // for diagonal part
               row = row + elementDistance;
               column = column - elementDistance;
               if(row>=width || column<0)
                  index = ERR_VALUE;
               else
                  index = row * width + column + diagonalStartIndex;                  
            }         
         }
         break;
      case SOUTHEAST:
         if(elementDistance < 0) { //negative moves
            elementDistance *= -1; //make positive
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               row = row + elementDistance;
               column = column + elementDistance;
               if(row<width && column<width)
                  index = row * width + column + diagonalStartIndex; 
               else
                  index = ERR_VALUE;                  
            }
            else { // for diagonal part
               index = ERR_VALUE;             
            }
         }
         else { //positive moves
            if(currentIndex < diagonalStartIndex) { // for hor/vert part
               index = ERR_VALUE;
            }
            else { // for diagonal part
               row = row + elementDistance;
               column = column + elementDistance;
               if(row<width && column<width)
                  index = row * width + column + diagonalStartIndex; 
               else
                  index = ERR_VALUE;                  
            }         
         }
         break;
      default:
         std::cerr <<"Unkown direction" <<std::endl;   
   }                                           
   return index; //negative index indicates impossible move                                        
}                                        

/**
* Purpose: This creates a node for a vertex adjacent to reference vertex and
*     adds node to reference vertex's linked list.
* Precondition: "rootIndex" refers to reference vertex.  "targetIndex" refers
*     to a vertex adjacent to the reference vertex.
* Postcondition: An adjacent vertex has been added to reference vertex's
*     linked-list.
*/
void Graph::addNode(int rootIndex, int targetIndex) {
   Node* newNode = new Node;   
   if(!newNode) {
      std::cerr <<"Failed to allocate new node" <<std::endl;
      return;
   }   
   newNode->setId(targetIndex);   
   newNode->next = adjacencyList[rootIndex].next;
   adjacencyList[rootIndex].next = newNode;
}

/**
* Purpose: This deletes the linked list of adjacent vertices associated
*     with each vertex.
* Precondition: Graph object is valid.
* Postcondition: Each vertex in adjacency list has no linked list.
*/
void Graph::removeAdjacencyList() {
   Node* temp = NULL;
   for(size_t i = 0; i < adjacencyList.size(); ++i) {//visit each array element
      while(adjacencyList[i].next) { //remove linked-list in array element
         temp = adjacencyList[i].next;
         adjacencyList[i].next = temp->next;
         delete temp;
      }
   }   
}

/**
* Purpose: This sets up each vertex in the vertexSet.
* Precondition: Graph object is valid.
* Postcondition: Each vertex in vertexSet is properly setup.  Each vertex
*     contains a set of pointers to its adjacent neighbors.  "next" and
*     "parent" pointers are NULL.
*/
void Graph::populateVertexSet() {   
   for(int i = 0; i < adjacencyArraySize; ++i) {
      vertexSet[i].setId(i);
      const Vertex* vertexPtr = operator()(i);
      if(!vertexPtr) { //err: fail to access vertex
         std::cerr <<"Fail to access vertex in adjacencyList" <<std::endl;
         throw MyBad("Fail to populate vertexSet!");
      } 
      while(vertexPtr->next) {
         vertexPtr = vertexPtr->next;
         vertexSet[i].vertexPointers.push_back(&vertexSet[vertexPtr->getId()]);
      }
   }   
}

/**
* Purpose: This sets up each edge in the EdgeSet.
* Precondition: Graph object is valid.
* Postcondition: "edgeSet" holds a set of edges representing each directed
*     arc between two vertices in the graph.
*/
void Graph::populateEdgeSet() {   
   const Vertex* temp = NULL;
   for(int i = 0; i < adjacencyArraySize; ++i) {
      temp = operator()(i);//get vertex from adjacencyList at index i    
      if(!temp) { //err: fail to access vertex
         std::cerr <<"Fail to access vertex in adjacencyList" <<std::endl;
         throw MyBad("Fail to populate edgeSet!");
      } 
      int distance = temp->getDistance();
      if(distance<0) distance *= -1; //make positive
      while(temp->next) {
         temp = temp->next;
         Edge edge(i,temp->getId(),distance);
         if(!findEdge(edge))
            edgeSet.push_back(edge);
      }
   }
}

/**
* Purpose: This finds a matching edge that exists in "edgeSet".
* Precondition: "lookFor" represents an edge that we want to find in edgeSet.
* Postcondition: A pointer to a matching Edge object is returned; otherwise,
*     NULL is returned if match was not found in edgeSet.
*/
const Edge* Graph::findEdge(const Edge& lookFor ) const {
   for(size_t i = 0; i < edgeSet.size(); ++i) {
      if( Edge::compare(edgeSet[i], lookFor) )
         return &edgeSet[i];
   }
   return NULL;
}

/**
* Purpose: This displays set of vertices to console.
* Precondition: Graph object is valid.
* Postcondition: All vertices in vertexSet is displayed.
*/
void Graph::displayVertexSet() const
{
   std::cout <<"\nDisplay \"vertexSet\" content..." <<std::endl;
   const std::vector<Vertex>& vertices = vertexSet;
   int count = 0;
   for(size_t i = 0; i < vertices.size(); ++i) {
      ++count;
      std::cout <<"[i=" <<vertices[i].getId() 
                <<",d=" <<vertices[i].getDistance() 
                <<",p=" ;
      vertices[i].parent?
         (std::cout <<(vertices[i].parent)->getId()<<"]"):
         (std::cout<<"NULL]");
      std::vector<Vertex*>::const_iterator 
         iter = vertices[i].vertexPointers.begin(),
         stop = vertices[i].vertexPointers.end();
      for( ; iter != stop; ++iter) {
         std::cout <<" -> [i=" <<(*iter)->getId()
                   <<",d=" <<(*iter)->getDistance()
                   <<",p=";
         ((*iter)->parent)?
            (std::cout<<(((*iter)->parent)->getId()) <<"]"):
            std::cout <<"NULL]";
      }           
      std::cout <<std::endl;
   }
   std::cout <<"Total number of vertices: " <<count <<std::endl;   
}

/**
* Purpose: This displays set of edges to console.
* Precondition: Graph object is valid.
* Postcondition: All edges in edgeSet is displayed.
*/
void Graph::displayEdgeSet() const {   
   std::cout <<"\nDisplay \"edgeSet\" content..." <<std::endl;
   const std::vector<Edge>& edges = edgeSet;
   std::vector<Edge>::const_iterator 
      iter = edges.begin(),
      stop = edges.end();     
   int count = 0;    
   for(int source = iter->getSource(), temp = 0 ; iter != stop; ++iter) {      
      ++count;
      temp = iter->getSource(iter->getHashCode()); 
      if(source != temp) {
         std::cout <<std::endl; 
         source = temp;        
      }               
      std::cout <<"[src=" <<iter->getSource() 
                <<",dest=" <<iter->getDestination() 
                <<",dist=" <<iter->getDistance() <<"]  ";
   }      
   std::cout <<"\nTotal number of edges: " <<count <<std::endl;   
}

/**
* Purpose: This displays each vertex along with its adjacent vertices.
* Precondition: "vertices" is a collection of pointers to each vertex in graph.
* Postcondition: Each vertex and its adjacent neighbors is displayed.
*/
void Graph::displayVertexSetPointers(const std::vector<Vertex*>& vertices)
   const
{
   std::cout <<"\nDisplay \"vertexSetPointers\" content..." <<std::endl;
   int count = 0;
   for(size_t i = 0; i < vertices.size(); ++i) {
      ++count;
      std::cout <<"[i=" <<vertices[i]->getId() 
                <<",d=" <<vertices[i]->getDistance() 
                <<",p=" ;
      vertices[i]->parent? 
         (std::cout <<(vertices[i]->parent)->getId()<<"]"):
         (std::cout<<"NULL]");
      std::vector<Vertex*>::const_iterator 
         iter = (vertices[i]->vertexPointers).begin(),
         stop = (vertices[i]->vertexPointers).end();
      for( ; iter != stop; ++iter) {
         std::cout <<" -> [i=" <<(*iter)->getId()
                   <<",d=" <<(*iter)->getDistance()
                   <<",p=";
         ((*iter)->parent)?
            (std::cout<<(((*iter)->parent)->getId()) <<"]"):
            std::cout <<"NULL]";
      }           
      std::cout <<std::endl;
   }
   std::cout <<"Total number of vertices: " <<count <<std::endl;   
}

/**
* Purpose: This gives the direction of reference vertex to adjacent vertex.
* Precondition: "startingIndex" refers to reference vertex.  "endingIndex"
*     refers to an adjacent vertex.
* Postcondition: A string of the direction is returned.
*/
std::string Graph::determineDirection(int startingIndex, int endingIndex)
const 
{
   int startingRow = (startingIndex<(width*width))?
      (startingIndex/width):((startingIndex-width*width)/width);
   int endingRow = (endingIndex<(width*width))?
      (endingIndex/width):((endingIndex-width*width)/width);
   int startingColumn = startingIndex % width;
   int endingColumn = endingIndex % width;
      
   std::stringstream ss;   
   if(endingRow > startingRow)
      ss<<"S";
   else if(endingRow < startingRow)
      ss<<"N";
   
   if(endingColumn > startingColumn)
      ss<<"E";
   else if(endingColumn < startingColumn)
      ss<<"W";
                               
   return ss.str();
}

/*======= class Node implementation =======*/ 

/**
* Purpose: This sets the distance value of a vertex.
* Precondition: "distance" refers to distance value.
* Postcondition: Member data "distance" is set.
*/
void Node::setDistance(const int& distance) { this->distance = distance; }   
   
/**
* Purpose: This returns distance value of vertex.
* Precondition: Vertex object is valid.
* Postcondition: The vertex distance value is returned.
*/   
int Node::getDistance() const { return distance; }

/**
* Purpose: This sets the member data "id".
* Precondition: "id" is index corresponding to position in adjacency list.
* Postcondition: Member data "id" is set.
*/
void Node::setId(const int& id) { this->id = id; }

/**
* Purpose: This returns "id" value of vertex.
* Precondition: Vertex object is valid.
* Postcondition: The vertex id value is returned.
*/
int Node::getId() const { return id; }  

/**
* Purpose: This sets the member data "parent".
* Precondition: Vertex object is valid.
* Postcondition: Member data "parent" points to its parent vertex.
*/       
void Node::setParent(Node* parent) { this->parent = parent; }

/**
* Purpose: This returns address of this vertex's parent.
* Precondition: Vertex object is valid.
* Postcondition: The address of this vertex's parent is returned.
*/
const Node* const Node::getParent() const { return parent; }    

/**
* Purpose: This compares two vertices based on distance values.
* Precondition: "n1" and "n2" are pointers to vertices in the graph.
* Postcondition: True is returned if "n1" is larger than or equal to "n2";
*     otherwise, false is returned.
*/      
bool Node::operator()(const Node* n1, const Node* n2) const {
   return !(n1->distance < n2->distance);
}       

/**
* Purpose: This returns set of vertices adjacent to "this" vertex object.
* Precondition: Vertex object is valid.
* Postcondition: A set of pointers to vertices adjacent to "this" vertex
*     object is returned.
*/      
const std::vector<Vertex*>& Node::getSetOfAdjacentVertices() const {
   return vertexPointers; 
}

/*======= class Edge implementation =======*/ 
/**
* Purpose: This creates a hash code for an edge object.
* Precondition: "source" is the index of the source vertex.  "destination"
*     is the index of the destination vertex.
* Postcondition: The hashcode for "this" edge object is returned.
*/
int Edge::hash(int source, int destination) {
   return (source*FACTOR) + (destination); 
}    

/**
* Purpose: This compares two edge objects based on hashCode.
* Precondition: "e1" and "e2" are two edge objects.
* Postcondition: True is returned if both edge objects has the same hashCode;
*     otherwise, false is returned.
*/      
bool Edge::compare(const Edge& e1, const Edge& e2) { 
   return e1._hashCode==e2._hashCode;
}

/**
* Purpose: This returns the index of source vertex of the directed arc.
* Precondition: Edge object is valid.
* Postcondition: The source vertex index of directed arc is returned.
*/      
int Edge::getSource() const { return _source; }

/**
* Purpose: This returns the index of source vertex of the directed arc.
* Precondition: "hashCode" is hash code of "this" edge object.
* Postcondition: The source vertex index of directed arc is returned.
*/   
int Edge::getSource(const int& hashCode) const { return hashCode/FACTOR; }

/**
* Purpose: This returns the index of destination vertex of directed arc.
* Precondition: Edge object is valid.
* Postcondition: The destination vertex index of directed arc is returned.
*/
int Edge::getDestination() const { return _destination; }

/**
* Purpose: This returns the distance of the edge object.
* Precondition: Edge object is valid.
* Postcondition: The distance of edge object is returned.
*/
int Edge::getDistance() const { return _distance; }

/**
* Purpose: This returns hash code of the edge object.
* Precondition: Edge object is valid.
* Postcondition: The hash code of edge object is returned.
*/
int Edge::getHashCode() const { return _hashCode; }    

/**
* Purpose: This compares two edge objects based on hashcode.
* Precondition: "e1" and "e2" are two edge objects.
* Postcondition: True is returned if "e1" is larger than or equal to "e2";
*     otherwise, false is returned.
*/      
bool Edge::operator()(const Edge& e1, const Edge& e2) const {
   return !(e1._hashCode<e2._hashCode);
}  

/*======= class MyBad implementation =======*/ 

/**
* Purpose: This returns the error message.
* Precondition: MyBad object is valid.
* Postcondition: The error message is returned.
*/
const char* MyBad::what() const throw() { return msg.c_str(); }


