#!/usr/bin/python3
"""
Python3 lesson.

"""

def subprocess_write_to():
	import subprocess;
	import sys;
	import io;

	output = io.open('lesson_subprocess/output.data','w');

	#exit_code = subprocess.call(['ls', '-l']);
	print('program start');
	running_process = subprocess.Popen(['lesson_subprocess/iterator', '.60'],\
		stdout = output);#run in different process
	print('program stop');
	running_process.wait();

	output.close();
	
def subprocess_read_from():
	import subprocess, io, os;
	
	readme = io.open('lesson_subprocess/output.data', 'r');
	
	exit_code = subprocess.call(['wc'], stdin = readme);
	
	readme.close();
	
test = subprocess_read_from;

test();	
