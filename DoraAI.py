import os
import streamlit as st
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from groq import Groq
from langdetect import detect

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

# Language prompts to guide the assistant response
language_prompts = {
    "en": "You are a helpful assistant. Reply in English.",
    "hi": "आप एक सहायक सहायक हैं। कृपया हिंदी में उत्तर दें।",
    "es": "Eres un asistente útil. Responde en español.",
    "fr": "Vous êtes un assistant utile. Répondez en français.",
    "de": "Du bist ein hilfreicher Assistent. Bitte antworte auf Deutsch.",
    "pa": "ਤੁਸੀਂ ਇੱਕ ਮਦਦਗਾਰ ਸਹਾਇਕ ਹੋ। ਕਿਰਪਾ ਕਰਕੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।"
}

def speak(text):
    temp_path = "response_audio.mp3"
    tts_engine.save_to_file(text, temp_path)
    tts_engine.runAndWait()
    if os.path.exists(temp_path):
        st.audio(temp_path, format="audio/mp3")
    else:
        st.error("Error generating audio.")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
        except sr.WaitTimeoutError:
            return "Listening timed out."

def detect_language(text):
    try:
        lang_code = detect(text)
    except:
        lang_code = "en"
    return lang_code if lang_code in language_prompts else "en"

# UI Setup
st.set_page_config(page_title="🌐 Multilingual Voice Chatbot", layout="centered")
st.title("DORA : The Chatbot 🔍")
st.write("Speak or type your question in your language. The bot will respond accordingly!")

# Session Init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Show Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Methods
col1, col2 = st.columns([4, 1])
with col1:
    user_prompt = st.chat_input("Type your question or use the 🎤 Speak button.")
with col2:
    if st.button("🎤 Speak"):
        user_prompt = recognize_speech()
        st.write(f"🗣 You said: {user_prompt}")

# Chatbot Logic
if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    user_lang = detect_language(user_prompt)
    chat_context = language_prompts.get(user_lang, language_prompts["en"])
    
    messages = [{"role": "system", "content": chat_context}] + st.session_state.chat_history

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
        for para in assistant_response.split('\n\n'):
            st.markdown(para.strip())

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    st.session_state.last_response = assistant_response
    st.session_state.last_lang = user_lang

# Text-to-Speech
if st.session_state.last_response:
    if st.button("🔊 Play Response"):
        speak(st.session_state.last_response)

# Prompt for next interaction
st.markdown("*Ask your next question or speak again!*")