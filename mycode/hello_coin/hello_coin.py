'''
Author: Vaddanak Seng
File: hello_coin.py
Purpose: Calculate the probability of getting at most H heads.
Date: 2015/07/27

Runs on both python2 and python3? YES
'''


from __future__ import print_function;

import sys;
import re;
import math; #factorial(+int)

p = 0.5; # probability of head
q = 0.5; # probability of not a head
_sum = 0.0; #total probability for each test case

'''
PURPOSE: Fn calculates the probability of observing r occurrences of HEAD when
	it gets flipped n times.
PRECON: args are keyword arguments internally stored as dict.  It contains key
	string "trials" which is mapped to an integral value.  It also contains key
	string "heads" which is mapped to an integral value.  nCr means n choose r.
	n is same as "trials" and r is same as "heads".
	Formula is [ "n choose r" * p**r * q**(n-r) ]
POSTCOND: Fn returns probability as float value.
'''
def calculateProbability(**args):	
	nCr = math.factorial(args['trials']) / 	\
		(math.factorial(args['heads']) * 	\
		math.factorial(args['trials']-args['heads']) );
	nCr = nCr * (p**args['heads']) * (q ** (args['trials']-args['heads']));	
	return nCr;



numberOfLines = int(sys.stdin.readline(), 10); # number of test cases

# get values for "trials" and "heads" for each test case
inputLines = [];
for x in range(numberOfLines):
	inputLines.append(sys.stdin.readline());
# pattern of each test case, ie 10 2
reo = re.compile(r'(?P<trials>\d+) +(?P<heads>\d+)');

# get total probability for each test case
for x in range(numberOfLines):
	mo = reo.search(inputLines[x]);
	if mo:
		for head in range(int(mo.group('heads'),10)+1):
			_sum += calculateProbability( trials=int(mo.group('trials'), 10), \
				heads=head );
		sys.stdout.write('%.4f\n' % _sum);
		_sum = 0;
		#if x < numberOfLines-1:
		#	sys.stdout.write('\n');
		
	

















