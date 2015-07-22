'''
Author: Vaddanak Seng
File: pebbles.py
Purpose: Determine probability of pebble color.
'''

from __future__ import print_function;

import re;

pebbleList = raw_input(); # get list of color counts
pebbleIndex = raw_input(); # get index

# generate list of color counts as list of integers
pebbleList = [int(x) for x in re.split(r'\s+',pebbleList) if re.search(r'\d',x)];
# convert index to int type and zero-base
pebbleIndex = int(pebbleIndex)-1;

# calculate probability and extract floating-point value to include two decimal
# places, no rounding.
print('%s' % re.search(r'.*\.\d{2}',(str(float(pebbleList[pebbleIndex])/float(sum(pebbleList))))).group() , end='');

