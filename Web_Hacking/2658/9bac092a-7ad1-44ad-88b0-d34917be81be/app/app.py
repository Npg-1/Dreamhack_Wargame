#!/usr/bin/env python3
import os
import shutil
from flask import Flask, request, render_template, redirect

APP = Flask(__name__)
UPLOAD_DIR = 'uploads'

@APP.route('/')
def index():
    files = os.listdir(UPLOAD_DIR)
    return render_template('index.html', files=files)

@APP.route('/upload', methods=['GET', 'POST'])
def upload_memo():
    if request.method == 'POST':
        filename = request.form.get('filename')     # Hmm.. filename은 그대로 filename에 입력함
        content = request.form.get('content').encode('utf-8') # content는 utf-8로 인코딩을 함
        if filename.find('..') != -1:   # ..가 filename에 포함되어 있다면 'bad characters,,'라는 문자열과 함께 upload_result.html을 전송함
            return render_template('upload_result.html', data='bad characters,,')
        with open(f'{UPLOAD_DIR}/{filename}', 'wb') as f:
            f.write(content)
        return redirect('/')
    return render_template('upload.html')


@APP.route('/read')
def read_memo():
    error = False
    data = b''
    filename = request.args.get('name', '')
    f = filename.replace("//", "/") # filename에서 '//' -> '/'로 변경
    f = f.replace("../", "")        # filename에서 '../' -> ''로 변경
    f = f.replace("./", "")         # filename에서 './' -> ''로 변경
    f = f.replace("\\\\", "\\")     # filename에서 '\\\\' -> '\\'로 변경
    f = f.replace("\\", "")         # filename에서 '\\' -> ''로 변경
    try:
        with open(f'{UPLOAD_DIR}/{f}', 'rb') as f:
            data = f.read()
    except (IsADirectoryError, FileNotFoundError):
        error = True
    return render_template('read.html',
                           filename=filename,
                           content=data.decode('utf-8'),
                           error=error)


if __name__ == '__main__':
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.mkdir(UPLOAD_DIR)
    APP.run(host='0.0.0.0', port=8000)
