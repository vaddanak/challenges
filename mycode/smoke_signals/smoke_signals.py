#!/usr/bin/env python
'''
Author: Vaddanak Seng
File: smoke_signals.py
Purpose: Complete a program which converts a binary sequence to ASCII.
Date: 2015/07/27

Runs on python2 and python3!
'''

from __future__ import print_function;

import sys;
import re;

'''
PURPOSE: Convert binary sequence to list of character.
PRECOND: binary_sequence is sequence of binary digits.
POSTCOND: Returns list of character.
'''
def convert(binary_sequence):
	_list = [];
	binary_sequence = list(reversed(binary_sequence));
	_sum = 0;
	for x in range(len(binary_sequence)):
		_sum += int(binary_sequence[x]) * (2**(x%7));
		if x%7==6:
			_list.append(chr(_sum));
			_sum = 0;
	return list(reversed(_list));


# first approach
#print(''.join(convert(raw_input())), end='');

# alternative approach
po = re.compile(r'\d+');
mo = po.search(sys.stdin.readline());

print(''.join(convert(mo.group(0))), end='');
