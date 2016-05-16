/******************************************************************************
*  File: bunchofgraphs.cpp
*  Author:  Vaddanak Seng
*  Purpose: This is the implementation of class BunchOfGraphs.  It holds
*     a collection of graph instances and provides Dijkstra algorithm to 
*     find a path through a graph.      
******************************************************************************/

#include "bunchofgraphs.h"

#include <fstream> //ifstream, ofstream
#include <iostream>
#include <exception>
#include <sstream>
#include <algorithm>

//file-scope global variables
static bool debug = false;
 
/**
* Purpose: This constructs a BunchOfGraph object.
* Precondition: "filename" is name of input file that has graph data.
*     It is default to "input.txt"
* Postcondition: Object of type BunchOfGraphs has been constructed.
*/
BunchOfGraphs::BunchOfGraphs(const std::string& filename) : 
   filename(filename)
{
   const int START_INDEX = 0; //path starts at this vertex index
   //retrieveData(filename.c_str());
   retrieveData2(filename.c_str());
      
   std::stringstream ss;
   size_t numberOfGraphs = graphContainer.size();
   for(size_t i = 0; i < numberOfGraphs; ++i) {
      ss <<dijkstra(graphContainer[i],START_INDEX);
      if(ss.str().size() && ((i+STEP) < numberOfGraphs))
         ss <<std::endl <<std::endl;      
   }   
   output(ss.str());   
}

/**
* Purpose: This output data to file.
* Precondition: "data" is data to output.  "filename" is name of output file,
*     which is default to "seng.txt"
* Postcondition: "data" has been written to file.
*/
void BunchOfGraphs::output(const std::string& data, 
                           const std::string& filename) const 
{
   std::ofstream output(filename.c_str());
   if(output && data.size()) {
      output <<data;
      output.close();  
   }      
}
     
/**
* Purpose: This retrieves graph data from file and create instances of Graph.
* Precondition: "filename" is the name of the file that contains graph data.
* Postcondition: True is returned if instances of Graph has been created
*     successfully; otherwise, false is returned.
*/
bool BunchOfGraphs::retrieveData(const char* filename) {   
   debug = false;
   
   std::ifstream input(filename);
   if(!input) {
      std::cerr <<"Fail to open file: " <<filename <<std::endl;
      return false;         
   }   
   
   int numberOfGraphs = 0;       
   if(!(input >>numberOfGraphs)) {
      std::cerr <<"Fail to read numberOfGraphs" <<std::endl;
      return false;         
   }    
         
   //retrieve all graph instances from file and add to vector container
   for(int j = 0, widthOfGraph = 0; j < numberOfGraphs; ++j) {      
      if(!(input >>widthOfGraph)) { //retrieve a graph width
         std::cerr <<"Fail to read widthOfGraph" <<std::endl;
         return false;         
      }              
      Graph graph(widthOfGraph); //create Graph object
      int numberOfElements = widthOfGraph * widthOfGraph;
      try { //populate Graph object with data
         for(int i = 0; i < numberOfElements; ++i) 
            input >>graph[i];            
      }      
      catch(MyBad err) {
         std::cerr <<"Fail to populate graph data.\n" <<err.what() <<std::endl;
         return false;
      }
      graphContainer.push_back(graph); //add Graph object to container  
      //graph.showDataStore();       
   }   
   input.close(); //close file    
   
   if(debug) {
      std::cout <<numberOfGraphs <<std::endl;      
      for( std::vector<Graph>::iterator iter = graphContainer.begin(); 
           iter != graphContainer.end(); ++iter)
         //(*iter).showDataStore();  
         iter->showAdjacencyList();                         
   }                
   return true;
}

bool BunchOfGraphs::retrieveData2(const char* filename, 
	enum Input_Format inputType) {
	
	debug = false;
   
   	std::ifstream input(filename);
   	if(!input) {
      	std::cerr <<"Fail to open file: " <<filename <<std::endl;
      	return false;         
  	}   
   
   	int numberOfGraphs = 0;
   
   	if(inputType == MULTIPLE_GRAPHS_WITH_COLUMN_WIDTH_ONLY) {     
	   	if(!(input >>numberOfGraphs)) {
		  	std::cerr <<"Fail to read numberOfGraphs" <<std::endl;
		  	return false;         
	   	}    
		     
	   	//retrieve all graph instances from file and add to vector container
	   	for(int j = 0, widthOfGraph = 0; j < numberOfGraphs; ++j) {      
		  	if(!(input >>widthOfGraph)) { //retrieve a graph width
		     	std::cerr <<"Fail to read widthOfGraph" <<std::endl;
		     	return false;         
		  	}              
		  	Graph graph(widthOfGraph); //create Graph object
		  	int numberOfElements = widthOfGraph * widthOfGraph;
		  	try { //populate Graph object with data
		     	for(int i = 0; i < numberOfElements; ++i) 
		        	input >>graph[i];            
		  	}      
		  	catch(MyBad err) {
		     	std::cerr <<"Fail to populate graph data.\n" <<err.what() <<std::endl;
		     	return false;
		  	}
		  	graphContainer.push_back(graph); //add Graph object to container  
		  	//graph.showDataStore();       
	   	}   
   
   }
   else if(inputType == SINGLE_GRAPH_WITH_ROW_COLUMN) {
   		
   		int row, column;   			
		numberOfGraphs = 1;
		     
	   	//retrieve all graph instances from file and add to vector container
	   
	  	if(!(input >>row >>column)) { //retrieve a graph row and column
	     	std::cerr <<"Fail to read row and column values" <<std::endl;
	     	return false;         
	  	}              
	  	Graph graph(row,column); //create Graph object
	  	int numberOfElements = row * column;
	  	try { //populate Graph object with data
	     	for(int i = 0; i < numberOfElements; ++i) 
	        	input >>graph[i]; //store distance values in array           
	  	}      
	  	catch(MyBad err) {
	     	std::cerr <<"Fail to populate graph data.\n" <<err.what() <<std::endl;
	     	return false;
	  	}
	  	graphContainer.push_back(graph); //add Graph object to container  
	  	//graph.showDataStore();       
	   
   	}
   
   	input.close(); //close file    
   
   	if(debug) {
      	std::cout <<numberOfGraphs <<std::endl;      
      	for( std::vector<Graph>::iterator iter = graphContainer.begin(); 
           	iter != graphContainer.end(); ++iter)
         	//(*iter).showDataStore();  
         	iter->showAdjacencyList();                         
   	}                
   	return true;	
}

/**
* Purpose: Algorithm finds a path from startIndex to goal.
* Precondition: "graph" is an instance of Graph.  "startIndex" is the index
*     of the starting vertex.
* Postcondition: A string containing direction to goal vertex is returned.
*/
std::string BunchOfGraphs::dijkstra(Graph& graph, int startIndex) const {
   debug = true;    
   
   std::vector<Vertex>& vertices = graph.getVertexSet();     
   
   //setup collection of vertices ordered based on distance
   std::vector<Vertex*> onlyVertexPointers(vertices.size(),NULL);
   for(size_t i = 0; i < vertices.size(); ++i)
      onlyVertexPointers[i] = &vertices[i];
      
   //setup starting vertex        
   if(onlyVertexPointers.size())
      onlyVertexPointers[startIndex]->setDistance(0);      
         
   //setup empty queue to hold path vertices
   std::queue<Vertex*> verticesQueue;
         
   //sort collection of vertices based on distance         
   std::make_heap<std::vector<Vertex*>::iterator,Vertex> 
      (onlyVertexPointers.begin(), onlyVertexPointers.end(), Vertex());
   std::sort_heap<std::vector<Vertex*>::iterator,Vertex>
      (onlyVertexPointers.begin(), onlyVertexPointers.end(), Vertex());
   //process each vertex 
   while(onlyVertexPointers.size()) {      
      std::make_heap<std::vector<Vertex*>::iterator,Vertex> 
         (onlyVertexPointers.begin(), onlyVertexPointers.end(), Vertex());
      std::pop_heap<std::vector<Vertex*>::iterator,Vertex>
         (onlyVertexPointers.begin(),onlyVertexPointers.end(),Vertex()); 
      Vertex* vptr = onlyVertexPointers.back();//get minimum
      onlyVertexPointers.pop_back();//remove min from collection of vertices
      
      verticesQueue.push(vptr);//add to queue
      //visit its adjacent neighbors          
      Vertex* temp = NULL;       
      const std::vector<Vertex*>& setOfAdjacentVertices = 
         vptr->getSetOfAdjacentVertices();
      for(size_t i = 0; i < setOfAdjacentVertices.size(); ++i) {
         temp = setOfAdjacentVertices[i];
         Edge edge(vptr->getId(),temp->getId());
         const Edge* edgePtr = graph.findEdge(edge);         
         
         int edgeDistance = edgePtr?edgePtr->getDistance():0;
         int tempDistance = temp->getDistance();
         if(tempDistance<0) tempDistance *= -1; //make positive
         int parentDistance = vptr->getDistance();
         if(parentDistance<0) parentDistance *= -1; //make positive
                 
         if(edgePtr && (tempDistance > parentDistance + edgeDistance) ) {
            temp->setDistance(parentDistance + edgeDistance);
            temp->setParent(vptr);            
         }         
      }      
      std::make_heap<std::vector<Vertex*>::iterator,Vertex> 
         (onlyVertexPointers.begin(), onlyVertexPointers.end(), Vertex());
      std::sort_heap<std::vector<Vertex*>::iterator,Vertex>
         (onlyVertexPointers.begin(), onlyVertexPointers.end(), Vertex());
   }   
   //graph.displayVertexSetPointers(onlyVertexPointers);
   //graph.displayVertexSet();
   //graph.displayEdgeSet();   
   
   /*
   std::queue<Vertex*> testpath(verticesQueue);
   while(!testpath.empty()) {
		std::cout <<((testpath.front())->getId()) <<" ";
		testpath.pop();
	}	
   std::cout <<std::endl;   		
   */    
   
   //retrieves the successful path
   std::vector<int> successPath;
   int find = graph.getRow() * graph.getColumn() - 1; //goalIndex   
   successPath.push_back(find);   
   const Vertex* vptr = NULL;
   while(find != startIndex) {
      vptr = vertices[find].getParent();
      if(!vptr) {
         std::cerr <<"ERROR?  Parent is NULL!" <<std::endl;
         break;
      }
      find = vptr->getId();  
      successPath.push_back(find);                  
   }   
   
   //display path using vertex index
   if(debug) {
      std::cout <<"STARTING VERTEX: " <<startIndex <<std::endl;
      std::cout <<"Path by vertex index: ";
      std::vector<int>::reverse_iterator 
         riter = successPath.rbegin(),
         rstop = successPath.rend();
      for( ; riter != rstop; ++riter)      
         std::cout <<(*riter % (graph.getWidth()*graph.getWidth()))<<" ";
      std::cout <<std::endl;         
   }        
      
   //display path using symbols: W E N S NW NE SW SE   
   std::stringstream ss;
   for(std::vector<int>::reverse_iterator riter = successPath.rbegin(); 
      riter != successPath.rend(); ++riter) 
   {             
      if( (riter + 1) != successPath.rend() ) {
         ss <<graph.determineDirection(*riter,*(riter+1));
         if( (riter + 2) != successPath.rend() )
            ss <<" "; 
      }            
      else             
         break;   
   }    
     
   if(debug) 
      std::cout <<"Path by direction: " <<ss.str() <<std::endl <<std::endl;  
      
   return ss.str();
}

