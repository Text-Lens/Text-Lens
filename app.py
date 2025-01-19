import openai

openai.api_key = "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"

# Example summarization
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize this: {text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Example question generation
def generate_questions(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate multiple-choice questions about this text: {text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()
