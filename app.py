import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')

def index():
    return "Welcome to TextLens!"

openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve the HTML page
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    questions = None
    error = None
    text = ""

    if request.method == 'POST':
        text = request.form['text']

        if not text:
            error = "Please enter some text."
        else:
            # Summarize the text
            if 'summarize' in request.form:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Summarize this: {text}",
                    max_tokens=100
                )
                summary = response.choices[0].text.strip()

            # Generate questions based on the text
            if 'test-yourself' in request.form:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Generate multiple-choice questions about this text: {text}",
                    max_tokens=150
                )
                questions = response.choices[0].text.strip()

    return render_template('index.html', summary=summary, questions=questions, error=error, text=text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
