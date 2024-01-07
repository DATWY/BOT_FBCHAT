from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-message', methods=['POST'])
def save_message():
    data = request.get_json()
    messages.append(data)
    return jsonify(success=True)

@app.route('/get-messages')
def get_messages():
    return jsonify(success=True, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
