#!/usr/bin/python3

from __future__ import print_function;

import cgi, cgitb; cgitb.enable();

import utility;
import pymysql;

"""
CAUTION:
This line is required:	#!/usr/bin/python or #!/usr/bin/python3
Otherwise, client-side, in browser console complains:
	POST http://localhost:8084/cgi-bin/howto.py 500 (Internal Server Error)
	
CAUTION:	
This line is required inorder to GET/POST using ajax with data.  If
ajax data is omitted, then not required.

	$.ajax({
		method: "POST",
		url: "cgi-bin/howto.py",
		//data: "action=get_topic_titles_xml", //ajax data omitted
		dataType: "text",	
		success: function(data, status, xhr) {
			$("#showme").text(status);
		}		
	});
However, if ajax data is sent, then "request = cgi.FieldStorage();" statement is
required to prevent error on client-side, in browser console:
	POST http://localhost:8084/cgi-bin/howto.py net::ERR_EMPTY_RESPONSE
	
	
"""
#print(request) -> 
#FieldStorage(None, None, [MiniFieldStorage('action', 'get_topic_titles_xml')])
#print(request['action']) -> MiniFieldStorage('action', 'get_topic_titles_xml')
client_request = cgi.FieldStorage();
action = client_request.getlist("action")[0].strip();

actions = {};
actions[0] = "get_topic_titles_xml";
actions[1] = "get_topic_solution";
actions[2] = "delete_topic_entry";


if action==actions[0]:
	#<topics><topic><title>some title</title></topic></topics>
	result = utility.compose_titles_xml(); #contains titles
	#<topics><topic><title>..</title><solution>..</solution></topic></topics>
	#result = utility.compose_xml(); #contains title and solution
elif action==actions[1]:	
	result = client_request.getlist("topic_title")[0];
	(key,result) = utility.read_from_shelve_file(utility.escape(result));
elif action==actions[2]:
	title = client_request.getlist("topic_title")[0];
	#delete from shelve file
	result = utility.remove_entry(utility.escape(title));
	#delete from MySQL; put this in separate module !
	conn = pymysql.connect(host="localhost", user="root", password="");
	cursor = conn.cursor();
	select_sql = "select title from howto.topics where title='" \
		+ utility.escape(title) + "';";
	result = cursor.execute(select_sql);
	if result:
		delete_sql = "delete from howto.topics where title='" \
			+ utility.escape(title) + "';";
		result = cursor.execute(delete_sql);
		conn.commit();
	conn.close();

print("Content-Type: text/plain; charset=utf-8");
print();
print();
print(result);


















