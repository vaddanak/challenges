/*
	Author:  Vaddanak Seng
	Purpose:  Stored procedure to execute multiple queries.
*/

/*
	PURPOSE:  Find the tier based on cost of make of car.
	INPUT:  car_make is make of car found in cars table
			num_of_tiers is number of tiers or categories based on cost.
			setting num_of_tiers to NULL default to 10 tiers.
	RETURN:  integer value representing tier into which cost of car_make falls
*/
DROP FUNCTION IF EXISTS insurance.get_tier;
DELIMITER |
CREATE FUNCTION insurance.get_tier (car_make TEXT, num_of_tiers INT)
	RETURNS INT
	NOT DETERMINISTIC
BEGIN
	DECLARE avg INT;
	DECLARE number_of_tiers INT DEFAULT 10;
	DECLARE min_price, max_price INT;
	DECLARE tier_group_count INT;
	DECLARE tier_part INT;
	DECLARE counter INT DEFAULT 1;
	DECLARE limit_whole, limit_part INT;
	DECLARE target_price INT;
	
	/* set number of tiers */
	IF (ISNULL(num_of_tiers) OR num_of_tiers<1 OR conv(num_of_tiers,10,10)<1)
		THEN SET number_of_tiers = 10;
		ELSE SET number_of_tiers = num_of_tiers;
	END IF;
	#SET number_of_tiers = IFNULL(num_of_tiers, 10);
	
	/* get price based on make of car */
	SELECT AVG(insurance.cars.cost) INTO target_price
	FROM insurance.cars
	WHERE insurance.cars.make = car_make;
	
	/* car make not found */
	IF (ISNULL(target_price))
		THEN RETURN 0;
	END IF;
	
	/* group base on price and get count of group */
	SELECT COUNT(grouped.cost) INTO tier_group_count
	FROM 
		(SELECT *
	 	FROM insurance.cars
	 	GROUP BY insurance.cars.cost) AS grouped;
	 	
	IF (number_of_tiers > tier_group_count)
		THEN SET number_of_tiers = tier_group_count;
	END IF;	 	
	
	/*  */
	SET tier_part = FLOOR(tier_group_count / number_of_tiers);
	SET limit_part = tier_part;
	
	WHILE (counter <= number_of_tiers) DO
		/*  */
		IF (counter < number_of_tiers)
			THEN SET limit_whole = counter * tier_part;
			ELSE SET limit_whole = tier_group_count;
				 SET limit_part = tier_group_count-((counter-1)*tier_part);
		END IF;
		/* get min and max price of sub-group, ie 1...number_of_tiers */
		SELECT MIN(grouped.cost), MAX(grouped.cost) INTO min_price, max_price
		FROM 
			(SELECT *
			 FROM insurance.cars
			 GROUP BY insurance.cars.cost 
			 ORDER BY insurance.cars.cost LIMIT limit_whole) AS grouped
		ORDER BY grouped.cost DESC
		LIMIT limit_part;
		/* check for target range */
		IF (target_price >= min_price AND target_price<= max_price)
			THEN RETURN counter;
		END IF;
		/* increment to next sub-group */
		SET counter = counter + 1;
	
	END WHILE;     
    
    /* car make is unknown, tier range is 1...number_of_tiers, default is 10 */
    RETURN 0;
    
    
END;|
DELIMITER ;  

DROP FUNCTION IF EXISTS insurance.getTier;
DELIMITER |
CREATE FUNCTION insurance.getTier (car_make TEXT, num_of_tiers INT)
	RETURNS INT
	NOT DETERMINISTIC
BEGIN
	DECLARE avg INT;
	DECLARE number_of_tiers INT DEFAULT 10;
	DECLARE min_price, max_price INT;
	DECLARE tier_group_count INT;
	DECLARE tier_part INT;
	DECLARE counter INT DEFAULT 1;
	DECLARE limit_whole, limit_part INT;
	DECLARE target_price INT;
	
	/* set number of tiers */
	IF (ISNULL(num_of_tiers) OR num_of_tiers<1 OR conv(num_of_tiers,10,10)<1)
		THEN SET number_of_tiers = 10;
		ELSE SET number_of_tiers = num_of_tiers;
	END IF;
	#SET number_of_tiers = IFNULL(num_of_tiers, 10);
	
	/* get price based on make of car */
	SELECT AVG(insurance.cars.cost) INTO target_price
	FROM insurance.cars
	WHERE insurance.cars.make = car_make;
	
	/* car make not found */
	IF (ISNULL(target_price))
		THEN RETURN 0;
	END IF;
	
	/* group base on price and get count of group */
	SELECT COUNT(grouped.cost) INTO tier_group_count
	FROM 
		(SELECT *
	 	FROM insurance.cars
	 	GROUP BY insurance.cars.cost) AS grouped;
	 	
	IF (number_of_tiers > tier_group_count)
		THEN SET number_of_tiers = tier_group_count;
	END IF;	 	
	
	/*  */
	SET tier_part = FLOOR(tier_group_count / number_of_tiers);
	SET limit_part = tier_part;
	
	WHILE (counter <= number_of_tiers) DO
		/*  */
		IF (counter < number_of_tiers)
			THEN SET limit_whole = counter * tier_part;
			ELSE SET limit_whole = tier_group_count;
				 SET limit_part = tier_group_count-((counter-1)*tier_part);
		END IF;
		/* get min and max price of sub-group, ie 1...number_of_tiers */
		SELECT MIN(grouped.cost), MAX(grouped.cost) INTO min_price, max_price
		FROM 
			(SELECT *
			 FROM insurance.cars
			 GROUP BY insurance.cars.cost 
			 ORDER BY insurance.cars.cost LIMIT limit_whole) AS grouped
		ORDER BY grouped.cost DESC
		LIMIT limit_part;
		/* check for target range */
		IF (target_price >= min_price AND target_price<= max_price)
			THEN RETURN counter;
		END IF;
		/* increment to next sub-group */
		SET counter = counter + 1;
	
	END WHILE;     
    
    /* car make is unknown, tier range is 1...number_of_tiers, default is 10 */
    RETURN 0;
    
    
END;|
DELIMITER ;  

#SELECT insurance.get_tier('Scion', NULL);
#SELECT get_tier('Jeep', 4);



/*
	PURPOSE:  Find all license plate in policy table for given user.
	INPUT:  username
	RETURN: comma-separated list of licenses in single string.
*/
DROP FUNCTION IF EXISTS insurance.getAllLicensePlates;
DELIMITER |
CREATE FUNCTION insurance.getAllLicensePlates (usn TEXT)
	RETURNS TEXT
	NOT DETERMINISTIC
BEGIN	
	DECLARE licenses TEXT DEFAULT NULL;
	DECLARE license_plate TEXT DEFAULT '';
	DECLARE counter INT DEFAULT 1;
	DECLARE limiter INT DEFAULT 0;
	
	SET limiter = (SELECT COUNT(license) FROM insurance.policy WHERE username=usn);
	
	REPEAT
		#SET licenses = (select license from policy where username='arichardsrr');
		
		SELECT p.license INTO license_plate
		FROM (SELECT license
			  FROM insurance.policy
			  WHERE username=usn
			  ORDER BY license ASC
			  LIMIT counter) AS p
		ORDER BY p.license DESC
		LIMIT 1;
		
		SET licenses = IF(ISNULL(licenses),license_plate,
			CONCAT_WS(",",licenses,license_plate)); 	
    	SET counter = counter + 1;
    UNTIL counter > limiter
    END REPEAT;
    
    
    RETURN licenses;
    
    
END;|
DELIMITER ;  

#select getAllLicensePlates('arichardsrr'); 


/*
	PURPOSE:  Find all policies in policy table for given user.
	INPUT:  username
	RETURN: comma-separated list of pids in single string.
*/
DROP FUNCTION IF EXISTS insurance.getAllPolicies;
DELIMITER |
CREATE FUNCTION insurance.getAllPolicies (usn TEXT)
	RETURNS TEXT
	NOT DETERMINISTIC
BEGIN	
	DECLARE pids TEXT DEFAULT NULL;
	DECLARE pid_one TEXT DEFAULT '';
	DECLARE counter INT DEFAULT 1;
	DECLARE limiter INT DEFAULT 0;
	
	SET limiter = (SELECT COUNT(pid) FROM insurance.policy WHERE username=usn);
	
	REPEAT				
		SELECT p.pid INTO pid_one
		FROM (SELECT pid
			  FROM insurance.policy
			  WHERE username=usn
			  ORDER BY pid ASC
			  LIMIT counter) AS p
		ORDER BY p.pid DESC
		LIMIT 1;
		
		SET pids = IF(ISNULL(pids),pid_one, CONCAT_WS(",",pids,pid_one)); 	
    	SET counter = counter + 1;
    UNTIL counter > limiter
    END REPEAT;    
    
    RETURN pids;    
    
END;|
DELIMITER ;  

#select getAllPolicies('arichardsrr'); 


/*
	PURPOSE:  Calculate premium for given policy pid.
	INPUT:  policy pid
	RETURN: sum of collision, personal, property, and bodily
*/
DROP FUNCTION IF EXISTS insurance.getPremium;
DELIMITER |
CREATE FUNCTION insurance.getPremium (policy_pid INT)
	RETURNS REAL
	NOT DETERMINISTIC
BEGIN	
	DECLARE pids TEXT DEFAULT NULL;
	DECLARE pid_one TEXT DEFAULT '';
	DECLARE counter INT DEFAULT 1;
	DECLARE limiter INT DEFAULT 0;
	DECLARE col TEXT;
	DECLARE per TEXT;
	DECLARE prop TEXT;
	DECLARE bod TEXt;
	DECLARE prem DOUBLE;
	
	SELECT bodily, personal, property, collision INTO bod, per, prop, col
	FROM insurance.policy
	WHERE insurance.policy.pid = policy_pid;
	
	SET prem = CAST(bod AS DECIMAL(20,5)) + CAST(per AS DECIMAL(20,5)) + 
		CAST(prop AS DECIMAL(20,5))	+ CAST(col AS DECIMAL(20,5));
	    
    RETURN prem;    
    
END;|
DELIMITER ;  

#select getPremium(111); 

















