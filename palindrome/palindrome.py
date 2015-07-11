#!/usr/bin/env python3

u'''
Author: Vaddanak Seng
File: palindrome.py
Purpose: Determine if user input test is a palindrome
'''

from __future__ import print_function;
import sys;


userInput = raw_input(); #get user input

mlist = [x for x in reversed(userInput)]; #convert str into reversed list
userInputReversed = u''.join(mlist);#join list values into a str

if userInput==userInputReversed:
	result = 1;
else:
	result = 0;

print(result, end='');


