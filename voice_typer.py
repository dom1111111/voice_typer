import speech_recognition as sr
import pyaudio
import keyboard
import winsound
from os import path

# get the file path for each audio file
script_path = path.realpath(__file__)        # gets the full file path of this script, including file name
script_dir = path.dirname(script_path)       # gets the file path of this script, NOT including file name
audio_file_name = 'chirp1.wav'
audio_file_path = path.join(script_dir, audio_file_name) # creates filepath for audio file to be opened


speech_hotkey = 'ctrl+alt+space'


def chirp():
    winsound.PlaySound(audio_file_path, winsound.SND_FILENAME)


# function to capture speaking and convert it text
def talk_to_text():
    print()
    print('wait for the sound before speaking...')
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chirp()                     # to let users know that the program is now listening
        print("Say something!")
        audio = r.listen(source)
    
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        recognized_audio = r.recognize_google(audio)
        print("\U0001F5E3" + "   " + recognized_audio)      # print "speaking head" emoji
        return recognized_audio.lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except:
        print("something went wrong")


# main program loop
print('Welcome!')
while True:
    print()
    print(f'press [{speech_hotkey}] to type with your voice!')
    print('say "hotkey" to change the hotkey which acesses the speech dictation')
    keyboard.wait(hotkey = speech_hotkey)
    speech_input = talk_to_text()
    if speech_input == 'hotkey':
        pass
    elif isinstance(speech_input, str):     # checks if speech_input is a string - avoids errors from exceptions
        keyboard.write(speech_input)        # allows to type with your voice!
    else:
        print('ERROR')
