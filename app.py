from flask import Flask, render_template, request, jsonify
import openai
import os


# Load API Key dari .env jika digunakan
api_key = ("")
# Setup client
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)
chat_history = []

# Konfigurasi
MODEL_NAME = "ft:gpt-4o-mini-2024-07-18:wahyu-luna:test-1:Bs4pmewS"
TEMPERATURE = 0.9
@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['prompt']
    chat_history.append({'role': 'user', 'message': user_input})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": "anda dalah assisten HR yang berpengetahuan luas,lakukan perkenalan diri lalu tugas anda menajawab pertanyaan seputar HR dan apa bila pertanyaan di luar konteks jawab: saya tidak bisa membantu"
}
            ] + [{"role": msg['role'], "content": msg['message']} for msg in chat_history]
        )

        bot_message = response.choices[0].message.content.strip()

    except Exception as e:
        bot_message = f"[Error dari OpenAI: {str(e)}]"

    chat_history.append({'role': 'assistant', 'message': bot_message})
    return jsonify({'response': bot_message})

if __name__ == '__main__':
    app.run(debug=True)