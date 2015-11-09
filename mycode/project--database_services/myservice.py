#!/usr/bin/env python3
#Author:  Vaddanak Seng
#Filename:  myservice.py
#Purpose:  To provide convenient, full service to "upper layer" gui application.

"""
Module provides MySQL services.


QUESTION OR CONCERN TO AUTHOR:
(If I overlook anything, please indicate it in this section.)






FEATURES:
1. Validate data_dict keys and values are str-type?? 
2. Handle dangerous special chars like * or . for input and output ?? not 
needed except backspace
3. Fetch all db row data 						DONE
4. Fetch criteria-based row data, ie search		DONE
5. Remove row data								DONE
6. Edit/update row data							DONE
7. Remove table columns							DONE


NOTES:
1. Returned row data is a tuple of dict-type.  Each dict is a row data.  This
	tuple of dict should not be modified by the user because it represents
	previous data.  So, when user needs to remove a row data or update row data,
	the user can pass this previous dict as an argument for the method parameter
	for old data.
2.  Column 'id' must be present and is created automatically.  Column 'id'
	cannot be added or removed by user.	
3.  The column names and values must be str-type.
4.  All methods will raise exception if error happens.  Upper layer application
	will have flexible to react as appropriate.


TEST CASE:
Create a connection to MySQL Server and also create database 'service_db' 
and create table 'contacts_table' using constructor
>>> service = Service(host='localhost', username='root', password='', \
database_name='service_db', table_name='contacts_table')
	
Remove database 'service_db'
>>> service.remove_database()

OR

Create a connection to MySQL Server...
>>> service = Service(host='localhost', username='root', password='')

and then, reuse connection to create database 'service_db' and 
table 'contacts_table'
>>> service.use_database('service_db')
>>> service.use_table('contacts_table')

Add row data using dict-type object and table column automatically created
using dict keys.  Dict object keys and values must be str-type.
>>> entry1 = {'firstname':'Vad', 'lastname':'Student1', \
'address':'123 USF Drive', 'city':'Tampa', 'state':'Florida', \
'zip_code':'35592', 'phone':'999-999-9999', 'email':'abc@usf.com'}
>>> entry2 = {'firstname':'Justin', 'lastname':'Student2', \
'address':'456 Lake Road', 'city':'Lakeland', 'state':'Florida', \
'zip_code':'35875', 'phone':'999-999-9999', 'email':'just@microsoft.com'}
>>> entry3 = {'firstname':'Matt', 'lastname':'Student3', \
'address':'789 Orange Place', 'city':'Orlando', 'state':'Florida', \
'zip_code':'56852', 'phone':'999-999-9999', 'email':'matter@usf.com'}
>>> entry4 = {'firstname':'Sean', 'lastname':'Student4', \
'address':'159 Palm Drive', 'city':'Tampa', 'state':'Florida', \
'zip_code':'35592', 'phone':'999-999-9999', 'email':'see@google.com'}
>>> service.add_rowdata(entry1)
>>> service.add_rowdata(entry2)
>>> service.add_rowdata(entry3)
>>> service.add_rowdata(entry4)

Fetch all row data.  Returned value is tuple of dict-type objects, where each
object is a row data.
>>> data = service.fetch_rowdata_all()
>>> len(data)
4

Fetch row data based on search criteria, which can be a regular expression.
Search criteria argument must be dict-type where key is str-type
column name and value is search criteria.  Regular expression string must be
raw string, like r'search criteria'

Here, user search for row data based on email criteria.
>>> criteria1 = {'email':r'[-\d\w]+@google\.(?:com|net|org)(?i)'}
>>> data = service.fetch_rowdata_criteria_and(criteria1)
>>> len(data)
1
>>> data[0]['email'], data[0]['address']
('see@google.com', '159 Palm Drive')

Here, user search in two fields, email and address.  User has the option to
obtain only row data where both field criteria match or where either field
criteria match.
>>> criteria2 = {'email':r'[-\d\w]+@google\.(?:com|net|org)(?i)', \
'address':r'^\d*5\d* .*$'}

>>> data = service.fetch_rowdata_criteria_or(criteria2)
>>> len(data)
2

>>> data = service.fetch_rowdata_criteria_and(criteria2)
>>> len(data)
1
>>> data[0]['email'], data[0]['address']
('see@google.com', '159 Palm Drive')

User can update current row data.  New, non-existing column can be included.
>>> entry5 = {'firstname':'Sean', 'lastname':'Student4', 'gender':'male', \
'address':'800 Palm Drive', 'city':'Tampa', 'state':'Florida', \
'zip_code':'35592', 'phone':'999-999-9999', 'email':'see@gmail.com'}
>>> service.update_rowdata(data[0], entry5)

User can add new row data.
>>> service.add_rowdata(entry4)
>>> data = service.fetch_rowdata_all()
>>> len(data)
5

User can sort the tuple of rowdata.
>>> data = service.sort_rowdata(data, ['firstname', 'lastname', 'email'])

>>> tuple(((rowdata['firstname'],rowdata['email']) for rowdata in data))
(('Justin', 'just@microsoft.com'), ('Matt', 'matter@usf.com'), ('Sean', 'see@gmail.com'), ('Sean', 'see@google.com'), ('Vad', 'abc@usf.com'))


User can remove row data.
>>> service.remove_rowdata({'firstname':'sean', 'lastname':'Student4'})
>>> data = service.fetch_rowdata_all()
>>> len(data)
3

User can remove table column. 
Note: add new column is automatic whenever adding
or updating rowdata that includes new columns.
>>> len(service.column_names)
10
>>> service.remove_column(['gender'])
>>> len(service.column_names)
9

User can access instance variables.
>>> service.host
'localhost'
>>> service.username
'root'
>>> service.password
''
>>> service.database_name
'service_db'
>>> service.table_name
'contacts_table'

Remove current database.
>>> service.remove_database()

"""

import sys
import re
import pymysql


class InvalidRE(Exception): pass
class GhostColumn(Exception): pass
class QueryFail(Exception): pass

class Service:
	"""
	Provides MySQL database services.
	
	self.__columns contains column names in active database
	
	"""
	def __init__(self, host='localhost', username='root', password='', 
				 database_name='', table_name=''):
		self.__host = host
		self.__username = username
		self.__password = password
		self.__database_name = database_name
		self.__table_name = table_name
		
		self.__connection = None
		try:
			self.__connection = pymysql.connections.Connection(
				host=self.host, user=self.username, password=self.password)
			
			#cursor = self.connection.cursor()
			
			#cursor.execute('use vadx;')
			
			self.use_database(database_name)
			self.use_table(table_name)
			
			#self.check_columns(['hi','joe', 'id'])
			
			#self.add_rowdata({'a':'dog place', 'b':'bird cage', 
			#	'c':'happy holiday'})
			
			#self.remove_column(['id','hi','joe'])
			
			#self.remove_rowdata({'id':'26'})
			
			#print(self.fetch_rowdata_all())
			
			#result = self.fetch_rowdata_criteria_and_or(
			#	{'a':'apple', 'b':'juice'}, is_and=False, is_or=True
			#)			
			#print(len(result))
			#print(result)
			
			#print('column_names ->',self.column_names)
				
		except (Exception,) as err: #unknown error
			print('IN __init__: ', sys.exc_info()) # -> (type, value, traceback)
			raise
			
	def sort_rowdata(self, rowdata_dict_returned_from_fetch, 
		columns_order_to_sort):
		"""
		Sort tuple of dict-type based on user-specified list of columns.
		
		rowdata_dict_returned_from_fetch is a sequence of dict-type, where
		each dict-type represents a row data.  keys and values are str-type.
		
		columns_order_to_sort is a sequence of column names that will be used
		to prioritize sorting.  For example, sorting is based first on
		columns[0] and if there's a tie, then columns[1] will break the tie,
		and so on.
		
		Fn returns a new, sorted tuple.
		"""
		try:
			rowdata = list(rowdata_dict_returned_from_fetch)
		
			def sorting_item(item_dict):
				return tuple((item_dict[column] for column in columns_order_to_sort 
					if column in item_dict))
			
			#rowdata.sort(key=sorting_item)
			rowdata.sort(key=lambda item_dict: tuple((item_dict[column] 
				for column in columns_order_to_sort if column in item_dict)) )
		
		except:
			print('IN sort_rowdata: ', sys.exc_info() )
			raise
		
		return tuple(rowdata)
			
			
	def update_rowdata(self, rowdata_dict_to_be_updated, new_rowdata_dict):
		"""
		Update the given old row data to the given new row data.
		
		The old rowdata must be the original, un-modified rowdata that was
		obtained using the fetch_* methods.
		The new rowdata may have new columns, that is, not currently present
		in database.		
		
		"""
		try:
			self.__check_columns(new_rowdata_dict.keys())
			with self.connection.cursor() as cursor:
				criteria = ['{0} = {1}'.format(str(key), 
					repr(str(rowdata_dict_to_be_updated[key]))) for key in
					rowdata_dict_to_be_updated]
				sql = 'select id from {0}.{1} where {2};'.format(
					self.database_name, self.table_name, ' and '.join(criteria) )
				#print(sql)		
				cursor.execute(sql)	#find match		
				if len(list(cursor)) == 1: #a row data match is found			
					criteria = ['{0} = {1}'.format(str(key), 
						repr(str(new_rowdata_dict[key]))) for key in 
						new_rowdata_dict if key!='id']						
					sql = 'update {0}.{1} set {2} where id = {3};'.format(
						self.database_name, self.table_name, 
						', '.join(criteria), rowdata_dict_to_be_updated['id'])
					#print(sql)
					cursor.execute(sql)
					self.connection.commit()
					#print(cursor.__dict__)
		except:
			print('IN update_rowdata: ', sys.exc_info() )
			raise
			
	def remove_rowdata(self, rowdata_dict):
		"""
		Remove a row data from database table.
		
		rowdata_dict is a dict-type.  keys and
		values are str-type.  keys can be any number of existing column names.
		Match is found when all field criteria exactly match, except it is
		not case sensitive.
		
		All matching row data will be removed.
		
		"""
		try:
			with self.connection.cursor() as cursor:
				criteria = ['{0} = {1}'.format(str(key), 
					repr(str(rowdata_dict[key]))) 
					for key in rowdata_dict]
				sql = ('delete from {0}.{1} where {2};'
					.format(self.database_name, self.table_name, 
					' and '.join(criteria) ) )
				#print(sql)
				cursor.execute(sql)
				self.connection.commit()
		except:
			print('IN remove_rowdata_flex: ', sys.exc_info() )	
			raise
			
	'''		
	def remove_rowdata(self, rowdata_dict_to_be_removed):
		"""
		Remove a row data from database table.
		
		rowdata_dict_to_be_removed is a dict-type with previous data.
		If remove attempt failed, fn will not re-raise.
		"""
		try:
			with self.connection.cursor() as cursor:
				sql = ('delete from {0}.{1} where id={2};'
					.format(self.database_name, self.table_name,
					rowdata_dict_to_be_removed['id']) )
				cursor.execute(sql)
				self.connection.commit()
		except:
			print('IN remove_rowdata: ', sys.exc_info() )		
	'''		
	
	def fetch_rowdata_all(self):
		"""
		Fetch all db row data stored as tuple of dict.
		
		Fn returns all db row data stored in a tuple of dict.  Each tuple item
		is a dict-type, which represents a row data.  Key of dict is table 
		column name and value of dict is value.  
		
		"""		
		try:
			data = []
			with self.connection.cursor() as cursor:
				sql = 'select * from {0}.{1};'.format(self.database_name,
					self.table_name)
				cursor.execute(sql)
				#print(cursor.fetchall()) #-> tuple of tuple items
				column_names = self.column_names
				for rowdata in cursor: # rowdata is an n-tuple
					data.append({key:str(value) for key, value in 
						zip(column_names, rowdata)} )
						
		except:
			print('IN fetch_rowdata: ', sys.exc_info())
			raise
				
		return tuple(data)
		
	def fetch_rowdata_criteria_and(self, search_criteria_dict=None):
		return self.fetch_rowdata_criteria_and_or(search_criteria_dict,
			is_and=True, is_or=False)
		
	def fetch_rowdata_criteria_or(self, search_criteria_dict=None):
		return self.fetch_rowdata_criteria_and_or(search_criteria_dict,
			is_and=False, is_or=True)
		
	def fetch_rowdata_criteria_and_or(self, search_criteria_dict=None, 
		is_and=True, is_or=False):
		"""
		Fetch all row data that matches the search criteria.
		
		The key for search_criteria_dict is the column name.  The value is
		the search expression.  Regular expression will work.
		If column name not exist in db, then raise exception.
		If regular expression syntax is invalid, then raise exception.
		is_and indicates each search criteria must match.
		is_or indicates at least one search criteria must match.
		
		If using regular expression, make sure you pass in the regular 
		expression using the raw string, like this r'search critera'
		
		"""
		data = self.fetch_rowdata_all() # tuple of dict
		if not search_criteria_dict: return tuple(data)
		result = []
		
		try:
			#check search column names exist in database table
			column_names = self.column_names
			for search_field in search_criteria_dict:
				if search_field not in column_names:
					raise GhostColumn('Column name "{0}" not exist!'.
						format(search_field) )
			#check each regular expression
			for search_field, search_exp in search_criteria_dict.items():
				search_criteria_dict[search_field] = re.compile(search_exp)
			
			#search each row
			for rowdata in data:
				status = []
				for search_field in search_criteria_dict:
					if (search_criteria_dict[search_field].
						search(str(rowdata[search_field])) ):
						status.append(True)
					else:
						status.append(False)
				if is_and and all(status):
					result.append(rowdata)
				elif is_or and any(status):
					result.append(rowdata)
				
		#except sre_constants.error as err: #what module is it located?
		#	print('IN fetch_rowdata_criteria_and_or:', err)
		#	raise InvalidRE(search_exp)
		except:
			print('IN fetch_rowdata_criteria_and_or:', sys.exc_info() )
			raise
			
		return tuple(result)
		
	def remove_database(self):
		"""
		Delete database but only the current db created by the user.
		"""
		#if database_name != self.database_name:
		#	return None
		try:
			with self.connection.cursor() as cursor:
				sql = 'drop database if exists {0};'.format(self.database_name)
				cursor.execute(sql)
				self.connection.commit()
		except:
			print('IN delete_database: ', sys.exc_info() )	
			raise	
			
	def remove_column(self, column_names):
		"""
		Remove columns from database table.
		
		column_names is a list of column names of str-type.  
				
		Column id cannot be removed.
		"""
		try:
			with self.connection.cursor() as cursor:
				temp = ['drop column ' + x for x in column_names 
					if x!='id']
				#can't use 'if exists' but ok to drop non-existing column
				sql = 'alter table {0}.{1} {2};'.format(self.database_name,
					self.table_name, ', '.join(temp) )
				
				#print(sql)
				cursor.execute(sql)
		except:
			print('IN remove_column: ', sys.exc_info() )
			raise		
			
	def add_rowdata(self, data_dict):
		"""
		Insert data into database, as a row in table.
		
		data_dict is dict-type.  keys are actual column names and values are
		data for column.  If submitted column not in db, then it is created.
		keys and values are expected to be str-type.
		
		If data fail to add to db, then exception is re-raise to caller.
		
		ISSUE: should keys and values string be suspect to contain 'dangerous'
		special characters?  If so, should be substitue with equivalent like
		unicode identifiers?
		"""
		self.__check_columns(data_dict.keys()) #create column for each key
		
		keys = []
		values = []
		for key, value in data_dict.items():
			keys.append(str(key)) #what about special char? substitute?
			values.append(repr(str(value))) #same issue?
			
		sql = 'insert into {db}.{0}({1}) values({2});'.format(self.table_name,
			', '.join(keys), ', '.join(values), db=self.database_name )
		
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(sql)
				self.connection.commit()
		except:
			print('IN add_row_data: ', sys.exc_info())
			raise
		
		#print(sql)
		
	def __check_columns(self, column_list):
		"""
		Create column in column_list if it is not present in database.
		
		Method re-raise exception to caller if error occurred while adding
		column.
		
		Column name 'id' cannot be added.
		"""
		self.column_names #get current column name list
		with self.connection.cursor() as cursor:
			for column in set(column_list):
				if (column.lower() not in self.__columns and 
					column.lower()!='id'):
					try:
						cursor.execute('alter table {0}.{1} add column '
							'{2} text;'.format(self.database_name, 
							self.table_name, column) )
					except:
						print('IN check_columns: ', sys.exc_info())
						raise
						
	def __update_columns(self):
		"""
		Update column list with current database columns.
		
		Column list holds lowercase version of column names in database.
		"""
		with self.connection.cursor() as cursor:
			try:
				cursor.execute('select * from {0}.{1};'
					.format(self.database_name, self.table_name) )
					
				self.__columns = [x[0].lower() for x in 
					cursor.__dict__['description']]	
				#print(cursor.__dict__['description'])	#->
				'''
				(('id', 3, None, 11, 11, 0, False), 
				('zip_code', 252, None, 65535, 65535, 0, True), 
				('email', 252, None, 65535, 65535, 0, True), 
				('firstname', 252, None, 65535, 65535, 0, True), 
				('city', 252, None, 65535, 65535, 0, True), 
				('phone', 252, None, 65535, 65535, 0, True), 
				('lastname', 252, None, 65535, 65535, 0, True), 
				('state', 252, None, 65535, 65535, 0, True), 
				('address', 252, None, 65535, 65535, 0, True))
				'''
				#print(self.__columns)
			except:
				#failed to read database column names
				print('IN update_columns: ', sys.exc_info() )
				raise
				
	@property
	def column_names(self):
		self.__update_columns()
		return self.__columns							
	
	def use_database(self, database_name='contact_db'):
		"""
		Attempt to make database database_name active.
		
		If database_name exists, then set it to be current active.
		If database_name does not exist, then create it and make it active.
		If database_name cannot be used or created, then exception is raised
		and must be caught by caller to signal that database is not 
		available.
		"""		
		self.__database_name = (database_name if database_name
			else 'contact_db')
		try:
			with self.connection.cursor() as cursor:
				try:
					#use an existing database
					cursor.execute('use ' + self.database_name + ';')
				except pymysql.err.InternalError as err:
					#database_name does not exist
					try:
						cursor.execute('create database if not exists {0}; '
							'use {0};'.format(self.database_name) )
					except pymysql.err.ProgrammingError as err:
						#database_name cannot be created
						#print('IN DEEP use_database:', sys.exc_info())
						print(err)
						raise
		except:
			#print('IN use_database:', sys.exc_info())
			print('IN use_database: Failed to access database: {0}'
				.format(self.database_name) )
			raise
			
	def use_table(self, table_name='contacts'):
		"""
		Attempt to access or create table; retrieve and store column names.
		
		Checks if table exists.  If table does not exist, then attempt to create
		table.  If failed to create table, then raise exception to caller to
		signal that table is not available.
		
		Retrieves table column names and store in private variable 
		self.__columns.
		"""
		self.__table_name = table_name if table_name else 'contacts'
		try:
			with self.connection.cursor() as cursor:
				try:
					#check if table exist in db; better way to do this???
					cursor.execute('select * from {0}.{1};'
						.format(self.database_name, self.table_name) )
						
					#self.__columns = [x[0].lower() for x in 
					#	cursor.__dict__['description']]	
					#print(cursor.__dict__['description'])	
					#print(self.column_names)
				except pymysql.err.ProgrammingError as err:
					#table does not exist, so create it
					try:
						cursor.execute('create table if not exists '
							'{0}.{1} (id int not null '
							'auto_increment primary key);'
							.format(self.database_name, self.table_name) )
					except pymysql.err.ProgrammingError as err:
						#fail to create table
						print(err)
						raise
		
		except:
			#print('IN use_table: ', sys.exc_info())
			print('Failed to access table: {0}.{1}'.
				format(self.database_name, self.table_name) )
			raise		
	
	def __del__(self):
		if self.connection is not None:
			self.connection.close()			
	
	@property
	def host(self):
		return self.__host
	
	@property
	def username(self):
		return self.__username
		
	@property
	def password(self):
		return self.__password	
		
	@property
	def database_name(self):
		return self.__database_name
		
	@property
	def table_name(self):
		return self.__table_name	
		
	@property
	def connection(self):
		return self.__connection	
	
	
	
	


#service = Service()


#print(service.username, service.table_name)				
				
if __name__ == '__main__':
	import doctest
	doctest.testmod()				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
