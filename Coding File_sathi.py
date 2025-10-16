import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import os
import webbrowser
import subprocess
import random
import pywhatkit

# Initialize recognizer and speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Define the function to speak
def talk(text, emotion=None):
    emotions = {
        "happy": ["I'm feeling happy! ", "That's great!", "I'm so excited! "],
        "sad": ["I'm feeling a bit down. ", "I'm here to cheer you up.", "I'm sorry to hear that. "],
        "confused": ["I'm not sure about that. ", "Can you please clarify?", "I need more information. "],
    }

    if emotion:
        response = random.choice(emotions.get(emotion, []))
        text = response + text
    engine.say(text)
    engine.runAndWait()

# Define the function to greet based on the time of day
def greet():
    current_time = datetime.datetime.now().time()
    if current_time < datetime.time(12):
        talk("Good morning, sir! I'm your voice assistant Chris. How can I assist you today?")
    elif datetime.time(12) <= current_time < datetime.time(17):
        talk("Good afternoon, sir! I'm your voice assistant Chris. How can I assist you today?")
    elif datetime.time(17) <= current_time < datetime.time(20):
        talk("Good evening, sir! I'm your voice assistant Chris. How can I assist you today?")
    else:
        talk("Good night, sir! I'm your voice assistant Chris. How can I assist you today?")

# Greet the user
greet()

# Define the function to take a voice command
def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Adjusting for background noise...')
            listener.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            voice = listener.listen(source, timeout=5, phrase_time_limit=7)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'chris' in command:
                command = command.replace('chris', '').strip()
                print(f"Command: {command}")
            if 'stop listening' in command:
                talk('Goodbye, sir. Have a great day!')
                exit()
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        talk("Sorry, I did not catch that. Could you please repeat?")
    except sr.RequestError:
        print("Network error.")
        talk("I'm having trouble reaching the network.")
    except Exception as e:
        print(f"Error: {e}")
    return command

# New functionalities
def search_web(query):
    talk(f"Searching the web for {query}")
    pywhatkit.search(query)

def tell_story():
    story = ("Once upon a time in a faraway land, there was a magical forest where all creatures lived in harmony. "
             "One day, a young girl discovered a hidden path that led her to an enchanted castle...")
    talk(story)

def give_suggestion():
    suggestions = ["How about taking a walk?", "Maybe read a book?", "Try learning something new online."]
    suggestion = random.choice(suggestions)
    talk(suggestion)

def movie_review(movie):
    review = f"The movie '{movie}' is considered a masterpiece. It received great reviews for its plot and direction."
    talk(review)

def info_about(person):
    try:
        info = wikipedia.summary(person, sentences=2)
        talk(info)
    except wikipedia.exceptions.DisambiguationError as e:
        talk("There are multiple people with that name. Could you specify more details?")
    except Exception as e:
        talk(f"I couldn't find information on {person}. Please try again.")

# Define the function to run the voice assistant
def run_chris():
    command = take_command()
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time)
        elif 'who is' in command or 'what is' in command or 'tell me about' in command:
            person = command.replace('who is', '').replace('what is', '').replace('tell me about', '')
            info_about(person)
        elif 'search' in command:
            query = command.replace('search', '').strip()
            search_web(query)
        elif 'suggest' in command:
            give_suggestion()
        elif 'tell me a story' in command:
            tell_story()
        elif 'review of' in command:
            movie = command.replace('review of', '').strip()
            movie_review(movie)
        elif 'date' in command:
            talk('Sorry, I have a headache')
        elif 'are you single' in command:
            talk('I am in a relationship with Wi-Fi')
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'open chrome' in command:
            talk('Opening Google Chrome')
            try:
                subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
            except Exception as e:
                print(f"Error opening Chrome: {e}")
        elif 'open youtube' in command:
            talk('Opening YouTube in Microsoft Edge')
            url = 'https://www.youtube.com'
            webbrowser.get('windows-default').open(url)

# Start the voice assistant loop
while True:
    run_chris()
