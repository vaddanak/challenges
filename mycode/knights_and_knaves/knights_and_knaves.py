#!/usr/bin/env python
'''
Author: Vaddanak Seng
File: knights_and_knaves.py
Purpose: ?
Date: 2015/07/27

Runs on both python2 and python3?
'''

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import re;
import io;



#io.open().read() -->type is unicode ; open().read() --> type is str
print(type(io.open('./mycode/knights_and_knaves/knights_and_knaves.h').read()));
#print((io.open('./mycode/knights_and_knaves/knights_and_knaves.h').read()));
