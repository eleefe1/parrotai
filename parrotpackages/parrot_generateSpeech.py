import requests
import subprocess
import inflect

DEFAULT_CHARACTER = 'pirate'

class ElevenLabsStream:
    #creates a class for streaming and playing Eleven Labs speech using ffmpeg
    
    def __init__(self: object, key: str) -> None:       
        

        self._querystring = {"optimize_streaming_latency":"3","output_format":"mp3_22050_32"}

        self._headers = {
            'accept': '*/*',
            'xi-api-key': key,
            'Content-Type': 'application/json'
        }
        
        self.voice = DEFAULT_CHARACTER
    
    def getVoiceID(self:object, voice: str) -> str:
    #function to return the voice ID requested by string
        if voice == "pirate":
            return "Co2Fniaxkf2HiwtEj34T"
                
        elif voice == "Barbara":
            return "kARntxLbX0EUozjrxp0G"
        
        elif voice == "sugar":
            return "03vEurziQfq3V8WZhQvn"
                
        else:
            return "Co2Fniaxkf2HiwtEj34T"
            
    def generateSpeech(self:object, text: str, voice="") -> None:    
    #method to generate and play the speech from text and voice
        if voice == "":
            voice = self.voice
        
        data = {
            'text': text,
            'model_id': "eleven_turbo_v2",
            'voice_settings': {
                'stability': 0.50,
                'similarity_boost': 0.30
            }
        }

        url = 'https://api.elevenlabs.io/v1/text-to-speech/' + self.getVoiceID(voice)
        
        response = requests.post(url, headers=self._headers, params=self._querystring, json=data, stream=True)
        #response.raise_for_status()

        # use subprocess to pipe the audio data to ffplay and play it
        ffplay_cmd = ['ffplay', '-autoexit', '-']
        ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for chunk in response.iter_content(chunk_size=4096):
            ffplay_proc.stdin.write(chunk)
            #print("Downloading...")

        
        # close the ffplay process when finished
        ffplay_proc.stdin.close()
        ffplay_proc.wait()

    def get_characterLimit(self:object):

        # Define the URL for the user info endpoint
        url = "https://api.elevenlabs.io/v1/user"
        
        #Make the GET request to the user info endpoint
        response = requests.get(url, headers=self._headers)

        # Parse the JSON response
        data = response.json()
        
        # Print the character count and limit
        print(f"Character Count: {data['subscription']['character_count']}")
        print(f"Character Limit: {data['subscription']['character_limit']}")

        remaining = data['subscription']['character_limit'] - data['subscription']['character_count'] 

        print(f"Characters Remaining: {remaining}")
        p = inflect.engine()
        self.generateSpeech(text=data['first_name']+', of your ' + p.number_to_words(data['subscription']['character_limit']) + 'limit,,, ' + p.number_to_words(remaining) + ' remain.', voice='Barbara')

        return
