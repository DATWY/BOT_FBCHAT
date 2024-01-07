from flask import Flask, render_template
from telegram import Bot

app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '6856621284:AAEBfMFjcy0iX8gMTVA-y935dhW548_3BaI'
bot = Bot(token=BOT_TOKEN)

@app.route('/')
def home():
    # Replace 'TARGET_CHAT_ID' with the chat ID you want to send the greeting message to
    target_chat_id = '-4066405074'
    
    # Send a greeting message
    greeting_message = 'Hello, welcome to my Flask app!'
    bot.send_message(chat_id=target_chat_id, text=greeting_message)
    
    return render_template('index.html', status='Message sent successfully')

if __name__ == '__main__':
    app.run(debug=True)
