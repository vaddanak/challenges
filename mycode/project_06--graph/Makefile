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
	rm *.o a.out *~ || true

.phony: clean

######################################


run:
	./a.out	
	
val:
	valgrind --leak-check=full ./a.out	
	

vad:
	gedit --new-window \
		Makefile \
		bunchofgraphs.cpp \
		bunchofgraphs.h \
		graph.cpp \
		graph.h \
		main.cpp \
		input.txt \
		readme.txt \
		\
		jim*.txt \
		small*.txt \
		output.txt \
		\
		&	
