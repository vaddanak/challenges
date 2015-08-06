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
		
def htmlemail():
	'''
	HTML email.
	'''
	import smtplib;		
	#from email.mime.multipart import MIMEMultipart as parts;
	import base64;
	import io;
	
	_from = 'vaddanak@gmail.com';
	to = ['vaddanak@gmail.com'];
	msg = '''From: vad seng <vaddanak@gmail.com>
		To: vad seng <vaddanak@gmail.com>
		Mime-Versin: 1.0
		Content-type: text/html
		Subject: test html email
		
		Testing html email.
		
		This is <b>bold</b>.
		'''
		
	fileName = 'test.txt';	
	fileObject = io.open(fileName, 'rb');
	fileContent = fileObject.read();
	fileContentEncoded = base64.b64encode(fileContent);	
		
	#print(fileContent); #Content of test file
	#print(fileContentEncoded); #Q29udGVudCBvZiB0ZXN0IGZpbGUK
		
	marker = 'AUNIQUEMARKER';
	body = 'This is a test email with file attachment.';
	
	part1 = '''From: vad seng <vaddanak@gmail.com>
		To: vad seng <vaddanak@gmail.com>
		Subject: test file attachment
		MIME-Version: 1.0
		Content-Type: multipart/mixed; boundary=%s
		--%s
		''' % (marker, marker);
		
	part2 = '''Content-Type: text/plain
		Content-Transfer-Encoding:8bit
		
		%s
		--%s
		''' % (body, marker);
		
	part3 = '''Content-Type: multipart/mixed; name=\"%s\"
		Content-Transfer-Encoding:base64
		Content-Disposition: attachment; filename=%s
		
		%s
		--%s--''' % (fileName, fileName, fileContentEncoded, marker);
	
	#msg = part1 + part2 + part3; # not work
	
	#this works and formats correctly in gmail, yea!
	msg = '\r\n'.join(['From: vaddanak@gmail.com', 'To: vaddanak@gmail.com',
		'Subject: testing', '', 'Something interesint']);
		
	try:
		#mp = parts();
		smtpObject = smtplib.SMTP('smtp.gmail.com', 587);
		smtpObject.ehlo();
		smtpObject.starttls();
		smtpObject.login('vaddanak', 'ttgg8771');
		smtpObject.sendmail(_from,to,msg);
		print('PASS');
	except smtplib.SMTPException as err:
		print('FAIL: ', err);	
		
		
		
		
		
		
		
		
		
		
		
		
