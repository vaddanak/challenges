#!/usr/bin/env python3

'''
Author: Vaddanak Seng
File: right_triangle.py
Purpose: Given any two edge lengths of a right triangle, find the missing third.
'''

from __future__ import print_function;

#get user input
#def formula given side or hypotenuse
#use builtin function "round"

def length(side1, side2, hypotenuse):
	if side1=="_":
		return (float(hypotenus)**2 - float(side2)**2)**0.5;
	
	elif side2=="_":
		return (float(hypotenuse)**2 - float(side1)**2)**0.5;		
	
	elif hypotenuse=="_":
		return (float(side1)**2 + float(side2)**2)**0.5;
		
	else:	
		return 0.0;


#userInput = input(); #python3
userInput = raw_input(); #python2

mlist = userInput.split();


if len(mlist)==3:
	result = length(mlist[0], mlist[1], mlist[2]);	
	result = round(result, 3);
	print(format(result,'.3f'), end="");
