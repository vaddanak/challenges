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
		
		String colors = scan.nextLine(); // get list of color counts
		int index = scan.nextInt(); // get index value
	
		Pattern pattern = Pattern.compile("\\s"); // pattern for whitespace
		String[] list = pattern.split(colors); // split values at whitespace
	
		int sumInt = 0;
		for(int i = 0; i < list.length; ++i)
			sumInt += Integer.parseInt(list[i]); // add up each value
		
		// calculate probability	
		double sumDouble = Double.parseDouble(list[index-1]) / (double)sumInt;
	
		String result = sumDouble + "00"; //ensure two digits after decimal
		//String result = "0.500";
	
		// extract double-type value to two decimal places, no rounding
		Matcher match = Pattern.compile("\\d+\\.\\d{2}").matcher(result);
		//boolean find = match.find();
		if(match.find())
			System.out.print(match.group(0)); //output whole matched subsequence	
	
	}




}
