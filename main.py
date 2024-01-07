from flask import Flask, render_template, request, jsonify
from fbchat import Client, Message, _get_params
from fbchat._client import ClientError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

def solve_checkpoint(email, password, browser):
    # Sử dụng Selenium để giải quyết bước kiểm tra an toàn
    driver = webdriver.Chrome()  # Cần cài đặt ChromeDriver: https://sites.google.com/chromium.org/driver/
    driver.get('https://www.facebook.com')

    # Điền thông tin đăng nhập
    driver.find_element_by_id('email').send_keys(email)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_id('pass').send_keys(Keys.ENTER)

    time.sleep(5)  # Chờ một khoảng thời gian để xử lý kiểm tra an toàn (điều này có thể cần điều chỉnh)

    # Lấy URL hiện tại
    current_url = driver.current_url
    driver.quit()

    # Trả về URL để người dùng tiếp tục xử lý
    return current_url

def send_fb_message(email, password, user_id, message):
    try:
        # Thử đăng nhập bằng fbchat
        client = Client(email, password)

        # Lấy thông tin người dùng để gửi tin nhắn
        user = client.searchForUsers(user_id)[0]

        # Gửi tin nhắn
        sent = client.send(Message(text=message), thread_id=user.uid, thread_type=user.type)

        # Đóng kết nối sau khi gửi tin nhắn
        client.logout()

        return sent
    except ClientError as e:
        if e.code == 1357001:  # Kiểm tra an toàn checkpoint
            checkpoint_url = solve_checkpoint(email, password, e.details.get("url"))
            return {'checkpoint_url': checkpoint_url}
        else:
            return {'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_id = request.form.get('user_id')
        message = request.form.get('message')

        result = send_fb_message(email, password, user_id, message)

        if 'checkpoint_url' in result:
            return render_template('checkpoint.html', checkpoint_url=result['checkpoint_url'])
        elif 'error' in result:
            return render_template('index.html', error=result['error'])

        return render_template('index.html', sent=True)

    return render_template('index.html', sent=None)

if __name__ == '__main__':
    app.run(debug=True)
