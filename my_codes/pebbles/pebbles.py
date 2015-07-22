'''
Author: Vaddanak Seng
File: pebbles.py
Purpose: Determine probability of pebble color.
'''

from __future__ import print_function;

import re;

pebbleList = raw_input();
pebbleIndex = raw_input();

pebbleList = [int(x) for x in re.split(r'\s+',pebbleList) if re.search(r'\d',x)];
pebbleIndex = int(pebbleIndex)-1;

print('%s' % re.search(r'.*\.\d{2}',(str(float(pebbleList[pebbleIndex])/float(sum(pebbleList))))).group() );

