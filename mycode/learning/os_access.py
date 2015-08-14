#!/usr/bin/python

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys, re;
version = sys.version;

###
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
