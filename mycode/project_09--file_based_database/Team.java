/******************************************************************************
*  Author:  Vaddanak Seng
*  File: Team.java
*  Purpose: Team type represents a row in table of teams.
******************************************************************************/

import java.util.HashMap;
import java.util.regex.*;

public class Team {
	//schema for Team table
	public static HashMap<String,Class> schema = new HashMap<String,Class>();
	//translation from input field names to getter method names
	public static HashMap<String,String> translate = new HashMap<>(),
		getterNames = translate;
	//translation from input field names to setter method names		
	public static HashMap<String,String> setters = new HashMap<>(),
		setterNames = setters;
	static {
		schema.put("id",String.class); //capital letters and/or digits
		//American city name, one or two English word(s)
		schema.put("location",String.class);
		schema.put("name",String.class);//team name, any reasonable English word
		schema.put("league",String.class);//one capital letter
		
		//field name to method name
		translate.put("id","getId");
		translate.put("team_id","getId");
		translate.put("teamid","getId");
		translate.put("team","getId");
		translate.put("location","getLocation");
		translate.put("city","getLocation");
		translate.put("name","getName");
		translate.put("league","getLeague");
		translate.put("leag","getLeague");
		
		//field name to setter method name
		setters.put("id","setId");
		setters.put("team_id","setId");
		setters.put("teamid","setId");
		setters.put("team","setId");
		setters.put("location","setLocation");
		setters.put("city","setLocation");
		setters.put("name","setName");
		setters.put("league","setLeague");
		setters.put("leag","setLeague");
	}

	private String id = null;
	private String location = null;
	private String name = null;
	private String league = null;
	
	public Team() {
	
	}
	
	public void setId(String id) throws Exception {
		try {
			id = id.trim();
			boolean res = Pattern.matches("(^[A-Z0-9]+$)?",id);
			if(!res)
				throw new Exception(id + 
					" is NOT capital letters and/or digits!");
			this.id = id;
		}
		catch(Exception e) {
			System.err.println("setId(String): " + e);
			throw e;
		}
	}
	
	public String getId() {
		return this.id;
	}
	
	public void setLocation(String location) {
		this.location = location.trim();
	}
	
	public String getLocation() {
		return this.location;
	}
	
	public void setName(String name) {
		this.name = name.trim();
	}
	
	public String getName() {
		return this.name;
	}
	
	public void setLeague(String league) throws Exception {
		try {
			league = league.trim();
			boolean res = Pattern.matches("(^[A-Z]$)?",league);
			if(!res)
				throw new Exception(league + " is NOT one capital letter!");
			this.league = league;
		}
		catch(Exception e) {
			System.err.println("setLeague(String): " + e);
			throw e;
		}
	}
	
	public String getLeague() {
		return this.league;
	}
	
	public String toString() {
		return String.format(
			//"%-10s%-15s%-12s%-5s",
			"%-10s%-16s%-16s%-5s",  
			(id==null?" ":id), 
			(location==null?" ":location), 
			(name==null?" ":name), 
			(league==null?" ":league));
	}

}




















