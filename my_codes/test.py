#!/usr/bin/env python3

'''
Test miscellaneous language attributes.

'''

from __future__ import print_function;
import re;



txt = "My houseis moving!";
phone = "236-965-9652 # unknown phone number";

matchObject = re.match(r'([Rr])ub[ye]+\1.*?(?:u)', 'rubyr ! rubyy rubye');
matchObject2 = re.search(r'[\s]??is', txt, re.M|re.I);

if matchObject is not None:
	print(matchObject.group());
	#print(matchObject);

if matchObject2 is not None:
	print(matchObject2.group());
	
print(re.sub(r'#.*','',phone));
print(re.sub(r'\D','',phone));
