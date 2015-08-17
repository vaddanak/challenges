#!/usr/bin/python

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import sys;
major = sys.version_info.major; # 2 for Python2, 3 for Python3

import socket;
import threading;
import re;

host = '0.0.0.0'; #all interfaces?
port = 9999;
bufferSize = 4096;

exitFlag = 0;

def process_client_request(clientSocket, clientAddress):
	global exitFlag;
	global server;
	reo = re.compile(r'(?i)(^quit)|(^exit)');
	reo1 = re.compile(r'(?i)^shutdown');
	while True:
		response = '';
		recv_length = 1;
		while recv_length:#ensure we read entire incoming message
			data = clientSocket.recv(bufferSize); #block to read socket
			response += data;
			recv_length = len(data);
			if recv_length < bufferSize: #last data sent
				break;
				
		print('Received: {:s}'.format(response));
		clientSocket.send('ACKNOWLEDGED!');#returns number of chr sent
		
		mo = reo1.search(response);#server shutdown request?		
		if mo:
			print('Request for server shutdown');
			exitFlag = 1;#set yes to server shutdown
			#clientSocket.close();
			server.close();#not working
			break;
			
		mo = reo.search(response);#find pattern in string
		if mo:		
			print('Request for client exit');
			break;#pattern found so break out of loop			
		
	clientSocket.close();#clean up		
		


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);#create TCP socket object
server.bind((host,port));#bind socket to port
server.listen(5);#allows 5 backlog connections

while True:
	(client, address) = server.accept(); #wait for client connection request
	print('Accepted connection {:s}:{:d}'.format(address[0], address[1]));
	thread = threading.Thread(target=process_client_request, 
		args=(client,address));
	thread.start(); #call thread run(), which calls target function
	
	if exitFlag:	
		break;
	
server.close();#clean up	
	
# ?? how to remotely shutdown this server ??
	
	
	

