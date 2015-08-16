#!/usr/bin/python

from __future__ import print_function; # use print()
from __future__ import division; #division result always float type
from __future__ import unicode_literals; #make encoding utf-8 ?
from __future__ import absolute_import; # ?

import getopt; #module to parse command options
import sys; # exit(), stdin, stdout, stderr, argv


#global variables
listen = False;	
command = False;
upload = False;	
upload_destination = '';
port = 0;
execute = '';
target_host = '';


def usage():
	print('python blackhat -t 99.99.99.99 -p 99');#sys.argv[0]=='blackhat'
	print(' -t --target-host=hostname');
	print(' -p --port=99');
	print(' -l --listen'); #listen for connection request
	print(' -h --help');
	print(' -u --upload="file_destination"');#?file to upload or write destination
	print(' -c --command');#launch command shell
	print(' -e --execute="file_to_run"');#execute content of file
	sys.exit(0); #exit normal
	
	
def main():
	'''
	Parse options in command line to run this program.
	Set the global variables based on the command line options.
	Launch functions based on global variable result ???
	'''
	global listen;#declare global variable, defined outside of function scope
	global command;
	global upload;
	global upload_destination;
	global port;
	global execute;
	global target_host;
	
	#print(sys.argv[1:]);

	if len(sys.argv[1:]) == 0: # '-t 99.99.99.99 -p 99' from above
		usage(); #display hints for proper command line syntax		
		
	#parse command line options, ie python blackhat -t 99.99.99.99 -p 99
	#sys.argv[1:]==	'-t 99.99.99.99 -p 99'
	(optionValuePairs, unrecognizedArguments) = getopt.getopt(sys.argv[1:], \
		'p:lhu:ce:t:x',\
		['port=','listen','help','upload=','command','execute=','target-host=']);
		
	print(optionValuePairs);#list of tuples, [('-o','value'),('--option','value')]	
	print(unrecognizedArguments);#leftover options list not complying w spec above
	
	for (option, value) in optionValuePairs: #lookup each tuple in list	
		if option in ('-t','--target-host'): #look for specific option
			target_host = value;
		elif option in ('-p','--port'):
			port = value; #value is a string; not int type
		elif option in ('-l','--listen'):
			listen = True;
		elif option in ('-h','--help'):
			usage();#ends program at end of this call
		elif option in ('-u','--upload'):
			upload_destination = value;
		elif option in ('-c','--command'):
			command = True;
		elif option in ('-e','--execute'):
			execute = value;
		else:	
			assert False, 'unhandled exception'; #forgot this line ???	
			
	if not listen and len(target_host) and int(port)>0:#request with host and port
		_buffer = sys.stdin.read();
	
		print('send to client:', _buffer);
		
	if listen:#request to only listen
		print('listen to socket on port continuously');		
	
def run_command(command):
	import subprocess;#any benefit for putting this here??
	
	#If command has trailing \n, then still works; but if it has trailing
	#	\r\n, then it will fail.  So, safer to remove any trailing whitespace.
	command = command.rstrip();
	
	try:
		#Command can be string or sequence of strings.  If sequence, then
		#	the first item must be the command and rest are options.
		#	Result of command is returned and stored in output.
		output = subprocess.check_output(command, stderr=subprocess.STDOUT,
			shell=True);
	except:
		output = 'Failed to run command';
	
	return output;#return result of command execution
	
print(run_command('ls / -al'));
	
'''	
try:
	result = sys.stdin.read();
	print('result: ', result); #ctrl-D gets you here
except:
	print('failed'); #ctrl-C gets you here; but not ctrl-D
'''
print(type('text')); #unicode in Python2; str in Python3
print(type(b'text'));#str in Python2; bytes in Python3
nums = 1,2,3;
print(type(nums)); # <type 'tuple'>
	
#main();		



























