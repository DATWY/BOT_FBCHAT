from flask import Flask, render_template
from telegram import Bot
import time
i = 0
app = Flask(__name__)
while True:
    i+=1
    time.sleep(1)
@app.route('/')
def home():
    # Replace 'TARGET_CHAT_ID' with the chat ID you want to send the greeting message to
    target_chat_id = '-4066405074'
    
    # Send a greeting message
    greeting_message = 'Hello, welcome to my Flask app!'
    bot.send_message(chat_id=target_chat_id, text=greeting_message)
    
    return i

if __name__ == '__main__':
    app.run(debug=True)
