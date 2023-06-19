from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

API = "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"
conversation = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    text = data.get('data')
    openai.api_key = API

    user_input = text
    print(user_input)

    global conversation

    try:
        conversation.append(f"User: {user_input}")
        prompt = "\n".join(conversation)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        model_reply = response['choices'][0]['text']
        conversation.append(f"AI: {model_reply}")
        print(response, model_reply)

        return jsonify({"response": True, "message": model_reply})

    except Exception as e:
        print(e)
        error_message = f'Error: {str(e)}'
        return jsonify({"message": error_message, "response": False})


if __name__ == '__main__':
    app.run(debug=False)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=False)
