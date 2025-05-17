# Intro to Machine Learning Project: Context-Aware Speech Textbot

This project implements a context-aware speech textbot using pre-trained Automatic Speech Recognition (ASR) and Large Language Model (LLM) models. The system transcribes audio input using Whisper Tiny, generates context-aware responses with Llama 3.2 1B. The app is deployed via a Streamlit interface with a flask based backend for processing and a database for storing conversation history.

This README provides instructions to set up and run the code files included in the project zip, covering dependencies, required access, and execution steps for Google Colab or local environments.

## Project Overview
- **ASR Model**: Pre-trained Whisper Tiny (`openai/whisper-tiny`) for speech-to-text.
- **LLM Model**: Pre-trained Llama 3.2 1B (`meta-llama/Llama-3.2-1B`) for context-aware response generation.
- **Deployment**: Streamlit app with a frontend, flask based backend, and SQLite database (`speech_textbot.db`).
- **Fine-Tuning**:
  - Whisper Tiny fine-tuned on LibriSpeech (2205 training, 271 testing files extracted).
  - Llama 3.2 1B fine-tuned on SQuAD for question-answering.

## Code Files
The zip file contains the following files and folders, with their purposes:
1. **whisper_setup.py**
   - **Purpose**: Sets up the Whisper Tiny model for ASR.
   - **Output**: Configured ASR model ready for use in the app.

2. **plot_script.ipynb**
   - **Purpose**: Jupyter notebook for visualizing fine-tuning results (not required to run the app).
   - **Functionality**: Generates plots (e.g., WER, CER, F1 scores) from fine-tuning experiments.
   - **Output**: Visualizations saved as image file.

3. **llama_transformers_setup.py**
   - **Purpose**: Sets up the Llama 3.2 1B model using Transformers.
   - **Output**: Configured LLM model ready for use in the app.

4. **llama_api_setup.py**
   - **Purpose**: Alternative setup for Llama 3.2 1B using an API (if applicable, unused in current setup).
   - **Output**: API client for LLM inference (optional).

5. **frontend.py**
   - **Purpose**: Implements the Streamlit frontend for user interaction.
   - **Functionality**: Provides a web interface to upload audio, display transcriptions, and play LLM responses.
   - **Output**: Streamlit app interface.

6. **database.py**
   - **Purpose**: Manages the SQLite database for storing conversation history.
   - **Functionality**: Creates and interacts with `speech_textbot.db` to store user inputs and responses.
   - **Output**: SQLite database file (`speech_textbot.db`).

7. **backend.py**
   - **Purpose**: Handles the app’s backend logic.
   - **Functionality**: 
     - Integrates ASR for speech-to-text.
     - Uses LLM for context-aware response generation.
     - Stores conversation history in the database.
   - **Output**: Processed transcriptions and responses.

9. **uploads** (folder)
   - **Purpose**: Stores user-uploaded audio files.
   - **Functionality**: Temporary storage for audio inputs (e.g., `temp_audio.wav`).
   - **Output**: Audio files uploaded via the Streamlit app.

10. **Llama-3.2-1B-Transformers** (Will need to be downloaded using the script provided, cannot upload the zip due to model size otherwise)
    - **Purpose**: Stores model files for Llama 3.2 1B (Transformers setup).
    - **Output**: Model files for inference (auto-downloaded if not present).

12. **speech_textbot.db**
    - **Purpose**: SQLite database file for conversation history.
    - **Functionality**: Stores user audio transcriptions and LLM responses.
    - **Output**: Persistent database file.

13. **temp_audio.wav**
    - **Purpose**: Temporary audio file for user input.
    - **Functionality**: Example of an uploaded audio file processed by the app.
    - **Output**: Temporary file (replaced with new uploads).

14. **requirements.txt**
    - **Purpose**: Lists Python dependencies for the project.
    - **Functionality**: Used to install required libraries.

15. **Llama_3_2_1B_Fine_Tune_and_Evaluation.ipynb** (in parent directory)
    - **Purpose**: Jupyter notebook for fine-tuning and evaluating Llama 3.2 1B.
    - **Functionality**: Fine-tunes Llama 3.2 1B on SQuAD, evaluates F1 and Exact Match scores.
    - **Output**: Fine-tuned model checkpoints and evaluation metrics.

16. **ASR_Model_Fine_Tuning_and_Evaluation.ipynb** (in parent directory)
    - **Purpose**: Jupyter notebook for fine-tuning and evaluating Whisper Tiny.
    - **Functionality**: Fine-tunes Whisper Tiny on LibriSpeech, evaluates WER and CER.
    - **Output**: Fine-tuned model checkpoints and evaluation metrics.

## Requirements
### Software and Libraries
- **Python**: Version 3.8 or higher.
- **Dependencies**: Install via `pip install -r requirements.txt`. Key libraries include:
- **requirements.txt** (included in zip, as listed above).

### Hardware
- **Google Colab**: Needed for running the app (use A100 GPU as the same was used in the project).
- **Streamlit Account**: Free tier sufficient for inference and Streamlit app.
- **Local Machine**:
  - CPU: Minimum 8 cores, 32GB RAM.
  - GPU: NVIDIA GPU with at least 16GB VRAM.
  - Storage: At least 10GB free space for models and temporary files.

### Access Requirements
- **Hugging Face Account**:
  - Required for accessing models (`openai/whisper-tiny`, `meta-llama/Llama-3.2-1B`).
  - Generate a Hugging Face token at [Hugging Face Settings](https://huggingface.co/settings/tokens).
  - Set token as environment variable

- **Google Colab**:
  - Google account for access.
  - Mount Google Drive to store temporary files

- **Model Access**:
  - You will need access to the meta Llama 3.2 1B Model and Whisper Tiny model on hugging face


## Usage
- Upload an audio file via the Streamlit interface (stored in the `uploads` folder as `temp_audio.wav`).
- The app transcribes the audio using Whisper Tiny, generates a response with Llama 3.2 1B.
- Conversation history is stored in `speech_textbot.db`.

## Notes
- Ensure your Hugging Face token has access to `meta-llama/Llama-3.2-1B`, as it is a gated model.
- Due to the size of the models and data files, as well as the limits imposed by github on repo size, we have excluded thse files. However, we have included setup scripts that may be run to download the files. In case of limited computational resources, please skip the fine tuning steps to integrate the base models directly