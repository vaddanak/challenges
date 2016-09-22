"""
Author:  Vaddanak Seng
Purpose:  Extract data from large file and insert into database

"""

import util2 as util


util.check_large_files_dir()

util.remove_shelve_files()
util.remove_sql_files()



util.compose_create_sql() # Rerun if column definition changed.	
util.execute_create_table_sql(auto_destroy=True) # Rerun if create_table.sql changed.
	

	
util.compose_insert_sql(limit=None) #Change limit=None to insert ALL row data
util.execute_insert_row_sql(auto_proceed=True)
					
					
					
util.report_insert_result()
