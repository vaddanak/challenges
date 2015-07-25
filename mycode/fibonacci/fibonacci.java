/*
Author: Vaddanak Seng
File: fibonacci.java
Purpose: Print out the first N numbers in the Fibonacci sequence.
Date: 2015/07/25
*/

import java.util.Scanner;
import java.util.Vector;

public class fibonacci {


	public static void main(String[] args) {
	
		fibonacci f = new fibonacci();
		Vector<Integer> storage = new Vector<Integer>();
		
		Scanner scan = new Scanner(System.in);
		int N = scan.nextInt();
	
		f.fibo(N, storage);
		
		int len = storage.size();
		for(int i = 0; i < len; ++i) {
			System.out.print(storage.get(i).intValue());
			if(i < len-1)
				System.out.print(" ");
		}
	}


	public void fibo(int N, Vector<Integer> storage) {
		if(N > 0) {
			int len = storage.size();
			if(len==0)
				storage.add(Integer.valueOf(0));
			else if(len==1) 				
				storage.add(Integer.valueOf(1));
			else
				storage.add(storage.get(len-1).intValue() + 
					storage.get(len-2).intValue());
			
			fibo(N-1, storage);
		}
	
	}














}
