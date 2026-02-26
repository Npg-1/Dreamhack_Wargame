#!/usr/bin/env python3
import os
import string
from flask import Flask, request, abort, render_template, session

SECRETS_PATH = 'secrets/'
ALLOWED_CHARACTERS = string.ascii_letters + string.digits + '/' # 알파벳과 숫자만 인정!!


app = Flask(__name__)
app.secret_key = os.urandom(32)


# create sample file
with open(f'{SECRETS_PATH}/sample', 'w') as f:
    f.write('Hello, world :)')


# create flag file
flag_dir = SECRETS_PATH + os.urandom(32).hex()      # secrets/(64자리 16진수 문자열)
os.mkdir(flag_dir)
flag_path = flag_dir + '/flag'                      # flag_path == secrets/(64자리 16진수 문자열)/flag
with open('/flag', 'r') as f0, open(flag_path, 'w') as f1:  # 서버 /의 flag를 읽어서 secrets/(64자리 16진수 문자열)/flag/에 덮어씀
    f1.write(f0.read())


# 현재 플래그는 secrets/(64자리 16진수 문자열)/flag 에 있음, secrets가 어디에 있는지는 모름

# GET요청이라서 홈페이지 들어갈 때 마다 출력되는줄 알았지만 Submit을 눌렀을 때 /로 GET요청이 일어나서 버튼을 눌러도 이 부분은 실행됨
@app.route('/', methods=['GET'])            
def get_index():
    # flag_path == secrets/(64자리 16진수 문자열)/flag
    session['secret'] = flag_path

    # provide file read functionality
    path = request.args.get('path')                 # path는 사용자가 입력한 경로임
    if not isinstance(path, str) or path == '':     # 경로를 입력 안 하면 '경로를 입력하라!' 라고 뜨면서 홈페이지로 돌아감
        return render_template('index.html', msg='input the path!')

    if any(ch not in ALLOWED_CHARACTERS for ch in path):        # 입력된 경로의 모든 문자들이 ALLOWED_CHARACTERS에 다 포함된 게 아니라면, 알파벳, 숫자 이외의 다른 문자가 들어온다면
        return render_template('index.html', msg='invalid path!')       # 잘못된 경로 입력!!

    full_path = f'./{SECRETS_PATH}{path}'                           # full_path = ./secrets/(사용자 입력 경로)
    if not os.path.isfile(full_path):                               # full_path가 가리키는 게 파일이 아니라면 '잘못된 경로 입력!!' 띄움
        return render_template('index.html', msg='invalid path!')   

    # 1. 경로를 입력 안 했거나
    # 2. 입력한 경로가 허용된 문자 이외의 문자를 사용했거나
    # 3. 입력한 경로와 SECRETS_PATH와 합쳤을 때 나온 경로가 파일을 가리키지 않는다면
    # 에러를 출력하고 그게 아니면 파일을 띄움

    try:
        with open(full_path, 'r') as f:
            return render_template('index.html', msg=f.read())      # 경로에 뜨는 파일의 내용을 읽어 홈페이지에 출력
    except:
        abort(500)



