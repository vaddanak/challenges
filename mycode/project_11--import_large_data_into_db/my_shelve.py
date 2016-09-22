"""
Author:  Vaddanak Seng
Purpose:  Custom data structure to store meta data

"""



import util2 as util


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

store2 = my_shelve.read_from_shelve_file()	
store = store2[table_name]
if store_key not in store:
	store[store_key] = {
		'row_count':0,
		'ok_inserted_rows':set(),
		'warning_inserted_rows':tuple(),
		'failed_inserted_rows':tuple(),
		'remove_sql_file_name':None }						
file_store = store[store_key]

				
'''

test_dict = {

	'demographic': {
		'file1.txt	file1.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file2.txt	file2.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file3.txt	file3.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}
			
	},
	
	'drug': {
		'file4.txt	file4.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file5.txt	file5.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file6.txt	file6.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}	
	},
	
	'indication': {
		'file7.txt	file7.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file8.txt	file8.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file9.txt	file9.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}	
	},
	
	'outcome': {
		'file10.txt	file10.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file11.txt	file11.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file12.txt	file12.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}	
	},
	
	'report_sources': {
		'file13.txt	file13.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file14.txt	file14.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file15.txt	file15.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}	
	},
	
	'reaction': {
		'file16.txt	file16.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file17.txt	file17.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file18.txt	file18.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}	
	},
	
	'therapy': {
		'file19.txt	file19.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file20.txt	file20.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		},
		
		'file21.txt	file21.slq': {
			'row_count':0,
			'ok_inserted_rows':set(),
			'warning_inserted_rows':tuple(),
			'failed_inserted_rows':tuple(),
			'remove_sql_file_name':None 
		}	
	}

}

shelve_data_structure = {
	'demographic': {},	
	'drug': {},	
	'indication': {},	
	'outcome': {},	
	'report_sources': {},	
	'reaction': {},	
	'therapy': {}
}

def write_to_shelve_file(my_shelve_data_dict = None):
	global shelve_data_structure
	
	test_dict = my_shelve_data_dict
	if not test_dict:
		test_dict = shelve_data_structure

	general = util.load_general_section()

	#ie ../istudy_large_files/SHELVE/shelve.data
	filename = '{}/{}'.format(general['shelve'], 'shelve.data')
	print('Writing to ', filename)	
	
	with open(filename, mode='w') as foo:		
		keys = list(test_dict.keys())
		keys.sort()
		#For each table name
		for e in keys:		
			print('[[{}]]'.format(e), file=foo )
		
			#For each data filename
			for filename in test_dict[e]:
				print('[{}]'.format(filename), file=foo )
			
				#For each key in filename section
				for key in test_dict[e][filename]:
					print('{}	{}'.format(key, test_dict[e][filename][key]),
						file=foo )
			
				print(file=foo)	
				
			print(file=foo)		
			
	
def read_from_shelve_file():
	import re
	import os
	
	global shelve_data_structure
	
	temp = shelve_data_structure
	
	general = util.load_general_section()
	filename = '{}/{}'.format(general['shelve'], 'shelve.data')
	
	#Create shelve file with empty data structure if not exist
	if not os.path.exists(filename):
		write_to_shelve_file()
	
	#Even matches empty between double-bracket pairs	
	table_section_pattern = re.compile(r'^\[\[(.*?)\]\]$')
	
	#At least 2 chars between brackets ??? fixed
	#filename_section_pattern = re.compile(r'^\[([^\[].*?[^\]])?\]$')
	filename_section_pattern = re.compile(r'^\[(?![\[])(.*?)(?<![\]])\]$')
	
	#Key is tab-separated from value
	data_section_pattern = re.compile(r'^(?P<key>[^\t]+)\t+(?P<value>[^\t]+)$')
	
	lines = []
	last_table = None
	last_filename = None
	with open(filename) as foo:
		last_position = foo.tell()
		#For each line
		for line in foo:
			line = line.strip()
			#Skip blank line
			if not line:	continue
			#Skip comment line
			if line[0] == '#':	continue
			
			#Store table name line
			#lines.append(line)
			mo = table_section_pattern.search(line)
			if mo:				
				#print(mo.group(1))
				last_table = mo.group(1)				
				continue
			
			#Store filename line
			mo = filename_section_pattern.search(line)
			if mo:				
				#print(last_table, mo.group(1))
				last_filename = mo.group(1)
				continue
				
			#Store data lines
			mo = data_section_pattern.search(line)
			if mo:
				#print(last_table, last_filename, mo.group('key'), mo.group('value'))
				if last_filename not in temp[last_table]:
					temp[last_table][last_filename] = {}
				try:	
					temp[last_table][last_filename][mo.group('key').strip()] = \
						eval(mo.group('value').strip())
				except SyntaxError as e:
					#print('[read_from_shelve_file] eval("{}") failed'
					#	.format(e.text) )
					...	
				except:	
					raise	
			
	#print(temp)	
	#write_to_shelve_file(temp)
	
	return temp

if __name__ == '__main__':
	#write_to_shelve_file(None)
	
	read_from_shelve_file()























