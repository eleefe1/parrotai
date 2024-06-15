from parrotpackages import parrot_GoogleTranscribe as stt
from parrotpackages import parrot_ChatGptSetup as aisetup
from parrotpackages import parrot_generateSpeech as speech
from parrotpackages import characterManager as charman
from parrotpackages import api_keys


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class Parrot:
	
	def __init__(self: object) -> None:
		
		#set up the Google Speech to Text client
		self.sttclient = stt.speech.SpeechClient()
		
		config = stt.speech.RecognitionConfig(
			encoding = stt.speech.RecognitionConfig.AudioEncoding.LINEAR16,
			sample_rate_hertz=RATE,
			language_code="en-US",
		)
		
		self.streaming_config = stt.speech.StreamingRecognitionConfig(
			config=config, interim_results=True
		)
		
		#create the character manager
		self.charmgr = charman.CharacterManager()
		
		#Set up the Eleven Labs client
		self.speechgen = speech.ElevenLabsStream(api_keys.get_elevenlabskey(),self.charmgr.currentCharacter['voiceID'])
		
		# Set up the AI client
		self.aiclient, self.messages = aisetup.chatgptsetup(api_keys.get_aikey(), self.charmgr.currentCharacter['desc'])
		
			
