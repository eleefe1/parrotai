import requests
import subprocess


class ElevenLabsStream:
    #creates a class for streaming and playing Eleven Labs speech using ffmpeg
    
    def __init__(self: object, key: str) -> None:       
        

        self._querystring = {"optimize_streaming_latency":"3","output_format":"mp3_22050_32"}

        self._headers = {
            'accept': '*/*',
            'xi-api-key': key,
            'Content-Type': 'application/json'
        }
    
    def generateSpeech(self:object, text: str, voiceID: str) -> None:    
        
        data = {
            'text': text,
            'model_id': "eleven_turbo_v2",
            'voice_settings': {
                'stability': 0.50,
                'similarity_boost': 0.30
            }
        }

        url = 'https://api.elevenlabs.io/v1/text-to-speech/' + voiceID
        
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
