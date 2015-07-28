#!/usr/bin/env python



from __future__ import print_function;

import socket;



#create socket object 
sock = socket.socket();

#setup address
host = socket.gethostname();
port = 12345;
address = (host, port);

#connect to server
sock.connect(address);

#communicate
print('Client: ', sock.recv(1024));

sock.sendto('Hello dare!', address);

print('Client: ', sock.recv(1024));

#close the socket
sock.close();
