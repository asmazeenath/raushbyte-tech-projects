import streamlit as st
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import base64

# Page settings
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="centered"
)

# Background image
with open("i.jpg", "rb") as f:
    img = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
}}
</style>
""", unsafe_allow_html=True)


st.title("🎙️ AI Voice Assistant")
st.write("Speak a command and I will perform the task.")
# Text to Speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Voice input
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        return command.lower()

    except sr.UnknownValueError:
        return "Sorry, I could not understand you."

    except sr.RequestError:
        return "Speech recognition service is unavailable."


# Process command
def process_command(command):

    if "hello" in command or "hi" in command:
        return "Hello! How can I help you?"

    elif "time" in command:
        time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {time}"

    elif "date" in command:
        date = datetime.now().strftime("%d %B %Y")
        return f"Today's date is {date}"

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "search" in command:
        query = command.replace("search", "").strip()

        if query:
            webbrowser.open(
                "https://www.google.com/search?q="
                + query.replace(" ", "+")
            )
            return f"Searching for {query}"

        return "Please tell me what you want to search."

    elif "exit" in command or "stop" in command:
        return "Goodbye!"

    else:
        return "I don't know that command yet."


# UI
st.divider()

if st.button("🎤 Start Listening", use_container_width=True):

    command = listen()

    st.subheader("🗣️ You said:")
    st.write(command)

    response = process_command(command)

    st.subheader("🤖 Assistant:")
    st.success(response)

    speak(response)

st.divider()

st.subheader("💡 Try saying")

st.write("""
- 👋 Hello
- 🕐 What is the time?
- 📅 What is today's date?
- 🌐 Open Google
- ▶️ Open YouTube
- 🔎 Search Artificial Intelligence
- 🛑 Exit
""",textColor="#FBFCFD")