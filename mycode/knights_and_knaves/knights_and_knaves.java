/*
Author: Vaddanak Seng
File: knights_and_knaves.java
Purpose: Determine which person is telling the truth.
Date: 2015/08/01
*/

import java.util.Scanner;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Formatter;



public class knights_and_knaves {

	public static void main(String[] args) {
	
		Scanner scan = new Scanner(System.in);
		Formatter fm = new Formatter(System.out);
		
		String line1 = scan.nextLine();
		String line2 = scan.nextLine();	
		
		//pattern based on problem description input format		
		Pattern pattern = 
			//Pattern.compile("^(?<speaker>[mv]):" + //javac 1.6.0_34 won't take
			//	"[mv](?<first>\\d)[mv](?<second>\\d)$");
			Pattern.compile("^([mv]):[mv](\\d)[mv](\\d)$");//javac 1.6.0_34 happy	
		
		int m1=0, v1=0, m2=0, v2=0;		
		//get match for first line		
		Matcher matcher = pattern.matcher(line1);				
		if(matcher.find()) {
			//fm.format("%s\n", matcher.group(0));
			m1 = Integer.parseInt(matcher.group(2)); //mike's truth code
			v1 = Integer.parseInt(matcher.group(3));//victor's truth code
			//fm.format("m=%d v=%d\n", m1, v1);
			
			//System.out.println(matcher.group("speaker").equals("m"));
			
			if(matcher.group(1).equals("m")) { //speaker is mike
				if(m1 == 0) //if mike is liar, v code is opposite
					v1 = v1==1?0:1;							
			}
			else { //speaker is victor
				if(v1 == 0) //if victor liar, m code is opposite
					m1 = m1==1?0:1;
			}
			//fm.format("m=%d v=%d\n", m1, v1);
		}
		
		matcher = pattern.matcher(line2);
		if(matcher.find()) {
			//fm.format("%s\n", matcher.group(0));
			m2 = Integer.parseInt(matcher.group(2));
			v2 = Integer.parseInt(matcher.group(3));
			//fm.format("m=%d v=%d\n", m2, v2);
			
			if(matcher.group(1).equals("m")) {
				if(m2 == 0) 
					v2 = v2==1?0:1;							
			}
			else {
				if(v2 == 0)
					m2 = m2==1?0:1;
			}
			//fm.format("m=%d v=%d\n", m2, v2);
		}	
		
		if( ((m1&m2)==1) && ((v1&v2)==0) && ((v1^v2)==0) ) // m1=m2=1 v1=v2=0
			fm.format("m");
		else if( ((v1&v2)==1) && ((m1&m2)==0) && ((m1^m2)==0) ) // v1=v2=1 m1=m2=0
			fm.format("v");
		else
			fm.format("u");			
		
	}

}






