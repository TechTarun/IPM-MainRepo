from gtts import gTTS
import os
from playsound import playsound

def say(text):
    myobj = gTTS(text, lang='en', slow=False)
    myobj.save('voice.mp3')
    playsound('voice.mp3')
    os.remove('voice.mp3')

# say("Create a new project tarunipm in jira")