#!/home/pi/parrotenv/bin/python

import queue
import re
import sys
import pyaudio
import time
from preferredsoundplayer import playsound
import RPi.GPIO as GPIO

#from google.cloud import speech
'''
from parrotpackages import api_keys
from parrotpackages import parrot_GoogleTranscribe as gt
from parrotpackages import parrot_ChatGptSetup as aisetup
from parrotpackages import parrot_generateSpeech as speech
from parrotpackages import characterManager as charman
'''

#from parrot import Parrot
import parrot as parrotpkg

PATH_TO_SOUND_FILES = '//home//pi//parrotai//SoundFiles//'
FILE_BEGIN_SOUND = 'bubble-begin.mp3'
FILE_END_SOUND = 'bloop-end.mp3'
FILE_FREEZE = 'Barbara-EnteringDiagnostics.wav'
FILE_LEAVING = 'Barbara-LeavingDiagnostics.wav'
FILE_SUGAR_ACK = 'Sugar-Ack.wav'
FILE_PIRATE_ACK = 'Pirate-Ack.wav'
FILE_COWBOY_ACK = 'Cowboy-Ack.wav'
FILE_PIRATE_EXIT = 'Pirate-Exit.wav'

#DEFAULT_CHARACTER = 'pirate'


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

#set up the switch
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_DOWN)



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
        elif sound == 'sugar ack':
            playsound(PATH_TO_SOUND_FILES+FILE_SUGAR_ACK)
        elif sound == 'cowboy ack':
            playsound(PATH_TO_SOUND_FILES+FILE_COWBOY_ACK)
        elif sound == 'pirate exit':
            playsound(PATH_TO_SOUND_FILES+FILE_PIRATE_EXIT)
        else:
            print('No audio file found')        



#def listen_print_loop(responses: object,stream, aiclient, messages, speechgen) -> str:#
def listen_print_loop(responses: object,stream, parrot) -> str:
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
        
        #this if breaks the loop if the switch is turned off
        if not GPIO.input(17):
            print ("Switch OFF - breaking the loop")
            break
        

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)
            
            
        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(good night parrot|good bye parrot|goodbye parrot)\b", transcript, re.I):
                print("Exiting..")
                playaudio('pirate exit')
                #break
                sys.exit()
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
                
            
                
            elif not stream._diagnostics:
                stream._listening = False
                print("Stopping listening...")
                playaudio('end')
                
                num_chars_printed = 0
                parrot.messages.append(
                   {
                       "role": "user",
                       "content": transcript
                    },
                )

                chat = parrot.aiclient.chat.completions.create(
                    messages=parrot.messages,
                    model="gpt-3.5-turbo"
                    )
                reply = chat.choices[0].message
                #print(reply)    #uncomment this line to show the whole response
                print("Assistant: ", reply.content)
                print("*****")

                parrot.messages.append(
                {
                    "role": "assistant",
                    "content": reply.content
                },
                )                    
                                
                parrot.speechgen.generateSpeech(text=reply.content)
                print("Resuming listening...")
                playaudio('begin')
                stream._listening = True
             
            if stream._diagnostics == True:
                print ("In diagnostics mode. Say 'pirate' 'sugar' 'cowboy' 'scientist' 'character limit' 'leave diagnostics'.")
                
                #if 
                '''
                if re.search(r"\b(pirate)\b", transcript, re.I):
                    speechgen.voice = 'pirate'
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(), speechgen.voice)
                    stream._listening = False
                    playaudio('pirate ack')
                    stream._listening = True
                    stream._diagnostics = False
                elif re.search(r"\b(sugar)\b", transcript, re.I):
                    speechgen.voice = 'sugar'
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),speechgen.voice)
                    playaudio('sugar ack')
                    stream._diagnostics = False
                elif re.search(r"\b(cowboy)\b", transcript, re.I):
                    speechgen.voice = 'cowboy'
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),speechgen.voice)
                    stream._listening = False
                    playaudio('cowboy ack')
                    stream._listening = True
                    stream._diagnostics = False
                elif re.search(r"\b(scientist|scientists)\b", transcript, re.I):
                    speechgen.voice = 'scientist'
                    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(),speechgen.voice)
                    #stream._listening = False
                    #playaudio('cowboy ack')
                    #stream._listening = True
                    print("mad scientist")
                    stream._diagnostics = False
                elif re.search(r"\b(character limit)\b", transcript, re.I):
                    speechgen.get_characterLimit()
                    stream._diagnostics = False
                '''
                if re.search(r"\b(character limit)\b", transcript, re.I):
                    stream._listening = False
                    parrot.speechgen.get_characterLimit()
                    stream._diagnostics = False
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
                    
                else:
                    #extracts character from speech prompt; if a character is named, update the character
                    tempCharacter = parrot.charmgr.getCharacterFromText(transcript)
                    if tempCharacter != None:
                        parrot.updateCharacter(tempCharacter)
                        
                        print("New Character: " + parrot.charmgr.currentCharacter['name'])
                        
                        stream._listening = False
                        playaudio(parrot.charmgr.currentCharacter['name'] + ' ack')
                        stream._diagnostics = False
                        print("Resuming listening...")
                        playaudio('begin')
                        stream._listening = True
                    

    return stream, parrot

def main() -> None:
    """Transcribe speech from audio file."""
    
    '''
    # Set up the Goolge Speech client    
    gtclient = gt.speech.SpeechClient()
    config = gt.speech.RecognitionConfig(
        encoding=gt.speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = gt.speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    
    #create the character manager
    charmgr = charman.CharacterManager()
    
    #Set up the Eleven Labs client
    speechgen = speech.ElevenLabsStream(api_keys.get_elevenlabskey())
    
    # Set up the AI client
    aiclient, messages = aisetup.chatgptsetup(api_keys.get_aikey(), speechgen.voice)
    #print ("messages from function: ", messages)
    '''
    parrot = parrotpkg.Parrot()
    
    switchOff_ONS = False
        
    while True:
        if GPIO.input(17):
            switchOff_ONS = False
            
            
            #update the character list when the switch turns on
            parrot.charmgr.characterList = parrot.charmgr.readCharacterList()
            
            with parrotpkg.stt.MicrophoneStream(RATE, CHUNK) as stream:
                                        
                audio_generator = stream.generator()
                
                playaudio('begin')                                             
                #stream._listening = True
                print("Listening...")
                stream._listening = True
                    
                requests = (
                    parrotpkg.stt.speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator
                )

                responses = parrot.sttclient.streaming_recognize(parrot.streaming_config, requests)

                try:
                    # Now, put the transcription responses to use.                
                    #messages, stream, aiclient, speechgen = listen_print_loop(responses, stream, aiclient, messages, speechgen)
                    stream, parrot = listen_print_loop(responses, stream, parrot)
                except Exception as exception:
                    print(exception)
                    
        else:
            if not switchOff_ONS:
                print ("Switch OFF - not running AI")   
                switchOff_ONS = True
        
    print("script exiting")


if __name__ == "__main__":
    main()
