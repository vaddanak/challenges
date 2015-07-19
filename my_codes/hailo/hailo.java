/*
Author: Vaddanak Seng
File: hailo.java
Purpose: Sort odd numbers in increasing order and even number in decreasing
	order.
*/

import java.lang.String;
import java.util.Scanner;
import java.util.Vector;
import java.util.regex.Pattern;
import java.util.Collections;

public class hailo {


	public static void main(String[] args) {
	
		Scanner scan = new Scanner(System.in);
		
		String inputString = scan.nextLine(); //get user input
		
		Pattern pattern = Pattern.compile("\\s+");//create regex object
		String[] matches = pattern.split(inputString);//split into words
		
		Vector<Integer> odds = new Vector<Integer>(); //store odd numbers
		Vector<Integer> evens = new Vector<Integer>();//store even numbers
		int num = 0;
		String result = "";//hold numbers in correct order for disply
	
		for(String x : matches) {
			num = Integer.parseInt(x);
			if( num % 2 != 0) //condition for odd numbers
				odds.add(new Integer(num));
			else // rest must be even numbers
				evens.add(new Integer(num));		
		}
		
		Collections.sort(odds); //sort in increasing order
		Collections.sort(evens);//Java needs to sort in increasing order,
		Collections.reverse(evens);//in order to put it in reverse order ???
		
		for(int x : odds)
			result += x + " ";
		for(Integer x : evens)
			result += x + " ";	
	
		System.out.print(result.trim());	
	
	}

}
