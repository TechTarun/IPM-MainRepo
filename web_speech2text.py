import speech_recognition as sr
import web_text2speech as t2s

def listen():
    r = sr.Recognizer()
    r.pause_threshold = 0.5
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Speak!!")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        t2s.say("Done!!")
        print(text)
        return(text)
    except:
        t2s.say("Can't listen properly, try again")
        listen()
