#!/usr/bin/env python3

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys;

###

if sys.version_info.major == 2: 	# Python 2 modules
	try:
		from email.MIMEMultipart import MIMEMultipart as mp;
		from email.MIMEText import MIMEText as mt;
		from __builtin__ import raw_input as input;
	except:
		print('Failed to import Python 2 modules');
		exit(None);
elif sys.version_info.major == 3: # Python 3 modules
	try:
		from email.mime.multipart import MIMEMultipart as mp;
		from email.mime.text import MIMEText as mt;
		from builtins import input as input;
	except:
		print('Failed to import Python 3 modules');
		exit(None);	
else:
	print('Unknow Python version');
	exit(None);

import smtplib;

import io;

###

def test1():
	print('coffee\ncaf\u00e8\ncaffe' + 
		'\u00e9nKaffee\n', end='');
	sys.stdout.write('How much? ');	
	_input = sys.stdin.readline();
	sys.stdout.write(str(float(_input) + 2.5));
	
def test2():
	print('1. ', 223 / 71);
	print('2. ', (1 + (1/10))**10 );
	print('3. ', (1 + (1/100))**100 );
	print('4. ', (1 + (1/1000))**1000);
	
def test3():
	print('sparrow' > 'eagle');
	print('dog' > 'Cat' or 45%3==0);
	print(60-45/5+10==1);
	
def email():	
	msg = mp();
	msg['From'] = 'vaddanak@gmail.com';
	msg['To'] = 'vaddanak@mail.usf.edu';
	msg['Subject'] = 'Testing smtp';
	body = 'Nothing interesting';
	msg.attach(mt(body,'plain'));
	
	_from = 'vaddanak@gmail.com';
	toList = ['vaddanak@mail.usf.edu'];
	message = \
		'''
		From: Vad Seng <vaddanak@gmail.com>
		To: Vad at USF <vaddanak@mail.usf.edu>
		Subject: Testing
		
		Message is a test.
		'''
	result = '';	
	try:
		#smtpObject.connect();
		smtpObject = smtplib.SMTP('smtp.gmail.com', 587);
		#smtpObject.ehlo();
		smtpObject.starttls();
		#smtpObject.ehlo();
		smtpObject.login(user='vaddanak',password='ttgg8771');
		#result = smtpObject.sendmail(_from, toList, message);
		result = smtpObject.sendmail(_from, toList, msg.as_text());		
		print("Sent OK");
	except smtplib.SMTPException as err:
		print("Sent BAD");
		print('RESULT: ' + result);
		print('ERR: ' + str(err));
		
	smtpObject.quit();
	
	print(type(io.open('cambridge.py')));
	
def email2():
	# Specifying the from and to addresses

	fromaddr = 'vaddanak@gmail.com'
	toaddrs  = 'vaddanak@mail.usf.edu'

	# Writing the message (this message will appear in the email)

	msg = 'testing smtp 2'

	# Gmail Login

	username = 'vaddanak'
	password = 'ttgg8771'

	# Sending the mail  
	
	#works after https://www.google.com/settings/security/lesssecureapps 
	#and 'turn ON' less secure access
	server = smtplib.SMTP('smtp.gmail.com:587') 
	#server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()	
	
def test4(*args):
	_input = input('Number? ');
	print(type(_input), type(args[1]), args[3]);
	#sys.stdout.write('Number? ');
	#_input = sys.stdin.readline();
	sys.stdout.write(str(int(_input)**0.5) + '\n');
	
	
def test5():
	list1 = [0.3, 0.0, 0.4];
	list2 = [0.2, 0.5, 0.6];
	
	sum = 0.0;
	for index in range(len(list1)):	
		sum += (list1[index]-list2[index])**2;
	del index;
	print(sum);
	
class testClass(object):
	def __init__(self):
		self.store = ['cat', 'mat', 'dog', 'fat'];
		# __fat or __fat_ are private _{2}[a-zA-Z]+_?
		# _fat or _fat__ or __fat__ are public
		self.__fat___ = 'lucy'; 
		
	def __getitem__(self, index):		
		return self.store[index];
		
	
def test6():
	foo = [4, 6, 2, 7, 3, 1, 9, 4, 2, 7, 4, 6, 0, 2];
	bar = foo[3:12:3];
	bar[2] += foo[4];
	foo[0] = bar[1];
	print(bar);	
	print(testClass()[1]);
	print(testClass().__fat___)
	
	_file = io.open(file='cambridge.py', mode='r');
	print(_file.readline());
	print(type(_file));
	
	_file.close();
	
def test7():
	nchars = nwords = nlines = 0;
	
	for line in io.open('cambridge.py', 'r'):
		nlines += 1;
		nchars += len(line);
		nwords += len(line.split());
		
	sys.stdout.write('lines:%d   characters:%d   words:%d\n' %
		(nlines, nchars, nwords) );	
	print(type(line)); # py2: <type 'unicode'>  py3: <class 'str'>
	
def test8():
	import class1;	
	class1.hi();
	
	_file = io.open('class2.py', 'w');
	content = \
	"from __future__ import print_function;\
	\ndef hello():\
	\n	print('hello');\
	"
	_file.write(content);
	if sys.version_info.major==2:
		exec(r'''_file.write(unicode('\n'));''');
		#TypeError: must be unicode, not str	
	exec(r'''_file.write('%d' % (5));''');
	_file.close();
	import class2;
	class2.hello();
	if sys.version_info.major==2:
		moduleObject = eval('reload(class1)');
		moduleObject.hi();
	elif sys.version_info.major==3:
		exec('import importlib;');
		mo = eval('importlib.reload(class1)');
		mo.hi();
		pass;	
		
def total(numbers):
	_sum = 0;
	for num in numbers:
		_sum += num;
	return _sum;
	
def product(numbers):
	_product = 1;
	for num in numbers:
		_product *= num;
	return _product;	
	
import utils;

def test9():
	en_to_fr = {'cat':'chat', 'dog':'chien', 'mouse':'souris', 'snake':'serpent'};
	for (key, value) in en_to_fr.items():
		print(key, value);

def test10(_list):
	_list = ['the', 'cat', 'sat', 'on', 'the', 'mat' ];
	_dict = {};
	for x in _list:
		if x in _dict.keys():
			_dict[x] += 1;
		else:
			_dict[x] = 1;
	
	_dict['bird'] = 1.2;
	itemList = list(_dict.items());	
	itemList.sort();
	for key, value in itemList:		
		print('{:<5} {:1}'.format(key,value));
	
def test11():
	dictionary = {'mouse':'rat\u00f3n', 'cat':'gato', 'dog':'perro'};
	copy = {};
	for key, value in dictionary.items():
		key, value = value, key;			
		copy[key] = value;
	#print(dictionary);	
	#print(dictionary['mouse']);
		print('%-8s %-8s' % (key, copy[key]) );
	
def test12():
	_list = [('Joe',9), ('Samantha',45), ('Methuselah',969)];
	_max = len(_list[0][0]);
	_maxLen = len(str(_list[0][1]));
	for item in _list:
		key, value = item;
		if len(key) > _max:
			_max = len(key);
		if len(str(value)) > _maxLen:
			_maxLen = len(str(value));	
			
	for item in _list:
		key, value = item;
		print('{0:<{1:}} {2:>{3:}d}'.format(key, _max, value, _maxLen) );
	
	
import utils; # second 'import utils' instance	
	
def test13():
	import getopt; # module object visible in function namespace	
	import sys;
	opts, args = getopt.getopt(sys.argv[1:],'ab:cp:', ['help=','host','port']);	
	print(opts);
	print(args);
	#print(sys.argv[1:]);
	
	
import threading;
import time;

class MyThread(threading.Thread):
	def __init__(self, threadName, delayDuration):
		
		self.threadName = threadName;
		self.delayDuration = delayDuration;
		threading.Thread.__init__(self, name=threadName);
		
	def run(self):		
		lock.acquire();	
		print('Starting --', self.threadName);		
		test14(self.threadName, self.delayDuration);
		print('Exiting --', self.threadName);
		lock.release();
	
def test14(threadName, delayDuration):
	import threading;
	import time;	
	
	count = 0;
	while count < 5:
		time.sleep(delayDuration);
		print(threadName, time.ctime(time.time()) );
		count += 1;
	
def test15():
	weights = [0.1, 0.5, 2.6, 7.0, 5.3];
	_sum = 0.0;
	for weight in weights:
		#print( '{:.1f} '.format(weight), end='');	
		_sum += weight;
	del weight; #remove loop variable 'weight'
	print(_sum);
	
def test16():
	metals = [ 'silver', 
           'gold', 
           'iron', 
           'zinc', 
           'aluminium', 
           'copper', 
           'magnesium', 
           'lead' ];
	#create new list from 'metals' list without 'copper' item           
	print( metals[:metals.index('copper')] + metals[metals.index('copper')+1:] );
	print( metals);
	
def test17():
	data = [ 5.75, 8.25, 2.625, 5.50, 0.125, -12.875, 56.50, -32.125, -0.96875,
         -5.875, 8.75, 53.9375, 192.125 ]
	_len = len(data);#length of list 'data'
	if _len % 2 == 0:
		part = int(_len/2);	#get index that is one pass center item	
	else:
		part = int(_len/2+1);
		
	#make deep-copy of 'metals' list	
	data1 = data[:part]; #create new list that is sublist of list 'data'
	data2 = data[part:];	
	
	print(_len);	
	print(data1);
	print(data2);
	print(data1 + data2); #create new list and has same values as 'data'
	print(data);      	           
	
	
def test18():
	import utils;
	utils.printDictionary(utils.names);
	utils.printDictionary(utils.reverseDictionary(utils.names));
	
def poly(x):
	return x**2 - 2.0;
	
			
	
###	

'''	
test = test18;
#test();
#print( utils.findRoot(poly,0.0,2.0, 1.0e-5) );
print(utils.calculateStat( 1,2,3,4,5,6 ));
print(utils.calculateStat() );
'''

'''
lock = threading.Lock();#define outside of run() bc need singleton
thread1 = MyThread('thread-1', 1);
thread2 = MyThread('thread-2', 1);
thread1.start();
thread2.start();
threads = [thread1, thread2];
for t in threads:
	t.join(); #allows main thread to wait for children to finish its activity
print('Exiting main thread');
'''

'''
for element in utils.chemicals:#each key in chemicals dictionary; value is 3-tuple
	(name, number, temperature) = utils.chemicals[element];#access tuple all at once
	print('{:s}: {:.1f}K'.format(name, temperature) );
	#print('{:s}: {:.1f}K'.format(utils.chemicals[element][0],
	#	utils.chemicals[element][2])); #access in sequential manner like list, BAD!
	
del name, number, temperature, element; #clean up		
'''

'''
#extract numbers from numbers.txt and find minimum, mean, and maximum number.
import io;
fileObject = io.open('numbers.txt');#use Python2/3 open function
numbers = [];#store float values
for number in fileObject:#data read in from file is a string; represents float value
	numbers.append(float(number));#convert float as str type to float type
fileObject.close();	#close file object
del number, fileObject;#clean up
print(utils.calculateStat(numbers));#find (minimum, mean, maximum) tuple
'''

'''
#copy file line by line
import sys, io;
for line in sys.stdin:
	sys.stdout.write(line);
del line;
'''

'''
#find (minimum,mean,maximum) for the numeric values given on command line
import sys;
from utils import calculateStat as stat;#create alias stat for calculateStat
numbers = [];
for arg in sys.argv[1:]:#create new list containing only options, access each one
	numbers.append(int(arg));#command line argument values are strings, so convert
if len(numbers):#arg defined if lenght is non-zero
	del arg;	
print(stat(numbers)); # print (minimum, mean, maximum
'''

#given list of element symbols on command line, display detail for each symbol
#	and determine symbol with lowest atomic number
import sys;
import utils;
from utils import calculateStat as stat;
from utils import chemicals;
numberToSymbol = {};
for symbol in sys.argv[1:]:
	(name, atomicNumber, boilingPoint) = chemicals[symbol];
	numberToSymbol[atomicNumber] = symbol;
	print('{:s} has a boiling point of {:.2f}K'.format(name, boilingPoint) );
del symbol, name, atomicNumber, boilingPoint;
(minimum, mean, maximum) = stat(numberToSymbol.keys());
print('{:s} has lowest atomic number of {:d}'
	.format(numberToSymbol[minimum], minimum) );


#import os;
#with os.popen('ls -al') as ls:
#	print(ls.readline());

#test = email2;

#numbers = [7, -4, 1, 6, 5];
#sys.stdout.write('total: %d\nproduct: %d\n' % 
#	(total(numbers), product(numbers)));

#filename = input('Enter filename: ');
#print(filename, utils.file_stats(filename));

#_listx = ['the', 'cat', 'sat', 'on', 'the', 'mat' ];
#test(_listx);



