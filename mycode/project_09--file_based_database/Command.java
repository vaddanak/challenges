/******************************************************************************
*  Author:  Provided by Professor Tu for Project 1 of Database Design course
*  Modified by: Vaddanak Seng
*  File: Command.java
*  Purpose: Store command and parameters.
******************************************************************************/


/**
 * Data container for an individual Command
 * 
 * @author dbettis
 */
public class Command {
	/*
	public static Command currentCommand = null;
	static {
		String[] list = {"BEGIN01","1993","1","John","Proba1","32","50","2","0",
			"HOU"};
		currentCommand = new Command("load_coaches", list);
	}
	*/

	public Command(String command, String[] parameters) {
		super();
		this.command = command.trim().toLowerCase();
		this.parameters = parameters;
	}
	
	public String getCommand() {
		return command;
	}
	
	public String[] getParameters() {
		return parameters;
	}

	public String toString() {
		StringBuffer sb = new StringBuffer();
		sb.append("Command: " + command + "\n");
		for (int i = 0; i < parameters.length; i++) {
			sb.append("parameters[");
			sb.append(i);
			sb.append("] = ");
			sb.append(parameters[i]);
			sb.append("\n");
		}
		return sb.toString();
	}
	
	private String command;
	private String[] parameters;
}
