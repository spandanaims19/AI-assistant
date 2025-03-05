import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from gtts import gTTS
import pygame
from browser import website_mapping
import musiclibrary
import io
import requests

recognizer=sr.Recognizer()
engine=pyttsx3.init()

voices=engine.getProperty('voices') #Geeting the current voice
engine.setProperty('voice',voices[0].id) #Changing the index to 1 for female voice

rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 150)     # setting up new voice rate

news_api_key="pub_68901aac3ef840ce3c1ebf54e759ea4f115c6"

def speak(text):
        try:
            # Generate audio in-memory
            tts = gTTS(text=text, lang='en')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Play using pygame
            pygame.mixer.init()
            pygame.mixer.music.load(audio_bytes)
            pygame.mixer.music.play()
            
            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(20)
                
        except Exception as e:
            print(f"Error: {e}")

def old_speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    c=command.lower()
    if "open" in c:
        try:
            website=c.split("open ",1)[1].strip()
            if(website in website_mapping):
                url=website_mapping[website]
                webbrowser.open(url)
                speak(f"Opening {website}")
        except Exception as e:
            print("Error {0}".format(e))
    
    elif(c.startswith("play")):
        song=c.split(" ",1)[1].strip()
        print(song)
        link=musiclibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c:
        try:
        # Make the API request
            url = f"https://newsdata.io/api/1/news?apikey={news_api_key}&q=pizza"
            response = requests.get(url)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                
                # Extract the articles (check the API response structure)
                articles = data.get('results', [])  # newsdata.io uses 'results' instead of 'articles'
                
                # Speak the headlines
                for article in articles:
                    title = article.get('title', 'No title available')
                    speak(title)  # Use your speak() function here
            else:
                print(f"Failed to fetch news. Status code: {response.status_code}")
                speak("Sorry, I couldn't fetch the news at the moment.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("Sorry, I encountered an error while fetching the news.")
        
    else:
        speak(f"I think you said {c}")


if __name__=="__main__":
    # obtain audio from the microphone
    speak("Welcome sir, Jarvis here")
    while True:
        #Listen for the wake word
        #obtain audio from the microphone
        r=sr.Recognizer()

        print("Recognizing....")

        try:
            with sr.Microphone() as source:
                print("Say something...")
                audio=r.listen(source)
            word=r.recognize_google(audio)
            if("jarvis" in word.lower()):

                with sr.Microphone() as source:
                    jar="Jarvis activated....."
                    speak(jar)
                    print(jar)
                    audio=r.listen(source)
                    command=r.recognize_google(audio)
                    # print("Google thinks you said :", command)
                    process_command(command)
        except Exception as e:
            print("Error : {0}".format(e))