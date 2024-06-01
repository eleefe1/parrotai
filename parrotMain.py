import queue
import re
import sys
import pyaudio
import time
from preferredsoundplayer import playsound

from google.cloud import speech

#from elevenlabs import play
#from elevenlabs.client import ElevenLabs


from parrotpackages import parrot_GoogleTranscribe as gt
from parrotpackages import parrot_ChatGptSetup as aisetup
from parrotpackages import api_keys
from parrotpackages import parrot_generateSpeech as speech

PATH_TO_SOUND_FILES = '//home//pi//Parrot//SoundFiles//'
FILE_BEGIN_SOUND = 'bubble-begin.mp3'
FILE_END_SOUND = 'bloop-end.mp3'
FILE_FREEZE = 'Barbara-FreezeMotorFunctions-Character.wav'
FILE_LEAVING = 'Barbara-LeavingDiagnostics.wav'
FILE_SASSY_ACK = 'Sassy-Ack.wav'
FILE_PIRATE_ACK = 'Pirate-Ack.wav'

DEFAULT_CHARACTER = 'pirate'


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


#set up the Eleven Labs TTS client
'''
speechclient = ElevenLabs(
  api_key=api_keys.get_elevenlabskey(), # Defaults to ELEVEN_API_KEY
)
'''

def playaudio(sound: str):
        if sound == 'begin':
            playsound(PATH_TO_SOUND_FILES+FILE_BEGIN_SOUND)
        elif sound == 'end':
            playsound(PATH_TO_SOUND_FILES+FILE_END_SOUND)
        elif sound == 'freeze':
            playsound(PATH_TO_SOUND_FILES+FILE_FREEZE)
        elif sound == 'leaving diagnostics':
            playsound(PATH_TO_SOUND_FILES+FILE_LEAVING)
        elif sound == 'pirate ack':
            playsound(PATH_TO_SOUND_FILES+FILE_PIRATE_ACK)
        elif sound == 'sassy ack':
            playsound(PATH_TO_SOUND_FILES+FILE_SASSY_ACK)
        else:
            print('No audio file found')        

def getVoiceID(voice) -> str:
    
    if voice == "pirate":
        return "Co2Fniaxkf2HiwtEj34T"
            
    elif voice == "Barbara":
        return "kARntxLbX0EUozjrxp0G"
    
    elif voice == "sassy":
        return "03vEurziQfq3V8WZhQvn"
            
    else:
        return "Co2Fniaxkf2HiwtEj34T"
    
def listen_print_loop(responses: object,stream, aiclient, messages, voice, speechgen) -> str:
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.

    Args:
        responses: List of server responses

    Returns:
        The transcribed text.
    """
    num_chars_printed = 0
    
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)
            
            
        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(quit)\b", transcript, re.I):
                print("Exiting..")
                break
            elif re.search(r"\b(freeze all motor functions)\b", transcript, re.I):
                
                stream._listening = False
                print("Stopping listening...")
                playaudio('end')                

                playaudio('freeze')
                
                #code for switching modes, voices, characters, etc goes here
                stream._diagnostics = True
                
                print("Resuming listening...")                
                playaudio('begin')
                
                stream._listening = True
                
            elif re.search(r"\b(leave diagnostics)\b", transcript, re.I):
                
                stream._listening = False                                
                print("Stopping listening...")
                playaudio('end') 
                playaudio('leaving diagnostics')
                stream._diagnostics = False 
                print("Resuming listening...")
                playaudio('begin')
                stream._listening = True 
                
            elif not stream._diagnostics:
                stream._listening = False
                print("Stopping listening...")
                playaudio('end')
                
                num_chars_printed = 0
                messages.append(
                   {
                       "role": "user",
                       "content": transcript
                    },
                )

                chat = aiclient.chat.completions.create(
                    messages=messages,
                    model="gpt-3.5-turbo"
                    )
                reply = chat.choices[0].message
                print(reply)
                print("Assistant: ", reply.content)
                print("*****")

                messages.append(
                {
                    "role": "assistant",
                    "content": reply.content
                },
                )                    
                '''
                #get the audio from the TTS client
                audio = speechclient.generate(
                  text=reply.content,
                  voice=getVoiceID(voice),
                  optimize_streaming_latency="2",
                  model="eleven_turbo_v2"
                )                            
                play(audio)
                '''
                speechgen.generateSpeech(reply.content, getVoiceID(voice))
                print("Resuming listening...")
                playaudio('begin')
                stream._listening = True
             
            if stream._diagnostics == True:
                print ("In diagnostics mode. Choose your character.")
                
                if re.search(r"\b(pirate)\b", transcript, re.I):
                    voice = 'pirate'
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),"pirate")
                    playaudio('pirate ack')
                    stream._diagnostics = False
                elif re.search(r"\b(sugar)\b", transcript, re.I):
                    voice = 'sassy'
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),"sassy")
                    playaudio('sassy ack')
                    stream._diagnostics = False
                else:
                    voice = DEFAULT_CHARACTER
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),DEFAULT_CHARACTER)

    return messages, stream, aiclient, voice

def main() -> None:
    """Transcribe speech from audio file."""
    # Set up the Goolge Speech client    
    language_code = "en-US"  # a BCP-47 language tag
    
    gtclient = gt.speech.SpeechClient()
    config = gt.speech.RecognitionConfig(
        encoding=gt.speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = gt.speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    
    speechgen = speech.ElevenLabsStream(api_keys.get_elevenlabskey())
    
    # Set up the AI client
    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),DEFAULT_CHARACTER)
    print ("messages from function: ", messages)
    voice = DEFAULT_CHARACTER

    with gt.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        #print('playing begin sound')
        playaudio('begin')
        requests = (
            gt.speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = gtclient.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        messages, stream, aiclient, voice = listen_print_loop(responses, stream, aiclient, messages, voice, speechgen)
        
        #append the transcript to the ChatGPT conversation        
        #messages.append(
            #{
              #  "role": "user",
             #   "content": transcript
            #},
           # )        
        
        
        
    print("script exiting")


if __name__ == "__main__":
    main()
