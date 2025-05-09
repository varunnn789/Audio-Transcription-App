import streamlit as st
import requests
import os
from database import init_db, authenticate_user, create_session, get_session

init_db()
st.title("Speech Textbot")

def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = None
    if "transcription" not in st.session_state:
        st.session_state["transcription"] = None
    if "show_transcription" not in st.session_state:
        st.session_state["show_transcription"] = False

initialize_session_state()
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = authenticate_user(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

else:
    st.subheader("Upload Audio and Ask Questions")
    if st.session_state.session_id is None:
        audio_file = st.file_uploader("Upload an audio file (WAV, MP3, FLAC)", type=["wav", "mp3", "flac"])
        if audio_file:
            audio_path = f"uploads/{audio_file.name}"
            os.makedirs("uploads", exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
            with st.spinner("Transcribing audio..."):
                files = {"audio": open(audio_path, "rb")}
                data = {"question": "Initial transcription (no question)"}
                response = requests.post("http://127.0.0.1:5000/process_query", files=files, data=data)
                files["audio"].close()

            if response.status_code == 200:
                result = response.json()
                transcription = result["transcription"]
                session_id = create_session(st.session_state.user_id, audio_path, transcription)
                st.session_state.session_id = session_id
                st.session_state.transcription = transcription
                st.session_state.show_transcription = False
                st.success("Audio transcribed successfully!")
                st.write("Debug: Session ID set to", st.session_state.session_id)
                st.rerun()
            else:
                st.error(f"Error: {response.json()['error']}")
                st.write("Debug: Failed to set session ID")
    else:
        st.write("Debug: Inside else block - Session ID:", st.session_state.session_id)
        st.write("Debug: Rendering toggle button")
        if st.button("Show Transcription" if not st.session_state.show_transcription else "Hide Transcription"):
            st.session_state.show_transcription = not st.session_state.show_transcription
            st.write("Debug: Show transcription toggled to", st.session_state.show_transcription)

        if st.session_state.show_transcription:
            st.write("Transcription:", st.session_state.transcription)
        st.subheader("Ask Questions")
        st.write("Debug: Rendering question input")
        question = st.text_input("Enter your question based on the transcription:", key="question_input")
        if st.button("Submit Question"):
            if question:
                with st.spinner("Generating answer..."):
                    data = {
                        "transcription": st.session_state.transcription,
                        "question": question
                    }
                    response = requests.post("http://127.0.0.1:5000/generate_answer", data=data)

                if response.status_code == 200:
                    result = response.json()
                    answer = result["answer"]
                    st.write("Answer:", answer)
                else:
                    st.error(f"Error: {response.json()['error']}")

        if st.button("End Session"):
            st.session_state.session_id = None
            st.session_state.transcription = None
            st.session_state.show_transcription = False
            st.success("Session ended. Upload a new audio file to start a new session.")
            st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.session_id = None
        st.session_state.transcription = None
        st.session_state.show_transcription = False
        st.success("Logged out successfully!")
        st.rerun()