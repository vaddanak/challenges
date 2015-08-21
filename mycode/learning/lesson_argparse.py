#!/usr/bin/python3
"""
Python3 lesson.

"""

import sys;
import argparse;


#create the parser
desc =\
	'This is a lesson on parsing the commandline options and arguments.';
credit = 'Author: Vaddanak Seng';	
parser = argparse.ArgumentParser(description=desc, epilog=credit);
#add argument
#action='store'	to store a user-given value in arguments, which is default;
#	also makes argument required if option is used
#action='count'	to store a count of how often the flag appears
#omitting flag like '-x' or '--limit' will make the argument compulsory;
#	Because there are no flags specified, this is known as a “positional” 
#	argument, defined by its position in the command line, rather than by any
#	associated flag.
parser.add_argument('-x', '--limit', help='Range of values of x', \
	dest='limit', default=1.0, type=float, metavar='X', action='store');
parser.add_argument('-m', '--lower', help='Minimum order of polynomial', \
	dest='lower', default=1, type=int, metavar='M1', action='store');
parser.add_argument('-n', '--upper', help='Maximum order of polynomial', \
	dest='upper', default=3, type=int, metavar='M2', action='store');
parser.add_argument('-k', '--npts', help='Number of points to plot', \
	dest='npts', default=512, \
	type=int, metavar='N', action='store');
parser.add_argument(dest='source_file', type=str, metavar='source', \
	help='The source file', action='store');
parser.add_argument(dest='dest_file', type=str, metavar='target', \
	help='The destination file', action='store');	
parser.add_argument('-t', '--title', help='Title of graph', dest='title', \
	default='', type=str, metavar='T', action='store');
parser.add_argument('-v', '--verbose', action='count', dest='verbosity', \
	help='Display more detail', default=0);#action='count' and type=int contradicts
#parser.add_argument(dest='filename', type=argparse.FileType(mode='wb'), \
#	default=sys.stdout, help='The output file (required)', \
#	metavar='fname', action='store');
	#Positional arguments are always placed at the end, regardless.
	
	
'''
destination The name of the variable in the arguments object.
action 		What to do with this flag (e.g. expect a value and to store it).
type 		What type that value should be.
default 	What value to use if the user doesn’t specify one.
'''	


#use the parser
arguments = parser.parse_args();

print(arguments);
