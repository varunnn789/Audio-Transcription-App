from transformers import pipeline
import soundfile as sf
import librosa
import numpy as np

print("Loading Whisper Tiny model...")
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", device=-1)

def transcribe_audio(audio_path):
    """
    Transcribe an audio file (WAV or MP3) using Whisper Tiny.
    Args:
        audio_path (str): Path to the audio file.
    Returns:
        str: Transcribed text.
    """
    try:
        audio, sr = sf.read(audio_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        print(f"Transcribing audio file: {audio_path}")
        result = whisper(audio)
        transcription = result["text"]
        return transcription

    except Exception as e:
        return f"Error during transcription: {str(e)}"

if __name__ == "__main__":
    audio_file = r"C:\Users\singh\Downloads\CSE 574_ML\Semester Project\App\test.flac"
    transcription = transcribe_audio(audio_file)
    print("Transcription:", transcription)