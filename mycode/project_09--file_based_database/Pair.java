/******************************************************************************
*  Author:  Vaddanak Seng
*  File: Pair.java
*  Purpose: Store field name and field value.
******************************************************************************/


public class Pair {
	public String name; //field name
	public String value;//field value
	
	public Pair(String k, String v) {
		name = k;
		value = v;
	}
	
	public String toString() {
		return name+":"+value;
	}
}
