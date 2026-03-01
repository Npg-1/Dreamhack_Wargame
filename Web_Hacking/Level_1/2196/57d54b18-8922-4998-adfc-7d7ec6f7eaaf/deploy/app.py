from flask import Flask, request, redirect, render_template, make_response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Crypto.Util.number import bytes_to_long
import random
import time
import base64
import urllib

app = Flask(__name__)
random.seed(time.time())

# base64로 인코딩 -> 디코딩 하는 과정을 거쳐서 꺠진 글자 없이 안전한 문자열로 바꿈
# 즉, NONCE는 따로 인코딩, 디코딩 된 값이 아니라 그냥 일반 랜덤한 문자열이라고 생각하면 될듯
NONCE = base64.b64encode(random.getrandbits(32).to_bytes(8, 'big')).decode()

USER_DATA = {
    "admin": "[**redacted**]",
    "user": "pass"
}

try:
    FLAG = open("./flag.txt", "r").read()
except:
    FLAG = "[**FLAG**]"

# 서버에 관리자 역할을 하는 가상의 브라우저를 띄워서 사용자가 제출한 특정 URL에 접속하게 만드는 기능을 함
def read_url(url, cookie={"name": "name", "value": "value"}):
    cookie.update({"domain": "127.0.0.1"})
    try:
        service = Service(executable_path="/usr/local/bin/chromedriver")
        options = webdriver.ChromeOptions()
        for _ in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox",
            "disable-dev-shm-usage",
        ]:
            options.add_argument(_)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get("http://127.0.0.1:8000/")
        driver.add_cookie({'name': 'username', 'value': 'admin'})
        driver.add_cookie(cookie)
        driver.get(url)
    except Exception as e:
        driver.quit()
        return False
    driver.quit()
    return True


# 들어온 param 값을 url 인코딩해서 url 뒤에 붙여서 반환
def check_xss(param, cookie={"name": "name", "value": "value"}):
    url = f"http://127.0.0.1:8000/memo?text={urllib.parse.quote(param)}"
    return read_url(url, cookie)



@app.route('/debug')
def debug():
    global NONCE
    param = request.args.get('param', '')
    if not check_xss(param, {'name': 'flag', 'value': FLAG.strip()}):
        return f'<script nonce={NONCE}>alert("wrong??");history.go(-1);</script>'

    return f'<script nonce={NONCE}>alert("good");history.go(-1);</script>'


# 사용자가 요청을 보내고 해당 요청을 처리를 다 끝내고 응답을 보내기 직전에 아래의 add_header()를 수행하는 부분
@app.after_request
def add_header(response):
    global NONCE
    response.headers[
        "Content-Security-Policy"
    ] = f"default-src 'self';base-uri 'none';style-src 'none';img-src *;script-src 'nonce-{NONCE}'"
    return response




# 홈페이지로 들어와! 근데 cookies에 username이 없다면 바로 /login으로 들어가!
@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        return redirect('/memo')
    return redirect('/login')




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USER_DATA and USER_DATA[username] == password:
            resp = make_response(redirect('/memo'))
            resp.set_cookie('username', username)
            return resp
        else:
            error = "Invalid username or password."

    resp = make_response(render_template("login.html", error=error))
    return resp



# 절.대.로.그.아.웃.을.하.지.마
@app.route('/logout', methods=['POST'])
def logout():
    global NONCE
    random.seed(time.time())

    # 로그아웃 될 때 NONCE가 초기화됨
    NONCE = base64.b64encode(random.getrandbits(32).to_bytes(8, 'big')).decode()

    resp = make_response(redirect('/login'))
    resp.delete_cookie('username')
    return resp



@app.route('/memo')
def memo():
    username = request.cookies.get('username')
    memo_text = request.args.get('text', '')
    
    if not username or username not in USER_DATA:
        return redirect('/login')

    if username != 'admin':
        return 'You are not admin!!!'

    try:
        r = random.getrandbits(32)
        memo_bytes = memo_text.encode('utf-8')
        memo_int = bytes_to_long(memo_bytes)
        xor_result = memo_int ^ r
        xor_hex = hex(xor_result)
    except Exception as e:
        xor_hex = f"Conversion fail: {e}"

    resp = make_response(render_template("memo.html", username=username, memo_text=memo_text, xor_result=xor_hex))
    return resp





app.run(host="0.0.0.0", port=8000)




