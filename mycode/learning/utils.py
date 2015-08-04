"""
Souvenir tools from Cambridge University tutorial.
"""

from __future__ import unicode_literals;
from __future__ import print_function;
from __future__ import division;

#SyntaxError: future feature import_absolute is not defined
#from __future__ import import_absolute;
from __future__ import absolute_import;

import io;

def file_stats(filename):
	'''
	Returns tuple of line numbers, word count, and character count of text
	content in filename.
	'''
	n_lines = n_words = n_chars = 0;
	fileObject = io.open(filename, mode='r');
	for line in fileObject:
		n_lines += 1;
		n_chars += len(line);
		n_words += len(line.split());
	return (n_lines, n_words, n_chars);
	
def sendmail():
	'''
	Fn to test smtp.
	'''
	import smtplib;
	sender = 'vaddanak@gmail.com';
	receivers = ['vaddanak@gmail.com','vaddanak@mail.usf.edu'];
	message = '''\
		From: Vad Seng <vaddanak@gmail.com>
		To: Me Myself I <vaddanak@mail.usf.edu>
		Subject: Testing smtp
		
		Hello world!
		'''
	try:
		smtpObject = smtplib.SMTP('smtp.gmail.com', 587);
		smtpObject.ehlo();
		smtpObject.starttls();
		smtpObject.login(user='vaddanak', password='ttgg8771')
		smtpObject.sendmail(from_addr=sender, to_addrs=receivers, msg=message);
		smtpObject.quit();
		print('PASS: Message sent!');
	except smtplib.SMTPException as err:
		print('FAIL: ', err);	
		
		
		
		
		
		
		
		
		
		
		
		
		
