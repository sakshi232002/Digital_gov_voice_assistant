# Digital_gov_voice_assistant
Certainly! Here's a **detailed and professional `README.md`** tailored for your project: **"Multilingual Voice Assistant for Government White Papers"**. This version includes expanded sections on setup, dependencies, how each module works, screenshots guidance, API endpoints, and contribution notes.

# 🗣️ Multilingual Voice Assistant for Government White Papers

A Flask-based interactive web application that allows users to ask questions about government white papers and get intelligent answers with audio responses. It supports **English**, **Hindi**, **Marathi**, **Spanish**, and **French**, making public documents accessible to a broader audience.

---

## 📌 Table of Contents

* [✨ Features](#-features)
* [📁 Project Structure](#-project-structure)
* [🛠️ Setup Instructions](#-setup-instructions)
* [📦 Dependencies](#-dependencies)
* [🚀 Running the App](#-running-the-app)
* [📡 API Endpoints](#-api-endpoints)
* [🌐 Supported Languages](#-supported-languages)
* [🧠 How It Works](#-how-it-works)
* [🤝 Contributing](#-contributing)
* [📝 License](#-license)

---

## ✨ Features

* ✅ Uploads and parses a real-world government PDF.
* ✅ Accepts user queries via text or microphone input.
* ✅ Translates queries and responses using Google Translate.
* ✅ Uses NLP (spaCy) to extract the most relevant answers from the document.
* ✅ Text-to-speech (TTS) responses via `gTTS` with fallback to `pyttsx3`.
* ✅ Clean, responsive Bootstrap frontend with language toggle.
* ✅ Real-time interaction with a chat-style interface.

---

## 📁 Project Structure

```
project/
├── app.py                      # Main Flask backend
├── templates/
│   └── index.html              # Frontend UI
├── static/
│   └── audio/                  # Stores generated audio files
├── data/
│   └── a-blueprint-for-modern-digital-government-web-optimised.pdf
├── requirements.txt            # Required Python libraries
├── README.md                   # Project documentation (this file)
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/white-paper-assistant.git
cd white-paper-assistant
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLP Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Create Required Folders

Ensure `static/audio/` exists:

```bash
mkdir -p static/audio
```

---

## 📦 Dependencies

Listed in `requirements.txt`:

```
Flask
spacy
PyMuPDF
gTTS
googletrans==4.0.0rc1
pyttsx3
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

Start the server:

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📡 API Endpoints

| Endpoint        | Method | Description                                    |
| --------------- | ------ | ---------------------------------------------- |
| `/`             | GET    | Loads the HTML UI                              |
| `/ask`          | POST   | Accepts a JSON query, returns text & audio URL |
| `/tts`          | POST   | Converts any given text to speech              |
| `/audio/<file>` | GET    | Serves audio files                             |
| `/languages`    | GET    | Lists supported languages and voices           |

### `/ask` Example Request:

```json
POST /ask
{
  "query": "What is the goal of digital inclusion?",
  "language": "hi"
}
```

### `/ask` Example Response:

```json
{
  "response": "डिजिटल समावेश का लक्ष्य यह सुनिश्चित करना है कि...",
  "audio_url": "/audio/abc123.mp3",
  "language": "hi"
}
```

---

## 🌐 Supported Languages

| Language | Code | Voice |
| -------- | ---- | ----- |
| English  | en   | en-US |
| Hindi    | hi   | hi-IN |
| Marathi  | mr   | mr-IN |
| Spanish  | es   | es-ES |
| French   | fr   | fr-FR |

You can ask questions in any of these languages using the interface or microphone.

---

## 🧠 How It Works

1. **PDF Parsing:** Uses `PyMuPDF` to extract raw text from the uploaded white paper.
2. **Question Analysis:** NLP (spaCy) analyzes your question and document to find matching sentences.
3. **Translation:** Non-English questions are translated to English using Google Translate API.
4. **Answer Extraction:** Best matching sentence is selected using keyword overlap.
5. **Speech Synthesis:** Response is spoken out using `gTTS` or `pyttsx3`.
6. **Frontend Interface:** Built using Bootstrap and JavaScript for dynamic interaction.

-

## 🤝 Contributing

Feel free to submit issues or feature requests. To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Open a pull request

---

## 📝 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

--
