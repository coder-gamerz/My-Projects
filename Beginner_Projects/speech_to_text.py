import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def Speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
 
while True: 
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print(MyText)
            Speak(MyText)
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occured")

# A simple speech-to-text program
        
