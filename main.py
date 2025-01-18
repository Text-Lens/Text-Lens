from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    # Get the input text from the request
    data = request.get_json()
    input_text = data.get('inputText', '')

    # Ensure the input text is not empty
    if not input_text:
        return jsonify({'error': 'No input text provided'}), 400

    # Initialize the client
    client = genai.Client(
        vertexai=True,
        project="textlens-448219",
        location="us-central1"
    )

    # Prepare the text for summarization
    text_part = types.Part.from_text(f"Summarize this text: {input_text}")

    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
            role="user",
            parts=[text_part]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ],
    )

    # Generate the summary
    result_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        for candidate in chunk.candidates:
            for part in candidate.content.parts:
                result_text += part.text  # Concatenate the text parts

    # Send back the summary as JSON
    return jsonify({'summary': result_text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
