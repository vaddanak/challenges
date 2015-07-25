#!/usr/bin/env python

'''
Author: Vaddanak Seng
File: fibonacci.py
Purpose: Print out the first N numbers in the Fibonacci sequence.
Date: 2015/07/25
'''

from __future__ import print_function;

import sys;
import re;

sequence = [0,1];

'''
Calculate and collect first N numbers in Fibonacci number sequence.
Store result in global variable "sequence".
'''
def fibonacci(N):
	global sequence;
	if N>2:
		sequence.append(sequence[len(sequence)-1] + sequence[len(sequence)-2]);
		fibonacci(N-1);
		
		
N = int(raw_input());
fibonacci(N);

listStr = [str(sequence[x]) for x in range(N)];

#for x in listStr:
#	print(x, end='');	#0112358132134 when N = 10; WRONG !!! WHY???
	# still won't space correctly eventhough sequence element is str type ???	

#for x in range(N):
	# won't space correctly when sequence element is int type ??? WHY???
	#print('%d' % sequence[x], end=''); #0112358132134	when N = 10; WRONG !!!
	
	
	

###option 1 -- using string join() function
mstr = ' '.join(listStr);
#print(mstr, end=''); #0 1 1 2 3 5 8 13 21 34 when N = 10; CORRECT spacing !!!




###option 2 -- using sys.stdout.write
#for x in range(N):	
#	sys.stdout.write('%d' % sequence[x]); 
#	if x < N-1: # alternative to force correct spacing
#		sys.stdout.write(' '); #0 1 1 2 3 5 8 13 21 34 when N = 10; CORRECT !!!
		
	

	
###option 3 -- using regular expression
sequence = [sequence[x] for x in range(N)]; #ensures number of elements == N
mstr2 = str(sequence);	
#print(mstr2); # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

#target string:  [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
reObject = re.compile(r'^(\[\s*){1}(\d+[, ]+)*\d+(\])$');#match whole string
reo1 = re.compile(r'^(\[ *){1}');#match left most [
reo2 = re.compile(r', +');#match each sequence of comma-followed-by-space
reo3 = re.compile(r'\]$');#match right most ]

matchObject = reObject.match(mstr2);
#if matchObject:
#	print(matchObject.group(0));# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34] when N=10

modifiedString = mstr2;
#print(modifiedString);# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34] when N=10; original	

modifiedString = reo1.sub('',modifiedString);
#print(modifiedString);# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

modifiedString = reo3.sub('',modifiedString);
#print(modifiedString);# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

modifiedString = reo2.sub(' ',modifiedString);
print(modifiedString, end='');# 0 1 1 2 3 5 8 13 21 34  ; CORRECT !!!


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

