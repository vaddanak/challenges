#!/usr/bin/env python


from __future__ import print_function;

import re;
import sys;



fileObject = open('names.txt','r');


#for line in fileObject:
#	print(line, end='');

#print();
#patternObject = re.compile(r'fred.*?(?ims)');
#matchObject = re.search(patternObject, fileObject.read());
#mlist = re.findall(patternObject, fileObject.read());

#if matchObject:
#	print(matchObject.group());
	
#print(mlist);	

for line in raw_input():
	#sys.stdout.write(line);
	#print(re.search(r'quit',line));
	print(line);
		
