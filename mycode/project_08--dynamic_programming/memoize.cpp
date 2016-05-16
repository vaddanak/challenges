/*
FILE:  memoize.cpp
TEAM:  	Micah Parcher, Darshankumar Patel, Vaddanak Seng
PURPOSE:  Project 2 uses dynamic programming to determine number of ways to
		arrange balls in some number of baskets.
*/

#include <cstdlib> //calloc, free
#include <iostream> //cout, cerr
#include <fstream> //ifstream, ofstream


void free(void *ptr);
void *calloc(size_t nmemb, size_t size);

int memoize(int b_balls, int n_baskets, int k_capacity, int** arr_storage);
int iterative(int B, int N, int K, int **arr);
int** makeStorage(int nRows, int nColumns);
void freeStorage(int** arr);
void printStorage(int** arr, int nColumns);


int main(int argc, char ** args) {

	int b; //number of balls
	int n; //number of baskets
	int k; //basket capacity
	int numInstances; //number of test instances
	int numWays; //number of ways to arrange the balls
	//int numWaysIter; //for testing iterative algorithm
	
	int** arr = 0;
	//int** arr_iter = 0; //for testing iterative algorithm
	
	std::ifstream in("input.txt");
	std::ofstream out("output.txt");
		
	if(!in.good() || !out.good()) { //validate files are opened successfully
		std::cerr <<"Failed to open file." <<std::endl;
		return -1;
	}
	
	in >>numInstances; //retrieve number of test cases
	
	for(int i = 0; i < numInstances; ++i) {
		in >>b >>n >>k; //retrieve a row of data from input file
		
		//testing memoized algorithm
		arr = makeStorage(b+1, n+1); //create data structure for memoization
		numWays = memoize(b,n,k,arr); //determines number of ways		
		//std::cout<<"memoize(b="<<b<<",n="<<n<<",k="<<k<<",arr): "<<numWays<<std::endl;
		out <<numWays <<std::endl; //write result to output file on its own line		
		//printStorage(arr, n+1);
		freeStorage(arr); //free memory allocated to arr
		
		/*
		//testing iterative algorithm
		arr_iter = makeStorage(b+1, n+1); //create data structure for iterative
		numWaysIter = iterative(b,n,k,arr_iter); //determines number of ways		
		std::cout<<"iterative(B="<<b<<",N="<<n<<",K="<<k<<",arr): "
			<<numWaysIter<<std::endl;		
		printStorage(arr_iter, n+1);
		freeStorage(arr_iter); //free memory allocated to arr		
		*/
	}

	in.close();
	out.close();	
	
	return 0;
}

/*
PURPOSE:  Determines the number of ways to arrange a number of balls in a given
		number of baskets and each basket has a fixed maximum capacity.
PRECON:	b is the number of balls.  n is the number of baskets.  k is the 
		maximum capacity for each basket.  arr is two-dimensional array where
		last row is NULL and used as sentinel to stop.
POSTCON:  Returns the number of ways that b balls can be arranged in n baskets.
*/
int memoize(int b, int n, int k, int** arr) {
	if(arr[b][n] > 0)
		return arr[b][n];
	//if(b==1 && n==1)
	//	return 1;
	if(b==0 && n==0)
		return 1;
	for(int i = 0; i <= k; ++i)
		if(b-i >= 0 && n-1 >= 0)
			arr[b][n] += memoize(b-i, n-1, k, arr);

	return arr[b][n];
}

/*
PURPOSE:  Determines the number of ways to arrange a number of balls in a given
		number of baskets and each basket has a fixed maximum capacity.
PRECON:	B is the number of balls.  N is the number of baskets.  K is the 
		maximum capacity for each basket.  arr is two-dimensional array where
		last row is NULL and used as sentinel to stop.
POSTCON:  Returns the number of ways that B balls can be arranged in n baskets.
*/
int iterative(int B, int N, int K, int **arr) {	
		
	arr[0][0] = 1;
		
	int n = 1;
	int b;	
	
	for(; n <= N; ++n) {
		for(b = 0; b <= B; ++b) {
			for(int i = 0; i <= K; ++i) {
				if( (b-i >= 0) && (n-1 >= 0) ) {
					if(arr[b-i][n-1] > 0) {
						arr[b][n] += arr[b-i][n-1];
					}	
				}			
			}		
		}	
	}	
	
	return arr[b-1][n-1];
}

/*
PURPOSE:  Allocate memory for two-dimensional array.
PRECON:	nRows is number of rows in array.  nColumns is number of columns in
		each row. IE array[nRows][nColumns]
POSTCON:  Return address to allocated and initialized with nRows rows and
		nColumns columns.
*/
int** makeStorage(int nRows, int nColumns) {
	//last row is NULL to indicate stop; a sentinel marker
	int **arr = (int**)calloc(nRows+1, sizeof(int*));
	for(int i = 0; i < nRows; ++i)
		*(arr+i) = (int*)calloc(nColumns, sizeof(int));
	return arr;	
}

/*
PURPOSE:  Free storage used by array.
PRECON:	arr is two-dimensional array where last row is NULL and used as 
		sentinel to stop.
POSTCON:  Allocated storage has been released back to system resource heap.
*/
void freeStorage(int** arr) {
	if(arr) {
		int **temp = arr;
		for(; *arr; ++arr) {
			free(*arr);
		}	
		free(temp);	
	}
}

/*
PURPOSE: Print content of array to screen.
PRECON:	arr is two-dimensional array where last row is NULL and used as 
		sentinel to stop.  nColumns is number of elements in each row.
POSTCON:  n/a
*/
void printStorage(int** arr, int nColumns) {
	if(arr) {
		for(; *arr; ++arr) {
			for(int j = 0; j < nColumns; ++j)
				std::cout <<*(*arr+j) <<" ";
			std::cout <<std::endl;				
		}	
	}
}





















