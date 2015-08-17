#!/usr/bin/python

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys; major = sys.version_info.major;
import getopt;
import socket;
import threading;
import subprocess;
import re;

#create alias to work with both python2 and python3
if major==2:
	try:
		from __builtin__ import raw_input as input;
	except:
		print('fail to import python2 module');
		sys.exit(1);
		
elif major==3:
	try:
		from builtins import input as input;
	except:
		print('fail to import python3 module');
		sys.exit(1);
else:
	print('unknown python version');
	sys.exit(1);

#global variables
target = '0.0.0.0';
port = 9999;
command = False;
listen = False;
execute = '';
upload = False;
upload_destination = '';

#mode flags; private
UPLOAD = '###UPLOAD###';
EXECUTE = '###EXECUTE###';
RE_QUIT = r'^\s*(quit|exit)\s*$(?i)';
RE_UPLOAD = r'^###UPLOAD###';
RE_EXECUTE = r'^###EXECUTE###';

def main():
	global target, port, command, listen, execute, upload, upload_destination;
	
	if len(sys.argv[1:]): #length of command-line options
		#parse obtions
		#options is [('-o','value1'), ('--option','value2', ...]
		#arguments is leftover ['-s','--option', ...] when given is bad syntax?
		try:#example: python netcat2.py -t '127.0.0.1' --port=9999 --help
			(options, arguments) = getopt.getopt(sys.argv[1:], 
				'ht:p:cle:u:', 
				['help', 'target=', 'port=', 'command', 'listen', 'execute=',\
					'upload=']);
			# ['netcat2.py', '-t', '127.0.0.1', '--port=9999', '--help']	
			print(sys.argv);
			# [('-t', '127.0.0.1'), ('--port', '9999'), ('--help', '')]		
			print(options); 
			print(arguments); # []	
			for pair in options:
				(option, value) = pair;
				if option in ('-h', '--help'): # pair is ('--help', '')
					pass;
				if option in ('-t', '--target'): # pair is ('-t', '127.0.0.1')
					target = value;
				if option in ('-p', '--port'): # pair is ('--port', '9999')
					port = int(value);
				if option in ('-c', '--command'):
					command = True;
				if option in ('-l', '--listen'):
					listen = True;	
				if option in ('-e', '--execute'):
					execute = value;	
				if option in ('-u', '--upload'):
					upload = True;
					upload_destination = value;
			
			if not listen and len(target) and port>0:
				data = '';
				if upload or (not command and not len(execute)):
					data = sys.stdin.read();#result includes newline, ie 'hi\n'
					if upload:
						data = UPLOAD + data;
					#outputs 2 newlines bc print() adds one '\n'; so let's turn
					#  one off
					#if data.strip():
					#	sys.stdout.write('You typed: %s' % data);
				
				if len(execute):
					data = EXECUTE + execute;							
								
				if command:
					data = '\n';
				
					#sys.stdout.write(repr(data));
				
				client_send(data);#minimal sent is '\n'
				
			if listen:
				print('Launch server at {:s}:{:d}'.format(target, port) );
				server_loop();	
	
		except:#dangerous to use provided 'traceback'
			(exceptionType, exceptionDetail, traceback) = sys.exc_info();
			print('in main():\n\t{:s}\n\t{:s}'
				.format( exceptionType, exceptionDetail) );


def client_handler(clientSocket, serverSocket):
	try:
		response = '';
		while True:
			data = clientSocket.recv(4096);
			response += data;
			if len(data) < 4096:#all remaining data are read
				break;
				
		#check for ###EXECUTE###
		if re.match(RE_EXECUTE, response):
			response = re.sub(RE_EXECUTE,'',response);#remove prepended flag
			(status, output) = process_command(response);
			clientSocket.send(output);
			if not status:
				print('Failed to execute command');			
			
		#check for ###UPLOAD###
		elif re.match(RE_UPLOAD, response):	
			print('requesting to upload');
		
		#check for command
		else:
			clientSocket.send('<shell> ');
			shell_loop(clientSocket);		
				
	except:
		(excType, excDetail, traceback) = sys.exc_info();
		print('in client_handler(clientSocket, serverSocket):\n'\
			'ExceptionType: {:s}\nExceptionDetail: {:s}\n'\
			.format(excType, excDetail) );
		
		
	'''
	try:
		while True:			
			response = '';	
				
			while '\n' not in response:
				data = clientSocket.recv(1024);
				response += data;
				if not data: #check for empty string
					break;
			
			try:
				if re.match(RE_UPLOAD, response):
					print('uploading... done');
					#remove prepended flag r'^###UPLOAD###'
					response = re.sub(RE_UPLOAD,'',response);
					print(response);
					break;
			except:
				pass;
				
			try:	
				if re.match(RE_EXECUTE, response):	
					print('executing ... done');
					#remove prepended flag r'^###EXECUTE###'
					response = re.sub(RE_EXECUTE,'',response);
					print(response);
					break;					
			except:
				pass;
				
			try:						
				#response contains '\n'
				if re.search(RE_QUIT, response):
					break;
				response = subprocess.check_output(response.strip(), 
					stderr=subprocess.STDOUT, shell=True);
			except subprocess.CalledProcessError as err:
				(excType, excDetail, traceback) = sys.exc_info();
				response = 'ExceptionType: {:s}\nExceptionDetail: {:s}\n'\
					.format(excType, excDetail);
					
			clientSocket.send(response + '<shell> '); 			
			#clientSocket.send('<shell> ');					
				
	except:
		(exceptionType, exceptionDetail, traceback) = sys.exc_info();
		print('in client_handler(clientSocket, serverSocket):\n  ' +\
			'ExceptionType: {:s}\n  ExceptionDetail: {:s}\n'
			.format(exceptionType, exceptionDetail) );
	'''
			
	if clientSocket:		
		print('in client_handler(...):  clientSocket closed');		
		clientSocket.close();	
			

def server_loop():
	global target, port;	
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);#IPv4, TCP	
	
	try:
		serverSocket.bind((target, port));
		serverSocket.listen(5);
	
		while True:
			(clientSocket, address) = serverSocket.accept();
			thread = threading.Thread(target=client_handler, 
				args=(clientSocket, serverSocket) );
			thread.start();	
	except:
		(exceptionType, exceptionDetail, traceback) = sys.exc_info();
		print('in server_loop():\n\t{:s}\n\t{:s}\n'
			.format(exceptionType, exceptionDetail) );
	
	if serverSocket:		
		print('in server_loop(): serverSocket closed');
		serverSocket.close();	


def client_send(data):
	global target, port, command, execute, upload;
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	memsize = 4096 * 1;
	try:
		clientSocket.connect((target, port));
		print('client connected on {:s}:{:d}'.format(target, port) );
		#if len(data.strip()):
		clientSocket.send(data); #why send here?? both ends recv is stalemate
			
		while True:
			response = '';
			recv_length = 1;			
			while recv_length:
				data = clientSocket.recv(memsize);
				response += data;
				recv_length = len(data);				
				if recv_length < memsize: #left over; nothing else after this
					break;
			#sys.stdout.flush() required if not output with '\n' ;
			#  for example, sys.stdout.write(response + '\n') or print(end='\n')
			#  otherwise, data is written to buffer and not pushed to display device
			sys.stdout.write(response);
			sys.stdout.flush(); 
						
			if command:
				response = input(); # '\n' not included
				if re.search(RE_QUIT, response):
					break;
				response += '\n'; #signal end-of-message to thread processing client
				clientSocket.send(response);
			else:
				break;							
							
	except:
		(exceptionType, exceptionDetail, traceback) = sys.exc_info();
		print('in client_send(data):\n\t{:s}\n\t{:s}\n'
			.format(exceptionType, exceptionDetail) );
			
	if clientSocket:		
		print('in client_send(data): clientSocket closed');
		clientSocket.close();	
		

def process_command(command_string):
	output = '';
	status = False;
	try:
		output = subprocess.check_output(command_string.strip(),\
			stderr = subprocess.STDOUT, shell = True);
		status = True;	
	except:
		(excType, excDetail, traceback) = sys.exc_info();
		print( 'in process_command(command_string):\nExceptionType: {:s}\n'\
			'ExceptionDetail: {:s}\n'.format(excType, excDetail) );
		output = 'Failed to process command: {:s}\n'.format(command_string);
		status = False;
	return (status,output);
	
	
def shell_loop(client_socket):
	while True:
		response = '';		
		try:
			while '\n' not in response:
				data = client_socket.recv(1024); #message expected to end with '\n'
				response += data;
				if not data: #empty string means no more message to read
					break;
		
			if re.search(RE_QUIT, response):#check if requesting to quit
				break;
			(status, response) = process_command(response);	
			client_socket.send(response + '<shell> ');	
		except:
			(excType, excDetail, traceback) = sys.exc_info();
			print('in shell_loop(client_client):\nExceptionType: {:s}\n'\
				'ExceptionDetail: {:s}\n'.format(excType, excDetail) );		
			break;
	if client_socket:
		client_socket.close();
		print('in shell_loop(client_socket):  client_socket is closed.');

			
main();	

















