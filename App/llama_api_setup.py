import requests


API_TOKEN = ""
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_answer(transcription, question):
    """
    Generate an answer using Llama 3.2 1B via API inference.
    Args:
        transcription (str): Transcribed audio text.
        question (str): User's text question.
    Returns:
        str: Generated answer.
    """
    try:
        prompt = f"Context: {transcription}\nQuestion: {question}\nAnswer:"
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 256,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        print("Sending API request to Llama 3.2 1B...")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result[0]["generated_text"].replace(prompt, "").strip()
        return answer

    except Exception as e:
        return f"Error during API call: {str(e)}"

if __name__ == "__main__":
    sample_transcription = "We discussed the budget for the new app in today’s meeting."
    sample_question = "What was discussed in the meeting?"    
    answer = generate_answer(sample_transcription, sample_question)
    print("Answer:", answer)