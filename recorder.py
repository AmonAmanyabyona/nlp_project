import streamlit as st

st.title("🎙️ Voice Recorder")

audio_file = st.audio_input("Click to record your voice")

if audio_file:
    st.audio(audio_file)  # Playback
    with open("saved_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())
    st.success("Audio saved successfully!")
