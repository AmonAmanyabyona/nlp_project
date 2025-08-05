#chat_flow_module.py
import streamlit as st
from autocomplete_search5 import search_quotes
from chat_completion import chat_with_rag
from audio_file_search7 import transcribe_audio
from gtts import gTTS
import tempfile
import os

def show_chat_flow():
    st.title("💬 Let's Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_processed_id" not in st.session_state:
        st.session_state.last_processed_id = None

    def generate_speech(text):
        tts = gTTS(text, lang="en")
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        return temp_audio.name

    # Display previous messages with custom layout
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            col_msg, col_avatar = st.columns([0.4, 0.4])
            with col_msg:
                st.markdown(
                    f"<div style='text-align: right; padding: 10px; background-color: #e6f7ff; border-radius: 10px; margin-bottom: 10px;'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
            with col_avatar:
                st.image("images/Amon_photo.jpg", width=100)
        else:
            col_avatar, col_msg = st.columns([0.1, 0.9])
            with col_avatar:
                st.image("images/bot.jpg", width=36)
            with col_msg:
                st.markdown(
                    f"<div style='text-align: left; padding: 10px; background-color: #f0f0f0; border-radius: 10px; margin-bottom: 10px;'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )

    mode = st.radio(
        "Choose your input method:",
        [None, "Text", "Audio"],
        index=0,
        format_func=lambda x: "" if x is None else x,
        key="input_mode_chatflow",
        horizontal=True
    )

    if mode == "Text":
        prompt = st.chat_input("Which quote?...")

        if prompt and st.session_state.last_processed_id != prompt:
            st.session_state.last_processed_id = prompt
            st.session_state.messages.append({"role": "user", "content": prompt})

            col_msg, col_avatar = st.columns([0.5, 0.5])
            with col_msg:
                st.markdown(
                    f"<div style='text-align: right; padding: 10px; background-color: #e6f7ff; border-radius: 10px; margin-bottom: 10px;'>{prompt}</div>",
                    unsafe_allow_html=True
                )
            with col_avatar:
                st.image("images/Amon_photo.jpg", width=70)

            quotes = search_quotes(prompt)
            if not quotes:
                quotes = [{"author": "Unknown", "quote": "No quotes available.", "score": 0.0}]

            response = chat_with_rag(prompt, quotes)
            st.session_state.messages.append({"role": "assistant", "content": response})

            col_avatar, col_msg = st.columns([0.1, 0.9])
            with col_avatar:
                st.image("images/bot.jpg", width=36)
            with col_msg:
                st.markdown(
                    f"<div style='text-align: left; padding: 10px; background-color: #f0f0f0; border-radius: 10px; margin-bottom: 10px;'>{response}</div>",
                    unsafe_allow_html=True
                )
                audio_path = generate_speech(response)
                st.audio(audio_path, format="audio/mp3")
                try:
                    os.remove(audio_path)
                except:
                    st.warning("Could not delete temporary audio file.")

    elif mode == "Audio":
        audio_file = st.audio_input("🎤 Which quote?...")
        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_file.getbuffer())
                temp_path = f.name

            transcribed = transcribe_audio(temp_path)
            if transcribed and st.session_state.last_processed_id != transcribed:
                st.session_state.last_processed_id = transcribed
                st.session_state.messages.append({"role": "user", "content": transcribed})

                col_msg, col_avatar = st.columns([0.5, 0.5])
                with col_msg:
                    st.markdown(
                        f"<div style='text-align: right; padding: 10px; background-color: #e6f7ff; border-radius: 10px; margin-bottom: 10px;'>{transcribed}</div>",
                        unsafe_allow_html=True
                    )
                with col_avatar:
                    st.image("images/Amon_photo.jpg", width=70)

                quotes = search_quotes(transcribed)
                if not quotes:
                    quotes = [{"author": "Unknown", "quote": "No quotes available.", "score": 0.0}]

                response = chat_with_rag(transcribed, quotes)
                st.session_state.messages.append({"role": "assistant", "content": response})

                col_avatar, col_msg = st.columns([0.1, 0.9])
                with col_avatar:
                    st.image("images/bot.jpg", width=36)
                with col_msg:
                    st.markdown(
                        f"<div style='text-align: left; padding: 10px; background-color: #f0f0f0; border-radius: 10px; margin-bottom: 10px;'>{response}</div>",
                        unsafe_allow_html=True
                    )
                    audio_path = generate_speech(response)
                    st.audio(audio_path, format="audio/mp3")
                    try:
                        os.remove(audio_path)
                    except:
                        st.warning("Could not delete temporary audio file.")

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
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
