#!/usr/bin/python3

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys, re;
version = sys.version; # ie '3.4.0 (default, Jun 19 2015, 14:20:21) \n[GCC 4.8.2]'
patternObject = re.compile(r'^(?P<major>\d+)\.(?P<minor>\d+)\..*');
matchObject = patternObject.search(version);

if matchObject:
	# 2.7.6 (default, Jun 22 2015, 17:58:13)
	# 3.4.0 (default, Jun 19 2015, 14:20:21)
	print(matchObject.group(0)); # major=2|2  minor=7|4
	
	if matchObject.group('major')=='2' and matchObject.group('minor')=='7':
		from __builtin__ import raw_input as input;
		from __builtin__ import unicode as str;
		from __builtin__ import str as bytes;
	
	elif matchObject.group('major')=='3' and matchObject.group('minor')=='4':
		from builtins import input as input;
		from builtins import str as str;
		from builtins import bytes as bytes;
		
	else:
		print('Surprise! Newer version major={:s} minor={:}'\
			.format(matchObject.group('major'), matchObject.group('minor') ) );
		sys.exit(1);	

else:
	print('unknown python version');
	sys.exit(1);

'''
Python2:
(1)	__builtin__.reload(importedModule)


Python3:
(1)	import importlib; importlib.reload(importedModule);

'''	
	

print( sys.argv );




def fun():
	pass;






















