import os
import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import time
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_CONTEXT = os.getenv("CHAT_CONTEXT", "You are a helpful assistant.")

client = Groq(api_key=GROQ_API_KEY)

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

def speak(text):
    """Generate speech audio and play it in the browser."""
    temp_path = "response_audio.mp3"  # Save to a permanent file
    tts_engine.save_to_file(text, temp_path)
    tts_engine.runAndWait()
    if os.path.exists(temp_path):
        st.audio(temp_path, format="audio/mp3")
    else:
        st.error("Error generating audio.")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)  # Increased listening timeout to 10 seconds
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
        except sr.WaitTimeoutError:
            return "Listening timed out."

st.set_page_config(page_title="Llama Voice Chatbot", layout="centered")

st.title("🤖 Llama Voice Chatbot")
st.write("Welcome! You can type your question, speak to the bot, and even listen to the response!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

col1, col2 = st.columns([4, 1])

with col1:
    user_prompt = st.chat_input("Type your question or use the 🎤 Speak button.")
with col2:
    if st.button("🎤 Speak"):
        user_prompt = recognize_speech()
        st.write(f"🗣️ You said: {user_prompt}")

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    messages = [{"role": "system", "content": CHAT_CONTEXT}] + st.session_state.chat_history
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=messages,
        stream=True
    )
    
    assistant_response = ""
    
    with st.chat_message("assistant"):
        for chunk in response:
            if chunk.choices[0].delta.content:
                assistant_response += chunk.choices[0].delta.content 
        paragraphs = assistant_response.split('\n\n')
        
        for paragraph in paragraphs:
            st.markdown(paragraph.strip())  
        
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        st.session_state.last_response = assistant_response
    
    st.session_state.pending_question = "Ask your next question or speak again!"

if st.session_state.last_response:
    if st.button("🔊 Play Response"):
        speak(st.session_state.last_response)

if st.session_state.pending_question:
    st.markdown(f"**{st.session_state.pending_question}**")
