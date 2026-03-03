#!/usr/bin/env python3
from flask import Flask, request, render_template

app = Flask(__name__)

try:
    FLAG = open("./flag.txt", "r").read()       # flag is here!
except:
    FLAG = "[**FLAG**]"

@app.route('/', methods=['GET', 'POST'])
def index():
    menu_str = ''
    org = FLAG[10:29]   # FLAG의 10~28번째 글자까지를 org로 넣음
    org = int(org)      # 10진수 값
    st = ['' for i in range(16)]    # ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    for i in range (0, 16):
        res = (int)(org / pow(2, 4 * i)) % 16 # res는 4의 배수만큼 나눈 다음, 16의 나머지 값을 res에 할당함
        if 0 < res < 12:
            if res == 11:    # 1~11의 범위에 대해서는 이 식이 맞긴함, (~res % 16 == res * (-1) + 15)
                st[15-i] = '_'
            else:
                st[15-i] = str(res)
        else:
            # 12~15 c, d, e, f (a와 b는 숫자로 들어가고 c, d, e, f만 알파벳으로 들어감)
            st[15-i] = format(res, 'x') # hex(res)와 값은 같은데 hex(res)는 앞에 0x 가 붙음
    menu_str = menu_str.join(st)

    # POST
    if request.method == "POST":
        input_str =  request.form.get("menu_input", "")
        if input_str == str(org):
            return render_template('index.html', menu=menu_str, flag=FLAG)
        return render_template('index.html', menu=menu_str, flag='try again...')
    # GET
    return render_template('index.html', menu=menu_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
