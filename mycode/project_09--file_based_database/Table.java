/******************************************************************************
*  Author:  Vaddanak Seng
*  File: Table.java
*  Purpose: Represent a table in a database which stores rows of data and 
*		corresponding column headings.
******************************************************************************/

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.lang.reflect.Method;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.regex.MatchResult;

public class Table<T> {
	//Table of rows
	private ArrayList<Object> rows = new ArrayList<Object>();
	//Headers from input file but filtered based on project description headers
	private ArrayList<String> preferredHeaders = new ArrayList<String>();
	//Headers extracted from input file
	private ArrayList<String> originalHeaders = new ArrayList<String>();
	//Headers as specified in project description for Coach table
	private ArrayList<String> coachHeaders = new ArrayList<String>();
	//Headers as specified in project description for Team table.
	private ArrayList<String> teamHeaders = new ArrayList<String>();
	private String name; //Table name
	private Class<T> clazz; //T class type discoverable at compile time
	
	/**
	* Constructor.
	*/
	public Table(String tableName, Class<T> clz) {
		this.name = tableName;	
		this.clazz = clz;	
		
		coachHeaders.add("coach_id");
		coachHeaders.add("season");
		coachHeaders.add("first_name");
		coachHeaders.add("last_name");
		coachHeaders.add("season_win");
		coachHeaders.add("season_loss");
		coachHeaders.add("playoff_win");
		coachHeaders.add("playoff_loss");
		coachHeaders.add("team");
		
		teamHeaders.add("team_id");
		teamHeaders.add("location");
		teamHeaders.add("name");
		teamHeaders.add("league");		
			
		//rows.add(new Coach());	
		//System.out.println(rows.get(0) instanceof Coach); //true
		
		//System.out.println("Class<T>.getName(): "+this.clazz.getName()); //Coach
		//System.out.println(clz.getClass()); //class java.lang.Class
		/*
		try {
			System.out.println(Class.forName("Coach")); //class Coach
		}
		catch(Exception err) {
			System.err.println(err);
		}
		*/
		//System.out.println(t.getClass().getName());
	}
	
	
	/**
	* Add t to this table.
	* Pre: t is instance of either Coach or Team type.
	* Post: Return t if add is successful, otherwise null
	*/
	public Object addRow(Object t) {
		if(t != null)
			return rows.add(t)?t:null;	
		else
			return null;		
	}
	
	/**
	* Get T type as String, ie Coach or Team
	* Pre: n/a
	* Post: Return Coach or Team as expected, or other T-specified type.
	*/
	public String getType() {
		return clazz.getName();
	}
	
	/**
	* Check if Coach type.
	* Pre: n/a
	* Post: Return true if Coach type.
	*/
	public boolean isCoachType() {
		return clazz.getName().equalsIgnoreCase("Coach");
	}
	
	/**
	* Check if Team type.
	* Pre: n/a
	* Post: Return true if Team type.
	*/
	public boolean isTeamType() {
		return clazz.getName().equalsIgnoreCase("Team");
	}
	
	/**
	* Load data from file.	
	* Pre: cmd is Command where cmd.getCommand() is either "load_coaches" or
	*	"load_teams" and cmd.getParameters()[0] is a filename.
	*	Data file is expected to have minimum set of column or field names
	*	as specified by columnHeaders and teamHeaders in first row of file.
	* Post: Populate rows of data from file in this table.
	*/
	public void loadFile(Command cmd) {
		try {
			if(cmd.getParameters().length==0)
				throw new Exception("Missing filename!");
			loadFile(cmd.getParameters()[0], cmd);
		}
		catch(Exception err) {
			System.err.println("loadFile(Command): " + err);
			if(isCoachType()) {
				System.err.println("USAGE: load_coaches filename");
				System.err.println("EXAMPLE: load_coaches c.txt");
			}
			else if(isTeamType()) {
				System.err.println("USAGE: load_teams filename");
				System.err.println("EXAMPLE: load_teams t.txt");
			}
		}
	}
	
	/**
	* Load data from file.  Helper function.
	* Pre: cmd is Command where cmd.getCommand() is either "load_coaches" or
	*	"load_teams" and cmd.getParameters()[0] is a filename.
	*	Data file is expected to have minimum set of column or field names
	*	as specified by columnHeaders and teamHeaders in first row of file.
	* Post: Populate rows of data from file in this table.
	*/
	private void loadFile(String filename, Command cmd) throws Exception {
		if(filename==null || cmd==null) {
			System.err.println(String.format("Filename is: %s\tCommand is:%s",
				(filename==null?"null":filename), 
				(cmd==null?"null":cmd.getCommand())) );
			return;
		}	
		try {			
			//Check if command is "load_coaches" or "load_teams"	
			boolean isLoadCoaches = cmd.getCommand()
				.trim().equalsIgnoreCase("load_coaches");
			boolean isLoadTeams = cmd.getCommand()
				.trim().equalsIgnoreCase("load_teams");	
			//Valid command is either "load_coaches" or "load_teams"
			if(!isLoadCoaches && !isLoadTeams) {
				System.err.println("Command is unknown: "+cmd.getCommand());
				throw new Exception("Neither load_coaches or load_teams!");
			}			
			//Retrieve and store headers present in first line of testcase
			BufferedReader reader =new BufferedReader(new FileReader(filename));
			originalHeaders = new ArrayList<String>();
			preferredHeaders = new ArrayList<String>();
			//Read raw column headers found in first line of data file.
			String headerString = reader.readLine().trim().toLowerCase();
			String[] rawHeaders = headerString.split(",");
			for(int i=0; i <rawHeaders.length; ++i)
				rawHeaders[i]=rawHeaders[i].trim().toLowerCase();
			ArrayList<String> rlist = new ArrayList<String>();			
			rlist.addAll(Arrays.asList(rawHeaders));//hold raw headers from file
			//System.out.println(rawHeaders[0]);
			//Validate command,T type, and table size
			if(isLoadCoaches) {
				if(!isCoachType()) {
					throw new Exception("Non-Coach type is trying to "+
						"load a coach table.");
				}
				//Validate first row of data file has proper column headers
				if((rlist.contains("first_name")||rlist.contains("firstname"))
					&&(rlist.contains("last_name")||rlist.contains("lastname"))
					&&rlist.contains("season_win")
					&&rlist.contains("season_loss") 
					&&rlist.contains("playoff_win")
					&&rlist.contains("playoff_loss")
					&&(rlist.contains("season")||rlist.contains("year"))
					&&(rlist.contains("team")||rlist.contains("team_id")||
					rlist.contains("teamid")||rlist.contains("id"))
					&&(rlist.contains("coach")||rlist.contains("coach_id")||
					rlist.contains("coachid")||rlist.contains("id")) ) {
					//OK
				}
				else	
					throw new Exception("This does not appear to be coach " +
						"data because headers given in first row of file is"+
						" not valid.\n"+headerString);
			}
			if(isLoadTeams) {
				if(!isTeamType()) {
					throw new Exception("Non-Team type is trying to "+
						"load a team table.");
				}
				if( (rlist.contains("location")||rlist.contains("city") )
					&&rlist.contains("name")
					&&(rlist.contains("league")||rlist.contains("leag"))
					&&(rlist.contains("team")||rlist.contains("team_id")||
					rlist.contains("teamid")||rlist.contains("id"))  ) {
					//OK
				}
				else
					throw new Exception("This does not appear to be team " +
						"data because headers given in first row of file is"+
						" not valid.\n"+headerString);
			}		
			//store column headers that were extracted from data file
			for(String s: rlist) {				
				originalHeaders.add(s);
				if( (isLoadCoaches && 
					Coach.getterNames.containsKey(s) ) ||
					(isLoadTeams && 
					Team.getterNames.containsKey(s) ) ) {
					preferredHeaders.add(s);		
					//System.out.println(s);		
				}	
				//System.out.println(s);
			}			
			//Parse and store each row of field values
			String result = null;
			while( (result = reader.readLine())!=null ) {//read file row data
				boolean res = Pattern.matches("^\\s*$",result);
				if(res) {
					//System.out.println("Row is blank!");
					continue;
				}
				result = result + " "; //allow all fields to be empty
				String[] parts = result.split(",");
				
				for(int i=0; i <parts.length; ++i) { 
					if(parts[i].equals("")) //allow all fields to be empty
						parts[i]=" ";
					//System.out.print("X"+parts[i]+"X");
				}	
				//System.out.println("size:" + parts.length);
				
					
				//Handle Coach type			
				if(isLoadCoaches) {					
					Coach coach = new Coach();					
					for(int i = 0; i < originalHeaders.size(); ++i) {
						//Get method name based on column header name
						String field = Coach.setterNames
							.get(originalHeaders.get(i));
						if(field==null) //Testcase header is not supported,
							continue;	//so... skip it			
						
						Coach.class.getMethod(field, String.class)
							.invoke(coach, parts[i].trim());
					}
					addRow(coach);	
					//System.out.println(coach);					
				}
				//Handle Team type
				else if(isLoadTeams) {
					Team team = new Team();					
					for(int i = 0; i < originalHeaders.size(); ++i) {
						//Get method name based on column header name
						String field = Team.setterNames
							.get(originalHeaders.get(i));
						if(field==null) //Testcase header is not supported,
							continue;	//so... skip it		
						
						Team.class.getMethod(field, String.class)
							.invoke(team, parts[i].trim());
							//.invoke(team, parts[i]);
					}
					addRow(team);		
					//System.out.println(team);	
				}					
			}
		}
		
		catch(Exception err) {
			//System.err.println("loadFile(String): " + err);
			//err.printStackTrace();
			throw err;
		}
	}
	
	/**
	* Create Coach or Team instance when provided with correct number of values.
	*
	* Precond: fieldValues are either 9 elements for Coach or 4 elements 
	* for Team.
	* Postcond: Return object instanceof of Coach or Team if ok, else null.
	*/
	private Object makeObject(String[] fieldValues) {
		if(clazz.getName().equalsIgnoreCase("Coach") ) {
			if(fieldValues.length!=coachHeaders.size()) {
				System.err.println("Coach type does not have "+
					coachHeaders.size() +" elements!");
				return null;
			}				
		}
		else if(clazz.getName().equalsIgnoreCase("Team")) {
			if(fieldValues.length!=teamHeaders.size()) {
				System.err.println("Team type does not have "+
					teamHeaders.size() +" elements!");
				return null;
			}
		}
		else {
			System.err.println("makeObject(String[]): unknown type " +
				clazz.getName() );
			return null;	
		}
		try {			
			//Handle Coach type			
			if(clazz.getName().equalsIgnoreCase("Coach")) {					
				Coach coach = new Coach();					
				for(int i = 0; i < coachHeaders.size(); ++i) {
					//Get setter method name based on column header name
					String field = Coach.setterNames
						.get(coachHeaders.get(i));
					if(field==null) //Testcase header is not supported,
						continue;	//so... skip it				
					//Remove potential + in field values
					if( coachHeaders.get(i).equals("first_name") ||	
						coachHeaders.get(i).equals("last_name") ) {
						fieldValues[i] = replacePlus(fieldValues[i]);	
					}					
					Coach.class.getMethod(field, String.class)
						.invoke(coach, fieldValues[i].trim());
				}
				return coach;	
				//System.out.println(coach);					
			}
			//Handle Team type
			else if(clazz.getName().equalsIgnoreCase("Team")) {
				Team team = new Team();					
				for(int i = 0; i < teamHeaders.size(); ++i) {
					//Get method name based on column header name
					String field = Team.setterNames
						.get(teamHeaders.get(i));
					if(field==null) //Testcase header is not supported,
						continue;	//so... skip it	
					//Remove potential + in field values
					if( teamHeaders.get(i).equals("location") ||	
						teamHeaders.get(i).equals("name") ) {
						fieldValues[i] = replacePlus(fieldValues[i]);	
					}					
					Team.class.getMethod(field, String.class)
						.invoke(team, fieldValues[i].trim());
				}
				return team;		
				//System.out.println(team);	
			}			
		}		
		catch(Exception err) {
			System.err.println("makeObject(String[]): " + err);
		}
		return null;
	}
	
	/**
	* Create object from field values and add to rows container.
	*
	* Precond: fieldvalues must have expected 9 values for Coach and 4 for Team.
	* Postcond: Return true if successful, otherwise false.
	*/
	public boolean addObject(String[] fieldValues) {
		Object o = makeObject(fieldValues);
		addRow(o);
		return o!=null;
	}
	
	/**
	* Add a coach to this table.
	* Pre: cmd.getCommand() is "add_coach" and cmd.getParameters() is String[]
	*	containing 9 values corresponding to each headers in coachHeaders.
	* Post: New row added to this table if successful.
	*/
	public void add_coach(Command cmd) {
		try {
			if(!isCoachType())
				throw new Exception("You are not Coach type.");
			if(cmd.getParameters().length!=coachHeaders.size())
				throw new Exception("Coach values do not match coach headers.");
			addObject(cmd.getParameters());
		}
		catch(Exception e) {
			System.err.println("add_coach(Command): " + e);
			System.err.println("USAGE: add_coach coach_id season first_name "+
				"last_name season_win season_loss playoff_win playoff_loss"+
				" team");
			System.err.println("EXAMPLE: add_coach EO01 2011 Even Odd 48 "+
				"34 3 4 WAC");
			System.err.println("EXAMPLE: add_coach EO01 2011 Even Smith+Jr 48 "+
				"34 3 4 WAC");	
		}			
	}
	
	/**
	* Add a team to this table.
	* Pre: cmd.getCommand() is "add_team" and cmd.getParameters() is String[]
	*	containing 4 values corresponding to each headers in teamHeaders.
	* Post: New row added to this table if successful.
	*/
	public void add_team(Command cmd) {
		try {
			if(!isTeamType())
				throw new Exception("You are not Team type.");
			if(cmd.getParameters().length!=teamHeaders.size())
				throw new Exception("Team values not match team headers.");	
			addObject(cmd.getParameters());
		}
		catch(Exception e) {
			System.err.println("add_team(Command): " + e);
			System.err.println("USAGE: add_team team_id location name league");
			System.err.println("EXAMPLE: add_team TB1 Tampa Bulls N");
			System.err.println("EXAMPLE: add_team TB1 New+York Bulls N");
		}	
	}
	
	/**
	* Prints to console all coaches with given last_name.
	* PRE: cmd.getCommand() is "coaches_by_name" and cmd.getParameters()[0]
	*	is non-spaced sequence of characters.
	* POST: Print to console result of search.
	*/
	public void coaches_by_name(Command cmd) {
		try {
			if(!isCoachType())
				throw new Exception("You are not Coach type.");
			if(cmd.getParameters().length!=1)
				throw new Exception("There must be one argument."); 	
			coaches_by_name(cmd.getParameters()[0].trim());
		}
		catch(Exception e) {
			System.err.println("coaches_by_name(Command): " + e);
			System.err.println("USAGE: coaches_by_name last_name");
			System.err.println("EXAMPLE: coaches_by_name Unseld");
			System.err.println("EXAMPLE: coaches_by_name end+end");
		}
	}
	
	/**
	* Prints to console all coaches with given last_name.
	* PRE: last_name is non-spaced sequence of characters.
	* POST: Print to console result of search.
	*/
	public void coaches_by_name(String last_name) {
		if(!clazz.getName().equalsIgnoreCase("Coach")) {
			System.err.println("Function coaches_by_name can only " +
				"provide information on coaches, not team info.");
			return;
		}	
		ArrayList<Object> arr = findElement(new Pair("last_name",last_name));
		for(Object o:arr)
			System.out.println(o);
	}
	
	/**
	* Prints to console all teams in given city.
	* PRE: cmd.getCommand() is "teams_by_city" and cmd.getParameters()[0] is
	*	non-spaced sequence of characters.
	* POST: Print result to console.
	*/
	public void teams_by_city(Command cmd) {
		try {
			if(!isTeamType())
				throw new Exception("You are not Team type.");
			if(cmd.getParameters().length!=1)
				throw new Exception("There must be one argument."); 	
			teams_by_city(cmd.getParameters()[0].trim());	
		}
		catch(Exception e) {
			System.err.println("teams_by_city(Command): " + e);
			System.err.println("USAGE: teams_by_city city_location");
			System.err.println("EXAMPLE: teams_by_city Washington");
			System.err.println("EXAMPLE: teams_by_city New+York");
		}
	}
	
	/**
	* Prints to console all teams in given city.
	* PRE: city is non-spaced sequence of characters.
	* POST: Print result to console.
	*/
	public void teams_by_city(String city) {
		if(!clazz.getName().equalsIgnoreCase("Team")) {
			System.err.println("Function teams_by_city provides only team " +
				"information, no coach stuff.");
			return;
		}
		ArrayList<Object> arr = findElement(new Pair("location",city));
		for(Object o:arr)
			System.out.println(o);
	}
	
	/**
	* Prints to console the winningest coach for a given season year.
	* PRE: cmd.getCommand() is "best_coach" and cmd.getParameters()[0] is
	*	four character year.
	* POST: Print result to console.
	*/
	public void best_coach(Command cmd) {
		try {
			if(!isCoachType())
				throw new Exception("You are not Coach type.");
			if(cmd.getParameters().length!=1)
				throw new Exception("There must be one argument."); 	
			best_coach(cmd.getParameters()[0].trim());	
		}
		catch(Exception e) {
			System.err.println("best_coach(Command): " + e);
			System.err.println("USAGE: best_coach YYYY");
			System.err.println("EXAMPLE: best_coach 1993");
		}
	}
	
	/**
	* Prints to console the winningest coach for a given season year.
	* PRE: season is four digit year.
	* POST: Print result to console.
	*/
	public void best_coach(Integer season) {
		best_coach(season.toString());
	}
	
	/**
	* Prints to console the winningest coach for a given season year.
	* PRE: season is four digit year.
	* POST: Print result to console.
	*/
	/*
	public void best_coach2(String season) {
		if(!clazz.getName().equalsIgnoreCase("Coach")) {
			System.err.println("Function best_coach can only " +
				"provide information on coaches, not team info.");
			return;
		}	
		ArrayList<Object> arr = findElement(new Pair("season",season));
		Object bestCoach = rows.get(0);
		int max = (((Coach)bestCoach).getSeasonWin().intValue()-
			((Coach)bestCoach).getSeasonLoss().intValue()) + 
			(((Coach)bestCoach).getPlayoffWin().intValue()-
			((Coach)bestCoach).getPlayoffLoss().intValue());
		int temp;
		for(Object o:arr) {
			temp = (((Coach)o).getSeasonWin().intValue()-
				((Coach)o).getSeasonLoss().intValue()) + 
				(((Coach)o).getPlayoffWin().intValue()-
				((Coach)o).getPlayoffLoss().intValue());
			if(temp>max) {
				max = temp;
				bestCoach=o;	
			}	
		}
		System.out.println(((Coach)bestCoach).getFirstName() + " " +
			((Coach)bestCoach).getLastName());
	}
	*/
	public void best_coach(String season) {
		if(!clazz.getName().equalsIgnoreCase("Coach")) {
			System.err.println("Function best_coach can only " +
				"provide information on coaches, not team info.");
			return;
		}	
		try {
			ArrayList<Object> arr = findElement(new Pair("season",season));
			Coach bestCoach = (Coach)rows.get(0);
			int seasonWin = bestCoach.getSeasonWin().trim().equals("")?0:
				Integer.parseInt(bestCoach.getSeasonWin());
			int seasonLoss = bestCoach.getSeasonLoss().trim().equals("")?0:
				Integer.parseInt(bestCoach.getSeasonLoss());
			int playoffWin = bestCoach.getPlayoffWin().trim().equals("")?0:
				Integer.parseInt(bestCoach.getPlayoffWin());
			int playoffLoss = bestCoach.getPlayoffLoss().trim().equals("")?0:
				Integer.parseInt(bestCoach.getPlayoffLoss());
		
			int max = (seasonWin-seasonLoss) + (playoffWin-playoffLoss);
			int temp;
			for(Object o:arr) {
				Coach c = (Coach)o;
				seasonWin = c.getSeasonWin().trim().equals("")?0:
					Integer.parseInt(c.getSeasonWin());
				seasonLoss = c.getSeasonLoss().trim().equals("")?0:
					Integer.parseInt(c.getSeasonLoss());
				playoffWin = c.getPlayoffWin().trim().equals("")?0:
					Integer.parseInt(c.getPlayoffWin());	
				playoffLoss = c.getPlayoffLoss().trim().equals("")?0:
					Integer.parseInt(c.getPlayoffLoss());		
				
				temp = (seasonWin-seasonLoss) + (playoffWin-playoffLoss);
				if(temp>max) {
					max = temp;
					bestCoach=c;	
				}	
			}
			System.out.println(bestCoach.getFirstName() + " " +
				bestCoach.getLastName());
		}
		catch(Exception e) {
			System.err.println("best_coach(String): "+e);
		}	
	}
	
	/**
	* Search coaches based on field=value criteria and prints to console.
	*
	* PRE:: Command provides array of parameters, each of the form
	* 	field=value.
	* POST: Print result to console.
	*/
	public void search_coaches(Command cmd) {
		try {			
			if(!isCoachType()) {				
				throw new Exception("Caller is not Coach type.");
			}
			if(cmd.getParameters().length==0) {
				throw new Exception("Incorrect syntax.");
			}
			search_coaches(cmd,true);			
		}
		catch(Exception e) {
			System.err.println("search_coaches(Command): " + e);	
			System.err.println("USAGE: search_coaches fieldName=fieldValue"+
					" [fieldName=fieldValue]...");	
			System.err.println("EXAMPLE: search_coaches lastname=Unseld"+
				" season_win=30");	
			System.err.println("EXAMPLE: delete_coaches lastname=Van+Gundy"+
				" season_win=30");			
		}		
	}
	
	/**
	* Search coaches based on field=value criteria and prints to console.
	*
	* PRE:: Command provides array of parameters, each of the form
	* 	field=value.
	* POST: Return list of Coach object.
	*/	
	private ArrayList<Object> search_coaches(Command cmd,boolean toConsole) 
		throws Exception {
		try {
			ArrayList<Pair> pairs = new ArrayList<Pair>();
			String[] parameters = cmd.getParameters();
			String[] pair = null;		
			for(int i=0; i < parameters.length; ++i) {
				pair = parameters[i].split("=");
				pairs.add(new Pair(pair[0].trim(),pair[1].trim()));	
				//System.out.println(pair[0] + " " + pair[1]);	
			}
			Pair[] parr = new Pair[pairs.size()];//each pair is fieldName,value
			pairs.toArray(parr);
			ArrayList<Object> arr = findElement(parr);
			//for(Object p:arr)
			//	System.out.println(p);
			if(toConsole) {
				for(Object o:arr)
					System.out.println(o);
			}
			return arr;
		}
		catch(Exception e) {
			throw e;
		}
	}
	
	/**
	* Delete coaches based on search criteria of form field=value.
	*
	* PRE:  Command provides array of parameters, each of the form
	* 	field=value.
	* POST: Rows matching criteria are removed from this table.
	*/
	public void delete_coaches(Command cmd) {		
		try {			
			if(!isCoachType()) {				
				throw new Exception("Caller is not Coach type.");
			}
			if(cmd.getParameters().length==0) {
				throw new Exception("Incorrect syntax.");
			}
			ArrayList<Object> list = search_coaches(cmd,false);
			rows.removeAll(list);		
		}
		catch(Exception e) {
			System.err.println("delete_coaches(Command): " + e);	
			System.err.println("USAGE: delete_coaches fieldName=fieldValue"+
					" [fieldName=fieldValue]...");	
			System.err.println("EXAMPLE: delete_coaches lastname=Unseld"+
				" season_win=30");	
			System.err.println("EXAMPLE: delete_coaches lastname=Van+Gundy"+
				" season_win=30");			
		}	
	}
	
	/**
	* Replaces + character with a single space.
	* PRE: fieldValue may contain + char.
	* POST: Return fieldValue but with all + char replaced by single space.
	*/
	public String replacePlus(String fieldValue) {
		Pattern patt = Pattern.compile("\\+");
		Matcher match = patt.matcher(fieldValue);		
		return match.replaceAll(" ");	
	}
	
	/**
	* Find element in container rows.
	*
	* PRE: args is variable-length of Pair type.  Pair contains
	* 	fieldname=fieldvalue as data members "name" and "value".
	* POST: Return list of Coach/Team type objects or empty.
	*/	
	public ArrayList<Object> findElement(Pair...args) {				
		int sz = rows.size();		
		ArrayList<Object> list = new ArrayList<Object>();//hold Coach or Team
		Object o;
		
		//for(Pair p: args)
		//	System.out.println("XX"+p.name+"XXXX"+p.value+"XX");
		
		for(int i = 0; i < sz; ++i) {
			o = rows.get(i);
			//System.out.println("BEFORE: " +o); //OK
			if(doesSatisfyCondition(o,args) ) {
				list.add(o);		
				//System.out.println(o); //FAILED 	
			}	
		}	
		
		//for(Object oo:list)
		//	System.out.println("AFTER: "+oo);		
			
		return list;	
	}
	
	/**
	* Check if Coach/Team satisfies condition(s) in args.
	* PRE: obj is Coach/Team instance from table to be compared to list of
	*	criteria contained in Pair[].  Each Pair has field name and field value
	*	as given by user and to be used to match Coach/Team in this table.
	*	NOTE: Criteria specified by args are performed as AND or intersection
	*	of individual criterion.
	*POST: Return true if all criteria per args are met; otherwise if any of
	*	the criteria failed.
	*/
	private boolean doesSatisfyCondition(Object obj, Pair...args) {		
		try {			
			String methodName = null;	
			//for(Pair p: args)
			//	System.out.println(p);	//OK	
			for(Pair pair:args) {
				//System.out.println(pair); //9 1992's  2 1993's
				if(clazz.getName().equalsIgnoreCase("Coach") ) {
					methodName=Coach.getterNames.get(pair.name);
					//replace potential + in field values
					if( pair.name.equalsIgnoreCase("first_name") ||	
						pair.name.equalsIgnoreCase("firstname") ||
						pair.name.equalsIgnoreCase("last_name") ||
						pair.name.equalsIgnoreCase("lastname") ) {
						pair.value = replacePlus(pair.value);	
					}		
				}
				else if(clazz.getName().equalsIgnoreCase("Team") ) {
					methodName=Team.getterNames.get(pair.name);	
					//replace potential + in field values
					if( pair.name.equalsIgnoreCase("location") ||	
						pair.name.equalsIgnoreCase("name") ) {
						pair.value = replacePlus(pair.value);	
					}					
				}
				else {
					//System.err.println("Unknown type: " + clazz.getName());
					throw new Exception("Unknown T type: " + clazz.getName());
				}
				
				if(methodName==null) {
					throw new Exception("Unknown field name: " + pair.name);
				}								
				
				if(!clazz.getMethod(methodName).invoke(obj).toString()
					.equalsIgnoreCase(pair.value) ) {
					//System.out.println(pair);
					
					
					return false;						
				}
			}
		}	
		catch(Exception err) {
			System.err.println("doesSatisfyCondition(Object,Pair...): " + err);
			return false;
		}
		
		//System.out.println(obj);
		return true;
	}
	
	/**
	* Display rows in nice format.
	* Implementatin for commands: print_coaches and print_teams.
	* PRE: n/a
	* POST: Return formatted string of all rows in this table.
	*/
	public String toString() {
		StringBuilder temp = new StringBuilder();
		for(int i = 0; i < rows.size(); ++i) {
			temp.append(rows.get(i).toString());	
			if(i < rows.size()-1)
				temp.append("\n");	
		}
		//System.out.println(temp);
		return temp.toString();
	}
	
	/**
	* Print this table to stdout.
	*
	*/
	public void print_coaches() {
		System.out.println(this);
	}
	
	/**
	* Print this table to stdout.
	*
	*/
	public void print_teams() {
		System.out.println(this);
	}
	
	
	
	/*
	public static void main(String[] args) {		
		Table<Coach> coaches = new Table<Coach>("coaches", Coach.class);
		String [] c1 = {"c1.txt"};
		coaches.loadFile(new Command("load_coaches",c1));
		//System.out.println(coaches);
		String[] c = {"EO01","2011","Even","Odd","48","34","3","4","WAC"};
		coaches.addObject(c);
		System.out.println(coaches);
		Table<Team> teams = new Table<Team>("teams", Team.class);
		String[] t1 = {"t1.txt"};
		teams.loadFile(new Command("load_teams",t1));
		//System.out.println(teams);
		String[] t = {"TB1","Tampa","Bulls","N"};
		teams.addObject(t);
		System.out.println(teams);
		
		coaches.coaches_by_name("Unseld");
		coaches.coaches_by_name("end+end");
		teams.teams_by_city("Washington");
		coaches.best_coach(1993);
		String[] arr = {"last_name=Unseld","season_win=30"};
		coaches.delete_coaches(new Command("search_coaches",arr));
		System.out.println(coaches);
		coaches.delete_coaches(new Command("search_coaches",arr));
		System.out.println(coaches);
		//System.out.println(coaches.findElement("last_name","xend+end"));
		//coaches.findElement("coaches_by_name","sspp");
	}
	*/

}


































