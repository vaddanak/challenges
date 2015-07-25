#!/usr/bin/env python


from __future__ import print_function;

import re;

'''
'''
pattern = r'^(a|b).*?xy';
patternObject = re.compile(pattern);


inputString = raw_input();

matchObject = re.match(patternObject, inputString);

if matchObject:
	print(matchObject.group());


