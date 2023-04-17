import sys
import threading
import tkinter as tk

import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant

class Assistant:

    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)
        
        self.assistant = GenericAssistant("intents.json", intent_methods={"file": self.create_file})
        self.assistant.load_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="Speak", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()
    
    def create_file(self):
        with open("somefile.txt", "w") as f:
            f.write("HELLO WORLD")

    def run_assistant(self):
        while True:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                print("Speak now!")
                audio = self.recognizer.listen(mic)
            try:
                text = self.recognizer.recognize_google(audio)
                text = text.lower()
                print("You said: {}".format(text))

                if "hey assistant" in text:
                    self.label.config(fg="red")
                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    if text == "stop":
                        self.speaker.say("Bye")
                        self.speaker.runAndWait()
                        self.speaker.stop()
                        self.root.destroy()
                        sys.exit()
                    else:
                        if text is not None:
                            response = self.assistant.request(text)
                            if response is not None:
                                self.speaker.say(response)
                                self.speaker.runAndWait()
                        self.label.config(fg="black")
            except:
                self.label.config(fg="black")
                continue

                

Assistant()
