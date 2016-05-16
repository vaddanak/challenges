/******************************************************************************
*  Author:  Vaddanak Seng
*  File: Coach.java
*  Purpose: Coach type represents a row in table of coaches.
******************************************************************************/

import java.util.HashMap;
import java.util.regex.*;

public class Coach {
	//schema for Coach table
	public static HashMap<String,Class> schema = new HashMap<>();
	//translation from input field names to getter method names
	public static HashMap<String,String> translate = new HashMap<>(), 
		getterNames = translate;
	//translation from input field names to setter method names	
	public static HashMap<String,String> setters = new HashMap<>(),
		setterNames = setters;	
	static {
		schema.put("id",String.class); // alphanumeric string
		schema.put("season",String.class); // 4 digit year
		schema.put("first_name",String.class); //any reasonable English name
		schema.put("last_name",String.class); //any reasonable English name
		schema.put("season_win",Integer.class); //non-negative integer
		schema.put("season_loss",Integer.class); //non-negative integer
		schema.put("playoff_win",Integer.class); //non-negative integer
		schema.put("playoff_loss",Integer.class); //non-negative integer
		schema.put("team",String.class); //capital letters and/or digits
		
		// ??? will there be variation with field names
		//field name to getter method name
		translate.put("id","getId");
		translate.put("coach_id","getId");
		translate.put("coachid","getId");
		translate.put("season","getSeason");
		translate.put("year","getSeason");
		translate.put("first_name","getFirstName");
		translate.put("last_name","getLastName");
		translate.put("firstname","getFirstName");
		translate.put("lastname","getLastName");
		translate.put("season_win","getSeasonWin");
		translate.put("season_loss","getSeasonLoss");
		translate.put("playoff_win","getPlayoffWin");
		translate.put("playoff_loss","getPlayoffLoss");
		translate.put("team","getTeam");
		translate.put("teamid","getTeam");
		translate.put("team_id","getTeam");
		
		//field name to setter method name
		setters.put("id","setId");
		setters.put("coach_id","setId");
		setters.put("coachid","setId");
		setters.put("season","setSeason");
		setters.put("year","setSeason");
		setters.put("first_name","setFirstName");
		setters.put("last_name","setLastName");
		setters.put("firstname","setFirstName");
		setters.put("lastname","setLastName");
		setters.put("season_win","setSeasonWin");
		setters.put("season_loss","setSeasonLoss");
		setters.put("playoff_win","setPlayoffWin");
		setters.put("playoff_loss","setPlayoffLoss");
		setters.put("team","setTeam");
		setters.put("teamid","setTeam");
		setters.put("team_id","setTeam");
		
	}
	
	private String id = null;
	private String season = null;
	private String first_name = null;
	private String last_name = null;
	private String season_win = null;
	private String season_loss = null;
	private String playoff_win = null;
	private String playoff_loss = null;
	private String team = null;
	private Pattern pattern = Pattern.compile("(^\\+?([0-9]+)$)?");
	private static final int G = 2;
	
	public Coach() {
		//System.out.println(schema.get("playoff_win")
		//	.isInstance(new Integer(5))); //true
	}

	public void setId(String id) throws Exception {
		try {
			id = id.trim();
			boolean patt = Pattern.matches("(^[0-9a-zA-Z]+$)?",id);
			if(!patt) {
				throw new Exception(id + " is NOT alphanumeric string!");
			}
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
	
	public void setSeason(String season) throws Exception {
		try {
			season = season.trim();
			boolean patt = Pattern.matches("(^[0-9]{4}$)?", season);
			if(!patt)				
				throw new Exception(season + " is NOT a 4 digit year!");
			this.season = season;
		}
		catch(Exception e) {
			System.err.println("setSeason(String): " + e);
			throw e;
		}	
	}
	
	public String getSeason() {
		return this.season;
	}
	
	public void setFirstName(String first_name) {
		this.first_name = first_name.trim();
	}
	
	public String getFirstName() {
		return this.first_name;
	}
	
	public void setLastName(String last_name) {
		this.last_name = last_name.trim();
	}
	
	public String getLastName() {
		return this.last_name;
	}
	
	//public void setSeasonWin(Integer season_win) {
	//	this.season_win = season_win;
	//}
	
	public void setSeasonWin(String season_win) throws Exception {
		try {
			season_win = season_win.trim();
			Matcher match = pattern.matcher(season_win);
			boolean res = match.matches();
			if(!res)
				throw new Exception(season_win + 
					" is NOT non-negative integer!");
			this.season_win = match.group(G);
		}
		catch(Exception e) {
			System.err.println("setSeasonWin(String): " + e);
			throw e;
		}	
	}
	
	public String getSeasonWin() {
		return this.season_win;
	}
	
	//public void setSeasonLoss(Integer season_loss) {
	//	this.season_loss = season_loss;
	//}
	
	public void setSeasonLoss(String season_loss) throws Exception {
		try {
			season_loss = season_loss.trim();
			Matcher match = pattern.matcher(season_loss);
			boolean res = match.matches();
			if(!res)
				throw new Exception(season_loss + 
					" is NOT non-negative integer!");
			this.season_loss = match.group(G);
		}	
		catch(Exception err) {
			System.err.println("setSeasonLoss(String): " + err);
			throw err;
		}	
	}
	
	public String getSeasonLoss() {
		return this.season_loss;
	}
	
	//public void setPlayoffWin(Integer playoff_win) {
	//	this.playoff_win = playoff_win;
	//}
	
	public void setPlayoffWin(String playoff_win) throws Exception {
		try {
			playoff_win = playoff_win.trim();
			Matcher match = pattern.matcher(playoff_win);
			boolean res = match.matches();
			if(!res)
				throw new Exception(playoff_win + 
					" is NOT non-negative integer!");
			this.playoff_win = match.group(G);
		}	
		catch(Exception err) {
			System.err.println("setPlayoffWin(String): " + err);
			throw err;
		}
	}
	
	public String getPlayoffWin() {
		return this.playoff_win;
	}
	
	//public void setPlayoffLoss(Integer playoff_loss) {
	//	this.playoff_loss = playoff_loss;
	//}
	
	public void setPlayoffLoss(String playoff_loss) throws Exception {
		try {
			playoff_loss = playoff_loss.trim();
			Matcher match = pattern.matcher(playoff_loss);
			boolean res = match.matches();
			if(!res)
				throw new Exception(playoff_loss + 
					" is NOT non-negative integer!");
			this.playoff_loss = match.group(G);
		}
		catch(Exception err) {
			System.err.println("setPlayoffLoss(String): " + err);
			throw err;
		}
	}
	
	public String getPlayoffLoss() {
		return this.playoff_loss;
	}
	
	public void setTeam(String team) throws Exception {
		try {
			team = team.trim();
			boolean res = Pattern.matches("(^[A-Z0-9]+$)?",team);
			if(!res)
				throw new Exception(team + 
					" is NOT capital letters and/or digits!");
			this.team = team;
		}
		catch(Exception e) {
			System.err.println("setTeam(String): " +e);
			throw e;
		}
	}
	
	public String getTeam() {
		return this.team;
	}
	
	public String toString() {
		return String.format(
			//"%-12s%-7s%-12s%-12s%5s%5s%5s%5s%5s",
			"%-12s%-7s%-13s%-15s%5s%5s%5s%5s%5s",
			(id==null?" ":id), 
			(season==null?" ":season), 
			(first_name==null?" ":first_name), 
			(last_name==null?" ":last_name), 
			(season_win==null?" ":season_win),
			(season_loss==null?" ":season_loss), 
			(playoff_win==null?" ":playoff_win),
			(playoff_loss==null?" ":playoff_loss), 
			(team==null?" ":team) );
	}

	/*
	public static void main(String[] args) {	
		new Coach();
	}
	*/

}
