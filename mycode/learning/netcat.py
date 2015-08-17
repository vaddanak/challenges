'''
netcat-like functionalities.


'''

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys;
major = sys.version_info.major;
import getopt;
import socket;
import threading;
import re;

### reconcile Python2 and Python3 differences
if major==2:
	try:
		from __builtin__ import raw_input as input;
	except:
		print('Failed to load Python2 module');
		sys.exit();

elif major==3:
	try:
		from builtins import input as input;
	except:
		print('Failed to load Python3 module');
		sys.exit();

else:
	print('Unknown Python version.');
	sys.exit();

### define global variables
target_host = '0.0.0.0';
port = 9999;
upload_destination = '';
execute = '';
command = False;
upload = False;
listen = False;
globalVariables = {};

### define functions

def usage():
	print('python[3] -t localhost -p 9999');
	print('-h	--help');
	print('-l	--listen');
	print('-e	--execute="file_to_run"		scripts to run');
	print('-u	--upload="upload_destination"	specify destination for file save');
	print('-t	--target_host="127.0.0.1"');
	print('-p	--port=9999');
	print('-c	--command	invoke shell mode');
	sys.exit(0);
	
	
def main():
	global target_host;
	global port;
	global upload_destination;
	global execute;
	global command;
	global upload;
	global listen;
	global globalVariables;
	
	optionsList = sys.argv[1:];#list command line options, sys.argv[0] is script name
	
	if len(optionsList):
		#options is list of tuples, ie [('-l',''),('--port','9999'),...]
		#arguments is list of leftover options not properly entered
		(options, arguments) = getopt.getopt(optionsList, 'hle:u:t:p:c',
			['help', 'listen', 'execute=', 'target_host=', 'port=', 'command']);	
	
		for (option, value) in options:
			if option in ('-h', '--help'):
				usage();
			elif option in ('-l', '--listen'):
				listen = True;
				globalVariables['listen'] = True;
			elif option in ('-e', '--execute'):
				execute = value;
				globalVariables['execute'] = value;
			elif option in ('-u', '--upload'):
				upload = True;
				upload_destination = value;
				globalVariables['upload_destination'] = value;
			elif option in ('-t', '--target_host'):
				target_host = value;
				globalVariables['target_host'] = value;
			elif option in ('-p', '--port'):
				port = int(value);
				globalVariables['port'] = int(value);
			elif option in ('-c', '--command'):
				command = True;
				globalVariables['command'] = True;
			else:
				assert False, 'unhandled option';
				
		print(optionsList, command);		
	
		if not listen and len(target_host) and port > 0:
			print('not listening');
			data = input('Main: ');
			client_send(data + '\n');
			
		if listen:
			print('listening');
			server_loop();
			
def client_send(data):
	global target_host;
	global port;
	
	patternObject = re.compile(r'(?i)(^quit)|(^exit)');
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);	
	print('client_sends', command);
	try:
		clientSocket.connect((target_host, port));
		
		if len(data):
			clientSocket.send(data);
			
		while True:
			response = '';
			recv_length = 1;
			
			while recv_length:
				#print('before');
				data = clientSocket.recv(4096);
				#print('after');
				recv_length = len(data);
				response += data;
				if recv_length < 4096:
					break;
					
			print(response, end='');
			response = input('Client: ');
			response += '\n';
			
			mo = patternObject.search(response);
			if mo:
				break;
			
			clientSocket.send(response);	
	
	except:
		print('exception in client_send');
		
	clientSocket.close();			


def client_handler(clientSocket, serverSocket):
	global command;
	global globalVariables;

	patternObject = re.compile(r'(?i)shutdown');	
	print('client_handler starts', command, globalVariables['command']);
	if command:
		print('command starts');
		while True:
			clientSocket.send('<shell>: ');	
			response = '';
			
			while '\n' not in response:
				#print('handler before');
				data = clientSocket.recv(1024);
				#print('handler after');
				response += data;
				if not data:
					break;
			clientSocket.send(response);
			
			#subprocess
			
			mo = patternObject.search(response);
			if mo:
				print('Server shutdown');
				serverSocket.close();
				break;
		print('Command ... thread exit');		
	print('client_handler ends');			
	
def server_loop():
	global target_host;
	global port;
	
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	serverSocket.bind((target_host, port));
	
	serverSocket.listen(5);	
	
	while True:
		try:
			(clientSocket, address) = serverSocket.accept();
			thread = threading.Thread(target=client_handler, \
				args=(clientSocket, serverSocket) );
			thread.start();			
		except:
			print('Server Exception in server_loop: Server closed');	
			serverSocket.close();
			break;

		

	
	
	
main();
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
