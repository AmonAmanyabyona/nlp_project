#user_interaction_moduleV2.py
import streamlit as st
from autocomplete_search5 import search_quotes
from audio_file_search7 import transcribe_audio
from second_model import chat_with_rag
from gtts import gTTS
from datetime import datetime
import tempfile
import os
import ffmpeg

def show_user_interaction():
    st.title("🧠 Wikiquote - User Interaction Flow")
    st.write("Search inspirational quotes and view context before chatting.")

    AUDIO_DIR = "spoken_words"
    os.makedirs(AUDIO_DIR, exist_ok=True)

    if "chat_completed" not in st.session_state:
        st.session_state.chat_completed = False

    def generate_speech(text):
        tts = gTTS(text, lang="en")
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        return temp_audio.name

    def adjust_speed(input_path, speed=1.0):
        output_path = input_path.replace(".mp3", f"_speed{speed}.mp3")
        try:
            (
                ffmpeg
                .input(input_path)
                .filter("atempo", speed)
                .output(output_path)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error:
            return input_path

    mode = st.radio("Choose input method:", ["Text", "Audio"])

    if mode == "Text" and not st.session_state.chat_completed:
        query = st.text_input("Type your question or phrase:")
        if query:
            quotes = search_quotes(query)
            if quotes:
                st.subheader("📚 Matching Quotes")
                for q in quotes:
                    st.markdown(f"> **{q['author']}**: \"{q['quote']}\"\n> _(Score: {q['score']:.2f})_")

                if st.button("🔮 Get Chatbot Response"):
                    response = chat_with_rag(query, quotes)
                    st.subheader("💬 LLAMA Response")
                    st.write(response)

                    audio_path = generate_speech(response)
                    st.audio(audio_path, format="audio/mp3")

                    if st.button("🔁 Start Over"):
                        st.session_state.chat_completed = False
                        st.experimental_rerun()
                    else:
                        st.session_state.chat_completed = True
            else:
                st.warning("No matching quotes found.")

    elif mode == "Audio" and not st.session_state.chat_completed:
        audio_file = st.audio_input("🎤 Speak your question or message:")
        if audio_file:
            audio_index = len(os.listdir(AUDIO_DIR)) + 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_path = os.path.join(AUDIO_DIR, f"audio{audio_index}_{timestamp}_raw.wav")

            with open(raw_path, "wb") as f:
                f.write(audio_file.getbuffer())
            st.success(f"✅ Audio saved as `{os.path.basename(raw_path)}`")
            st.audio(audio_file, format="audio/wav")

            clean_path = os.path.join(AUDIO_DIR, f"audio{audio_index}_{timestamp}.wav")
            try:
                (
                    ffmpeg
                    .input(raw_path)
                    .output(clean_path, format='wav', ac=1, ar=16000)
                    .overwrite_output()
                    .run(quiet=True)
                )
            except ffmpeg.Error:
                st.error("Audio conversion failed.")
                st.stop()

            if not os.path.exists(clean_path):
                st.error("Converted file not found.")
                st.stop()

            transcribed_query = transcribe_audio(clean_path)
            st.subheader("📝 Transcribed Text")
            st.write(transcribed_query)

            quotes = search_quotes(transcribed_query)
            if quotes:
                st.subheader("📚 Matching Quotes")
                for q in quotes:
                    st.markdown(f"> **{q['author']}**: \"{q['quote']}\"\n> _(Score: {q['score']:.2f})_")

                if st.button("🔮 Get Chatbot Response"):
                    response = chat_with_rag(transcribed_query, quotes)
                    st.subheader("💬 LLAMA Response")
                    st.write(response)

                    speed = st.slider("🕒 Playback Speed", 0.5, 2.0, 1.0, 0.1)
                    audio_path = generate_speech(response)
                    adjusted_path = adjust_speed(audio_path, speed)
                    st.audio(adjusted_path, format="audio/mp3")

                    for path in [audio_path, adjusted_path]:
                        try:
                            os.remove(path)
                        except:
                            st.warning(f"Could not delete file: {path}")

                    if st.button("🔁 Start Over"):
                        st.session_state.chat_completed = False
                        st.experimental_rerun()
                    else:
                        st.session_state.chat_completed = True
            else:
                st.warning("No matching quotes found.")
