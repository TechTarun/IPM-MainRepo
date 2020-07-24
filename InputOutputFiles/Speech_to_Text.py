import speech_recognition as sr
import Text_to_Speech as speak

def listen_input():
    r = sr.Recognizer()
    # r.energy_threshold = 500
    # r.pause_threshold = t
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        speak.say('Speak your query')
        audio = r.listen(source)
    text = r.recognize_google(audio, language='en')
    speak.say(text)
    return text

print(listen_input())