#!/usr/bin/env python3

"""
Author:  Vaddanak Seng
Purpose:  Extract data from large file and insert into database

"""

import re
import os
import sys



heavy_check_mark = '\u2714'
large_circle = '\u25EF'

line_text_pattern = re.compile(r'(?P<key>[^\t]+)\t+(?P<value>[^\t]+)')

def load_column_definition_section():
	'''
	Read file parameters and load column definition into dictionary.
	Key is column name.  Value is column defintion.
	
	Return:  dict containing column_name:column_definition as key:value pairs
	'''
	parameter_filename = 'parameters'
	parameter_section = '[SECTION5]'
	
	#pattern = re.compile(r'(?P<column>\w+)\t+(?P<def>[a-zA-Z].*)')
	pattern = re.compile(r'^(?P<column>[^\t]+)\t+(?P<def>[^\t]+)')
	
	storage = {}
	
	with open(parameter_filename) as foo:
		for line in foo:
			if parameter_section == line.strip(): #section found
				for line in foo: #iterate over desired section
					line = line.strip()
					if not line or '#' == line[0]: #line is empty or comment
						continue
					elif '[' == line[0]: #start of next section
						break
					else: #content of desired section
						mo = pattern.match(line)
						if mo: #match found
							storage[mo.group('column')] =mo.group('def').strip()
						else: #NOT match
							print('[load_column_definition] match failed:',line)
				break #done with desired section
	#print(len(storage))			
	return storage
	
def load_table_column_names_section():
	'''
	Load table name and associated column names into dict.
	
	Return: dict with table_name:list_of_column_names as key:value pairs.
	'''	
	parameter_section = '[SECTION3]'	
	#po = re.compile(r'(?P<table_name>\w+)\t+(?P<column_names>\w.*)')
	po = re.compile(r'^(?P<table_name>[^\t]+)\t+(?P<column_names>[^\t]+)')
	storage = {}
	lines = get_section_content(parameter_section)
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[mo.group('table_name')] = \
				mo.group('column_names').strip().split(', ')
		else:
			print('[laod_table_column_names] unknown match:', line)
	#print(len(storage), storage)		
	return storage
	
def load_general_section():
	'''
	Load content in general section.
	
	Return: dict with key:value pairs.
	'''
	parameter_section = '[SECTION1]'
	storage = {}
	lines = get_section_content(parameter_section)
	#po = re.compile(r'(?P<key>\w+)\t+(?P<value>\w.*)')
	po = re.compile(r'^(?P<key>[^\t]+)\t+(?P<value>[^\t]+)')
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[mo.group('key')] = mo.group('value')
		else:
			print('[load_general_section] unknown:', line)
	return storage
	
def load_data_location_section():
	'''
	Load section with location to data files.
	
	Return: dict fda_dir_root:path_to_data_txt_filenames pairs
	'''
	parameter_section = '[SECTION4]'
	#po = re.compile(r'(?P<key>\w+)\t+(?P<path>\w.*)')
	po = re.compile(r'^(?P<key>[^\t]+)\t+(?P<path>[^\t]+)')
	storage = {}
	lines = get_section_content(parameter_section)
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[mo.group('key')] = mo.group('path')
		else:
			print('[load_data_location_section] unknown:', line)
	return storage

def load_alias_column_section():
	'''
	Load section 6 which contains mapping of column name alias to preferred
	column name.
	
	Different ascii data files have more, less, or different column names as
	compared to the latest data file.  This information allows mapping of 
	various possible column names to a single column name which was chosen to
	make MySQL table.
	
	Return: dict with alias_column_names_tuple:MySQL_column_name pairs
	'''
	parameter_section = '[SECTION6]'
	lines = get_section_content(parameter_section)
	po = re.compile(r'^([^\t]+)\t+([^\t]+)$')
	storage = {}
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[tuple([x.strip() for x in mo.group(1).strip().split(', ') \
				if x])] = mo.group(2).strip()
	return storage
	
def load_alias_column_section2():
	'''
	Load section 6 which contains mapping of column name alias to preferred
	column name.
	
	Different ascii data files have more, less, or different column names as
	compared to the latest data file.  This information allows mapping of 
	various possible column names to a single column name which was chosen to
	make MySQL table.
	
	Return: dict with alias_column_name:MySQL_column_name pairs
	'''
	parameter_section = '[SECTION6]'
	lines = get_section_content(parameter_section)
	po = re.compile(r'^([^\t]+)\t+([^\t]+)$')
	storage = {}
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[mo.group(1).strip()] = mo.group(2).strip()
	return storage	
	
def load_check_duplicate_field_section():
	'''
	
	'''
	parameter_section = '[SECTION7]'
	lines = get_section_content(parameter_section)
	storage = {}
	po = re.compile(r'^(?P<table>[^\t]+)\t+(?P<columns>[^\t]+)$')
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[mo.group('table')] = mo.group('columns').strip().split(', ')
	return storage
	
def load_table_prefixes():
	'''
	Table prefix used in first part of ascii data file names.
	
	RETURN: dict of table_name:list_of_prefixes pairs
	'''
	parameter_section = '[SECTION2]'
	lines = get_section_content(parameter_section)
	po = re.compile(r'^(?P<table_name>[^\t]+)\t+(?P<prefixes>[^\t]+)')
	store = {}
	for line in lines:
		mo = po.match(line)
		if mo:
			store[mo.group('table_name')] = [x.strip() for x in 
				mo.group('prefixes').strip().split(', ')]	
	return store
	#ie {'reaction': ['reac'], 'outcome': ['outc'], 'therapy': ['ther', 'xxx'], 'indication': ['indi'], 'report_sources': ['rpsr'], 'demographic': ['demo'], 'drug': ['drug']}		
	
	
def load_db_connection_section():
	'''
	
	'''
	parameter_section = '[SECTION10]'
	lines = get_section_content(parameter_section)
	storage = {}
	po = re.compile(r'^(?P<key>[^\t]+)\t+(?P<value>[^\t]+)$')
	for line in lines:
		mo = po.match(line)
		if mo:
			storage[mo.group('key')] = mo.group('value')
	if 'password' not in storage and 'passwd' not in storage:
		storage['passwd'] = ''
				
	return storage
	
def get_quarter_to_data_filenames_dict():
	'''
	Store key:value pairs in dict where key is the FDA quarterly directory name 
	and value is a list of qualified ascii data filenames located in the 
	directory.
	'''
	general = load_general_section()
	location = load_data_location_section()
	storage = {}
	for e in location:#ie e --> faers_ascii_2015q4
		#ie DATA_FILES/faers_ascii_2015q4/ascii/
		path = re.sub('base_data_dir', general['base_data_dir'], location[e])
		storage[e] = []
		try:
			for x in os.listdir(path):
				if os.path.splitext(x.lower())[1] == '.txt':
					storage[e].append(os.path.join(path, x))
		except (FileNotFoundError) as err:
			print('[get_quarter_to_data_filenames_dict] Error, make sure {} '
				'exists \n{}'.format(path, err) )
		except:
			print('[get_quarter_to_data_filenames_dict] Unknown error')
			raise
		storage[e].sort()	
	#print(storage)	
	return storage
	
def get_table_name(ascii_data_filename):
	'''
	Determine table name associated with ascii data filename.
	
	Return: Table name or None
	'''
	ascii_data_filename = os.path.basename(ascii_data_filename)
	
	#map table name to possible prefix (ie as found in ascii data filename)
	tables = load_table_prefixes()
	'''
	tables = {
		'reaction':('reac',),
		'outcome':('outc',),
		'report_sources':('rpsr',),
		'demographic':('demo',),
		'drug':('drug',),
		'therapy':('ther', 'xxx'),
		'indication':('indi',)
	}
	'''
	
	for table_name in tables:
		for prefix in tables[table_name]:
			#po = re.compile(r'^{}'.format(prefix))
			po = re.compile(r'{}'.format(prefix))
			#mo = po.match(ascii_data_filename.lower())
			mo = po.search(ascii_data_filename.lower())
			if mo:
				return table_name
	print('[get_table_name] fail to match table name to file {}'
		.format(ascii_data_filename) )
	return None #fail to associate table name to passed in filename
	


def get_section_content(section):
	'''
	Read file parameters and extract content of specified content without
	comment lines or empty lines.
	
	Return:  List of lines of text.
	'''	
	parameter_filename = 'parameters'
	lines = []
	with open(parameter_filename) as foo:
		for line in foo: # iterate over file
			if section == line.strip(): # found specified section
				for line in foo: # iterate over specified section
					line = line.strip()
					if not line or '#'==line[0]: # ignore empty or comment line
						continue
					elif '['==line[0]: # reached beginnning of next section
						break
					else: # content of specified section
						lines.append(line)
				break
	#print(len(lines))
	#print(lines)
	return lines		
				
	
def check_table_column_compatibility():
	'''
	All tables and columns must match.
	
	Return:  False if match check failed.
	'''		
	#Map table name to expected prefix of ascii data filenames
	#ie prefix 'ther' corresponds to ascii data filename 'ther12q4.txt'
	table_prefixes = load_table_prefixes()
	'''
	table_prefixes = { 
		'therapy':['ther'],
		'indication':['indi'],
		'drug':['drug'],
		'demographic':['demo'],
		'reaction':['reac'],
		'outcome':['outc'],
		'report_sources':['rpsr','xxxx'] }
	'''	
	
	#ie {('ther',): 'therapy', ('reac',): 'reaction', ...}	
	prefix_to_table = {tuple(table_prefixes[k]):k for k in table_prefixes}	
	#print(prefix_to_table)
		
	#Collect all prefixes into a list; extract values from table_prefixes
	#ie ['indi', 'rpsr', 'xxxx', 'ther', 'outc', 'drug', 'reac', 'demo']	
	prefixes = []
	for x in table_prefixes.values():
		prefixes += x				
		
	#dictionaries of parameters	
	#ie {..., 'data_dir': 'ASCII_DATA_FILES', 'base_data_dir': 'DATA_FILES'}
	general = load_general_section()
	
	#ie {'faers_ascii_2015q4': 'base_data_dir/faers_ascii_2015q4/ascii/', ...}
	location = load_data_location_section()
	
	#table name mapped to column names; table:columns pairs
	table_columns = load_table_column_names_section()
	
	#dict with tuple_alias_columns:MySQL_column pairs
	alias_columns = load_alias_column_section() #ie {('gndr_cod',): 'sex'}
	
	#print(general)
	#print(location)
	#print(table_columns)
		
	#iterate over dir entries in base_data_dir
	#ie ['faers_ascii_2012q4', 'faers_ascii_2015q4', ...]
	for e in os.listdir(general['base_data_dir']):		
		print('======================================================')
		#obtain path to ascii data file for specific FDA quarterly data
		#ie DATA_FILES/faers_ascii_2015q4/ascii/
		try:
			path = (re.sub('base_data_dir', general['base_data_dir'], 
				location[e]))
		except:
			print('Check SECTION4 in parameters file, make sure it'
				' contains line for "{}"'.format(e) )
			#print(sys.exc_info()) # exc_info() -> (type, value, traceback)
			#raise
			continue
					
				
		#list of qualified filenames to ascii data files
		#ie ['DATA_FILES/faers_ascii_2015q4/ascii/DEMO15Q4.txt', ...]
		try:
			filenames = ['{}{}'.format(path,p) for p in os.listdir(path) if 
				os.path.splitext(p)[1]=='.txt']
		except:
			print('Check your filesystem to make sure that path "{}" exists'
				.format(path) )
			raise		
			
		#Make sure there are 7 data files correspdonding to 7 tables.
		filenamesLength = len(filenames)
		tablePrefixesLength = len(table_prefixes)
		if filenamesLength != tablePrefixesLength:
			print('[check_table_column_compatiblity] FAIL! Expected {} files. '
				'{} ascii data files found in {}'
				.format(tablePrefixesLength, filenamesLength, path) )
			return False
		else:
			print('OK. {} ascii data files found in {}\n'
				.format(tablePrefixesLength, path) )
			...
		
		prefixPattern = re.compile(r'^(?P<prefix>[A-Za-z]{4})')
							
		#iterate over each filename; num of iteration equals num of expected tables
		for i in range(tablePrefixesLength):
			#ie DATA_FILES/faers_ascii_2015q4/ascii/DEMO15Q4.txt
			#print(filenames[i])
			
			#prefix = (prefixPattern.match( os.path.basename(filenames[i]) )
			#	.group('prefix').lower())				
			mo = prefixPattern.match( os.path.basename(filenames[i]) )
			if not mo:
				print("[check_table_column_compatibility] FAIL!  prefix "
					"does not match expected pattern '{}' for file '{}'"
					.format(prefixPattern.pattern, filenames[i]) )
				return False
			else:
				prefix = mo.group('prefix').lower()
			
				
			
			#Make sure all expected data filenames exist	
			if prefix not in prefixes:
				print('[check_table_column_compatiblity] FAIL! '
					'Unknown prefix "{}" for file {}'
					.format(prefix, filenames[i]) )
				return False
			else:
				print('OK. Prefix "{}" matches data file {}'
					.format(prefix, filenames[i]))
				...	
				
			#Get headers located in first line of ascii data file
			headers = None
			with open(filenames[i]) as foo:
				headers = foo.__next__().strip()
				
			if headers:
				headers = [x.strip().lower() for x in headers.split('$')]
				headers.sort()
			else:
				print('[check_table_column_compatiblity] FAIL! '
					'headers is None for file {}'.format(filenames[i]))
				return False	
					
			#Get table name by looking up prefix in prefix_to_table dict	
			table_name = None
			for key in prefix_to_table:
				if prefix in key:
					table_name = prefix_to_table[key]
					break #skip 'else' block
			else:
				print('[check_table_column_compatiblity] FAIL! '
					'prefix "{}" not match known table names, for file {}'
					.format(prefix, filenames[i]) )
				return False						
			
			
			#Make sure each ascii data file contains expected columns	
			expected_columns = table_columns[table_name]
			expected_columns.sort()
			#if 'num' in expected_columns:
			#	expected_columns.remove('num') #not include 'num'
			
			#CAUTION: Check can still pass if fewer columns in header line 
			# of data file than expected columns.
			if len(headers) != len(expected_columns):
				print('CAUTION: There are {} columns in data file header'
					' but {} are expected.'
					.format(len(headers), len(expected_columns) ) )
			#what is the missing column??		
			set1 = set(headers)
			set2 = set(expected_columns)
			result = set1.difference(set2)			
			if result:
				print("WARNING. Column '{}' in data file header but"
					" not in standard"
					.format(', '.join(result)) )
			result = set2.difference(set1)
			if result:
				print("Column '{}' in standard but not in data file header"
					.format(', '.join(result)) )			
					
			
			for c in headers:
				if c not in expected_columns:
					print('WARNING. Column "{}" in data file header '
						'not recognized.'.format(c) )
					for alias in alias_columns:
						if c in alias:
							print('RECONCILE. Column "{}" is alias of "{}"'
								.format(c,alias_columns[alias]))
							break #skip 'else' block
					else:		
						print('[check_table_column_compatiblity] FAIL! '
							'column "{}" not recognized, for file {}, check'
							' alias SECTION6'
							.format(c, filenames[i]) )
						print('SUSPECT ', headers)	
						print('EXPECTED', expected_columns)	
						return False
					
			print('PASS. Column names in file {} are compatible with known columns'
				.format(filenames[i]) )
			print()

def show_data_file_info():
	'''
	Look for duplicate row data based on columns and tables specified in 
	SECTION7 and FDA quarters specified in SECTION4 of file parameters.
	
	'''	
	general = load_general_section() #section 1
	files = get_quarter_to_data_filenames_dict() #section 4
	dup_check = load_check_duplicate_field_section() #section 7
	alias = load_alias_column_section2() #section 6
	with open('duplicates', 'w') as dup_file:#create or empty file 'duplicates'
		...
	#ie e -> faers_ascii_2012q4
	for e in sorted(files.keys()):
		print('================== {} =================='.format(e) )
		#ie DATA_FILES/faers_ascii_2015q4/ascii/DEMO15Q4.txt
		for filename in sorted(files[e]):
			#get table name based on data filename		
			table_name = get_table_name(filename)
			#check if table name was selected in parameters file SECTION7
			if table_name not in dup_check:
				continue
				
			with open(filename) as foo:
				headers = []
				#get headers from data file, convert to MySQL if needed
				for x in foo.__next__().strip().split('$'):
					if x in alias: #header is a variant so use MySQL header
						headers.append(alias[x])
					else: #header same as MySQL header
						headers.append(x)
				
				#get list of fields that are used in duplicate row checking				
				check_fields = dup_check[table_name]				
				indices = []
				#get index numbers in headers that correspond to check_fields
				for x in check_fields:
					try:
						indices.append(headers.index(x))
					except ValueError:
						print('[show_data_file_info] column name {} is not '
							'found in header line of file {}'
							.format(x, filename) )
						continue
					except:
						print('[show_data_file_info] column name {} result in '
							'unknown error, associated with file {}'
							.format(x, filename) )	
						raise
				#indices is empty so we move on to next filename
				if not indices:
					continue
						
				indices.sort()
				#print(headers, check_fields, indices)
				uniques = set()
				duplicates = {}
				#data = []
				count = 0
				count_dup = 0
				dup = {}
				#get each data row (not include headers row)
				for x in foo:
					count += 1					
					row = [r.strip() for r in x.strip().split('$')]#data in list
					temp = []
					for i in indices:
						temp.append(row[i])#get field at preferred index
					#data.append(tuple(temp))#store data
					if tuple(temp) not in uniques:	
						uniques.add(tuple(temp))#add data if seen first time
					else: #duplicate found
						count_dup += 1
						if tuple(temp) in duplicates:
							duplicates[tuple(temp)] += 1#exist so increment
							if count_dup <= 5:
								dup[tuple(temp)] += 1
						else:
							duplicates[tuple(temp)] = 2#not exist so set 2
							if count_dup <= 5:
								dup[tuple(temp)] = 2
						
					'''			
					#Compose insert sql statement					
					if count <= 5:
						sql = ('INSERT INTO {}.{} ({}) VALUES ({});'
							.format(general['database_name'], table_name, 
							', '.join(headers), 
							', '.join(['"{}"'.format(x) for x in row]) ) )
						print(sql)
					else:	
						break
					'''
								
					#if count >= 5:#limit iteration for testing purposes
					#	break
			print('FILE: {}  ROWS: {}'.format(filename, count))
			print('Based on table: {}  columns: {}'
				.format(table_name, tuple(check_fields)) )
			#print('\tdata', data)
			#print('\tuniques', uniques)
			temp = ['{}: {}'.format(x, dup[x]) for x in dup]
			temp.sort()
			print('\tduplicates  {}'.format( ', '.join(temp) if temp else 'None') )
			
			with open('duplicates', 'a') as dup_file:
				print('FILE: {}  ROWS: {}'.format(filename, count), file=dup_file)
				print('Based on table: {}  columns: {}'
					.format(table_name, tuple(check_fields)), file=dup_file )
				temp = ['{}: {}'.format(x, duplicates[x]) for x in duplicates]
				temp.sort()
				print('\tduplicates  {}'
					.format( ', '.join(temp) if temp else 'None'),
					file=dup_file )
			
	print('Above are few sample results.  All duplicates are '
		'saved in file: {}'.format('duplicates') )			
				
	
def reconcile_columns_to_standard(table_name, suspect_list_of_columns, 
	verbose=False):
	'''
	Given a list of columns that belong to table_name, 
	find non-standard column name in list and
	match and replace with alias as specified in parameters file in section 6.
	
	Note that some data file have few columns than standard columns, ie those
	used in MySQL.  Columns in data file should match or have equivalent
	compatibility. 
	
	What about new column type?  Such column will be added as standard by
	adding it to parameters file in sections 3 and 5.
	
	RETURN: list of standardized column names
	'''
	standard = load_table_column_names_section()
	if table_name not in standard:	
		print('[reconcile_columns_to_standard] ERROR: '
			'Table "{}" is not recognized'
			.format(table_name) )
		return None
		
	standard = standard[table_name]
	alias = load_alias_column_section2()
	replace = False
	if verbose:
		print('BEFORE:', suspect_list_of_columns)
	for column in suspect_list_of_columns:		
		column = column.strip().lower()
		if column not in standard:
			if column in alias:
				print('{} Replacing column "{}" with "{}"'
					.format(large_circle, column, alias[column]) )
				suspect_list_of_columns[suspect_list_of_columns.index(column)] \
				= alias[column]
				replace = True
			else:
				print('[reconcile_columns_to_standard] ERROR: '
					'Column "{}" of table "{}" is not found as alias.  '
					'You will need to add'
					' it to section 6 of parameters file.'
					.format(column, table_name) )
				return None
	if not replace:
		print('{} All columns match standard columns'.format(heavy_check_mark))
	if verbose:		
		print('AFTER:', suspect_list_of_columns)
	return suspect_list_of_columns
	
def remove_shelve_files():
	'''
	Remove all files in directory SHELVE.
	'''
	
	general = load_general_section()
	
	for filename in os.listdir(general['shelve']):
		filename = '{}/{}'.format(general['shelve'], filename)
		if os.path.exists(filename):
			print('Removing file: {}'.format(filename) )
			os.remove(filename)

def remove_sql_files():
	'''
	Remove all files in directory SHELVE.
	'''
	general = load_general_section()
	
	po = re.compile(r'\.sql')
	
	for filename in os.listdir(general['sql']):
		mo = po.search(filename)
		if not mo:
			continue
		if not get_table_name(filename):
			continue	
		#if filename=='create_table.sql' or filename=='main.sql':
		#	continue
		filename = '{}/{}'.format(general['sql'], filename)
		if os.path.exists(filename):
			print('Removing file: {}'.format(filename) )
			os.remove(filename)		
	
	
def compose_insert_sql(limit=None, auto_proceed=False):
	'''
	Create insert sql statement for each row data in each table for each quarter.
	Maintain table info in shelve file.
	Create directory '.../istudy_large_files', if not exist, to store large
	files and avoid githud error.
	
	Maintain table information with following data structure:
	Stored in shelve, one for each table, ie 
	therapy: { 
	  'qualified_ascii_data_filename1\tqualified_sql_insert_filename1':
	  {	  		
	  		row_count: some_int,	  		
	  		ok_inserted_rows: set(insert_id,...),
	  		warning_inserted_rows: tuple((insert_id,insert_sql,line_number),...)
	  		failed_inserted_rows: tuple((insert_sql,line_number),...),	  		
	  		remove_sql_file_name: None
	  },
	  'qualified_ascii_data_filename2\tqualified_sql_insert_filename2': {..},
	  'qualified_ascii_data_filename3\tqualified_sql_insert_filename3': {..}, ...
	}

	indication: {...}

	
	RETURN: None.
	'''
	#import shelve
	import my_shelve
			
	
	#Get shelve file content
	store2 = my_shelve.read_from_shelve_file()		
	
	general = load_general_section()
	
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'db': 'faers'}
	args = load_db_connection_section()
	general['database_name'] = args['db']
		
	files = get_quarter_to_data_filenames_dict()
	keys = list(files)
	keys.sort()
	
	#escape_patt = re.compile(r'(\\)$')
	
	check_large_files_dir() #check and if necessary, create large files dir
	
	#Not need to remove shelve files after shelve data structure is defined.
	#remove_shelve_files() #remove shelve files; ??? remove in final version
	
	#Is this a good idea?
	#If remove sql file, then need to remove its shelve info?
	remove_sql_files()
	
	with open('{}/main.sql'.format(general['sql']), mode='w') as foo:
		print('SOURCE {};'.format('create_table.sql'), file=foo)
	
	for quarterly_dir in keys:
		print('================= {} ================='.format(quarterly_dir))
		for ascii_data_filename in files[quarterly_dir]:
			table_name = get_table_name(ascii_data_filename)
			counter = 0			
			#num = 0
			
			#Get header line and count number of row data in data file
			with open(ascii_data_filename) as foo:
				#get headers from data file
				headers = foo.__next__().strip()
				headers = [x.strip().lower() for x in headers.split('$')]				
				#convert to standard column names; count is same as original	
				headers = reconcile_columns_to_standard(table_name, headers)
				#count number of row data
				for _ in foo:
					counter += 1
					
			print('{} -> {} ({} columns, {} rows)'
				.format(ascii_data_filename, table_name, len(headers), counter))	
			
			#Compose filename for shelve; one per table, so will be 7 total			
			store_name = '{}/{}'.format(general['shelve'], table_name)
				
			#Check if quarterly dir that was split up
			is_split_dir = quarterly_dir == 'faers_ascii_2015q3b'	
				
			#Compose insert_sql_file_name
			insert_sql_file_name = ('{}/insert_{}{}.sql'.format(general['sql'], 
				os.path.splitext(os.path.basename(ascii_data_filename))[0],
				'b' if is_split_dir else '') )
			remove_sql_file_name = ('{}/remove_{}{}.sql'.format(general['sql'],
				os.path.splitext(os.path.basename(ascii_data_filename))[0],
				'b' if is_split_dir else '') )
			
			store_key = '{}\t{}'.format(ascii_data_filename, insert_sql_file_name)
			# ('DATA_FILES/faers_ascii_2014q1/ascii/DEMO14Q1.txt', 
			# '../istudy_large_files/SQL_FILES/insert_DEMO14Q1.sql')
			#print(store_key)
						
			#Compose sql and store in shelve
			with open(ascii_data_filename) as foo:
			
				#Store in shelve
				'''
				store = shelve.open(store_name)
				if store_key not in store:
					store[store_key] = {
						'row_count':0,
						'ok_inserted_rows':set(),
						'warning_inserted_rows':set(),
						'failed_inserted_rows':tuple(),
						'remove_sql_file_name':None }
				file_store = store[store_key]
				store.close()
				'''	
						
				store = store2[table_name]	
				if store_key not in store:
					store[store_key] = {
						'row_count':0,
						'ok_inserted_rows':set(),
						'warning_inserted_rows':tuple(),
						'failed_inserted_rows':tuple(),
						'remove_sql_file_name':None }		
				file_store = store[store_key]							
				
				#Update here???	
				#Check if insert sql was previously created and available	
				if counter==file_store['row_count'] and \
					counter==(len(file_store['ok_inserted_rows']) + \
					len(file_store['warning_inserted_rows'])):
					print('Insert sql for row data in {} is available.  Examine'
						' file {}\n'
						.format(ascii_data_filename, insert_sql_file_name) )
					user_input = input('Do you want to proceed? (y/n) ')
					if user_input != 'y':
						print('You chose to NOT proceed.')
						foo.close()						
						continue
					else:
						print('You chose to proceed.')	
						
					
				#Skip header line
				foo.__next__()
				#Allocate variables
				#data = [] #contains each row data for current data file
				#data_set = set() #contains 2-tuple (num,primaryid) for each row
				counter = 0
				
				primaryid_index = headers.index('primaryid')
				
				#Open file to write insert sql into
				foo_insert = open(insert_sql_file_name, mode='w')
				
				#Create insert sql for each row data
				for row_data in foo:
					#num += 1
					counter += 1					
					
					#Check if field contains single or double quote marks
					has_single_quote = False
					has_double_quote = False
					for e in row_data.strip().split('$'):
						if '\'' in e:
							has_single_quote = True
						if '\"' in e:
							has_double_quote = True
					
					#Split row data into list of fields
					#Some row data have escape char as solo or at end. So?
					row_data = ['{}'.format(x) 
						for x in row_data.strip().split('$')]
					for i in range(len(row_data)):
						if row_data[i] == '\\':
							row_data[i] = '\\\\'
						elif row_data[i] and row_data[i][-1] == '\\':
							row_data[i] = row_data[i] + '\\'	
										
							
					#dict contains {'headers':headers_list, 'data':data_list}
					temp = prune_columns(headers, row_data)	
					
					if has_double_quote:
						sql = '''INSERT INTO {}.{} ({}) VALUES ({});'''\
							.format(general['database_name'], table_name, \
							', '.join(temp['headers']), \
							', '.join(["'{}'".format(x) for x in temp['data']]) )
					else:
						sql = '''INSERT INTO {}.{} ({}) VALUES ({});'''\
							.format(general['database_name'], table_name, \
							', '.join(temp['headers']), \
							', '.join(['"{}"'.format(x) for x in temp['data']]) )		
					
										
					print(sql, file=foo_insert)
					
					
					if limit and counter >= limit: break
				
				#Finished with data file and so, update store				
				file_store['row_count'] = counter						
				file_store['remove_sql_file_name'] = remove_sql_file_name
				
				#store = shelve.open(store_name)
				#store[store_key] = file_store
				#store.close()
				
				store2[table_name][store_key] = file_store
				my_shelve.write_to_shelve_file(store2)
				
				#Close files				
				foo_insert.close()
				foo.close()
				
				#Append insert file to content of main.sql file
				with open('{}/main.sql'.format(general['sql']), mode='a') as foo:
					print('SOURCE {};'
						.format(os.path.basename(insert_sql_file_name)), 
						file=foo)
				
			print()
			
def prune_columns(headers, data):
	'''
	Remove column and data field that are blanks.
	'''
	store = {'headers':[], 'data':[]}
	
	for i in range(len(headers)):
		if data[i].strip():
			store['headers'].append(headers[i])
			store['data'].append(data[i])
	
	return store
	
def check_large_files_dir():
	'''
	Check if directories for large files exist and if not create them.
	'''
	general = load_general_section()
	
	if not os.path.exists(general['large_files']):
		os.mkdir(general['large_files'])
		print('Created {}'.format(general['large_files']))
		
	if not os.path.exists(general['sql']):
		os.mkdir(general['sql'])
		print('Created {}'.format(general['sql']))
		
	if not os.path.exists(general['shelve']):
		os.mkdir(general['shelve'])
		print('Created {}'.format(general['shelve']))
	
def compose_create_sql():
	'''
	Create sql to create database and tables.
	'''
	general = load_general_section()
	table_columns = load_table_column_names_section()
	column_def = load_column_definition_section()
	
	check_large_files_dir()
	
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'db': 'faers'}
	args = load_db_connection_section()	
	general['database_name'] = args['db']
	
	sql22 = ('DROP DATABASE IF EXISTS `{0}`;\n'
		'CREATE DATABASE `{0}` CHARACTER SET utf8;\n'
		'USE `{0}`;\n'
		.format(general['database_name']))
	print(sql22)	
	
	tables = list(table_columns)
	# ['demographic', 'drug', 'indication', 'outcome', 'reaction', 
	# 'report_sources', 'therapy']
	tables.sort()
	
	#Table 'demographics'
	defs = []
	for col in table_columns['demographic']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql0 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY (`num`, `primaryid`), KEY `primaryid` (`primaryid`) )"		
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[0], ', '.join(defs)) )	
	'''	
	sql0 = ("DROP TABLE IF EXISTS `{0}.{1}`;\n"
		"CREATE TABLE `{0}.{1}` ({2}, "
		"PRIMARY KEY (`num`, `primaryid`), KEY `primaryid` (`primaryid`), "
		"FOREIGN KEY (`primaryid`) REFERENCES `reaction` (`primaryid`), "
		"FOREIGN KEY (`primaryid`) REFERENCES `outcome` (`primaryid`), "
		"FOREIGN KEY (`primaryid`) REFERENCES `report_sources` (`primaryid`), "
		"FOREIGN KEY (`primaryid`) REFERENCES `drug` (`primaryid`) ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[0], ', '.join(defs)) )
	'''	
	print(sql0)
	
		#Table 'drug'
	defs = []
	for col in table_columns['drug']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql1 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY (`num`, `primaryid`, `drug_seq`) ) "
		#"KEY `primaryid` (`primaryid`, `drug_seq`), "
		#"FOREIGN KEY (`primaryid`) REFERENCES `demographic` (`primaryid`) ) "		
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[1], ', '.join(defs)) )	
	'''	
	sql1 = ("DROP TABLE IF EXISTS {0}.{1};\n"
		"CREATE TABLE {0}.{1} ({2}, "
		"PRIMARY KEY ('num', 'primaryid', 'drug_seq'), "
		"FOREIGN KEY ('primaryid') REFERENCES 'demographic' ('primaryid'), "
		"FOREIGN KEY ('primaryid', 'drug_seq') "
		"REFERENCES 'therapy' ('primaryid', 'dsg_drug_seq'), "
		"FOREIGN KEY ('primaryid', 'drug_seq') "
		"REFERENCES 'indication' ('primaryid', 'indi_drug_seq') ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[1], ', '.join(defs)) )	
	'''	
	print(sql1)
	
		#Table 'indication'
	defs = []
	for col in table_columns['indication']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql2 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY (`num`, `primaryid`, `indi_drug_seq`) ) "
		#"FOREIGN KEY (`primaryid`, `indi_drug_seq`) "
		#"REFERENCES `drug` (`primaryid`, `drug_seq`) ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[2], ', '.join(defs)) )	
	'''	
	sql2 = ("DROP TABLE IF EXISTS {0}.{1};\n"
		"CREATE TABLE {0}.{1} ({2}, "
		"PRIMARY KEY ('num', 'primaryid', 'indi_drug_seq'), "
		"FOREIGN KEY ('primaryid', 'indi_drug_seq') "
		"REFERENCES 'drug' ('primaryid', 'drug_seq') ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[2], ', '.join(defs)) )
	'''	
	print(sql2)
	
		#Table 'outcome'
	defs = []
	for col in table_columns['outcome']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql3 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY (`num`, `primaryid`) ) "
		#"FOREIGN KEY (`primaryid`) REFERENCES `demographic` (`primaryid`) ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[3], ', '.join(defs)) )	
	'''	
	sql3 = ("DROP TABLE IF EXISTS {0}.{1};\n"
		"CREATE TABLE {0}.{1} ({2}, "
		"PRIMARY KEY('num', 'primaryid'), "
		"FOREIGN KEY 'primaryid' REFERENCES 'demographic' ('primaryid') ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[3], ', '.join(defs)) )	
	'''	
	print(sql3)
	
		#Table 'reaction'
	defs = []
	for col in table_columns['reaction']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql4 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY (`num`, `primaryid`) ) "
		#"FOREIGN KEY (`primaryid`) REFERENCES `demographic` (`primaryid`) ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[4], ', '.join(defs)) )	
	'''	
	sql4 = ("DROP TABLE IF EXISTS {0}.{1};\n"
		"CREATE TABLE {0}.{1} ({2}, "
		"PRIMARY KEY('num', 'primaryid'), "
		"FOREIGN KEY ('primaryid') REFERENCES 'demographic' ('primaryid') ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[4], ', '.join(defs)) )
	'''	
	print(sql4)
	
		#Table 'report_sources'
	defs = []
	for col in table_columns['report_sources']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql5 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY(`num`, `primaryid`) ) "
		#"FOREIGN KEY (`primaryid`) REFERENCES `demographic` (`primaryid`) ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[5], ', '.join(defs)) )	
	print(sql5)
	
		#Table 'therapy'
	defs = []
	for col in table_columns['therapy']:
		defs.append('`{}` {}'.format(col, column_def[col]))
	sql6 = ("CREATE TABLE `{1}` ({2}, "
		"PRIMARY KEY(`num`, `primaryid`, `dsg_drug_seq`) ) "
		#"FOREIGN KEY (`primaryid`, `dsg_drug_seq`) "
		#"REFERENCES `drug` (`primaryid`, `drug_seq`) ) "
		"ENGINE = InnoDB;\n"
		.format(general['database_name'], tables[6], ', '.join(defs)) )	
	print(sql6)
			
	
	sql10 = 'USE `{}`;\n'.format(general['database_name'])
	print(sql10)
	
	with open('{}/create_table.sql'.format(general['sql']), mode='w') as foo:
		print(sql22, file=foo)
		print(sql0, file=foo)
		print(sql1, file=foo)
		print(sql2, file=foo)
		print(sql3, file=foo)
		print(sql4, file=foo)
		print(sql5, file=foo)
		print(sql6, file=foo)
		print(sql10, file=foo)
		
	#with open('{}/main.sql'.format(general['sql']), mode='w') as foo:
	#	print('SOURCE {};'.format('create_table.sql'), file=foo)
	

def execute_create_table_sql(auto_destroy=False):
	'''
	Execute sql statements in create_table.sql file.
	'''
	import pymysql as my
	
	#database connection settings
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'database': 'faers'}
	args = load_db_connection_section()
		
	general = load_general_section()
	
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'db': 'faers'}
	args = load_db_connection_section()
	general['database_name'] = args['db']
	args['db'] = ''
	
	#Check db connection with empty db
	dbCheck = get_connection(False)
	if not dbCheck:
		print('[execute_create_table_sql] Database connection failed!')
		exit()
	
	#Prompt for user confirmation before destroying existing database data
	if not auto_destroy:
		userinput = input('Entire content of database "{}" will be destroyed. '
			'Continue? (y/n) '.format(general['database_name']))
		if userinput.strip() != 'y':
			print('You chose to leave database as is.')
			return
	
	#Remove shelve files
	remove_shelve_files()
	
	#Qualified path to create_table.sql
	#ie ../istudy_large_files/SQL_FILES/create_table.sql
	create_sql_path = '{}/{}'.format(general['sql'], 'create_table.sql')		
	
	
	with my.connect(**args) as cursor: #faster  option
	#with conn.cursor() as cursor: #slower option
		
		''' {'_result': None, 'arraysize': 1, 'rowcount': -1, 'connection': <pymysql.connections.Connection object at 0x7f0407bc3ba8>, '_rows': None, '_executed': None, 'description': None, 'rownumber': 0} '''
		#print(cursor.__dict__)		
		
		
		''' {'affected_rows': 0, 'warning_count': 1, 'unbuffered_active': False, 'rows': None, 'message': b'', 'field_count': 0, 'has_next': 0, 'insert_id': 0, 'description': None, 'server_status': 0, 'connection': False} '''
		#print(cursor.__dict__['_result'].__dict__)
		
		
		with open(create_sql_path) as foo: #open create_table.sql
			for line in foo: #iterate over each line
				if not line.strip():	continue #skip blank line				
				cursor.execute(line)				
				#print(cursor.__dict__['_result'].__dict__)
				warning_count = cursor.__dict__['_result'].__dict__['warning_count']
				if warning_count:
					print('[execute_create_table_sql] '
						'WARNING: This sql statement produced {} warning(s).\n'
						'{}\n'
						.format(warning_count, line))
			else: #for-loop completed without interruption
				cursor.execute('show tables;')				
				tables = [', '.join(x) for x in cursor.fetchall()]
				tables.sort()
				tables = ', '.join(tables)
				print('Database "{}" created successfully!\n'
					'Tables were created: {} !'
					.format(general['database_name'], tables))	
	
	
		
	
def execute_insert_row_sql(auto_proceed=False):
	'''
	Execute the insert sql files in SQL_FILES directory.
	'''
	import pymysql as my
	#import shelve
	
	import my_shelve
	
	#Get shelve data structure containing shelve.data content
	store2 = my_shelve.read_from_shelve_file()
	
	#database connection settings
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'database': 'faers'}
	args = load_db_connection_section()
	
	#File ending with '.sql' but not '.sql~'
	po = re.compile(r'\.sql$')
	
	general = load_general_section()
	
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'db': 'faers'}
	args = load_db_connection_section()
	general['database_name'] = args['db']
	
	#Check db connection
	dbCheck = get_connection()
	if not dbCheck:
		print('[execute_insert_row_sql] Database connection failed!')
		exit()
	
	#List of qualified sql filenames in SQL_FILES directory
	#ie ['../istudy_large_files/SQL_FILES/insert_demo12q4.sql', ...]
	sqls = (['{}/{}'.format(general['sql'], x) 
		for x in os.listdir(general['sql']) 
		if po.search(x) and x!='create_table.sql' and x!='main.sql'] )
	sqls.sort()	
	
	
	with my.connect(**args) as cursor:		
		
		conn = cursor.__dict__['connection']		
		
			
		for filename in sqls: #each qualified sql filename in SQL_FILES dir
		#for filename in temp: #each qualified sql filename in SQL_FILES dir
		
			
			table_name = get_table_name(filename)			
			shelve_filename = '{}/{}'.format(general['shelve'], table_name)
			found = None
			store = None
			
			#Open shelve file associated with table
			'''
			with shelve.open(shelve_filename) as foo:				
				for key in foo:
					if filename in key:
						found = key
						break
				if found:
					store = foo[found]
			'''		
			for key in store2[table_name]:
				if filename in key:
					found = key
					break
			if found:
				store = store2[table_name][found]
			
			#Problem... key not found in shelve file
			if not found:
				print('[execute_insert_row_sql] ERROR key not found for '
					'file {} in shelve'.format(filename) )
				continue
			
			#Check if data already inserted in database; if proceed, then 
			# need to remove from database.	
			if store['ok_inserted_rows'] or store['warning_inserted_rows']:
				if not auto_proceed:
					user_input = input('Insert sql in {} has already been executed'
						' and is in the database. If you proceed, they will be '
						'removed from database and re-inserted.  Proceed? (y/n) ')
					if user_input != 'y':
						continue
				#Remove data from database	
				for e in store['ok_inserted_rows']:
					sql = ('DELETE FROM {}.{} WHERE num="{}";'
						.format(general['database_name'], table_name, e))
					cursor.execute(sql)
					conn.commit()
					
				for e in store['warning_inserted_rows']:
					sql = ('DELETE FROM {}.{} WHERE num="{}";'
						.format(general['database_name'], table_name, e[0]))
					cursor.execute(sql)					
		
		
			ok_inserted_rows = set()
			warning_inserted_rows = []
			failed_inserted_rows = []
		
			print('INSERTING ROW DATA... {}'.format(filename) )
			with open(filename) as file_content: #access insert sql file
				line_number = 0 #Header line
				for line in file_content:
					#print(line)
					line_number += 1
					try:
						cursor.execute(line)						
						result = cursor.__dict__['_result']
						warning_count = result.__dict__['warning_count']
						insert_id = result.__dict__['insert_id']
						if warning_count: # WARNING on insert
							print('Sql statement produced {} warning(s). '
								'Line number {}.\n'
								'{}\n'.format(warning_count, line_number, line))
							warning_inserted_rows.append(tuple((insert_id, line, line_number)))	
						else: # OK on insert
							ok_inserted_rows.add(insert_id)
							print(insert_id, 'OK {}'.format(filename))				
					
					except UnicodeEncodeError:
						cursor.execute(bytes(line, encoding='utf-8'))					
						result = cursor.__dict__['_result']
						warning_count = result.__dict__['warning_count']
						insert_id = result.__dict__['insert_id']
						if warning_count: # WARNING on insert
							print('Sql statement produced {} warning(s). '
								'Line number {}.\n'
								'{}\n'.format(warning_count, line_number, line))
							warning_inserted_rows.append(tuple((insert_id, line, line_number)))	
						else: # OK on insert
							ok_inserted_rows.add(insert_id)
							print(insert_id, 'OK')	
							
					except: # ERROR on insert
						print('[execute_insert_row_sql] ERROR in line number {} '
							'when execute '
							'insert sql statement\n{}\n'.format(line_number, line) )
						failed_inserted_rows.append(tuple((line, line_number)))				
					
					
			
			#Store in shelve file	
			'''		
			with shelve.open(shelve_filename) as foo:
				store = foo[found]
				store['ok_inserted_rows'] = ok_inserted_rows
				store['warning_inserted_rows'] = warning_inserted_rows
				store['failed_inserted_rows'] = tuple(failed_inserted_rows)
				foo[found] = store
			'''	
			store['ok_inserted_rows'] = ok_inserted_rows
			store['warning_inserted_rows'] = tuple(warning_inserted_rows)
			store['failed_inserted_rows'] = tuple(failed_inserted_rows)
			store2[table_name][found] = store
			
			my_shelve.write_to_shelve_file(store2)		
			
			
			
					
		
def report_insert_result():
	'''
	
	Maintain table information with following data structure:
	Stored in shelve, one for each table, ie 
	therapy: { 
	  'qualified_ascii_data_filename1\tqualified_sql_insert_filename1':
	  {	  		
	  		row_count: some_int,	  		
	  		ok_inserted_rows: set(insert_id,...),
	  		warning_inserted_rows: tuple((insert_id,insert_sql,line_number),...)
	  		failed_inserted_rows: tuple((insert_sql,line_number),...),	  		
	  		remove_sql_file_name: None
	  },
	  'qualified_ascii_data_filename2\tqualified_sql_insert_filename2': {..},
	  'qualified_ascii_data_filename3\tqualified_sql_insert_filename3': {..}, ...
	}
	
	indication: {...}
	'''	
	#import shelve
	
	import my_shelve
	
	store2 = my_shelve.read_from_shelve_file()
	
	general = load_general_section()
	report_filename = '{}/{}'.format(general['sql'], 'report')
	report = open(report_filename, mode='w')
	
	tables = list(load_table_column_names_section().keys())
	tables.sort()
	print('============================================================'
		'====================')
	print('============================================================'
		'====================',
		file=report)
	print('		Insertion Result Report							 ')
	print('		Insertion Result Report							 ', 
		file=report)
	print('============================================================'
		'====================')
	print('============================================================'
		'====================',
		file=report)
	for table_name in tables:
		shelve_filename = '{}/{}'.format(general['shelve'], table_name)
		print('====== {} ({}) ======'.format(table_name.upper(), 
			shelve_filename) )
		print('====== {} ({}) ======'.format(table_name.upper(), 
			shelve_filename), file=report )	
		
		#with shelve.open(shelve_filename) as storexx:
		store = store2[table_name]
		#keys = list(store.keys())
		keys = list(store) #list of data_sql_filename
		keys.sort()
		
		
		for data_sql_filenames in keys:
			table_store = store[data_sql_filenames]
			data_filename, sql_filename = data_sql_filenames.split('\t')
			print('{}\n{}'.format(data_filename, sql_filename) )
			print('{}\n{}'.format(data_filename, sql_filename), file=report)
			row_count = table_store['row_count']
			inserted_count = len(table_store['ok_inserted_rows'])
			warning_count = len(table_store['warning_inserted_rows'])
			failed_count = len(table_store['failed_inserted_rows'])
			print('row_count: {}   inserted_count: {}   '
				'warning_count: {}   failed_count: {}'
				.format(row_count, inserted_count, warning_count, 
				failed_count) )
			print('row_count: {}   inserted_count: {}   '
				'warning_count: {}   failed_count: {}'
				.format(row_count, inserted_count, warning_count, 
				failed_count), file=report )	
				
			if row_count == inserted_count:
				print('No problem detected while inserting row data')
				print('No problem detected while inserting row data', 
					file=report)
			
			if warning_count:
				print('Warnings issued for the following sql statements:')
				print('Warnings issued for the following sql statements:',
					file=report)
				for e in table_store['warning_inserted_rows']:
					print('{} {}'.format(e[0], e[1]) )#insert_id  insert_sql				
					print('Line number: {}  Row data: {}'.format(e[2], 
						get_offending_row_data(data_filename, e[2])))
					print('{} {}'.format(e[0], e[1]), file=report )			
					print('Line number: {}  Row data: {}'.format(e[2], 
						get_offending_row_data(data_filename, e[2])),
						file=report)	
				
				
			if failed_count:
				print('Error occurred for the following sql statements:')
				print('Error occurred for the following sql statements:',
					file=report)
				for e in table_store['failed_inserted_rows']:
					print(e[0]) #insert_sql
					print('Line number: {}  Row data: {}'.format(e[1],
						get_offending_row_data(data_filename, e[1])))	
					print(e[0], file=report) #insert_sql
					print('Line number: {}  Row data: {}'.format(e[1],
						get_offending_row_data(data_filename, e[1])),
						file=report)			
				
					
			print()
			print(file=report)
				
		print()	
		print(file=report)		
	
	report.close()
	print('Report saved in:  {}\n'.format(report_filename))
	

def get_offending_row_data(ascii_data_qualified_filename, line_number):
	'''
	Return row data in ascii data file that caused the warning or failure.
	'''
	#Line numbering starts with 0.
	with open(ascii_data_qualified_filename) as foo:
		counter = -1
		for line in foo:
			counter += 1
			if counter == line_number:
				return line

def get_connection(does_database_exists=True):
	"""
	Obtain a connection object.  Connection setting is based on section 10 in
	"parameters" file.
	
	Close returned connection when done.
	
	does_database_exists should be False if you want to connect without 
	specifying a database, especially if the database does not exist.
	
	Return: Object of type <class 'pymysql.connections.Connection'> 
		or None if error	
	"""
	import pymysql as my
	
	#database connection settings
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'db': 'faers'}
	args = load_db_connection_section()
	
	if not does_database_exists:
		args['db'] = ''
	
	### pymysql.err.OperationalError
	host_pattern = re.compile(r".*?Name or service not known.*")
	user_pattern = re.compile(r".*?Access denied for user.*?using password: (NO|no).*")
	pwd_pattern = re.compile(r".*?Access denied for user.*?using password: (YES|yes).*")
	
	### pymysql.err.InternalError
	db_pattern = re.compile(r".*?Unknown database.*")
	
	try:
		#with my.connect(**args) as c:
		conn = my.connect(**args)
		
		'''
		c = conn.cursor()
		c.execute('show databases;')		
		c.close()
		conn.close()
		'''
		
		#ie <class 'pymysql.connections.Connection'>
		#print(type(conn) )
		
		return conn
	
	except (my.err.OperationalError) as e:
		#Error with 'host' connection parameter
		if host_pattern.search(str(e)):
			print('Possible issue with host name "{}"'.format(args['host']))
		
		#Error with 'user' connection parameter
		elif user_pattern.search(str(e)):
			print('Possible issue with user name "{}"'.format(args['user']))
		
		#Error with 'passwd' connection parameter	
		elif pwd_pattern.search(str(e)):
			print('Possible issue with password "{}"'.format(args['passwd']))
		
		#Error is unexpected so must raise it	
		else:	
			print('[get_connection] Unknown OperationalError!')
			print(e)
			raise
	
	except (my.err.InternalError) as e:
		#Error with 'db' connection parameter
		if db_pattern.search(str(e)):
			print('Possible issue with database.  Check that database "{}" exists!'
				.format(args['db']))
			print('Suggestion: execute commands "compose_create_sql()" and '
				'"execute_create_table_sql(auto_destroy=True)" before '
				'executing "compose_insert_sql(limit=10)" and '
		
				'"execute_insert_row_sql(auto_proceed=True)" .')
				
		#Error is unknown so must raise it		
		else:
			print('[get_connection] Unknown InternalError!')
			print(e)
			raise
	
	#Error is unknown so must raise it
	except:
		print('[get_connection] UNKNOWN ERROR !!!')
		raise
		
	return None	
	
	
	
def test():
	sql = \
	"""
	INSERT INTO faers.drug (primaryid, caseid, drug_seq, role_cod, drugname, val_vbm, route, dose_vbm, rechal, lot_num, nda_num, dose_form, dose_freq) VALUES ("88830361", "8883036", "1", "PS", "HUMIRA", "1", "SUBCUTANEOUS", "\", "D", "UNKNOWN", "125057", "Solution for injection", "QOW");
	
	"""	
	#import pymysql as my
	
	#database connection settings
	#ie {'host': 'localhost', 'passwd': '', 'user': 'root', 'database': 'faers'}
	#args = load_db_connection_section()	
	
	#with my.connect(**args) as c:
		#c.execute('show databases;')
		#c.execute(bytes(sql, encoding='utf-8')) #For weird unicode chars
		
	conn = get_connection()
	c = conn.cursor()	
	c.execute('show databases;')
	
	c.close()
	conn.close()
	
def test2():
	
	#ie 100069422$10006942$HP
	print(get_offending_row_data('DATA_FILES/faers_ascii_2015q4/ascii/RPSR15Q4.txt', 2))

"""		
TO-DO				
### Compose sql create table statements			
### Compose sql insert statements
### Compose sql remove statements
### Diagnose data file ie number data rows, duplicates, headers

1.  Find number of rows in each table and store; for numbering all rows --OK
2.  Ensure all column names and tables are compatible to standard  --OK
3.  Create insert sql and store each row id for undo  --OK
4.  Create remove sql to undo
5.  Create create sql --OK
6.  Write program to read sql file and execute each statement 
	and report status




"""

check_for_duplicates = show_data_file_info

if __name__ == '__main__':
	
	#print(get_table_name('vad/xxxx98.txt')) #ie therapy
	#ie demographic
	#print(get_table_name('../istudy_large_files/SQL_FILES/insert_DEMO15Q4.sql'))
	#print( get_quarter_to_data_filenames_dict() )
	#print(load_table_prefixes())
	
	#test()
	print(get_connection())
	
	
	###Check for duplicates
	#check_for_duplicates()
	
		
	###1. Ensure expected tables and columns exist in quarterly directory
	
	#check_table_column_compatibility()
	
	###2. Compose create sql
	
	#compose_create_sql() # Rerun if column definition changed.
	#execute_create_table_sql(auto_destroy=True) # Rerun if create_table.sql changed.
	
		
	
	###3. Compose insert sql and store in file.  Such, file can be executed
	### by db system.  Also, this method stores table info in shelve.
	
	
	
	#remove_shelve_files()
	#remove_sql_files()
	
	#compose_insert_sql(limit=10) #Change limit=None to insert ALL row data
	#execute_insert_row_sql(auto_proceed=True)
					
						
	#report_insert_result()					
						
						
	
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
