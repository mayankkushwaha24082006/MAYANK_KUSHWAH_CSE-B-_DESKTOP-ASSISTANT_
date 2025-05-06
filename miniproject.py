import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import wikipedia
import random
import requests
import pywhatkit as kit
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

engine = pyttsx3.init()

engine.setProperty('rate', 150)  
engine.setProperty('volume', 1)  

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, the speech service is unavailable.")
            return None

def get_weather():
    speak("Please tell me your city name:")
    city = listen()
    
    if city:
        speak(f"Fetching weather details for {city}...")
        search_url = f"https://www.google.com/search?q=weather+{city}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            temp = soup.find('span', class_="wob_t").text
            weather_desc = soup.find('span', class_="wob_dc").text
            humidity = soup.find('span', text="Humidity").find_next('span').text
            speak(f"The temperature in {city} is {temp}°C with {weather_desc}. The humidity is {humidity}.")
        except AttributeError:
            speak("Sorry, I couldn't find the weather for that city.")

def send_email():
    speak("Please provide the recipient's email address:")
    to_email = listen()

    if to_email:
        speak("What is the subject of the email?")
        subject = listen()

        speak("What would you like to say in the email?")
        body = listen()

        sender_email = "your_email@example.com"  
        sender_password = "your_password"  

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, to_email, text)
            server.quit()
            speak("Email has been sent successfully.")
        except Exception as e:
            speak(f"Sorry, there was an error: {str(e)}")

def get_news():
    speak("Fetching top news headlines...")
    url = "https://www.bbc.com/news"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('a', class_="gs-c-promo-heading")
    
    if headlines:
        speak(f"Here are the top news headlines:")
        for i, article in enumerate(headlines[:5]):
            title = article.text.strip()
            speak(f"Headline {i + 1}: {title}")
    else:
        speak("Sorry, I couldn't fetch the news at this moment.")

def play_music():
    speak("Which song would you like to play?")
    song = listen()
    
    if song:
        speak(f"Playing {song} on Spotify.")
        kit.playonyt(song)

def tell_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why don't scientists trust atoms? Because they make up everything.",
        "I told my computer I needed a break, and now it won’t stop sending me beach pictures."
    ]
    speak(random.choice(jokes))

def fun_fact():
    facts = [
        "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
        "A day on Venus is longer than a year on Venus.",
        "There’s a species of jellyfish that is biologically immortal!"
    ]
    speak(random.choice(facts))

def calculate():
    speak("Please tell me the math problem you would like me to solve.")
    problem = listen()
    
    if problem:
        try:
            result = eval(problem)
            speak(f"The answer is {result}")
        except Exception as e:
            speak(f"Sorry, I couldn't solve that problem. Error: {e}")

def open_file():
    speak("Please tell me the file name or path you want to open.")
    file_name = listen()
    
    if file_name:
        try:
            os.startfile(file_name)
            speak(f"Opening {file_name}")
        except Exception as e:
            speak(f"Sorry, I couldn't open that file. Error: {e}")

def convert_currency():
    speak("Please tell me the amount and the currencies you would like to convert.")
    conversion_request = listen()

    if conversion_request:
        try:
            words = conversion_request.split()
            amount = words[1]
            from_currency = words[2]
            to_currency = words[4]
            search_url = f"https://www.google.com/search?q={amount}+{from_currency}+to+{to_currency}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            conversion_result = soup.find('span', class_="DFlfde SwHCTb").text
            speak(f"The conversion result is: {conversion_result} {to_currency}.")
        except Exception as e:
            speak(f"Sorry, I couldn't convert that currency. Error: {e}")

def search_wikipedia():
    speak("What topic would you like to search on Wikipedia?")
    query = listen()

    if query:
        search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        webbrowser.open(search_url)
        speak(f"Opening Wikipedia for {query}")

def execute_task(command):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f"The current time is {current_time}")
    
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        speak(f"Today's date is {current_date}")
    
    elif 'hello' in command or 'hi' in command:
        greet = random.choice(["Hello!", "Hi there!", "Greetings!", "Hey!"])
        speak(greet)
    
    elif 'open' in command and 'website' in command:
        speak("Which website would you like to open?")
        website = listen()
        if website:
            webbrowser.open(f'http://{website}.com')
            speak(f"Opening {website}.com")
    
    elif 'search' in command:
        speak("What would you like to search for?")
        search_query = listen()
        if search_query:
            speak(f"Searching for {search_query} on Wikipedia.")
            try:
                result = wikipedia.summary(search_query, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Could you be more specific? There are several topics related to {search_query}.")
            except wikipedia.exceptions.HTTPTimeoutError:
                speak("Sorry, I couldn't connect to Wikipedia. Please try again later.")
    
    elif 'weather' in command:
        get_weather()

    elif 'send email' in command:
        send_email()

    elif 'news' in command:
        get_news()

    elif 'play music' in command:
        play_music()

    elif 'tell a joke' in command:
        tell_joke()

    elif 'fun fact' in command:
        fun_fact()

    elif 'calculate' in command:
        calculate()

    elif 'open file' in command:
        open_file()

    elif 'convert currency' in command:
        convert_currency()

    elif 'wikipedia' in command:
        search_wikipedia()

    elif 'open google' in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    
    elif 'open' in command:
        apps = {
            'notepad': 'notepad',
            'calculator': 'calc',
            'paint': 'mspaint',
            'word': 'winword',  
            'excel': 'excel',  
            'powerpoint': 'powerpnt',  
            'browser': 'chrome',  
            'file explorer': 'explorer',  
            'spotify': 'spotify',  
            'discord': 'discord', 
            'zoom': 'zoom',  
            'slack': 'slack',  
        }
        for app in apps:
            if app in command:
                os.system(apps[app])
                speak(f"Opening {app}")
                break
    
    elif 'exit' in command or 'quit' in command or 'goodbye' in command:
        speak("Goodbye! Have a great day!")
        exit()

if __name__ == "__main__":
    speak("Hello! I am your desktop assistant. How can I help you?")
    while True:
        command = listen()
        if command:
            execute_task(command)