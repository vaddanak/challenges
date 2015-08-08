#!/usr/bin/python
'''
Author: Vaddanak Seng
File: vigenere_cipher.py
Purpose: Encryption and decryption using Vigenere Cipher.
Date: 2015/08/06

Runs on both python2 and python3? YES
'''

from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;

'''
Encryption and decryption using Vigenere Cipher.
'''


class PHPGoAway(object):
	'''
	setKey(...) to set common key used for encryption and decryption
	forLove(...) to encrypt message
	fromLove(...) to decrypt message
	'''
	def __init__(self):
		'''
		Constructor creates a dict with 52 keys [a-zA-Z], each key corresponds
		to a row of 26 alphabets contained in a list.  The row key indicates
		the letter that starts the alphabet in the row.  For example, if
		key=='c', then list of alphabets (the value) is cdefghijklmnopqrstuvwxyzab
		If key=='y', then value is ['y','z','a','b','c',...,'x']
		'''
		self.tabulaRecta = self.__generateTabulaRecta();		
		
	def __generateTabulaRecta(self): #private method
		'''
		Fn creates dict with keys [a-zA-Z].  The corresponding values are lists
		of alphabets that start with the alphabet same as key and includes all
		26 alphabetic letters in correct order, wrapping around when necessary.
		'''
		tr = {}; #empty dictionary
		letters = 'abcdefghijklmnopqrstuvwxyz';#string of lower case letters
		uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';#string of upper case letters
		count = 0;
		for x in letters: #create rows for lower case letters				
			tr[x] = [ chr(((ord(x)-ord('a')+a)%len(letters))+ord('a')) \
				for a in range(len(letters)) ];			
			
		for x in uppers: #create rows for upper case letters					
			tr[x] = [ chr(((ord(x)-ord('A')+a)%len(uppers))+ord('A')) \
				for a in range(len(uppers)) ];								
		
		return tr; #return reference to dict
	
	def setKey(self, key):		
		'''
		The key is used to encrypt and decrypt the message.  Whitespace in key
		is ignored.
		
		Split key string at sep=' ' into list of words, then join the individual
		word into a new string without separating whitespaces.
		'''
		self.__key = ''.join(key.split());
		print('setKey: ', self.__key, sep='');


	def __generateKeyLetters(self, word): # private method
		'''
		Fn generates list of key letters that will have the same length as 'word'.
		Returned _list has property len[_list]==len[word].
		
		If key has fewer characters than word, then _list will have repeating
		key letters.  If key=='cat' and word=='house', 
		_list=['c','a','t','c','a'].
		
		If key=='mouse' and word=='hi', _list=['m','o'].
		'''
		_list = [self.__key[index%len(self.__key)] for index in range(len(word))];	
		return _list;
		
	def forLove(self, message):
		'''
		Encrypt message.
		
		Each key letter will correspond to a dict key.  Each message letter will
		correspond to a column letter.  The column letters are either [a-z] or
		[A-Z], depending if the key letter is lowercase or uppercase.
		
		The key letter will be used to look up a value, which is a list of
		26 alphabet letters and that row starts with the letter same as the key.
		
		For each message letter, the corresponding encrypted letter is the
		intersection of the row and the column.  For example, if key='lemon' and
		message='attackatdawn' (original message was 'attack at dawn'), then
		row is self.tabulaRecta['l'] and column=='a', so encrypted letter is 'a';
		self.tabulaRecta['e'] and column=='t', so encrypted letter is 'x'
		
		Space in message is not interpreted and remain as is in the output.
		'''		
		wordList = message.split();#list of words in the message
		_list = []; #empty list
		#keyLetters is list of key letters such that len[keyLetters]==length
		# of message without spaces
		keyLetters = self.__generateKeyLetters(''.join(wordList));
		index = 0;
		print('keyLetters:', ''.join(keyLetters));
		print('message:', message);
		for letter in message:#translate each letter in messaage, ignore whitespace
			if letter == ' ':
				_list.append(' ');#ignore space but keep it final output
				continue;
				
			if letter.islower():#find row, then offset to column position
				_list.append(self.tabulaRecta[keyLetters[index].lower()]\
					[ord(letter)-ord('a')] );
			elif letter.isupper():
				_list.append(self.tabulaRecta[keyLetters[index].upper()]\
					[ord(letter)-ord('A')] );		
						
			index += 1;	
					
		try:
			if _list.index(' ', -1): #remove last space item in list
				_list.pop(-1);
		except:
			pass;
				
		return ''.join(_list); #turn list into literal string
		
	def fromLove(self, encryptedMessage):
		'''
		Decrpyt encryptedMessage.
		
		1. For each letter in key letters, select the row with this letter as
			the key name in tabulaRecta dict.		
		2. Locate encryptedMessage letter in row.
		3. Find correspoding column letter, which will be the decrypted letter.
		
		For example, assume key=='lemon' and encryptedMessage=='lxfopvefrnhr'.
		Row is self.tabulaRecta['l'].  Find 'l' in row.  So, column letter is 'a'
		Next, self.tabulaRecta['e'].  Find 'x' in row. So, column letter is 't'
		'''
		encryptedWordList = encryptedMessage.split();#get list of 'words'
		_list = [];# empty list
		#get list of key letters such that len[keyLetters]==length of
		# encryptedMessage without space
		keyLetters = self.__generateKeyLetters(''.join(encryptedWordList));
		index = 0;
		#look at each letter in encryptedMessage
		for letter in encryptedMessage:			
			if letter == ' ':
				_list.append(' ');#ignore space but include it in final output
				continue;
				
			#locate row based on keyLetter, get list index of encryptedMessage
			# letter, convert to ascii to find column letter (decrypted letter)		
			if letter.islower():#lowercase letters				
				_list.append( chr(self.tabulaRecta[keyLetters[index].lower()]\
					.index(letter) + ord('a')) );
			elif letter.isupper():#uppercase letters
				_list.append( chr(self.tabulaRecta[keyLetters[index].upper()]\
					.index(letter) + ord('A')) );		
					
			index += 1;			
		
		try:
			if _list.index(' ', -1):#remove trailing space
				_list.pop(-1);
		except:
			pass;	
				
		return ''.join(_list);#convert list of letters to literal string
		
#--------------------------------------------		
classAlias = PHPGoAway;#create new name for class

#vig = PHPGoAway();
vig = classAlias();#create new class object and attach name 'vig' to it

vig.setKey('LEMON');
print('forLove:', 'AttackAtDawn ->', vig.forLove('AttackAtDawn') );#LxfopvEfRnhr
print('fromLove:', 'LxfopvEfRnhr ->', vig.fromLove('LxfopvEfRnhr'));#AttackAtDawn
print();

vig.setKey('yophp');
print('forLove:', 'i love you ->', vig.forLove('i love you')); #g zdct wcj
print('fromLove:', 'g zdct wcj ->', vig.fromLove('g zdct wcj'));#i love you
print();

#the feelings are mutual
print('fromLove:', 'Rvt mtczxuvq ogl bshjha ->', \
	vig.fromLove('Rvt mtczxuvq ogl bshjha') );
print('forLove:', 'The feelings are mutual ->', \
	vig.forLove('The feelings are mutual') );













