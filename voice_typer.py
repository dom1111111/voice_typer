from cgitb import text
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


def chirp():
    winsound.PlaySound(audio_file_path, winsound.SND_FILENAME)


class TalkToText:
    listening = False

    r = sr.Recognizer()
    m = sr.Microphone()

    with m as source:                           # use the default microphone as the audio source
        r.energy_threshold = 300                # adjust this float number to adjust microphone sensitivity for picking up audio
        r.adjust_for_ambient_noise(source, duration = 1)    # listen for 1 second to calibrate the energy threshold for ambient noise levels
        r.dynamic_energy_threshold = False      # set this to True when you're in a place with changing background noisy levels
        r.pause_threshold = 0.8                 # the the minimum length of silence (in seconds) that will register as the end of a phrase

    def recognize_audio(self, recognizer_instance, audio):
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # print(self.r.energy_threshold)
            recognized_audio = recognizer_instance.recognize_google(audio)
            print("\U0001F5E3" + "   " + recognized_audio)      # print "speaking head" emoji
            text_to_typing(recognized_audio)
        except sr.WaitTimeoutError:
            print("the program assumed you were done speaking")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except:
            print("something went wrong")

    def start(self):
        self.listening = True
        print()
        print('wait for the sound before speaking...')
        # starts the background listening
        self.voice_typing = self.r.listen_in_background(self.m, self.recognize_audio)
        chirp()                             # to let users know that the program is now listening
        print()
        print(f"minimum energy threashhold for microphone set to {self.r.energy_threshold}")
        print()
        print("Say something!")
    
    def stop(self):
        print()
        self.listening = False
        print("Stopping Listening")
        self.voice_typing(wait_for_stop=False)        # stops the background listening
        print()
        print(main_message)


def text_to_typing(text):
    if isinstance(text, str):               # checks if speech_input is a string - avoids errors from exceptions
        formated_text = f"{text} "          # adds a space after each typed statement
        keyboard.write(formated_text)       # types with the keyboard
    else:
        print('ERROR')


#################


print()
print("starting...")

# instatiate the TalkToText class
voice_typing = TalkToText()

def toggle_voice_typing():
    if not voice_typing.listening:
        voice_typing.start()
    elif voice_typing.listening:
        voice_typing.stop()

speech_hotkey = 'ctrl+alt+space'

keyboard.add_hotkey(speech_hotkey, toggle_voice_typing, args=())

main_message = f'press [{speech_hotkey}] to start typing with your voice! Then press it again to stop'

print()
print('Welcome!')
print()
print(main_message)

while True:
    # blocks the program indefinitely
    keyboard.wait()


