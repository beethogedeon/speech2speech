import os
import streamlit as st
import requests
from openai import OpenAI
from io import BytesIO

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Hugging Face API URLs
DENDI_API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-ddn"
FON_API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-fon"
YOR_API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-yor"
BBA_API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-bba"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

# Load models at initialization
def load_models():
    requests.post(DENDI_API_URL, headers=headers, json={"inputs": "y"})
    requests.post(FON_API_URL, headers=headers, json={"inputs": "y"})
    requests.post(YOR_API_URL, headers=headers, json={"inputs": "y"})
    requests.post(BBA_API_URL, headers=headers, json={"inputs": "y"})

def transcribe(audio_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text

def generate_prompt_text(lang_source, lang_target, texte):
    prompt = f"""
    Traduit moi cet texte du {lang_source} vers le {lang_target} :
    {texte}
    renvoie uniquement le texte traduit.
    """
    return prompt

def get_gpt4_json_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert en traduction en langues locales béninoises. Tu peux traduire en Dendi, Yoruba, Fongbe et Baatonum"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

def translate_gpt(lang_source, lang_target, doc):
    dico_lang = {
        'fr': 'français', 'yo': 'yoruba',
        'en': 'anglais', 'den': 'dendi',
        'fon': 'fongbe', 'bba': 'baatonum'
    }
    lang_source = dico_lang[lang_source]
    lang_target = dico_lang[lang_target]
    prompt = generate_prompt_text(lang_source, lang_target, doc)
    response = get_gpt4_json_response(prompt)
    return response

def generate_speech(text, lang):
    lang_api_dict = {'fon': FON_API_URL, 'den': DENDI_API_URL, 'yo': YOR_API_URL, 'bba': BBA_API_URL}
    response = requests.post(lang_api_dict[lang], headers=headers, json={"inputs": text})
    return response.content

def speech2speech(audio_file, source, target):
    transcription = transcribe(audio_file)
    translation = translate_gpt(source, target, transcription)
    translated_speech = generate_speech(translation, target)
    return transcription, translation, translated_speech
