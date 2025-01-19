import os
import openai
from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return "Welcome to TextLens!"

openai.api_key = os.getenv("OPENAI_API_KEY")

# Example summarization

def summarize_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize this: {text}",
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Example question generation
def generate_questions(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate multiple-choice questions about this text: {text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
