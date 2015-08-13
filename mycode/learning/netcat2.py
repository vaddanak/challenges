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




def main():
	global target, port, command, listen;
	
	if len(sys.argv[1:]): #length of command-line options
		#parse obtions
		#options is [('-o','value1'), ('--option','value2', ...]
		#arguments is leftover ['-s','--option', ...] when given is bad syntax?
		try:#example: python netcat2.py -t '127.0.0.1' --port=9999 --help
			(options, arguments) = getopt.getopt(sys.argv[1:], 
				'ht:p:cl', 
				['help', 'target=', 'port=', 'command', 'listen']);
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
			
			if not listen and len(target) and port>0:
				data = sys.stdin.readline();#result includes newline, ie 'hi\n'
				#outputs 2 newlines bc print() adds one '\n'; so let's turn one off
				#if data.strip():
				#	sys.stdout.write('You typed: %s' % data);
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
		while True:			
			response = '';		
			while '\n' not in response:
				data = clientSocket.recv(1024);
				response += data;
				if not data: #check for empty string
					break;
					
			try:		
				#response contains '\n'
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
			
	if clientSocket:		
		print('in client_handler(...): clientSocket closed');		
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
	global target, port;
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	
	try:
		clientSocket.connect((target, port));
		print('client connected on {:s}:{:d}'.format(target, port) );
		if len(data.strip()):
			clientSocket.send(data); #why send here??
			
		while True:
			response = '';
			recv_length = 1;
			
			while recv_length:
				data = clientSocket.recv(4096);
				response += data;
				recv_length = len(data);
				if recv_length < 4096: #left over; nothing else after this
					break;
					
			sys.stdout.write(response);
			response = input(); # '\n' not included
			response += '\n'; #signal end-of-message to thread processing client
			clientSocket.send(response);			
		
	except:
		(exceptionType, exceptionDetail, traceback) = sys.exc_info();
		print('in client_send(data):\n\t{:s}\n\t{:s}\n'
			.format(exceptionType, exceptionDetail) );
			
	if clientSocket:		
		print('in client_send(data): clientSocket closed');
		clientSocket.close();	
			
main();	

















