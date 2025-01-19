from flask import Flask, render_template, request
from google.cloud import genai
import os

# Initialize Flask app
app = Flask(__name__)

# Set up GenAI client
client = genai.Client(
    vertexai=True,
    project="textlens-448219",  # Replace with your project ID
    location="us-central1"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    user_text = request.form['user-text']

    # Call GenAI API to summarize the text
    summary = summarize_text(user_text)

    return render_template('index.html', summary=summary)

@app.route('/test', methods=['POST'])
def test():
    user_text = request.form['user-text']

    # Generate questions using GenAI
    questions, answers = generate_questions_from_text(user_text)
    
    return render_template('test.html', questions=questions, answers=answers)

def summarize_text(text):
    prompt = f"Summarize the following text:\n\n{text}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", 
        contents=[genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])]
    )
    
    return response.candidates[0].content.parts[0].text.strip()

def generate_questions_from_text(text):
    prompt = f"Generate multiple-choice questions based on the following text:\n\n{text}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", 
        contents=[genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])]
    )
    
    questions = response.candidates[0].content.parts[0].text.strip().split("\n")  # Assuming each question is on a new line
    answers = [
        ["Option 1", "Option 2", "Option 3", "Option 4"] for _ in questions
    ]
    
    return questions, answers

if __name__ == '__main__':
    app.run(debug=True)
