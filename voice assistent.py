import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime

# ----------------- TTS SETUP -----------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)   # speaking speed
engine.setProperty("volume", 1.0) # 0.0 to 1.0

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ----------------- STT (LISTEN) -----------------
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.8
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language="en-IN")
        print("You:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not catch that.")
    except sr.RequestError:
        speak("There is a problem with the speech service.")
    return ""

# ----------------- COMMAND HANDLER -----------------
def handle_command(command):
    if command == "":
        return

    # 1. greeting
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    # 2. time
    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    # 3. date
    elif "date" in command or "today" in command:
        today = datetime.now().strftime("%d %B %Y")
        speak(f"Today is {today}")

    # 4. simple web search
    elif "search" in command or "google" in command:
        speak("What should I search for?")
        query = listen()
        if query:
            url = "https://www.google.com/search?q=" + query.replace(" ", "+")
            speak(f"Searching Google for {query}")
            webbrowser.open(url)

    # 5. exit
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Okay, goodbye!")
        raise SystemExit

    # 6. fallback predefined response
    else:
        speak("I can say hello, tell time or date, and search the web. Try saying, 'what is the time' or 'search for AI'.")
        
# ----------------- MAIN LOOP -----------------
if __name__ == "__main__":
    speak("Hello, I am your simple voice assistant. Say something after the beep.")

    while True:
        cmd = listen()
        handle_command(cmd)
