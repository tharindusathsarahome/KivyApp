
import time,threading
import pyttsx3
import speech_recognition as sr
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

EMAIL_ID=''
PASSWORD=''
LANGUAGE=''

Builder.load_string("""
<AnimWidget@Widget>:
    canvas:
        Color:
            rgba: 0.7, 0.3, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: 400, 30


<RootWidget>:
    cols: 1

    canvas:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size

    anim_box: anim_box
    but_1: but_1
    lab_1: lab_1
    lab_2: lab_2

    Button:
        id: but_1
        font_size: 20
        text: 'Start second thread'
        on_press: root.start_second_thread(lab_2.text)

    Label:
        id: lab_1
        font_size: 30
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'

    AnchorLayout:
        id: anim_box

    Label:
        id: lab_2
        font_size: 100
        color: 0.8, 0, 0, 1
        text: '3'
""")


class RootWidget(GridLayout):

    stop = threading.Event()

    def start_second_thread(self, l_text):
        threading.Thread(target=self.main,).start()

    def StartAnimation(self, *args):
        # self.remove_widget(self.but_1)
        self.lab_2.text = ('Starting')

        anim_bar = Factory.AnimWidget()
        self.anim_box.add_widget(anim_bar)

        anim = Animation(opacity=0.3, width=100, duration=0.6)
        anim += Animation(opacity=1, width=400, duration=0.8)
        anim.repeat = True
        anim.start(anim_bar)

    @mainthread
    def printMsg(self, msgtxt):
        self.lab_1.text = msgtxt

    @mainthread
    def StopAnimation(self):
        self.lab_2.text = ('ok')

        self.remove_widget(self.anim_box)

    def speak(self,audio):
        self.printMsg(audio)
        Clock.schedule_once(self.StartAnimation, 0)
        engine.say(audio)
        engine.runAndWait()
        self.StopAnimation()

    def wishMe(self):
        self.speak("Hello !")

        assname =("Jarvis 1 point o")
        self.speak("I am your Assistant")
        self.speak(assname)
        

    def username(self):
        self.speak("What should i call you sir")
        uname = self.takeCommand()
        self.speak("Welcome Mister")
        self.speak(uname)
        self.speak("How can i Help you, Sir")

    def takeCommand(self):
        
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            
            print("Listening...")
            self.lab_2.text = "Listening..."
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language ='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
        
        self.lab_2.text = ""
        return query

    def main(self):
        """
        Main function that handles primary choices
        """

        self.wishMe()
        self.username()
        
        while True:
            
            query = self.takeCommand().lower()
            
            if 'how are you' in query:
                self.speak("I am fine, Thank you")
                self.speak("How are you, Sir")

            elif 'fine' in query or "good" in query:
                self.speak("It's good to know that your fine")

            elif "change my name to" in query:
                query = query.replace("change my name to", "")
                assname = query

            elif "change name" in query:
                self.speak("What would you like to call me, Sir ")
                assname = self.takeCommand()
                self.speak("Thanks for naming me")

            elif "what's your name" in query or "What is your name" in query:
                self.speak("My friends call me")
                self.speak(assname)
                print("My friends call me", assname)

            elif 'exit' in query:
                self.speak("Thanks for giving me your time")
                exit()

            elif "who made you" in query or "who created you" in query:
                self.speak("I have been created by Gaurav.")
                
            elif "who i am" in query:
                self.speak("If you talk then definitely your human.")

            elif "why you came to world" in query:
                self.speak("Thanks to Gaurav. further It's a secret")

            elif 'is love' in query:
                self.speak("It is 7th sense that destroy all other senses")

            elif "who are you" in query:
                self.speak("I am your virtual assistant created by Gaurav")

            elif 'reason for you' in query:
                self.speak("I was created as a Minor project by Mister Gaurav ")

            elif "don't listen" in query or "stop listening" in query:
                self.speak("for how much time you want to stop jarvis from listening commands")
                a = int(self.takeCommand())
                time.sleep(a)
                print(a)

            elif "write a note" in query:
                self.speak("What should i write, sir")
                note = self.takeCommand()
                file = open('jarvis.txt', 'w')
                self.speak("Sir, Should i include date and time")
                snfm = self.takeCommand()
                if 'yes' in snfm or 'sure' in snfm:
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)
            
            elif "show note" in query:
                self.speak("Showing Notes")
                file = open("jarvis.txt", "r")
                print(file.read())
                self.speak(file.read(6))

            elif "Good Morning" in query:
                self.speak("A warm" +query)
                self.speak("How are you Mister")
                self.speak(assname)

            # most asked question from google Assistant
            elif "will you be my gf" in query or "will you be my bf" in query:
                self.speak("I'm not sure about, may be you should give me some time")

            elif "how are you" in query:
                self.speak("I'm fine, glad you me that")

            elif "i love you" in query:
                self.speak("It's hard to understand")

class RunApp(App):

    def on_stop(self):
        self.root.stop.set()

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    RunApp().run()