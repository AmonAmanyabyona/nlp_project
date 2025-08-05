#audio_file_search7.py
import whisper
import subprocess
from pathlib import Path
from autocomplete_search5 import search_quotes

# 🎙️ Configuration
MODEL_NAME = "small"
AUDIO_DIR = Path("audios") 
# AUDIO_DIR = Path("spoken_words") 

WAV_FILENAME = "converted.wav"

#Load Whisper ASR model
model = whisper.load_model(MODEL_NAME)

#Convert audio to WAV using ffmpeg
def convert_to_wav(input_path, output_path=WAV_FILENAME):
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(input_path),
            "-ar", "48000", "-ac", "1", "-f", "wav", str(output_path)
        ], check=True)
        print(f"Converted {input_path} → {output_path}")
        return output_path
    except subprocess.CalledProcessError:
        print("Failed to convert audio.")
        return None

# Transcribe audio
def transcribe_audio(filepath):
    print("🧠 Transcribing audio...")
    result = model.transcribe(filepath)
    text = result["text"].strip()
    print(f"\n Transcribed text: {text}")
    return text

# Main app logic
def main():
    print("\n🎧 Available audio files:")
    audio_files = list(AUDIO_DIR.glob("*.*"))
    for i, file in enumerate(audio_files, 1):
        print(f" {i}. {file.name}")
    choice = input("\nSelect audio file number: ").strip()

    try:
        selected_index = int(choice) - 1
        audio_path = audio_files[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Convert to WAV
    wav_path = convert_to_wav(audio_path)
    if not wav_path:
        return

    # Transcribe and search quotes
    phrase = transcribe_audio(wav_path)
    matches = search_quotes(phrase)

    if matches:
        print("\n🔍 Matching quotes:\n")
        for i, match in enumerate(matches, 1):
            print(f" {i}. {match['author']}:")
            print(f"   \"{match['quote']}\"")
            print(f"   (Score: {match['score']:.2f})\n")
    else:
        print("No matching quotes found.")

# Run the script
if __name__ == "__main__":
    main()
