import asyncio
import re
import speech_recognition as sr
import pyttsx3
from EdgeGPT import Chatbot, ConversationStyle
import datetime
import subprocess

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def greet():
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if hour < 12:
        print("Good morning sir, how can i help you today?")
        speak("Good morning sir, how can i help you today?")
    elif 12 <= hour < 18:
        print("Good afternoon sir, how can i help you today?")
        speak("Good afternoon sir, how can i help you today?")
    else:
        print("Good evening sir, how can i help you today?")
        speak("Good evening sir, how can i help you today?")

async def assistant():
    clear = lambda: subprocess.run('cls', shell = True)
    clear()
    greet()
    while True:
        bot = Chatbot(cookie_path=r'C:\Users\shrey\OneDrive\Documents\My-Projects\Voice_assistant\cookies.json')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                a = r.recognize_google(audio)
                print("You said: " + a)
            except sr.UnknownValueError:
                speak("Sorry, I did not understand what you said.")
                continue
            except sr.RequestError as e:
                speak("Sorry, could not request results from Google Speech Recognition service. {0}".format(e))
                continue

        response = await bot.ask(prompt=a, conversation_style=ConversationStyle.creative)
        for msg in response['item']['messages']:
            if msg['author'] == 'bot':
                bot_response = msg['text']

        bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
        print(bot_response)
        speak(bot_response)
        await bot.close()

if __name__ == '__main__':
    asyncio.run(assistant())