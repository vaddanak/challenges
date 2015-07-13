/*
Author:  Vaddanak Seng
File:  palindrome.java
Purpose:  Determine if user input is a palindrome.
*/

import java.util.Scanner;


public class palindrome {





	public static void main(String[] args) {
	
		Scanner scan = new Scanner(System.in);
		String input = scan.next();//obtain user input
		
		StringBuilder sb = new StringBuilder(input);//create mutable string
		sb.reverse();//reverse in place
		
		if(input.compareTo(sb.toString())==0)//test for equal condition
			System.out.print(1);
		else
			System.out.print(0);
	
		//System.out.println("Hello " + sb.toString());
	
	
	}

}






