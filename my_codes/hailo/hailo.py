#!/usr/bin/env python3

'''
Author: Vaddanak Seng
File:
Purpose:
'''

from __future__ import print_function;
import re;
import sys;



doPython2 = \
'''
userInput = raw_input(); #get user input
userInput = re.split(r' +', userInput); #split into list of words

#create 4 lists of numbers
oddNegative = [int(x) for x in userInput if int(x)%2 and int(x) < 0]
oddPositive = [int(x) for x in userInput if int(x)%2 and int(x) > 0]
evenNegative = [int(x) for x in userInput if not int(x)%2 and int(x) < 0]
evenPositive = [int(x) for x in userInput if not int(x)%2 and int(x) > 0]

#sort lists of numbers
oddNegative = sorted(oddNegative, reverse=False)
oddPositive = sorted(oddPositive)
evenNegative = sorted(evenNegative, reverse=True)
evenPositive = sorted(evenPositive, reverse=True)

#combine lists into one list
numbers = oddNegative + oddPositive + evenPositive + evenNegative

#put list values into string
numberStr = ''
for x in numbers:
	numberStr = numberStr + str(x) + ' '

#print(oddNegative);
#print(oddPositive)
#print(evenNegative)
#print(evenPositive)
print( numberStr.strip(), end='' )
'''
	
doPython3 = \
'''
userInput = input(); #get input
userInput = re.split(r' +', userInput); #split into list of words
oddNegative = [int(x) for x in userInput if int(x)%2 and int(x) < 0]
oddPositive = [int(x) for x in userInput if int(x)%2 and int(x) > 0]
evenNegative = [int(x) for x in userInput if not int(x)%2 and int(x) < 0]
evenPositive = [int(x) for x in userInput if not int(x)%2 and int(x) > 0]

oddNegative = sorted(oddNegative, reverse=False)
oddPositive = sorted(oddPositive)
evenNegative = sorted(evenNegative, reverse=True)
evenPositive = sorted(evenPositive, reverse=True)

numbers = oddNegative + oddPositive + evenPositive + evenNegative
numberStr = ''
for x in numbers:
	numberStr = numberStr + str(x) + ' '
	
print(oddNegative);
print(oddPositive)
print(evenNegative)
print(evenPositive)
print( numberStr.strip(), end='' )

'''


pythonVersion = sys.version;
#print(pythonVersion);
python2 = re.search(r'2(.{1})\d{1,2}\1\d{1,2}', pythonVersion);
python3 = re.search(r'3.{1}\d{1,2}.{1}\d{1,2}', pythonVersion);

if python2:
	#print(python2.group(0));
	exec(doPython2);

if python3:	
	print(python3.group(0));
	exec(doPython3);
	
	



