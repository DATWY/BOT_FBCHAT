from flask import Flask, render_template, request, jsonify
from fbchatv1 import *
from fbchatv1 import Client, Message

app = Flask(__name__)

def send_fb_message(email, password, user_id, message):
    try:
        # Tạo một đối tượng Client của fbchat
        client = Client(email, password)

        # Lấy thông tin người dùng để gửi tin nhắn
        user = client.searchForUsers(user_id)[0]

        # Gửi tin nhắn
        sent = client.send(Message(text=message), thread_id=user.uid, thread_type=user.type)

        # Đóng kết nối sau khi gửi tin nhắn
        client.logout()

        return sent
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_id = request.form.get('user_id')
        message = request.form.get('message')

        sent = send_fb_message(email, password, user_id, message)
        return render_template('index.html', sent=sent)

    return render_template('index.html', sent=None)

if __name__ == '__main__':
    app.run(debug=True)
