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

   enum Input_Format {	SINGLE_GRAPH_WITH_ROW_COLUMN, 
   						MULTIPLE_GRAPHS_WITH_COLUMN_WIDTH_ONLY};

   public:      
      BunchOfGraphs(const std::string& filename);      
      std::string dijkstra(Graph& graph, int startIndex) const;

   private:
      std::vector<Graph> graphContainer;
      std::string filename;

      bool retrieveData(const char* filename);
      bool retrieveData2(const char* filename, 
      	enum Input_Format inputType = SINGLE_GRAPH_WITH_ROW_COLUMN);
      void output(const std::string& data, 
         const std::string& filename = "output.txt") const;
};

#endif // BUNCHOFGRAPHS_H_
