#chat_flow9.py
import streamlit as st
from autocomplete_search5 import search_quotes
from chat_completion import chat_with_rag
from audio_file_search7 import transcribe_audio
from gtts import gTTS
import tempfile
import os

# 🎛 Page setup
st.set_page_config(page_title="Wikiquote Chatbot", layout="centered")
st.title("🧠 Wikiquote Chatbot")
st.write("Ask a question or speak your thoughts — and get inspiring replies!")

# Session initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_processed_id" not in st.session_state:
    st.session_state.last_processed_id = None

#TTS Function
def generate_speech(text):
    tts = gTTS(text, lang="en")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

#Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#Input selector
# mode = st.radio("Choose your input method:", ["Text", "Audio"], horizontal=True)
mode = st.radio(
    "Choose your input method:",
    [None, "Text", "Audio"],
    index=0,
    format_func=lambda x: "" if x is None else x,
    key="input_mode",
    horizontal=True
)


# TEXT MODE
if mode == "Text":
    prompt = st.chat_input("Which quote?...")

    # Only process new prompt
    if prompt and st.session_state.last_processed_id != prompt:
        st.session_state.last_processed_id = prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        matched_quotes = search_quotes(prompt)
        if not matched_quotes:
            matched_quotes = [{"author": "Unknown", "quote": "No quotes available.", "score": 0.0}]

        response = chat_with_rag(prompt, matched_quotes)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)
            audio_path = generate_speech(response)
            st.audio(audio_path, format="audio/mp3")
            try:
                os.remove(audio_path)
            except:
                st.warning("Could not delete temporary audio file.")

# AUDIO MODE
elif mode == "Audio":
    audio_file = st.audio_input("🎤 Which quote?...")
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_file.getbuffer())
            temp_path = f.name

        transcribed_text = transcribe_audio(temp_path)

        # Only process new audio message
        if transcribed_text and st.session_state.last_processed_id != transcribed_text:
            st.session_state.last_processed_id = transcribed_text

            st.session_state.messages.append({"role": "user", "content": transcribed_text})
            with st.chat_message("user"):
                st.markdown(transcribed_text)

            matched_quotes = search_quotes(transcribed_text)
            if not matched_quotes:
                matched_quotes = [{"author": "Unknown", "quote": "No quotes available.", "score": 0.0}]

            response = chat_with_rag(transcribed_text, matched_quotes)
            st.session_state.messages.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)
                audio_path = generate_speech(response)
                st.audio(audio_path, format="audio/mp3")
                try:
                    os.remove(audio_path)
                except:
                    st.warning("Could not delete temporary audio file.")

# Continue / Exit prompt (safe placement)
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "assistant":
    continue_chat = st.radio(
        "Would you like to ask about another quote?",
        [None, "Yes", "No"],
        index=0,
        format_func=lambda x: "" if x is None else x,
        key=f"continue_{len(st.session_state.messages)}",
        horizontal=True
    )

    if continue_chat == "No":
        st.info("Thanks for chatting! Feel free to close the tab or change the input method to restart.")
        st.stop()
