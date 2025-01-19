import os
import openai
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    print("API key found!")
else:
    print("API key not found!")
# Function for summarizing text
def summarize_text(text):
    prompt = f"Please summarize the following text:\n\n{text}\n\nProvide a concise summary with the main points."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or any other chat model you're using
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Please summarize the provided text."},
            {"role": "user", "content": text}
        ],
        max_tokens=150,
        temperature=0.5
    )
    return response['choices'][0]['message']['content']


# Function for generating multiple-choice questions
def generate_questions(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate multiple-choice questions about this text: {text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Route for handling the form
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        text = request.form['text']
        action = request.form['action']

        if action == 'summarize':
            result = summarize_text(text)
        elif action == 'test_yourself':
            result = generate_questions(text)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
