#!/usr/bin/python


from __future__ import print_function;
from __future__ import division;
from __future__ import unicode_literals;
from __future__ import absolute_import;



class PHPGoAway(object):
	def __init__(self):
		self.tabulaRecta = self.__generateTabulaRecta();
		
		
	def __generateTabulaRecta(self):
		tr = {};
		letters = 'abcdefghijklmnopqrstuvwxyz';
		uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
		count = 0;
		for x in letters:				
			tr[x] = [ chr(((ord(x)-ord('a')+a)%len(letters))+ord('a')) \
				for a in range(len(letters)) ];			
			
		for x in uppers:					
			tr[x] = [ chr(((ord(x)-ord('A')+a)%len(uppers))+ord('A')) \
				for a in range(len(uppers)) ];								
		
		return tr;
	
	def setKey(self, key):		
		self.__key = ''.join(key.split());
		print('setKey: ', self.__key, sep='');


	def __generateKeyLetters__(self, word):
		_list = [self.__key[index%len(self.__key)] for index in range(len(word))];	
		return _list;
		
	def forLove(self, message):
		'''
		Encrypt message.
		
		Rows correspond to keyLetters.
		Columns correspond to message letters.
		'''		
		wordList = message.split();
		_list = [];
		keyLetters = self.__generateKeyLetters__(''.join(wordList));
		index = 0;
		print('keyLetters:', ''.join(keyLetters));
		print('message:', message);
		for letter in message:					
			if letter == ' ':
				_list.append(' ');
				continue;
				
			if letter.islower():
				_list.append(self.tabulaRecta[keyLetters[index].lower()]\
					[ord(letter)-ord('a')] );
			elif letter.isupper():
				_list.append(self.tabulaRecta[keyLetters[index].upper()]\
					[ord(letter)-ord('A')] );		
						
			index += 1;	
					
		try:
			if _list.index(' ', -1):
				_list.pop(-1);
		except:
			pass;
				
		return ''.join(_list);
		
	def fromLove(self, encryptedMessage):
		'''
		Decrpyt encryptedMessage.
		
		1. For each letter in key letters, select the row with this letter as
			the key name in tabulaRecta dict.
		2. Determine letter in encryptedMessage with same index position as
			key in key letters.
		3. Find encryptedMessage letter in row.
		4. Find its	column letter, which will be the decrypted letter.
		'''
		encryptedWordList = encryptedMessage.split();
		_list = [];
		keyLetters = self.__generateKeyLetters__(''.join(encryptedWordList));
		index = 0;
		
		for letter in encryptedMessage:			
			if letter == ' ':
				_list.append(' ');				
				continue;
					
			if letter.islower():				
				_list.append( chr(self.tabulaRecta[keyLetters[index].lower()]\
					.index(letter) + ord('a')) );
			elif letter.isupper():
				_list.append( chr(self.tabulaRecta[keyLetters[index].upper()]\
					.index(letter) + ord('A')) );		
					
			index += 1;			
		
		try:
			if _list.index(' ', -1):
				_list.pop(-1);
		except:
			pass;	
				
		return ''.join(_list);

vig = PHPGoAway();
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













