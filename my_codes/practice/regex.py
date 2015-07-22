#!/usr/bin/env python


#from __future__ import print_function;

import re;
import sys;

'''
Useful online results:
google keywords:  Pattern Matching Using Regular Expressions UCS
also:	regular expression examples python

'''


'''
grep -Ei 'run.*\.\bdat\b\s*\.$' <atoms.log
matches only the following line in file atomes.log:
RUN 000001 COMPLETED. OUTPUT IN FILE hydrogen.dat.

grep -Ei 'run.*\Bdat\b\s*\.$' <atoms.log
matches:
RUN 000001 COMPLETED. OUTPUT IN FILE hydrogendat.

\B bounded by word characters, ie [a-zA-Z_0-9]
'''

'''
fileObject = raw_input()
while fileObject:
	if fileObject:
		print(fileObject);
	try:	
		fileObject = raw_input();
	except EOFError as err:
		break;	
'''

#patternObject = re.compile('Fred(?i)');
#patternObject = re.compile(
#	r'^RUN\s+[o0-9]{6}\s+COMPLETED. OUTPUT IN FILE'
#	r' [a-z]+\.\bdat\b\s*\.$');
#patternObject = re.compile('Fred', re.I);
#patternObject = re.compile(r'.*Invalid user.*');
# data in file atoms.log
po1 = re.compile(
	r'''						# group 0 is the whole match
	^           
	RUN\ 				#first word
	(?P<jobNumber>[o0-9]{6})\             			# group 1         
	COMPLETED\.\sOUTPUT\sIN\ FILE\                             
	([a-z]+\.\bdat\b)					# group 2
	\.		# last part
	$(?x)						
	''');

# data in file names.txt	
po2 = re.compile (
	r'''
	
	#^(?P<name>[a-z]+?)(?P=name)$
	#[a-z]+[a-z]+$
	#^(([a-z]+)[a-z]+)\1\2$
	^(?P<first>(?P<second>[a-z]+)[a-z]+)(?P=first)(?P=second)$
	
	(?xi)
	'''	);
	
# data in file boil.txt	
po3 = re.compile (
	r'''
	
	(?P<element>[A-Z][a-z]?)	# element
	\s+				# whitespace
	(?P<boil>\d+\.\d+)		# boiling point
	
	(?x)
	'''
);	

# data in paragraph.txt
po4 = re.compile (
	r'''
	
	\s*(?P<word>[a-zA-Z0-9]+)\s*
	
	(?x)
	'''

);

#for line in sys.stdin:
	#sys.stdout.write(line);
	#mo = po3.search(line);	
	#if mo:
		#sys.stdout.write('%s\t%s\n' % (mo.group('jobNumber'), mo.group(2)));
		#sys.stdout.write(matchObject.group() + '\n');
		#sys.stdout.write(mo.group(1) + '\t' + mo.group(2) + '\n');
		#sys.stdout.write('%s\n' % (mo.group(0)) );
	
	#mo = po3.finditer(line);#collection of match objects
	#for x in mo:#x is match object
		#if x:
			#sys.stdout.write('%s\t%s\n' %(x.group('element'),x.group('boil')));	


	#words = po4.finditer(line); # list of words
	#for word in words:
		#sys.stdout.write('%s\n' % (word.group('word')));

	






