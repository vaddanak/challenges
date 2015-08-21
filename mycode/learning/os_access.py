#!/usr/bin/python

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys, re;
version = sys.version;
### '3.4.0 (default, Jun 19 2015, 14:20:21) \n[GCC 4.8.2]'
### '2.7.6 (default, Jun 22 2015, 17:58:13) \n[GCC 4.8.2]'
patternObject = re.compile(r'^(?P<major>\d+)\.(?P<minor>\d+)\.\d+\s?.*?');
matchObject = patternObject.search(version);
print('{:s}\n{:s}'.format(repr(version), matchObject.group(0)) );

if matchObject:
	try:
		if matchObject.group('major')=='2' and matchObject.group('minor')=='7':
			print('Python2');
			from __builtin__ import raw_input as input;
			from __builtin__ import unicode as str;
			from __builtin__ import str as bytes;
		
		elif matchObject.group('major')=='3' and matchObject.group('minor')=='4':
			print('Python3');
			from builtins import input as input;
			from builtins import str as str;
			from builtins import bytes as bytes;
		
		else:
			print('Unknown Python version: {:s}'.format(version) );
			sys.exit(1);
		
	except:
			(excType, excDetail, traceback) = sys.exc_info();
			print('ExceptionType: {:s}\nExceptionDetail: {:s}\n'\
				.format(excType, excDetail) );		
			sys.exit(1);	

else:
	print('Unknown Python: {:s}'.format(version) );
	sys.exit(1);
	
###

def test1():
	"""
	Demonstrate using module argparse to parse command line input.
	"""
	import argparse;

	description_text = '''This is the description text that is fed to the 
	constructor when the parser is created.  It will be automatically formatted,
	so do not attempt to make clever format.'''
	parser = argparse.ArgumentParser(description=description_text);
	parser.add_argument('-o','--output', help='Name of output file', 
		dest='output_file', default='output.dat', type=str);
	parser.add_argument(help='Directories to be processed', dest='directories',
		nargs='*', default=[], type=str);
	arguments = parser.parse_args();


	# python os_access.py --output='foo.out' dir1 dir2 dir3
	# Namespace(directories=[u'dir1', u'dir2', u'dir3'], output_file=u'foo.out')
	print(arguments);
	print('output file:', arguments.output_file);# output file: foo.out
	#print('output_file' in arguments); # True
	# directories: [u'dir1', u'dir2', u'dir3']
	print('directories:', arguments.directories);
	
	print(arguments.__weakref__); # None
	# {'directories': [u'dir1', u'dir2', u'dir3'], 'output_file': u'foo.out'}
	print(arguments.__dict__);
	
def test2():
	"""
	
	
	"""
	import argparse, os; #import module
	#create parser
	parser = argparse.ArgumentParser();	
	description = \
		"""
		Usage: %prog [options] directories...

		Visit listed directories and process the
		data found in them.  In each directory 
		merge the input files given by the --input
		pattern and put the processing's output
		in the file name given by the --output 
		option.  The processor's parameters come
		from a file in the directory given by the
		--params option.
		""";
	#set help description text	
	parser.__dict__["description"] = description;
	#add the options
	parser.add_argument("-o","--output", # ie NamespaceObject.output_file
		help="The output file (default: output.dat)", 
		dest="output_file", default="output.dat", type=str);
	parser.add_argument("-i", "--input", # ie NamespaceObject.input_pattern
		help="The wildcard for the input files to use (default: *.dat)",
		dest="input_pattern", default="*.dat", type=str);	
	parser.add_argument("-p", "--params", # ie NamespaceObject.params_file
		help="The parameter file in the directory (default: params.cfg)", 
		dest="params_file",
		default="params.cfg", type=str);
	parser.add_argument(dest="directories", # ie NamespaceObject.directories
		help="The directories to search in", default=[], type=str, nargs="+");
	#use the parser; arguments is NamespaceObject
	arguments = parser.parse_args();#create Namespace to hold option-value pairs
	#display the results
	print("input_pattern:", arguments.input_pattern);
	print("output_file:", arguments.output_file);
	print("params_file:", arguments.params_file);
	print("directories:", arguments.directories);
	
	#AttributeError: 'Namespace' object has no attribute 'somethingElse'
	if "somethingElse" in arguments: # now will work correctly
		print("None?", arguments.somethingElse); #
		
	old_cwd = os.getcwd();# store current working directory	
	for directory in arguments.directories: #access item in list
		os.chdir(directory);#change directory
		something_useful(arguments);#do something
		os.chdir(old_cwd);#change back to old current working directory
	del old_cwd, directory;	
		

def something_useful(arguments):
	"""
	
	"""
	import fnmatch, os; # filename matching module; os specific functions
	import subprocess, io;
	print("CURRENT WORKING DIRECTORY:", os.getcwd());
	names = os.listdir(".");# get list of names in current working directory
	print("NAMES:", names);# display names in current working directory
	if arguments.output_file in names:
		names.remove(arguments.output_file); #remove output file
	if arguments.params_file in names:
		names.remove(arguments.params_file); #remove parameter file
	#get sublist of files matching input pattern	
	namesSublist = fnmatch.filter(names, arguments.input_pattern);
	namesSublist.sort(); #sorted input files only
	print("NAMES filtered for {:}: {:}".format(arguments.input_pattern,
		namesSublist) ); #display sorted, filtered sublist of names

	#make command "ls" with options and arguments
	#concat = ["ls","-l"];
	#concat[2:2] = namesSublist
	
	#create file object to write result of above command to
	output = io.open(arguments.output_file, "w");
	
	#subprocess.call(concat, stdout = output);
	#output.flush();
	
	#run "sort" in its own process, like running in background in shell,
	#  prepare its output to be sent out, store process object reference
	sort_proc = subprocess.Popen(['sort','-n'] + namesSublist,
		stdout = subprocess.PIPE );
	#run "cat" in its own process, feed above stdout into below's stdin
	cat_proc = subprocess.Popen(['cat'], 
		stdin = sort_proc.stdout,
		stdout = output);
	#wait for the two processes to finish
	sort_rc = sort_proc.wait();
	cat_rc = cat_proc.wait();
	#commit output to file system
	output.close();
	
	#print(concat);
	
	
	
##########################	
#test = test1
test = test2;

test()	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
