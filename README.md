
# 🤖 DORA: The Multilingual Voice Chatbot

**DORA** is an intelligent, multilingual chatbot built using Python and Streamlit. It leverages large language models (LLMs), speech recognition, language detection, and text-to-speech to provide seamless voice and text interactions in multiple languages.

## 🌍 Features

- 🔊 **Voice Input**: Users can speak instead of typing.
- 🧠 **AI-Powered Responses**: Uses LLaMA 3.1 model via Groq API for intelligent, context-aware replies.
- 🌐 **Multilingual Support**: Detects and responds in English, Hindi, Spanish, French, German, and Punjabi.
- 🗣 **Text-to-Speech**: Converts AI responses to audio.
- 📜 **Chat History**: Persistent session-based conversation flow.
- 🎛 **Streamlit UI**: Clean, user-friendly interface for real-time chatting.

## 🛠 Technologies Used

- **Python 3.9+**
- [Streamlit](https://streamlit.io/) – for UI
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – for voice input
- [pyttsx3](https://pypi.org/project/pyttsx3/) – for text-to-speech
- [LangDetect](https://pypi.org/project/langdetect/) – for detecting language
- [Groq API](https://groq.com/) – for LLaMA model integration
- [dotenv](https://pypi.org/project/python-dotenv/) – for managing API keys

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/DoraAI.git
cd DoraAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create a `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the App
```bash
streamlit run DoraAI.py
```

## 🗣 Supported Languages

| Code | Language  |
|------|-----------|
| en   | English   |
| hi   | Hindi     |
| es   | Spanish   |
| fr   | French    |
| de   | German    |
| pa   | Punjabi   |

## 📌 Folder Structure

```
├── DoraAI.py          # Main chatbot app
├── .env               # API key (not committed)
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
```

## 🧪 Coming Soon

- Real-time translation support
- UI customization options
- Voice customization (multiple accents/voices)
- Deployment on cloud (Streamlit Sharing, Heroku, etc.)

## 👨‍💻 Authors

- Kanishka Soni
- Kartavya Arora
- Pratik
- Dhruv

## 📜 License

This project is for academic and non-commercial use only.

---

### ✨ Talk to DORA: “Your multilingual AI companion”
