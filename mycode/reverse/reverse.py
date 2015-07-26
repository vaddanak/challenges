'''
Author: Vaddanak Seng
File: reverse.py
Purpose: Given two positive integers, reverse them (58 = 85), add them together,
	then reverse the final answer.
Date: 2015/07/25
'''

from __future__ import print_function;

import sys;
import re;

numbers = sys.stdin.readline();

patternObject = re.compile(r'^\s*(?P<first>\d+)\s*(?P<second>\d+)\s*$');
matchObject = patternObject.search(numbers);

first = ''
second = ''
if matchObject:
	first = matchObject.group('first');
	first = ''.join(reversed(first))	
	second = matchObject.group('second');
	second = ''.join(reversed(second))
	
_sum = int(first) + int(second);
	

#print(first, second);
print( ''.join(reversed(str(_sum))), end='' )
