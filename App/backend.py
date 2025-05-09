from flask import Flask, request, jsonify
import torch
from transformers import pipeline
import soundfile as sf
import librosa
import numpy as np
import time

app = Flask(__name__)

print("Loading Whisper Tiny model...")
whisper = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=-1
)

print("Loading Llama 3.2 1B model...")
llama = pipeline(
    "text-generation",
    model="Llama-3.2-1B-Transformers",
    torch_dtype=torch.float32,
    device=-1
)

def transcribe_audio(audio_path):
    """
    Transcribe an audio file using Whisper Tiny.
    Args:
        audio_path (str): Path to the audio file.
    Returns:
        str: Transcribed text or error message.
    """
    try:
        start_time = time.time()
        audio, sr = sf.read(audio_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
            sr = 16000
        result = whisper(audio, return_timestamps=True)
        transcription = result["text"]

        print(f"Transcription took {time.time() - start_time:.2f} seconds")
        return transcription

    except Exception as e:
        return f"Error during transcription: {str(e)}"

def generate_answer(transcription, question):
    """
    Generate an answer using Llama 3.2 1B with transcription as context.
    Args:
        transcription (str): Transcribed audio text.
        question (str): User's text question.
    Returns:
        str: Generated answer or error message.
    """
    try:
        start_time = time.time()
        prompt = f"Context: {transcription}\nQuestion: {question}\nAnswer:"
        output = llama(
            prompt,
            max_new_tokens=128,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            return_full_text=False
        )
        answer = output[0]["generated_text"].strip()
        if "." in answer:
            answer = answer.split(".")[0] + "."
        print(f"Answer generation took {time.time() - start_time:.2f} seconds")
        return answer

    except Exception as e:
        return f"Error during generation: {str(e)}"

@app.route('/')
def home():
    return "Speech Textbot Backend Server is Running! Use the /process_query endpoint to transcribe audio and get answers."

@app.route('/process_query', methods=['POST'])
def process_query():
    """
    Endpoint to process an audio file and a text question.
    Expects a POST request with:
    - 'audio': Audio file (WAV or MP3)
    - 'question': Text question
    Returns:
    - JSON response with transcription and answer
    """
    try:
        if 'audio' not in request.files or 'question' not in request.form:
            return jsonify({"error": "Missing audio file or question"}), 400

        audio_file = request.files['audio']
        question = request.form['question']
        audio_path = "temp_audio.wav"
        audio_file.save(audio_path)
        transcription = transcribe_audio(audio_path)
        if "Error" in transcription:
            return jsonify({"error": transcription}), 500
        if question == "Initial transcription (no question)":
            answer = ""
        else:
            answer = generate_answer(transcription, question)
            if "Error" in answer:
                return jsonify({"error": answer}), 500
        return jsonify({
            "transcription": transcription,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_answer', methods=['POST'])
def generate_answer_endpoint():
    """
    Endpoint to generate an answer given a transcription and question.
    Expects a POST request with:
    - 'transcription': Transcribed text
    - 'question': Text question
    Returns:
    - JSON response with the answer
    """
    try:
        if 'transcription' not in request.form or 'question' not in request.form:
            return jsonify({"error": "Missing transcription or question"}), 400

        transcription = request.form['transcription']
        question = request.form['question']
        answer = generate_answer(transcription, question)
        if "Error" in answer:
            return jsonify({"error": answer}), 500
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)