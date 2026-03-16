from flask import Flask, request, send_from_directory, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
import os
import threading
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

try:
    FLAG = open("./flag", "r").read()
except:
    FLAG = "[**FLAG**]"

@app.route('/')
def index():
    file = request.args.get('file', 'uploads/default.svg') 
    return render_template('index.html', file=file)

@app.route('/uploads/<filename>')       # /uploads/<filename> 에서 들어가는 값에 따라 filename 변수에 저장됨
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    # Upload SVG 버튼을 통해서 받은 svg 파일이 있고, 파일 이름도 존재한다면
    if file:
        filename = secure_filename(file.filename)   # 파일명에 들어있을 수 있는 위험한 문자(../) 같은 걸 제거 또는 안전하게 바꿈
        unique_id = uuid.uuid4().hex
        unique_filename = f"{unique_id}_{filename}" # unique_id에 파일 이름을 붙여서 중복되지 않게끔 만듦
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)  # uploads/unique_filename 인 경로를 만들고 반환함
        file.save(file_path)        # 입력된 파일을 uploads/unique_filename 에 저장함
        # 여기까지 실행되고 나면 uploads/ 에 unique_filename라는 이름을 가진 파일이 저장이 됨

        read_file(unique_filename)  # 
        return redirect(url_for('index', file=f'uploads/{unique_filename}'))
    return '', 204

def read_file(filename):
    driver = None
    cookie = {"name": "flag", "value": FLAG}
    cookie.update({"domain": "127.0.0.1"})
    # cookie = {"name": "DELTA", "value": ECHO, "domain": "127.0.0.1"} cookie는 이런 모양의 딕셔너리가됨
    try:
        # ---------------------------------------------------------------------------
        service = Service(executable_path="/usr/local/bin/chromedriver")
        options = webdriver.ChromeOptions()
        for arg in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox", 
            "disable-dev-shm-usage",
        ]:
            options.add_argument(arg)

        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        # ---------------------------------------------------------------------------
        # 위 부분은 어차피 봐도 잘 모르니까 패스

        driver.get("http://127.0.0.1:8000/")        # 로컬호스트에 접속
        driver.add_cookie(cookie)                   # 위에서 설정한 쿠키를 브라우저에 삽입
        driver.get(f"http://127.0.0.1:8000/?file=uploads/{filename}")   # 쿠키를 가진채로 특정 파일을 보여주는 페이지로 이동

        # 쿠키를 가진 채로 
        
        # <svg> 태그가 나타낼 때 까지 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "svg")))

    except Exception as e:
        driver.quit()
        return False
    driver.quit()
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
