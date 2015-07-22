/*
Author: Vaddanak Seng
File: pebbles.java
Purpose: Determine probability of pebble color.
*/

import java.util.Scanner;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Formatter;



public class pebbles {


	public static void main(String[] args) {
	
		Scanner scan = new Scanner(System.in);
		//Formatter format = new Formatter();
		
		String colors = scan.nextLine();
		int index = scan.nextInt();
	
		Pattern pattern = Pattern.compile("\\s");
		String[] list = pattern.split(colors);
	
		int sumInt = 0;
		for(int i = 0; i < list.length; ++i)
			sumInt += Integer.parseInt(list[i]);
			
		double sumDouble = Double.parseDouble(list[index-1]) / (double)sumInt;
	
		String result = sumDouble + "00";
		//String result = "0.500";
	
		Matcher match = Pattern.compile("\\d+\\.\\d{2}").matcher(result);
		//boolean find = match.find();
		if(match.find())
			System.out.print(match.group(0));
			
		//System.out.println(sumDouble);
	
	}




}
