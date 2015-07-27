/*
Author: Vaddanak Seng
File: smoke_signals.java
Purpose: Complete a program which converts a binary sequence to ASCII.
Date: 2015/07/27
*/

import java.util.Scanner;
import java.util.regex.Pattern;
import java.util.regex.Matcher;




public class smoke_signals {


	public static void main(String[] args) {

		Scanner scan = new Scanner(System.in);
		String input = scan.nextLine();
		
		
		/*
		//option 1
		StringBuilder b = new StringBuilder(input);
		int asciiBinaryLength = 7;		
		for(int i = 0; i < b.length(); i += asciiBinaryLength) {
			//System.out.println(b.substring(i, i+asciiBinaryLength));
			Integer codePoint = Integer.valueOf(b.substring(i, i+asciiBinaryLength),2);
			//System.out.println(codePoint);
			System.out.print(String.valueOf(Character.toChars(codePoint.intValue())));
		}
		*/

	
		//option 2
		Pattern po = Pattern.compile("\\d{7}");
		Matcher m = po.matcher(input);		
		while(m.find())			
			System.out.print(Character.toChars(Integer.valueOf(m.group(0),2))[0]);

	}
}





