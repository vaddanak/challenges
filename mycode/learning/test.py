#!/usr/bin/python

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys; major = sys.version_info.major;

###
if major==2:
	try:
		from __builtin__ import raw_input as input;
	except:
		print('Fail to load Python2 module.');
		sys.exit(1);	
	
elif major==3:
	try:
		from builtins import input as input;
	except:
		print('Fail to load Python3 module.');
		sys.exit(1);

else:
	print('Unknown Python version.');
	sys.exit(1);
	
	
###

import csv;
import io;

###

def test1():
	_input = io.open('csv_input.dat', 'rb');
	_output = io.open('csv_output.dat', 'wb');
	#returns iterator, each next() -> list of row_fields
	rows = csv.reader(_input, quoting=csv.QUOTE_ALL, lineterminator='\n'); 
	csv_writer = csv.writer(_output, quoting=csv.QUOTE_ALL, lineterminator='\n');
	for row in rows:
		print(row);
		csv_writer.writerow(row);
	
	_input.close();	
	_output.close();
	
	
	
'''
"hello world", 12, "nice day"
"eat more fruit", 40, "less chicken"
"wash your hands", 8, "clean is good"

'hello world', 12, 'nice day'
'eat more fruit', 40, 'less chicken'
'wash your hands', 8, 'clean is good'

input:
"hello world","   cat",12
"eat more fruit","dot",40
"wash your hands","house",8

output:
"hello world","   cat",12.0
"eat more fruit","dot",40.0
"wash your hands","house",8.0

input:
"hello world","   cat","12"
"eat more fruit","dot","40"
"wash your hands","house","8"

output:
"hello world","   cat","12"
"eat more fruit","dot","40"
"wash your hands","house","8"
'''
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
