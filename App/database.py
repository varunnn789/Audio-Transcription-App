import sqlite3
import os

def init_db():
    """Initialize the SQLite database with users and sessions tables."""
    conn = sqlite3.connect("speech_textbot.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            audio_path TEXT NOT NULL,
            transcription TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user1", "password1"))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Authenticate a user by checking username and password."""
    conn = sqlite3.connect("speech_textbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def create_session(user_id, audio_path, transcription):
    """Create a new session for a user with the given audio file and transcription."""
    conn = sqlite3.connect("speech_textbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (user_id, audio_path, transcription) VALUES (?, ?, ?)",
                   (user_id, audio_path, transcription))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_session(session_id):
    """Retrieve a session by ID."""
    conn = sqlite3.connect("speech_textbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, audio_path, transcription FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    conn.close()
    return {"id": session_id, "user_id": session[0], "audio_path": session[1], "transcription": session[2]} if session else None

if __name__ == "__main__":
    init_db()