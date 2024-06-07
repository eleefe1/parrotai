Requires API keys for ElevenLabs API and ChatGPT API. Add an untracked file locally to /parrotpacakges named api_keys.py with contents:
-------------------------------------------------
#container for parrot API keys

def get_aikey() -> str:
	return '{your ChatGPT API Key}'
	
def get_elevenlabskey() -> str:
	return '{your Eleven Labs API Key}'
-------------------------------------------------

Say the command "freeze all motor functions" to enter diagnostic mode.
In diagnostic mode, the following commands can be given:
- "pirate": changes voice to pirate character
- "sugar": changes voice to Southern belle character
- "character limit": fetches characters remaining in Eleven Labs billing account.
- "leave diagnostics": returns to normal mode with last character used

At any time, the command "good night parrot" will exit the script entirely.

