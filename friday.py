import pyttsx3
import datetime
import speech_recognition
import wikipedia
import webbrowser
from time import sleep
from googlesearch import search
import random
import os
import json
import requests
import pyjokes 

class Friday():

    def __init__(self, user = 'stranger'):
        self.name = user

    @staticmethod
    def speak(sentence):
        '''
        speak() function takes sentence as argument and then speak it, using the sapi5 voice.
        '''
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate',150)
        engine.setProperty('volume',1)

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        print(f"Friday: {sentence}")
        engine.say(sentence)
        engine.runAndWait()


    def openWebsiteOnChrome(self, url):
        '''
        Open the given url in the windows default browser.
        '''
        try:
            c = webbrowser.get('windows-default')
            c.open_new_tab(url)
        
        except Exception as e:
            self.speak(e)

    def wishMe(self):
        '''
        wishMe() function simply wishes you according to time.
        '''
        time = datetime.datetime.now().hour
        
        if time >= 5 and time < 12:
            self.speak(f"Good Morning, {self.name} sir.\n")

        elif time >= 12 and time < 17:
            self.speak(f"Good Afternoon, {self.name} sir.\n")

        elif time >= 17 and time < 22:
            self.speak(f"Good Evening, {self.name} sir.\n")
        
        else: 
            self.speak(f"Good Night, {self.name} sir.\n")
        
        self.speak("How can I help you?\n")

    def takeCommand(self):
        '''
        takeCommand() function takes the audio input from the user.
        And return the query (audio) as a string.
        '''
        recognizer = speech_recognition.Recognizer()

        with speech_recognition.Microphone() as source:
            print("\nListening...")
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"{self.name}: {query}\n")

        except Exception as e:
            print(e)
            self.speak("Say that again please...")
            return 'None'
        
        if "jarvis" in str(query).lower() and "google search" not in str(query).lower():
            self.speak("I am not Jarvis, I am Friday!")
            query = str(query).lower().replace("jarvis", '')

        return query

    def googleSearch(self, query):
        '''
        Searches the given query on google and opens the first website.
        '''
        try:
            self.speak("Searching google...")
            for result in search(query, tld= 'co.in', num= 1, stop=1, pause=2):
                self.openWebsiteOnChrome(result)

        except Exception:
            self.speak("Something went wrong...")

    def speechToText(self):
        '''
        First say the name of file in which you have to save your text.
        It will generate a txt file according to the name.
        Just say any sentence one by one it will generate text from it and then save it in the file.
        '''
        self.speak("Initializing...")
        print("Say 'stop' or 'exit' to come out of speech to text coverter.")
        sleep(2)
        
        self.speak("Say the name of file in which you have to save the text.")
        name = self.takeCommand()

        with open(f"{name}.txt", 'w') as f:
            while True:
                text = self.takeCommand()
        
                if text == "stop" or text == "exit":
                    self.speak(f"Your file is saved in the current working directory as {name}.txt")
                    self.speak("Exiting Text to speech...")
                    break

                else:
                    f.write(text + "\n")

    def news_reader(self):
        try:
            r = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=edc0c107419f4e90a294413e5897d74a')

        except Exception as e:
            self.speak(e)

        raw_news = json.loads(r.text)
        art = raw_news['articles']

        for i in range(len(art)):
            article = art[i]
            news = f"News number {i+1} This article is by {article['source']['name']}, author is {article['author']}, (Title) {article['title']} (description) {article['description']} Done"

            news_url = f"Published at {article['publishedAt']}.\n For more info ctrl+click on --> {article['url']}"

            self.speak(news)
            print(f"\n{news_url}\n")
            sleep(2)
    
    
if __name__ == "__main__":

    try:
        with open("user.txt") as f:
            name = f.read()
    except FileNotFoundError:
        print("Cannot find user data.\nThe user.txt may deleted or currently can't be accessed.")

    except Exception as e:
        print(e)

    friday = Friday(name)

    friday.wishMe()
    while True:
        task = friday.takeCommand().lower()

        if "hello" in task: 
            friday.speak("Hello Sir, how may I help you?")

        elif "sorry" in task:
            friday.speak("It's Ok!")

        elif "thanks" in task or "thank you" in task:
            friday.speak("Welcome!")

        elif task == "ok":
            continue

        elif "your" in task and "full form" in task:
            friday.speak("Female Replacement Intelligent Digital Assistant Youth.")

        elif "can you dance" in task:
            friday.speak("Sorry I can't!")

        elif "who are you" in task or "what you can do" in task:
            try:
                with open("About.txt") as f:
                    content = f.read()
                friday.speak(content)
            
            except FileNotFoundError:
                friday.speak("Cannot find About.txt. The file may deleted or currently can't be accessed.")

            except Exception as e:
                friday.speak(e)

        elif "what is my name" in task:
            friday.speak(f"Your name is {name}")

        elif "change your name" in task:
            friday.speak("It is not possible!")

        elif "change my name" in task:
            friday.speak("Say the name from which I should call you")
            new_name =  friday.takeCommand()

            friday.speak(f"Say 'confirm' if you want to set your name as {new_name}")
            friday.speak("Don't worry you can change your name anytime.")
            confirm = friday.takeCommand().lower()

            if confirm == "confirm":
                friday.name = new_name
                try:
                    with open('user.txt', 'w') as f:
                        f.write(new_name)
                    friday.speak(f"From now I will call you {new_name}")

                except FileNotFoundError:
                    friday.speak("Cannot find user data.\nThe user.txt may deleted or currently can't be accessed.")

                except Exception as e:
                    friday.speak(e)

        elif "artificial intelligence" in task and "you" in task:
            friday.speak("Yes I am an AI")

        elif "joke" in task:
            joke = pyjokes.get_joke()
            friday.speak(joke)

        elif task == "friday":
            friday.speak("Yes, sir!")

        elif "wikipedia" in task:
            friday.speak("Searching wikipedia...")
            task = task.replace("wikipedia", '')
            try:
                result = wikipedia.summary(task, sentences = 2)
                friday.speak(result)

            except Exception:
                friday.speak("Something went wrong...")


        elif "open google" in task:
            friday.speak("Opening Google...")
            friday.openWebsiteOnChrome('https://google.com')

        elif "open youtube" in task:
            friday.speak("Opening Youtube...")
            friday.openWebsiteOnChrome('https://youtube.com')

        elif "open stack" in task:
            friday.speak("Opening Stack over flow...")
            friday.openWebsiteOnChrome('https://stackoverflow.com')

        elif "google search" in task:
            query = task.replace("google search", '')
            friday.googleSearch(query)

        elif "translator" in task:
            friday.speak("Opening google translate...")
            friday.openWebsiteOnChrome("https://translate.google.co.in/?hl=en&tab=rT")

        elif "time" in task:
            friday.speak(f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif "date" in task:
            friday.speak(f"Todays date is {datetime.date.today()}")

        elif "music" in task or "song" in task:
            music_path = "E:\\Ganpati song" 
            music = os.listdir(music_path)
            rmusic = music[random.randint(0, len(music))]

            os.startfile(os.path.join(music_path, rmusic))

        elif "next music" in task or "another music" in task or "next song" in task:
            os.close(rmusic)

        elif "speech to text" in task:
            friday.speechToText()
            
        elif "open vs code" in task:
            friday.speak("Opening VS code...")
            os.popen("C:\\Users\\Harshit\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

        elif "open notepad" in task:
            friday.speak("Opening notepad...")
            os.system("notepad")

        elif "open word" in task or "open microsoft word" in task:
            friday.speak("Opening word...")
            os.system("winword")

        elif "open powerpoint" in task or "open microsoft powerpoint" in task:
            friday.speak("Opening power point...")
            os.system("powerpnt")

        elif "open excel" in task or "open microsoft excel" in task:
            friday.speak("Opening excel...")
            os.system("excel")

        elif "news" in task:
            friday.news_reader()

        elif "quit" in task or "exit" in task or "end" in task:
            friday.speak("Thank you for using FRIDAY")
            print("Exiting...")
            sleep(1)
            exit()

        elif "none" in task:
            continue

        else:
            friday.speak(f"Should I search \"{task}\" on Google?")
            yesOrNo = friday.takeCommand().lower()

            if "yes" in yesOrNo or "ok" in yesOrNo:
                friday.googleSearch(task)

            elif "no" in yesOrNo or "don't" in yesOrNo:
                friday.speak("Ok!")