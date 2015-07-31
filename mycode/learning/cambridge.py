#!/usr/bin/env python3

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys;

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
		
	
test = test4;
#test = email2;




test(1,2,3,4,5);



















