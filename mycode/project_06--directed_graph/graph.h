/******************************************************************************
*  File: graph.h
*  Author:  Vaddanak Seng
*  Purpose: Header file contains definition of Graph, Node, Edge, and
*     MyBad classes.
******************************************************************************/

#ifndef GRAPH_H_
#  define GRAPH_H_

#include <string>
#include <exception>
#include <vector>
//#include <climits> //INT_MAX

//forward declaration
class Node;
class MyBad;
class Graph;
class Edge;

typedef class Node Vertex;

//global variables
static const int DISTMAX = 88888;
static const int FACTOR = 1000;
static const int ERR_VALUE = -1;
static const int NULL_ZERO = 0;
static const int TWO = 2;
static const int STEP = 1;

enum Direction { WEST, EAST, NORTH, SOUTH, NORTHWEST, NORTHEAST, 
                 SOUTHWEST, SOUTHEAST};

/**
* Purpose:  Class Graph represents a graph using an adjacency list.  It is also
*     represented by a set of vertices and set of edges.
* How-to-use:
*     1)  Default constructor is used to initialize collection of graphs.
*     2)  Graph(int) constructs a graph with a specified side length.
*     3)  The operator[](int) allows access to graph data at specified index.
*     4)  The operator()(int) allows access to graph vertex at specified index.
*     5)  You can retrieve set of graph vertices using function getVertexSet().
*     6)  You can retrieve set of graph edges using function getEdgeSet().
*     7)  Function findEdge(const Edge&) returns a pointer to a unique Edge
*         object in the edgeSet if it exists.
*     8)  Functions show... and display... output content to console for
*         debugging usages.
*     9)  Function getWidth() returns side lenght of graph and
*         getAdjacencySize() returns number of elements in adjacencyList.
*    10)  Function determineDirection(int,int) gives W, E, N, S, NW, NE, SW,
*         or SE direction when moving from startingIndex to endingIndex.
*/
class Graph {
   public:
      Graph();
      Graph(const int& width);
      Graph(const Graph& rhs);
      ~Graph();
      Graph& operator=(const Graph& rhs);
      //access element at "index" in "dataStore" array
      int& operator[](const int& index);      
      //access linked list at "index" in "adjacencyList" array 
      const Node* operator()(int index) const; 
      
      std::vector<Vertex>& getVertexSet();
      const std::vector<Edge>& getEdgeSet() const;
      const Edge* findEdge(const Edge& lookFor) const; 
      std::string determineDirection(int start, int end) const;
      
      void showDataStore() const;
      void showAdjacencyList() const;      
      void displayVertexSet() const;
      void displayEdgeSet() const;
      void displayVertexSetPointers(const std::vector<Vertex*>&) const;
      
      int getWidth() const;
      int getAdjacencySize() const;     
   
   private:
      int width; // n
      int numberOfElements; // n * n
      int * dataStore; // n * n memory allocation; holds input table values      
      int adjacencyArraySize; // 2 * n * n
      //each element in vector container is a linked list to adjacent vertices;
      //"next" pointer links the vertices in the linked list; "parent" pointer
      //is not used here
      std::vector<Node> adjacencyList;          
      //collection of vertices; "next" pointer is always NULL here; "parent"
      //pointer points to another element in the vector
      std::vector<Vertex> vertexSet; 
      std::vector<Edge> edgeSet; //collection of edges; distances are positive

      //helper functions            
      void initializeDataStore();
      void removeDataStore();
      int* createDataStore();
      void copyDataStore(const int* sourceData);
      void removeAdjacencyList();
      void removeAdjacencyList2();
      void createAdjacencyList();
      void addNode(int rootIndex, int targetIndex);
      int determineAdjacencyArrayIndex( int currentIndex, 
                                        enum Direction direction);
      void populateVertexSet();
      void populateEdgeSet();                                             
};

/**
* Purpose:  Class Node represents the vertex in a graph.
* How-to-use:
*     1)  Default constructor initializes all data members.
*     2)  Once default Node object is created, you can set the distance, id,
*         and parent data members using the corresponding set... functions.
*     3)  The get... functions will return the corresponding distance, id,
*         and parent data members.
*     4)  Calling getSetOfAdjacentVertices() returns a vector container that
*         holds pointers to vertices adjacent to this vertex.
*     5)  operator()(const Node*, const Node*) allows two Node objects to be
*         compared based on distance values.
*/
class Node {  
   public:
      Node() : distance(DISTMAX), id(ERR_VALUE), next(NULL), 
               parent(NULL), vertexPointers(NULL_ZERO,NULL) 
      {}     
      
      void setDistance(const int& distance);
      void setId(const int& id);
      void setParent(Node* parent);
      
      int getDistance() const;      
      int getId() const;      
      const Node* const getParent() const;
      const std::vector<Vertex*>& getSetOfAdjacentVertices() const;
      
      bool operator()(const Node* n1, const Node* n2) const;      
      
   private:
      int distance;
      int id; // location index between 0 to (n x n - 1)
      Node* next; //root is element of adjacency list array     
      Node* parent;
      std::vector<Vertex*> vertexPointers;//holds pointers to adjacent vertices
      friend class Graph;
};

/**
* Purpose:  Class Edge represents the edge between two vertices in a graph.
* How-to-use:
*     1)  Default constructor initializes all data members, which is mainly
*         useful for a container class.
*     2)  You should use Edge(int,int,int) to construct Edge object with
*         source, destination, and distance arguments.
*     3)  Function hash(int,int) creates a hashcode unique for each different
*         pair of vertices.
*     4)  Function compare(const Edge&,const Edge&) provides equality
*         comparison based on hashCode.
*     5)  Function operator()(const Edge&,const Edge&) provides less-than
*         comparison based on hashCode.
*     6)  The get... functions will return corresponding source index,
*         destination index, distance, and hashCode.
*/
class Edge {
   public:
      Edge() : _source(NULL_ZERO), _destination(NULL_ZERO), _distance(DISTMAX)
      {
         _hashCode = hash(_source, _destination);
      }
   
      Edge(int source, int destination, int distance=DISTMAX) :
         _source(source), _destination(destination), _distance(distance)
      {
         _hashCode = hash(_source, _destination);
      }     
      
      static int hash(int source, int destination);      
      static bool compare(const Edge& e1, const Edge& e2);
      bool operator()(const Edge& e1, const Edge& e2) const;
      
      int getSource() const;
      int getSource(const int& hashCode) const;
      int getDestination() const;
      int getDistance() const;
      int getHashCode() const;     
   
   private:
      int _source;
      int _destination;
      int _distance;
      int _hashCode;      
};

/**
* Purpose:  Class MyBad is a custom exception type, which is used for various
*     possible erroneous occurrences.
* How-to-use:
*     1)  You should use constructor MyBad(const string&) with custom message.
*     2)  If this type was thrown and caught, you should call what() to get
*         hint on cause of error.
*/
class MyBad : public std::exception {
   public:
      MyBad(const std::string& msg) : msg(msg) {}
      const char* what() const throw();
      ~MyBad() throw() {}
   private:
      std::string msg;
};

#endif // GRAPH_H_
