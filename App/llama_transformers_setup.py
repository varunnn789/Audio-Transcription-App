import torch
from transformers import pipeline

#Define model path
model_id = "Llama-3.2-1B-Transformers"
print("Loading Llama 3.2 1B model...")
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float32,
    device=-1
)

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
        prompt = f"Context: {transcription}\nQuestion: {question}\nAnswer:"

        print("Generating answer...")
        output = pipe(
            prompt,
            max_new_tokens=256,  
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            return_full_text=False
        )
        answer = output[0]["generated_text"].strip()
        if "." in answer:
            answer = answer.split(".")[0] + "."
        return answer

    except Exception as e:
        return f"Error during generation: {str(e)}"

if __name__ == "__main__":
    sample_transcription = "We discussed the budget for the new app in today’s meeting."
    sample_question = "What was discussed in the meeting?"
    answer = generate_answer(sample_transcription, sample_question)
    print("Answer:", answer)