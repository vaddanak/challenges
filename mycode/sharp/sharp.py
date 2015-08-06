#!/usr/bin/python
# -*- coding: utf8 -*-


'''
Author: Vaddanak Seng
File: sharp.py
Purpose: Implement a math operation that performs incremental exponentiation
	on a previous result.
Date: 2015/08/05

Runs on both python2 and python3? YES

The first or second line must match the regular expression
"coding[:=]\s*([-\w.]+)" to specify source code encoding different from
default ascii. (for Python2)
'''

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;


def sharp(x):
	"""
	x# = ((((((2 ^ 3) ^ 4) ^ 5)  …)  …)     x-1) ^  x)
	
	For example ->
	2# = 2
	3# = (2 ^ 3) = 8
	4# = ((2 ^ 3) ^ 4) = (8 ^ 4) = 4096
	"""
	
	if x > 2:
		return sharp(x-1) ** x;
	elif x==2:
		return 2;
	else:
		return None;

def num_digits(x):
	'''
	Return number of digits in number x.
	'''		
	_type = type(x);
	if _type == type(1) or type(1.0):
		count = 0;
		for x in str(x):
			count += 1;
		if _type == type(1.0):
			count -= 1;
	return count;
	
	
result = num_digits(sharp(7)) + 2 * num_digits(sharp(6)) + num_digits(5) \
	+ num_digits(4); # 979
	
print(result);		












