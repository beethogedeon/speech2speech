import os
import streamlit as st
import requests
from openai import OpenAI
from io import BytesIO
from utils import *

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Streamlit UI
st.title('Audio-to-Audio Translation App')

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

dico_lang_2 = {
        'Français':'fr',  'Yoruba':'yo',
        'Anglais':'en',   'Dendi':'den',
        'Fongbe':'fon',  'Baatonum':'bba'
    }

# Select source and target languages
source_lang = dico_lang_2[st.selectbox("Select source language", ['Français', 'Anglais'])]
target_lang = dico_lang_2[st.selectbox("Select target language", ['Dendi', 'Baatonum', 'Fongbe', 'Yoruba'])]

if uploaded_file and st.button("Translate"):
    transcription, translation, translated_speech = speech2speech(uploaded_file, source_lang, target_lang)

    # Display the results
    st.header("Transcription of Original Audio")
    st.write(transcription)

    st.header("Translated Text")
    st.write(translation)

    st.header("Translated Audio")
    st.audio(BytesIO(translated_speech), format="audio/wav")