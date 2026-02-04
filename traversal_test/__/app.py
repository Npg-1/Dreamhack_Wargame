
from flask import Flask, render_template
import os.path
import os

app = Flask(__name__)
TEMP_DIR = "temp"

if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

@app.route('/', methods=['GET'])
def main():
    file_path = '/flag'
    
    # 2. 파일 읽기 처리
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    else:
        file_content = "/_flag 파일을 찾을 수 없습니다."

    # 3. render_template을 통해 msg 변수로 전달
    return render_template('index.html', msg=file_content)


@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = '/flag'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    else:
        file_content = "/upload_flag 파일을 찾을 수 없습니다."

    return render_template('index.html', msg=file_content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
