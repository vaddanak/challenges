/******************************************************************************
*  Author:  Provided by Professor Tu for Project 1 of Database Design course
*  Modified by: Vaddanak Seng
*  File: CommandParser.java
*  Purpose: Parse command line input into command and parameters.
******************************************************************************/

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class CommandParser {

	public Command fetchCommand() {
		
		try {
			String s = reader.readLine();
			if (s == null) {
				return null;
			}

			// \s+ = 1 or more of a whitespace char
			String[] pieces = s.trim().split("\\s+",10/*max command len + 1 */);
			String[] params = new String[pieces.length - 1];
			System.arraycopy(pieces, 1, params, 0, pieces.length - 1);
			
			return new Command(pieces[0], params);
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	
	
	private BufferedReader reader = 
		new BufferedReader(new InputStreamReader(System.in));
}
