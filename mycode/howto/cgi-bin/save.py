#!/usr/bin/python3
"""
Save topic title and solution to MySQL database and shelve file 'topics'

web server calls line 1 to load and run this module.
"""

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;#not work with Python2.7 shelve module?
from __future__ import absolute_import;

import sys;
import pymysql;
import cgi, cgitb; cgitb.enable();

import utility;#custom module

major = sys.version_info.major; # 2 or 3
minor = sys.version_info.minor; # 7 or 4

'''
mysql> describe howto.topics;
+----------+----------+------+-----+---------+----------------+
| Field    | Type     | Null | Key | Default | Extra          |
+----------+----------+------+-----+---------+----------------+
| id       | int(11)  | NO   | PRI | NULL    | auto_increment |
| title    | text     | YES  |     | NULL    |                |
| solution | longtext | YES  |     | NULL    |                |
+----------+----------+------+-----+---------+----------------+
3 rows in set (0.01 sec)

CAUTION:
Python2.7 shelve key may need to be non-unicode string so do myShelve[str(key)].
'''



columns = [];#list of column values for database input, ie ['"user"', '"pwd"']
content = [];

#returned class ->
#	FieldStorage(None,None,[MiniFieldStorage('topic_title','hi'),
#	MiniFieldStorage('topic_solution','home sweet home')])
request = cgi.FieldStorage();

key_topic_textbox_name = 'topic_title';
key_solution_textarea_name = 'topic_solution';

try:#make connection
	conn = pymysql.connect(host='localhost', user='root', password='',\
		database='vad');
	cursor = conn.cursor();# get cursor to perform action

	#data from client is for one row (at a time) in database
	#request[key] -> MiniFieldStorage('topic_title','hi'); read via name, value
	#textbox HTML element contains 'topic_title'; represents a name-value pair
	#textarea HTML element contains 'topic_solution'; represents a name-value pair
	#for key in request:#effectively, for each data entry HTML element with name-value
		#works for single or multiple values, ie as single value or list of values
		#characters < > " are replaced with HTML entities
		#columns.append('"' + utility.escape(request.getlist(key)[0]) + '"');
	
	#characters < > " are replaced with HTML entities
	if (key_topic_textbox_name in request) and \
	(key_solution_textarea_name in request):
		#get and escape topic_title value
		topic_title = utility.escape(request.getlist(key_topic_textbox_name)[0]);
		#get and escape topic_solution value
		topic_solution = utility.escape(\
			request.getlist(key_solution_textarea_name)[0]);
		#store topic_title,topic_solution as key,value pair in shelve file	
		utility.write_to_shelve_file(topic_title, topic_solution);
		#setup text to be used in sql insert syntax, 
		#	ie in insert...values("topic_title","topic_solution");
		columns.append('"' + topic_title + '"');
		columns.append('"' + topic_solution + '"');
	#compose sql insert syntax
	content = '(' + ','.join(columns) + ')';
	content = 'insert into howto.topics (title,solution) values ' + content + ';';
	
	#cursor.execute('select * from vad.contacts;');#returns number of rows found
	cursor.execute(content); # returns number of rows affected
	conn.commit();#ensure changes made in actual database
	cursor.close();
	conn.close();#clean up
except Exception as err:
	(excType, excDetail, traceback) = sys.exc_info();
	content = 'ExceptionType: {:}\nExceptionDetail: {:}\n'\
		.format(excType, excDetail);
	content = err.__str__();	
	if conn:
		conn.close();

#store_key_value(str(cgi.escape(content)), 'sql execute query');#ok

print('Content-Type: text/plain; charset=utf-8\n\n');

#print(request.getlist('topic_title'));
#print( request['topic_title'] );
print(content);
print(utility.escape( content) );
print(request);



