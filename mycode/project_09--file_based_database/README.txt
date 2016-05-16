*** Extract program files from tar file ***
$ tar xvf proj1-42941752.tar

*** Program files included: ***
1) Command.java
2) CommandParser.java
3) P1.java
4) Coach.java
5) Team.java
6) Table.java
7) Pair.java
8) README.txt

*** Compile program: ***
$ javac P1.java

This will create a new file called P1.class

*** Run program: ***
$ java P1

PLEASE NOTE:
Comparison, like when searching based on criteria, is case-insensitive.

The table schemas are strictly adhered per project description.
For example, coach_id is only uppercase or lowercase letters and/or digits (alphanumeric).
Season is 4 digit year, even for unreasonable years like 0000 or 9999.
team_id is capital letters and/or digits.
league is only one capital letter.

If data are introduced that violate schemas, then exception will be thrown,
caught, and message displayed to provide helpful tips.  The program should not
crash upon invalid data.  However, invalid data will not be added to table.

When enter coach or team on command line, names consisting of two words should
be concatenated using + to replace any space separating them, for example,
New York becomes New+York.

The criteria used in the following commands are considered to be AND or
intersection of the individual criterion:
search_coaches lastname=Unseld season_win=30
delete_coaches lastname=Unseld season_win=30

For example, search_coaches lastname=Unseld season_win=30 is interpreted as
search_coaches lastname=Unseld AND season_win=30 .
