#!/usr/bin/env python

from __future__ import print_function;

import sys;

def test1():
	print('coffee\ncaf' + unichr(0x00e8) + '\ncaffe' + 
		unichr(0x00e9) + '\nKaffee\n', end='');
	sys.stdout.write('How much? ');	
	_input = sys.stdin.readline();
	sys.stdout.write(str(float(_input) + 2.5));
	



test = test1;





test();
