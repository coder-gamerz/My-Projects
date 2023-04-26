import wolframalpha
import subprocess
import clipboard
import pywhatkit
import sys
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import pyautogui as py
import psutil
import urllib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
api_id = 'XLHTW8-XVEA9H9WJV'

def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d hours and %02d minutes" % (hours, minutes)


def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def scrape_meaning(audio):
    word = audio
    url = 'https://www.dictionary.com/browse/' + word
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup
    meanings = soup.findAll('div', attrs =  {'class': 'css-1o58fj8 e1hk9ate4'})
    meaning = [x.text for x in meanings]
    first_meaning = meaning[0]
    for x in meaning:
        print(x)
        print('\n')
    
    speak(first_meaning)

def make_list():
    speak("what is your list's name sir")
    ln = takeCommand()
    yes = True
    while yes:
        speak('what is on your list today sir')
        audio = takeCommand()
        with open(r'C:\Users\shrey\OneDrive\Documents\{}.txt'.format(ln),'a') as f:
            f.write(audio)
            f.write('\n')
        speak('is there anything else sir')
        f = takeCommand()
        if f == 'yes':
            continue
        if f == 'no':
            yes = False
    speak('list noted down sir')

def tellDay():
    day = datetime.datetime.today().weekday() + 1 
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
     
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day today is" + day_of_the_week)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12 :
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18 :
        speak("Good Afternoon Sir !")
    
    else:
        speak("Good Evening Sir !")

    speak("I am your Assistant") 
    speak("how can i help you")


def takeCommand():
	
	r = sr.Recognizer()
	
	with sr.Microphone() as source:
		
		print("Listening...")
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)

	try:
		print("Recognizing...")
		query = r.recognize_google(audio, language ='en-in')
		print(f"User said: {query}\n")

	except Exception as e:
		print(e)
		print("Unable to Recognize your voice sir.")
		return "None"
	
	return query

if __name__ == "__main__":    

    clear = lambda: os.system('cls')
     
    clear()
    wishMe()
     
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'joke' in query or 'tell me a joke' in query:
            joke = pyjokes.get_joke(language="en", category="neutral")
            speak('the joke is')
            speak(joke)

        elif 'battery' in query:
            battery = psutil.sensors_battery()
            speak(f'battery percent is {battery.percent} and battery remaining is {convertTime(battery.secsleft)}')
 
        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'day' in query or 'what is the day' in query:
            tellDay()
 
        elif 'open google' in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")
 
        elif 'open stackoverflow' in query:
            speak("Here you go to Stack Over flow. Happy coding")
            webbrowser.open("stackoverflow.com")

        elif 'play' in query:
            vid = query.replace('play', '')
            speak(f'playing {vid}')
            pywhatkit.playonyt(vid)

        elif 'set alarm' in query:
            speak('for how many hours sir')
            abc = takeCommand()
            abc = int(abc)
            
            now = datetime.datetime.now().hour
            now = int(now)

            alarm = now + abc
            if now == abc:
                webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")   
            speak(f"Sir, the time is {strTime}")

        elif 'open browser' in query:
            os.system('start opera')

        elif 'screenshot' in query:
            speak('say name for the screenshot sir')
            s = takeCommand()
            speak('hold on for a few seconds sir')
            time.sleep(3)
            img = py.screenshot()
            img.save(r'C:\Users\shrey\Pictures\Screenshots\{}.jpg'.format(s))
            speak('taken and saved the screenshot sir')

        elif "calculate" in query:
            client = wolframalpha.Client(api_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif 'meaning' in query:
            speak('what do you want meaning for sir')
            a = takeCommand()
            scrape_meaning(a)

        elif "list" in query:
            make_list()

        elif 'search' in query:
            speak("what do you want to search sir")
            s = takeCommand()
            s = s.lower()
            webbrowser.open(f'''https://www.google.com/search?client=opera-gx&q={s}&sourceid=opera&ie=UTF-8&oe=UTF-8''')

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif "what is" in query:
            client = wolframalpha.Client(api_id)
            res = client.query(query)
             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results")
 
        elif 'shutdown system' in query:
            speak("shutting down pc")
            subprocess.call('shutdown / p /f')

        elif 'restart system' in query:
            speak('restarting pc')
            subprocess.call('shutdown /r /t 2')
                 
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "where is" in query:
                query = query.replace("where is", "")
                location = query
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.nl / maps / place/" + location + "")

        elif "camera" in query or "take a photo" in query:
                ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif 'weather' in query:
            city = "mumbai"
            appid = '16f0afad2fd9e18b7aee9582e8ce650b'
            res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}b&units=metric").json()
            temp1 = res["weather"][0]["description"]
            speak(f"The temperature today is {format(temp1)}")

        elif 'exit' in query:
            speak('goodbye sir')
            sys.exit()

# A voice assistant that helps in automating daily tasks

