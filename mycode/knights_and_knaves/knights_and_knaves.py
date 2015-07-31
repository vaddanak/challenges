#!/usr/bin/env python
'''
Author: Vaddanak Seng
File: knights_and_knaves.py
Purpose: Determine which person is telling the truth.
Date: 2015/07/31

Runs on both python2 and python3? YES
'''

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import re;
import io;
import sys;

# condition to load proper module depending on which Python version is running
if sys.version_info.major == 2:
	try:
		from __builtin__ import raw_input as input;
	except:
		print("Failed to import Python2 module!");
		exit();


elif sys.version_info.major == 3:
	try:
		from builtins import input as input;
	except:
		print("Failed to import Python3 module!");
		exit();

else:
	print('Unknow Python version!');
	exit();

# specify the regular expression pattern
po = re.compile(r'''
	(?x)
	^(?P<speaker>[mv]{1}):(?P<first>[mv]{1})(?P<first_class>\d{1})
	(?P<second>[mv]{1})(?P<second_class>\d{1})$	
	''');

mo1 = po.match(input());
mo2 = po.match(input());

if mo1 and mo2:
	#print(mo1.group(0));
	#print(mo2.group(0));
	# first input line, ie m:m1v0; m1-->"m1"  v1-->"v0"
	if int(mo1.group('first_class')): # if mike is a knight, then "as is"
		m1 = 1;
		v1 = int(mo1.group('second_class'));
	else: # if mike is a knave, then victor is opposite of what's given
		m1 = 0;
		if int(mo1.group('second_class')):
			v1 = 0;
		else:
			v1 = 1;
	# second input line, ie v:m0v0; m2-->"m0"  v2-->"v0"
	if int(mo2.group('second_class')): # if victor is a knight ...
		v2 = 1;
		m2 = int(mo2.group('first_class'));
	else: # if victor is a knave, then mike is opposite of what's given
		v2 = 0;
		if int(mo2.group('first_class')):
			m2 = 0;
		else:
			m2 = 1;

	#print(m1,v1);
	#print(m2,v2);


	if m1&m2 and not v1&v2 and not v1^v2: # when m1=m2=1 and v1=v2=0
		print('m', end='');
	elif v1&v2 and not m1&m2 and not m1^m2: # when v1=v2=1 and m1=m2=0
		print('v', end='');
	else:
		print('u', end='');



#io.open().read() -->type is unicode ; open().read() --> type is str
#print(type(io.open('./mycode/knights_and_knaves/knights_and_knaves.h').read()));
#print((io.open('./mycode/knights_and_knaves/knights_and_knaves.h').read()));
