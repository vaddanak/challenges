"""
Author:  Vaddanak Seng
Purpose:  Update database with generic drug attribute

"""

import re
import pymysql

import util2 as util



patt = util.line_text_pattern

mod = 'generic_drug.py'
target_table = 'drug'
target_column = 'generic_name'
target_column_source = 'drugname'

#Check db connection
conn = util.get_connection()
if not conn:
	print('[generic_drug.py] Failed to connect!')
	exit()
conn.close()	

#Check if column 'generic_name' exist in sections 3 and 5 of file 'parameters'
#  Column 'generic_name' MUST exist in sections 3 and 5 of file 'parameters'.
section3 = util.load_table_column_names_section()
section5 = util.load_column_definition_section()


try:
	temp = section3[target_table] #obtain list of column names
	temp = temp.index(target_column)
	
except (KeyError) as err:
	print('Table name \'{}\' does NOT exist in section 3'.format(target_table))
	exit()
	
except (ValueError) as err:
	print('Table \'{}\' columns does NOT have \'{}\' in section 3'
		.format(target_table, target_column) )
	exit()
	
except:
	print('[{}] UKNOWN ERROR!'.format(mod))
	raise
	

try:
	temp = section5[target_column]
	
except (KeyError) as err:
	print('Column name \'{}\' does NOT exist in section 5'.format(target_table))
	exit()
	
except:
	print('[{}] UKNOWN ERROR!'.format(mod))
	raise
	

#Check if 'generic_name' column exists in MySQL 'drug' table
conn_args = util.load_db_connection_section()
sql = 'SELECT {} FROM {}.{} LIMIT 3;'.format(target_column, 
	conn_args['db'], target_table)
	
unknown_column_patt = re.compile(r'unknown column(?i)')	
	
#print(sql)
with pymysql.connect(**conn_args) as cursor:
	try:
		cursor.execute(sql)		
			
	except (pymysql.err.InternalError) as err:
		#ie (1054, "Unknown column 'drugnamex' in 'field list'")
		#print(err)
		mo = unknown_column_patt.search(str(err))
		if mo:
			print('Column \'{}\' does not exist in MySQL table \'{}\''
				.format(target_column, target_table))
			exit()
		else:
			print('[{}] UNKNOWN InternalError'.format(mod))
			raise
		
	except:
		print('[{}] UKNOWN ERROR'.format(mod))
		raise	


#Obtain name of file containing 'drugname' to 'generic_name' mapping
#  from 'parameters' file.
section1 = util.load_general_section()
filename = section1['generic_names']
print('File containing \'drugname\' to \'generic_name\' mapping is: {}'
	.format(filename) )
	
	
#Ask if user wants to proceed to add column 'generic_name' to table 'drug'
user_input = input('Next action will modify MySql column {}.{}.{}\n'
	'Do you want to proceed? (y/n)'
	.format(conn_args['db'], target_table, target_column))
if user_input.strip() != 'y':
	print('You chose NOT to proceed.  Exiting...')
	exit()
	

#If so, open file containing 'drugname' to 'generic_name' mapping
#  Each line in file must be tab-separated to separate fields
#  First line in file MUST be column names, ie'drugname		generic_name'
fi = open(filename)
first_line = fi.__next__().strip()
mo = patt.search(first_line)
if not mo:
	print('File text does not comply with pattern: {}'.format(patt.pattern))
	exit()
key = mo.group('key').strip()
value = mo.group('value').strip()
index_source = -1
index_dest = -1

if key==target_column_source:
	index_source = 0
elif value==target_column_source:
	index_source = 1
	
if key==target_column:
	index_dest = 0
elif value==target_column:
	index_dest = 1
	
if index_source == -1 or index_dest == -1 or index_source==index_dest:
	print('Column names in first line of file {}, \'{}\' and \'{}\' does not '
		'match with expected column names \'{}\' and \'{}\''
		.format(filename, key, value, target_column_source, target_column))	
	exit()	
#print(index_source, key, index_dest, value)

#Create 'update' sql statement for each row 
#Execute each 'update' sql statement
with open('generic_list') as fi:
	fi.__next__() # skip header in first line
	with pymysql.connect(**conn_args) as cursor:
		for line in fi:
			mo = patt.search(line.strip())
			if mo:
				fields = [mo.group('key').strip(), mo.group('value').strip()]
				sql = ('UPDATE {}.{} SET {} = "{}" WHERE {} REGEXP "{}";'
					.format(conn_args['db'], target_table, target_column, 
					fields[index_dest], target_column_source, 
					fields[index_source]))				
				#print(sql)
				cursor.execute(sql)
				#print(cursor.__dict__['_result'].__dict__)
				affected_rows = cursor.__dict__['_result'].__dict__['affected_rows']
				print('Attempting to update \'{}\' to \'{}\'.  {} rows updated.'
					.format(fields[index_source], fields[index_dest], affected_rows))
				













