Requires API keys for ElevenLabs API and ChatGPT API. Add an untracked file locally to /parrotpacakges named api_keys.py with contents:

#container for parrot API keys

def get_aikey() -> str:
	return '{your ChatGPT API Key}'
	
def get_elevenlabskey() -> str:
	return '{your Eleven Labs API Key}'
