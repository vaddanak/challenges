#!/usr/bin/env python



from __future__ import print_function;

import socket;




#create socket object
sock = socket.socket();

#setup address (hostname, port)
hostname = socket.gethostname();
port = 12345;
address = (hostname, port);

#bind socket to port
sock.bind(address);

#listen to port
sock.listen(5);

#handle connections
while True:
	(connection, address) = sock.accept();#accept client request to connect
	print('Server says: ', address[0], address[1]);
	connection.send('Server says:  May I help you?');
	connection.send('Server says:  Don\'t be shy!');
	connection.send('Server says that you sent: ' + connection.recv(1024));
	connection.close();



