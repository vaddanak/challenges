#!/usr/bin/python3
"""
Line 1 is required.  Else, if it is omitted, it defaults to /usr/bin/python,
which is Python2.

TO-DO
1. Output shelve file content to backup file called backup.html and backup.xml
2. Order the list of topic titles
3. Keywords???
4. Font effect in iframe display???
5. Make topic title sortable and draggable???
6. Show 'changed' event to indicate need to save??

"""

import shelve;
import cgi;#for cgi.escape(s,quote=True)
import re;

###Symbols that might be replaced with HTML character entities.
symbol_to_html_entity = {};
symbol_to_html_entity['<'] = '&lt;';
symbol_to_html_entity['>'] = '&gt;';
symbol_to_html_entity['"'] = '&quot;';
symbol_to_html_entity["'"] = '&apos;';


def escape(value):
	"""
	& < > "  These four characters can be escaped using cgi.escape(s,quote=True)
	and replaced with HTML-safe entities.  
	However, we will only escape < > " '
	"""			
	value_chrs = list(value);#convert to list of characters
	
	###Replace < > " ' characters in 'value'
	for index in range(len(value_chrs)):
		if value_chrs[index] in symbol_to_html_entity:
			value_chrs[index] = symbol_to_html_entity[value_chrs[index]];
				
	return ''.join(value_chrs);	
	
	
def write_to_shelve_file(key, value, shelve_filename='topics'):
	"""
	Write to shelve file.  It is dict-like.
	The characters < > " ' are escaped in key and value.
	"""		
	###Open a persistent dictionary for reading and writing.
	foo = shelve.open(shelve_filename);
	foo[key.strip()] = value.strip();
	foo.close();	

def read_from_shelve_file(key, shelve_filename='topics'):
	"""	
	Read from shelve file.  It is dict-like.
	Fn returns 2-tuple (key, value).
	"""	
	###Open a persistent dictionary for reading and writing.
	foo = shelve.open(shelve_filename);
	key = key.strip();#remove leading and trailing spaces
	value = foo[key];	
	foo.close();	
	return key, value.strip();
	
	
def display(shelve_filename='topics'):
	"""
	Display content in shelve file.
	"""	
	###Open a persistent dictionary for reading and writing.
	foo = shelve.open(shelve_filename);
	for key in foo:
		print('{:s}: {:s}'.format(key, foo[key]) );	
	foo.close();
	
def clear(shelve_filename='topics'):
	"""
	Remove all content from shelve file.
	"""	
	###Open a persistent dictionary for reading and writing.
	foo = shelve.open(shelve_filename);
	foo.clear();
	foo.close();
	
def remove_entry(key, shelve_filename='topics'):
	"""
	Remove key entry from shelve file.
	Returns 2-tuple (key,value); value is None if key does not exist.
	"""
	###Open a persistent dictionary for reading and writing.
	foo = shelve.open(shelve_filename);
	key = key.strip();
	if key in foo:
		value = foo[key];
		del foo[key];
	else:
		value = None; 
	
	foo.close();
	return key,value;
	
def compose_xml(shelve_filename='topics'):
	"""
	Retrieve all key-value pairs in shelve file and construct xml format.
	Return xml-formatted key-value pairs.
	"""
	###Open a persistent dictionary for reading and writing.
	text_xml = ['<topics>'];
	foo = shelve.open(shelve_filename);
	for key in foo:
		text_xml.append('<topic>');
		text_xml.append('<title>');
		text_xml.append(key);
		text_xml.append('</title>');
		text_xml.append('<solution>');
		text_xml.append(foo[key]);
		text_xml.append('</solution>');
		text_xml.append('</topic>');	
	foo.close();
	text_xml.append('</topics>');
	return ''.join(text_xml);	
	
	
def compose_titles_xml(shelve_filename='topics'):
	"""
	Retrieve all key-value pairs in shelve file and construct xml format.
	Return xml-formatted key-value pairs.
	
	type(foo.keys()) ->  <class 'collections.abc.KeysView'>
	foo.keys() -> KeysView(<shelve.DbfilenameShelf object at 0x7f58dfc02978>)
	collections.KeysView issubclass of collections.Iterable
	"""
	###Open a persistent dictionary for reading and writing.
	text_xml = ['<topics>'];
	foo = shelve.open(shelve_filename);
	keys = list(foo.keys()); #convert Iterable into a list type
	keys.sort(); #sort in place; returns nothing
	for key in keys:
		text_xml.append('<topic>');
		text_xml.append('<title>');
		text_xml.append(key);
		text_xml.append('</title>');		
		text_xml.append('</topic>');	
	foo.close();
	text_xml.append('</topics>');
	return ''.join(text_xml);	
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
