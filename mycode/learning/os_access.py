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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
