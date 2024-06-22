import re

DEFAULT_CHARACTER = None

class CharacterManager:
	
	def __init__(self: object) -> None:
		
		self.characterList = self.readCharacterList()
		
		#If default character is not set above, 
		#set first character in the list as default
		if not DEFAULT_CHARACTER:
			self.currentCharacter = self.characterList[list(self.characterList)[0]]
		else:
			self.currentCharacter = self.characterList[DEFAULT_CHARACTER]
			
	def readCharacterList(self: object):
		#method to read in the list of characters from the text file
		characterList = {}
		with open("characters.txt") as f:
			for line in f:
			   (name, voiceID, desc) = line.split("	")
			   characterList[name] = {'name': name, 'voiceID': voiceID, 'desc':desc}
		
		print('------Chracter List-------')	   
		for key in characterList:
			print (characterList[key]['name'], end=" ")
		print("\n")
		
		return characterList
		
	def getCharacterFromText(self: object, lookupString: str):
		
		#iterate through the character list		
		for key in self.characterList:
			if re.search(key, lookupString, re.I):
				return self.characterList[key] #if a character is found, return the info
			else:
				pass				  
						
		return None #return None if no character is found
		
	def getCharacterByName(self: object, name:str):
		
		return self.characterList[name]
