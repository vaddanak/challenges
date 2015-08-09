"""
A collection of some functions.
"""

from __future__ import unicode_literals;
from __future__ import print_function;
from __future__ import division;

#SyntaxError: future feature import_absolute is not defined
#from __future__ import import_absolute;
from __future__ import absolute_import;

import io;

def file_stats(filename):
	'''
	Returns tuple of line numbers, word count, and character count of text
	content in filename.
	'''
	n_lines = n_words = n_chars = 0;
	fileObject = io.open(filename, mode='r');
	for line in fileObject:
		n_lines += 1;
		n_chars += len(line);
		n_words += len(line.split());
	return (n_lines, n_words, n_chars);
	
def sendmail():
	'''
	Fn to test smtp.
	'''
	import smtplib;
	sender = 'vaddanak@gmail.com';
	receivers = ['vaddanak@gmail.com','vaddanak@mail.usf.edu'];
	message = '''\
		From: Vad Seng <vaddanak@gmail.com>
		To: Me Myself I <vaddanak@mail.usf.edu>
		Subject: Testing smtp
		
		Hello world!
		'''
	try:
		smtpObject = smtplib.SMTP('smtp.gmail.com', 587);
		smtpObject.ehlo();
		smtpObject.starttls();
		smtpObject.login(user='vaddanak', password='ttgg8771')
		smtpObject.sendmail(from_addr=sender, to_addrs=receivers, msg=message);
		smtpObject.quit();
		print('PASS: Message sent!');
	except smtplib.SMTPException as err:
		print('FAIL: ', err);	
		
def htmlemail():
	'''
	HTML email.
	'''
	import smtplib;		
	#from email.mime.multipart import MIMEMultipart as parts;
	import base64;
	import io;
	
	_from = 'vaddanak@gmail.com';
	to = ['vaddanak@gmail.com'];
	msg = '''From: vad seng <vaddanak@gmail.com>
		To: vad seng <vaddanak@gmail.com>
		Mime-Versin: 1.0
		Content-type: text/html
		Subject: test html email
		
		Testing html email.
		
		This is <b>bold</b>.
		'''
		
	fileName = 'test.txt';	
	fileObject = io.open(fileName, 'rb');
	fileContent = fileObject.read();
	fileContentEncoded = base64.b64encode(fileContent);	
		
	#print(fileContent); #Content of test file
	#print(fileContentEncoded); #Q29udGVudCBvZiB0ZXN0IGZpbGUK
		
	marker = 'AUNIQUEMARKER';
	body = 'This is a test email with file attachment.';
	
	part1 = '''From: vad seng <vaddanak@gmail.com>
		To: vad seng <vaddanak@gmail.com>
		Subject: test file attachment
		MIME-Version: 1.0
		Content-Type: multipart/mixed; boundary=%s
		--%s
		''' % (marker, marker);
		
	part2 = '''Content-Type: text/plain
		Content-Transfer-Encoding:8bit
		
		%s
		--%s
		''' % (body, marker);
		
	part3 = '''Content-Type: multipart/mixed; name=\"%s\"
		Content-Transfer-Encoding:base64
		Content-Disposition: attachment; filename=%s
		
		%s
		--%s--''' % (fileName, fileName, fileContentEncoded, marker);
	
	#msg = part1 + part2 + part3; # not work
	
	#this works and formats correctly in gmail, yea!
	msg = '\r\n'.join(['From: vaddanak@gmail.com', 'To: vaddanak@gmail.com',
		'Subject: testing', '', 'Something interesint']);
		
	try:
		#mp = parts();
		smtpObject = smtplib.SMTP('smtp.gmail.com', 587);
		smtpObject.ehlo();
		smtpObject.starttls();
		smtpObject.login('vaddanak', 'ttgg8771');
		smtpObject.sendmail(_from,to,msg);
		print('PASS');
	except smtplib.SMTPException as err:
		print('FAIL: ', err);	
	
def reverseDictionary(keyToValueDict):
	'''
	Fn reverses key <--> value
	starts with {key1:value1, key2:value2}
	returns {value1:key1, value2:key2}
	'''
	reversedDict = {};
	for key, value in keyToValueDict.items():	
		reversedDict[value] = key;
	return reversedDict;
	
def printDictionary(keyToValueDictionary):
	'''
	Prints dictionary to sys.stdout
	'''
	import sys;
	longest = determineLongestItemLength(list(keyToValueDictionary.keys()));
	for key, value in keyToValueDictionary.items():
		sys.stdout.write('{a:{len:}s} : {b:{len:}s}\n'\
			.format(a=key,b=value, len=longest) );
		
def determineLongestItemLength(listOfStrings):
	'''
	Input is list of strings, ie ['cat', 'house', 'sugar']
	Fn looks at each string and determines the longest length of all the items,
	in this case, it would be len['house'], so it would return 5.
	'''
	longest = len(listOfStrings[0]);
	for string in listOfStrings:
		if len(string) > longest:
			longest = len(string);
	return longest;
	
def findRoot(function, lower, upper, tolerance):
	'''
	The function is positive on one end of the root and negative on the other
	end of the root.  The lower and upper are ends of an interval around the
	root.  f(a)*f((a+b)/2) will tell us if the midpoint is on the same side
	as a or b; if product is positive, then midpoint is on same side as a. But
	if it is negative, then midpoint is on same side as b.
	'''
	while upper-lower > tolerance:
		midpoint = (upper+lower)/2.0;
		if function(midpoint) * function(lower) > 0.0:
			lower = midpoint;
		else:
			upper = midpoint;
			
	return (lower, upper);
	
def calculateStat(*tupleOfNumbers):
	'''
	Fn finds lowest number, mean, and largest number and 
	returns (lowest, mean, largest)
	
	If input was originally a list or tuple, then function will fail, ie
	calculateStat( [...] ) or calculateStat( (...) ) -- FIXED
	
	Passed-in argument should be integers separated by comma
	for example calculateStat(2, 4, 6, 1, 4, ...)
	
	Fn can also handle an empty input.
	'''	
	if len(tupleOfNumbers) and \
		(type(tupleOfNumbers[0])==type([]) or type(tupleOfNumbers[0])==type(())):
		tupleOfNumbers = tupleOfNumbers[0];
	total = 0.0 if len(tupleOfNumbers)>0 else None;
	lowest = largest = tupleOfNumbers[0] if len(tupleOfNumbers)>0 else None;
	for num in tupleOfNumbers:
		total += num;
		if num < lowest:
			lowest = num;
		if num > largest:
			largest = num;
	return (lowest, total/len(tupleOfNumbers) if len(tupleOfNumbers)>0 else None,
		largest); #indent to allow long expression to extend to multiple lines
	
	
	
	
		
names = {
    'H':  'hydrogen',
    'He': 'helium',
    'Li': 'lithium',
    'Be': 'beryllium',
    'B':  'boron',
    'C':  'carbon',
    'N':  'nitrogen',
    'O':  'oxygen',
    'F':  'fluorine',
    'Ne': 'neon',
    'Na': 'sodium',
    'Mg': 'magnesium',
    'Al': 'aluminium',
    'Si': 'silicon',
    'P':  'phosphorus',
    'S':  'sulphur',
    'Cl': 'chlorine',
    'Ar': 'argon',
    'K':  'potassium',
    'Ca': 'calcium',
    'Sc': 'scandium',
    'Ti': 'titanium',
    'V':  'vanadium',
    'Cr': 'chromium',
    'Mn': 'manganese',
    'Fe': 'iron',
    'Co': 'cobalt',
    'Ni': 'nickel',
    'Cu': 'copper',
    'Zn': 'zinc',
    'Ga': 'gallium',
    'Ge': 'germanium',
    'As': 'arsenic',
    'Se': 'selenium',
    'Br': 'bromine',
    'Kr': 'krypton',
    'Rb': 'rubidium',
    'Sr': 'strontium',
    'Y':  'yttrium',
    'Zr': 'zirconium',
    'Nb': 'niobium',
    'Mo': 'molybdenum',
    'Tc': 'technetium',
    'Ru': 'ruthenium',
    'Rh': 'rhodium',
    'Pd': 'palladium',
    'Ag': 'silver',
    'Cd': 'cadmium',
    'In': 'indium',
    'Sn': 'tin',
    'Sb': 'antimony',
    'Te': 'tellurium',
    'I':  'iodine',
    'Xe': 'xenon',
    'Cs': 'caesium',
    'Ba': 'barium,',
    'La': 'lanthanum',
    'Ce': 'cerium',
    'Pr': 'praesodymium',
    'Nd': 'neodymium',
    'Pm': 'promethium',
    'Sm': 'samarium',
    'Eu': 'europium',
    'Gd': 'gadolinium',
    'Tb': 'terbium',
    'Dy': 'dysprosium',
    'Ho': 'holmium',
    'Er': 'erbium',
    'Tm': 'thulium',
    'Yb': 'ytterbium',
    'Lu': 'lutetium',
    'Hf': 'hafnium',
    'Ta': 'tantalum',
    'W':  'tungsten',
    'Re': 'rhenium',
    'Os': 'osmium',
    'Ir': 'iridium',
    'Pt': 'platinum',
    'Au': 'gold',
    'Hg': 'mercury',
    'Tl': 'thallium',
    'Pb': 'lead',
    'Bi': 'bismuth',
    'Po': 'polonium',
    'At': 'astatine',
    'Rn': 'radon',
    'Fr': 'francium',
    'Ra': 'radium',
    'Ac': 'actinium',
    'Th': 'thorium',
    'Pa': 'protactinium',
    'U':  'uranium',
};
		
chemicals = {
    'H':  ('hydrogen',	1,	20.28),
    'He': ('helium',	2,	4.22),
    'Li': ('lithium',	3,	1615.0),
    'Be': ('beryllium',	4,	2742.0),
    'B':  ('boron',	5,	4200.0),
    'C':  ('carbon',	6,	5100.0),
    'N':  ('nitrogen',	7,	77.36),
    'O':  ('oxygen',	8,	90.20),
    'F':  ('fluorine',	9,	85.03),
    'Ne': ('neon',	10,	27.07),
    'Na': ('sodium',	11,	1156.0),
    'Mg': ('magnesium',	12,	1363.0),
    'Al': ('aluminium',	13,	2792.0),
    'Si': ('silicon',	14,	3538.0),
    'P':  ('phosphorus',	15,	553.0),
    'S':  ('sulphur',	16,	717.8),
    'Cl': ('chlorine',	17,	239.11),
    'Ar': ('argon',	18,	87.30),
    'K':  ('potassium',	19,	1032.0),
    'Ca': ('calcium',	20,	1757.0),
    'Sc': ('scandium',	21,	3109.0),
    'Ti': ('titanium',	22,	3560.0),
    'V':  ('vanadium',	23,	3680.0),
    'Cr': ('chromium',	24,	2944.0),
    'Mn': ('manganese',	25,	2334.0),
    'Fe': ('iron',	26,	3134.0),
    'Co': ('cobalt',	27,	3200.0),
    'Ni': ('nickel',	28,	3186.0),
    'Cu': ('copper',	29,	2835.0),
    'Zn': ('zinc',	30,	1180.0),
    'Ga': ('gallium',	31,	2477.0),
    'Ge': ('germanium',	32,	3106.0),
    'As': ('arsenic',	33,	887.0),
    'Se': ('selenium',	34,	958.0),
    'Br': ('bromine',	35,	332.0),
    'Kr': ('krypton',	36,	119.93),
    'Rb': ('rubidium',	37,	961.0),
    'Sr': ('strontium',	38,	1655.0),
    'Y':  ('yttrium',	39,	3609.0),
    'Zr': ('zirconium',	40,	4682.0),
    'Nb': ('niobium',	41,	5017.0),
    'Mo': ('molybdenum',	42,	4912.0),
    'Tc': ('technetium',	43,	5150.0),
    'Ru': ('ruthenium',	44,	4423.0),
    'Rh': ('rhodium',	45,	3968.0),
    'Pd': ('palladium',	46,	3236.0),
    'Ag': ('silver',	47,	2435.0),
    'Cd': ('cadmium',	48,	1040.0),
    'In': ('indium',	49,	2345.0),
    'Sn': ('tin',	50,	2875.0),
    'Sb': ('antimony',	51,	1860.0),
    'Te': ('tellurium',	52,	1261.0),
    'I':  ('iodine',	53,	457.4),
    'Xe': ('xenon',	54,	165.03),
    'Cs': ('caesium',	55,	944.0),
    'Ba': ('barium,',	56,	2170.0),
    'La': ('lanthanum',	57,	3737.0),
    'Ce': ('cerium',	58,	3716.0),
    'Pr': ('praesodymium',	59,	3793.0),
    'Nd': ('neodymium',	60,	3347.0),
    'Pm': ('promethium',	61,	3273.0),
    'Sm': ('samarium',	62,	2067.0),
    'Eu': ('europium',	63,	1802.0),
    'Gd': ('gadolinium',	64,	3546.0),
    'Tb': ('terbium',	65,	3503.0),
    'Dy': ('dysprosium',	66,	2840.0),
    'Ho': ('holmium',	67,	2993.0),
    'Er': ('erbium',	68,	3503.0),
    'Tm': ('thulium',	69,	2223.0),
    'Yb': ('ytterbium',	70,	1469.0),
    'Lu': ('lutetium',	71,	3675.0),
    'Hf': ('hafnium',	72,	4876.0),
    'Ta': ('tantalum',	73,	5731.0),
    'W':  ('tungsten',	74,	5930.0),
    'Re': ('rhenium',	75,	5900.0),
    'Os': ('osmium',	76,	5285.0),
    'Ir': ('iridium',	77,	4701.0),
    'Pt': ('platinum',	78,	4098.0),
    'Au': ('gold',	79,	3129.0),
    'Hg': ('mercury',	80,	630.0),
    'Tl': ('thallium',	81,	1746.0),
    'Pb': ('lead',	82,	2022.0),
    'Bi': ('bismuth',	83,	1837.0),
    'Po': ('polonium',	84,	1235.0),
    'At': ('astatine',	85,	610.0),
    'Rn': ('radon',	86,	211.3),
    'Fr': ('francium',	87,	950.0),
    'Ra': ('radium',	88,	2010.0),
    'Ac': ('actinium',	89,	3471.0),
    'Th': ('thorium',	90,	5061.0),
    'Pa': ('protactinium',	91,	4300.0),
    'U':  ('uranium',	92,	4404.0),
};		
		
		
		
		
		
		
		
