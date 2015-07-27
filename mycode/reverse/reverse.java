/*
Author: Vaddanak Seng
File: reverse.java
Purpose: Given two positive integers, reverse them (58 = 85), add them together,
	then reverse the final answer.
Date: 2015/07/25
*/

import java.util.Scanner;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Arrays;
import java.util.List;
import java.util.Vector;

public class reverse {


	public static void main(String[] args) {

		Scanner scan = new Scanner(System.in);
		String input = scan.nextLine();

		/*
		//Mooshak complains with "Compile Time Error" when this section of
		//code is used.
		Pattern patternObject = 
			Pattern.compile("^\\s*(?<first>\\d+)\\s*(?<second>\\d+)\\s*$");
		//create object, not start search engine
		Matcher match = patternObject.matcher(input);
	
		String first = "";
		String second = "";	
		if(match.find()) { //attempts to find the match; start search engine
			first = match.group("first");
			second = match.group("second");			
		}
		*/
	
		String[] inputs = input.split("\\s");
		String first = inputs[0];
		String second = inputs[1];

		StringBuilder b1 = new StringBuilder(first);
		b1.reverse();
		
		StringBuilder b2 = new StringBuilder(second);
		b2.reverse();
		
		int sum = Integer.parseInt(b1.toString()) + 
			Integer.parseInt(b2.toString());
			
		StringBuilder b3 = new StringBuilder(String.valueOf(sum));
		b3.reverse();	
		
		//System.out.println(first + " " + second);
		System.out.print(b3);
		
		/*
		//testing converting char[] to Character[] to List
		System.out.println();
		
		Vector<Character> vc = new Vector<Character>();
		char[] charArray = b3.toString().toCharArray();
		for(char ch : charArray)
			vc.add(new Character(ch));
		List<Object> list = Arrays.asList(vc.toArray());	
		
		for(Object c : list)
			System.out.print( (Character)c + " ");
		System.out.println();
			
		list.sort(null);
		
		for(Object c : list)
			System.out.print( (Character)c + " ");
		System.out.println();	
		*/
	}


}
