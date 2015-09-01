/******************************************************************************
*  File: bunchofgraphs.h
*  Author:  Vaddanak Seng
*  Purpose: Header file contains class BunchOfGraphs definition.  It holds
*     a collection of graph instances and provides Dijkstra algorithm to 
*     find a path through a graph.      
******************************************************************************/

#ifndef BUNCHOFGRAPHS_H_
#  define BUNCHOFGRAPHS_H_

#include "graph.h"

#include <string>
#include <vector>
#include <queue>

/**
* Purpose:  It holds a collection of graph instances and provides Dijkstra
*     algorithm to find a path through a graph.      
* How-to-use:
*     1)  BunchOfGraphs(const std::string&) creates instance using graph data
*         in "filename" to create instances of Graph.
*     2)  Function dijkstra(Graph&,int) finds a path through "graph" starting
*         at vertex "startingIndex".
*/
class BunchOfGraphs {

   public:      
      BunchOfGraphs(const std::string& filename = "input.txt");      
      std::string dijkstra(Graph& graph, int startIndex) const;

   private:
      std::vector<Graph> graphContainer;
      std::string filename;

      bool retrieveData(const char* filename);
      void output(const std::string& data, 
         const std::string& filename = "seng.txt") const;
};

#endif // BUNCHOFGRAPHS_H_
