/*
Author: Vaddanak Seng
File: hello_coin.java
Purpose: Calculate the probability of getting at most H heads.
Date: 2015/07/28
*/


import java.util.Scanner;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Vector;
import java.util.Formatter;


public class hello_coin {

	/*
	PURPOSE: Program execution starts here!
	PRECON:
	POSTCON:
	*/
	public static void main(String[] args) {

		Formatter f = new Formatter(System.out);//outputs to display
		Scanner scan = new Scanner(System.in);
		//Vector<Hold> holds = new Vector<Hold>();
		hello_coin hc = new hello_coin();
		
		int numberOfCases = Integer.parseInt(scan.nextLine());
		
		/*
		// option 1
		//supported in Java 1.8 but what about Java 1.6 ??? NO
		//Pattern pattern = Pattern.compile(" *(?<trials>\\d+) +(?<heads>\\d+) *");
		//how about it Java 1.6 ??? unknown, Mooshak still complaining.
		Pattern pattern = Pattern.compile(" *(\\d+) +(\\d+) *");
		for(int i = 0; i < numberOfCases; ++i) {
			Matcher match = pattern.matcher(scan.nextLine());
			if(match.find()) {
				Hold h = new Hold();
				//h.trials = Integer.parseInt(match.group("trials"));
				//h.heads = Integer.parseInt(match.group("heads"));
				h.trials = Integer.parseInt(match.group(1));
				h.heads = Integer.parseInt(match.group(2));
				holds.add(h);				
			}
		}
		*/		
		
		/*
		// option 2
		for(int i = 0; i < numberOfCases; ++i) {
			String[] parts = scan.nextLine().split("\\s+");
			Hold h = new Hold();
			h.trials = Integer.parseInt(parts[0]);
			h.heads = Integer.parseInt(parts[1]);
			holds.add(h);
		}
		*/
		
		// option 3
		for(int i = 0; i < numberOfCases; ++i) {
			String[] parts = scan.nextLine().split("\\s+");
			int trials = Integer.parseInt(parts[0]);
			int heads = Integer.parseInt(parts[1]);
			double sum = 0.0;
			for(int head = 0; head < heads+1; ++head)
				sum += hc.calculate(trials, head);
			
			//System.out.println(String.format("%.4f", sum));
			f.format("%.4f\n", sum);
		}
		
		/*			
		//loop through each case, calculate probability, and add to sum				
		for(int i = 0; i < holds.size(); ++i) {
			Hold h = holds.get(i);
			double sum = 0.0;
			for(int j = 0; j < h.heads+1; ++j)  //loop over heads 0,1,2,...,h
				sum += calculate(h.trials,j);
			
			System.out.println(String.format("%.4f", sum) );
			//f.format("%.4f", sum);
			//f.flush(); //not needed bc System.out implements Flushable
			
			//if( i < hold.size()-1 )
			//	System.out.println(); 
				//f.format("\n");//Mooshak complains when \n is last char.		
		}
		*/
	}
	
	/*
	PURPOSE: Fn calculates factorial.
	PRECON: num is unsigned int.
	POSTCON: Fn returns num! .  Return type needs to be at least long because
		overflow occurs for 15!
	*/
	//public static long factorial(int num) {
	public long factorial(int num) {
		if(num>1)
			return num * factorial(num-1);
		return 1;	
	}
	
	/*
	PURPOSE: Fn calculates formula [ "n choose r" * p^r * q^(n-r) ], where
		"n choose r" is n! / (r! (n-r)!) , n is number of trials, r is 
		occurrences of head, p is probability of head for one flip, q is 
		probability of not head for one flip.
	PRECON:
	POSTCON: Fn returns result of formula.
	*/
	//public static double calculate(int trials, int heads) {
	public double calculate(int trials, int heads) {
		return ( factorial(trials) /
			(factorial(heads)*factorial(trials-heads)) )
			* Math.pow(0.5,heads) * Math.pow(0.5,trials-heads) ;	
	}

}

/*
class Hold {
	public int trials;
	public int heads;
}
*/
