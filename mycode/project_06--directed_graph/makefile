CXX = g++
CXXFLAGS = -g -Wall
INC_DIR =
LIB_DIR =
LIBS =

TARGET = a.out
DEPENDENCIES = main.o bunchofgraphs.o graph.o
#DEPENDENCIES = *.o

$(TARGET): $(DEPENDENCIES)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(INC_DIR) $(LIB_DIR) $(LIBS)

clean:
	rm *.o a.out;

.phony: clean

######################################


run:
	./a.out	
