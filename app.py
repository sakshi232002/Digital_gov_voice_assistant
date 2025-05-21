import os
import uuid
import fitz  # PyMuPDF
import spacy
import pyttsx3
from flask import Flask, request, jsonify, send_from_directory, render_template
from googletrans import Translator
from gtts import gTTS
import json

# Initialize Flask app
app = Flask(__name__)

# Load NLP models once
try:
    nlp_en = spacy.load("en_core_web_sm")
    print("Loaded English NLP model")
except:
    print("Warning: English model not found. Using spaCy's default model.")
    nlp_en = spacy.load("en")

# Initialize translator
translator = Translator()

# Directory to save audio responses
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# List of supported languages
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'nlp': nlp_en, 'voice': 'en-US'},
    'hi': {'name': 'Hindi', 'nlp': nlp_en, 'voice': 'hi-IN'},  # Using English NLP for processing, translation for response
    'mr': {'name': 'Marathi', 'nlp': nlp_en, 'voice': 'mr-IN'},
    'es': {'name': 'Spanish', 'nlp': nlp_en, 'voice': 'es-ES'},
    'fr': {'name': 'French', 'nlp': nlp_en, 'voice': 'fr-FR'}
}

# Load and preprocess the PDF text
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Find best answer sentence from text given a question
def find_answer(question, document_text, lang_code='en'):
    # Always process in English first (since document is in English)
    if lang_code != 'en':
        try:
            # Translate question to English for processing
            question = translator.translate(question, dest='en').text
        except Exception as e:
            print(f"Translation error: {e}")
            # Continue with original question if translation fails
    
    # Process with English NLP model
    doc = nlp_en(document_text.lower())
    question_doc = nlp_en(question.lower())
    
    # Extract keywords from question
    keywords = [token.lemma_ for token in question_doc if not token.is_stop and token.is_alpha]
    
    # Find best matching sentence
    best_sentence = ""
    max_overlap = 0
    
    for sent in doc.sents:
        sent_tokens = [token.lemma_ for token in sent if not token.is_stop and token.is_alpha]
        overlap = len(set(keywords) & set(sent_tokens))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sentence = sent.text
    
    answer = best_sentence if best_sentence else "Sorry, I couldn't find an answer."
    
    # Translate answer back to requested language if not English
    if lang_code != 'en' and answer:
        try:
            answer = translator.translate(answer, dest=lang_code).text
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original answer if translation fails
    
    return answer

# Convert text to speech and save as audio file
def text_to_speech(text, lang_code='en'):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    
    try:
        # Use gTTS for better language support
        voice = SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES['en'])['voice']
        tts = gTTS(text=text, lang=voice[:2])  # Extract language code (first 2 chars)
        tts.save(filepath)
    except Exception as e:
        print(f"TTS error with gTTS: {e}")
        try:
            # Fallback to pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, filepath)
            engine.runAndWait()
        except Exception as e2:
            print(f"TTS fallback error: {e2}")
            # Create empty file to avoid 404 errors
            with open(filepath, 'wb') as f:
                f.write(b'')
    
    return filename

# Load the document once on startup
PDF_PATH = "data/a-blueprint-for-modern-digital-government-web-optimised.pdf"
print("Loading document text...")
DOCUMENT_TEXT = extract_text_from_pdf(PDF_PATH)
print(f"Document loaded. Text length: {len(DOCUMENT_TEXT)} characters")

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "").strip()
    lang_code = data.get("language", "en")
    
    # Validate language code
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = "en"  # Default to English
    
    if not query:
        # Return empty response in the requested language
        empty_responses = {
            'en': "Please ask a question.",
            'hi': "कृपया एक प्रश्न पूछें।",
            'mr': "कृपया एक प्रश्न विचारा.",
            'es': "Por favor, haga una pregunta.",
            'fr': "Veuillez poser une question."
        }
        return jsonify({"response": empty_responses.get(lang_code, empty_responses['en'])})

    # Get answer based on query and language
    answer = find_answer(query, DOCUMENT_TEXT, lang_code)
    
    # Generate audio for the answer
    audio_filename = text_to_speech(answer, lang_code)
    audio_url = f"/audio/{audio_filename}"

    return jsonify({
        "response": answer,
        "audio_url": audio_url,
        "language": lang_code
    })

@app.route("/tts", methods=["POST"])
def generate_tts():
    data = request.get_json()
    text = data.get("text", "").strip()
    lang_code = data.get("language", "en")
    
    if not text:
        return jsonify({"error": "No text provided"})
    
    # Generate audio for the text
    audio_filename = text_to_speech(text, lang_code)
    audio_url = f"/audio/{audio_filename}"
    
    return jsonify({
        "audio_url": audio_url,
        "language": lang_code
    })

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

# Add language info endpoint
@app.route("/languages")
def get_languages():
    languages = {}
    for code, info in SUPPORTED_LANGUAGES.items():
        languages[code] = {
            'name': info['name'],
            'voice': info['voice']
        }
    return jsonify(languages)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Startup error: {e}")