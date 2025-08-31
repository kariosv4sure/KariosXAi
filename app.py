from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Helper function to call Groq API
def call_groq_api(prompt, model="llama-3.1-70b-versatile"):
    api_url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful AI exam assistant for Maths and English."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1500
    }

    res = requests.post(api_url, headers=headers, json=data)

    # Raise error if API call fails
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()


@app.route('/', methods=['GET', 'POST'])
def home():
    response = ""

    if request.method == 'POST':
        user_question = request.form.get('question', '').strip()

        if user_question:
            # ✍️ AI prompt
            prompt = f"""
You are KARIOS EXAM GENIUS — an AI tutor that ONLY answers Maths and English exam-style questions with clarity and helpful explanation.

Here is the user's question:
\"\"\"{user_question}\"\"\"

Now, solve it or answer it as clearly as possible. If it is a writing task (like an essay or formal letter), write at least 450 words.
"""
            try:
                # ✅ Try main model first
                response = call_groq_api(prompt, model="llama-3.1-70b-versatile")
            except Exception as e:
                try:
                    # 🔄 Fallback to smaller/faster model
                    response = call_groq_api(prompt, model="llama-3.1-8b-instant")
                except Exception as e2:
                    # ⚠️ If both fail, show error details
                    response = f"⚠️ API Error: {str(e2)}"
        else:
            response = "❗ Please enter a question."

    return render_template("index.html", response=response)


if __name__ == '__main__':
    app.run(debug=True)
