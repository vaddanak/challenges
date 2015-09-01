/******************************************************************************
*  File: main.cpp
*  Author:  Vaddanak Seng
*  Purpose: We will test Dijkstra's algorithm on each instance of graphs
*     in class BunchOfGraphs.
******************************************************************************/

#include "bunchofgraphs.h"

#include <iostream>

/**
* Purpose: This tests class BunchOfGraphs implementation.
* Precondition: Class BunchOfGraphs and associated members were defined
*     and implemented.
* Postcondition: Operations on creating instances of graphs and running
*     Dijkstra's algorithm were performed.  Results of finding path through
*     each graph instance can be found in file "seng.txt"
*   
*     NOTE:  The "input.txt" contains data for all instances of graph.
*            The format of this file must be strictly adhered according to
*            project description.  This program is designed to retrieve all
*            the data from the "input.txt" file and create all instances of
*            Graph based on the data.
*/
int main(int argc, char ** args) {
   
   BunchOfGraphs g("input.txt");    
       
   return 0;
}
