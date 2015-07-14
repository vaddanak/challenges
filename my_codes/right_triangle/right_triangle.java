/*
Author: Vaddanak Seng
File: right_triangle.java
Purpose: Given any two edge lengths of a right triangle, find the missing third.
*/

import java.util.Scanner;
import java.util.Formatter;

public class right_triangle {


	public static void main(String[] args) {
	
		Formatter form = new Formatter();
		Scanner scan = new Scanner(System.in);
		
		String input = scan.nextLine(); //get user input
		String[] words = input.split("\\s"); //split into array of words
		double result = 0.0; //hold length of right triangle leg
		
		if(words[0].compareTo("_")==0) { //find side1 length
			result = Math.sqrt(
			Math.pow(Double.parseDouble(words[2]),2) - 
			Math.pow(Double.parseDouble(words[1]),2));
		}
		else if(words[1].compareTo("_")==0) { //find side2 length
			result = Math.sqrt (
				Math.pow(Double.parseDouble(words[2]),2) -
				Math.pow(Double.parseDouble(words[0]),2));
		}
		else if(words[2].compareTo("_")==0) { //find hypotenuse
			result = Math.hypot (
				Double.parseDouble(words[0]), Double.parseDouble(words[1]) );
		}
		
		//format with 3 decimal places, also rounds it
		System.out.print( form.format("%.3f",result) );
	
	
	}


}
