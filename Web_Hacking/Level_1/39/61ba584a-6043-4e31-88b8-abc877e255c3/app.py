#!/usr/bin/python3
from flask import Flask, request, render_template, render_template_string, make_response, redirect, url_for
import socket

app = Flask(__name__)

try:
    FLAG = open('./flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

app.secret_key = FLAG


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def Error404(e):
    template = '''
    <div class="center">
        <h1>Page Not Found.</h1>
        <h3>%s</h3>
    </div>
''' % (request.path)
    return render_template_string(template), 404

app.run(host='0.0.0.0', port=8000)


# 대충 풀이를 하자면 http://host8.dreamhack.games:16296/ 이 메인 화면에서 뒤에 문자열이 붙으면 해당 문자열의 링크로 이동하는 로직임
# 근데 404Error, robots.txt를 뒤에 붙이면 Page Not Found. 가 뜸. 말그대로 해당 페이지가 없기 때문인데 여기서 중요한 점은 template를 보면
# <h3>%s</h3> 에서 %s를 출력하는데 웹 템플릿 엔진에서는 %s에 {{config}}를 문자열이 아닌 명령어로 인식해서 {{config}}의 내용을 출력함

# 답: 뒤에 "/{{config}}" 를 붙이면 됨

# 참고한 사이트(사실 여기서 답이 나옴)
# https://www.igloo.co.kr/security-information/%EC%9B%B9-%ED%85%9C%ED%94%8C%EB%A6%BF-%EC%97%94%EC%A7%84-%EA%B8%B0%EB%B0%98%EC%9D%98-ssti-%EC%B7%A8%EC%95%BD%EC%A0%90-%EB%B6%84%EC%84%9D/


# def _list():
#     kw = request.args.get('kw', type=str, default='')   # 입력값을 받아와서 kw에 대입
#     search = '%%{}%%'.format(kw)                        # 입력값을 '%%{}%%' 형태로 변환해서 search에 대입
#     filter(Question.subject.like(search))               # 

#     template= '''
#     <form id=searchFrom method=get type=submit action={{ url_for('question._list)}}>
#         <input type=hidden id = ke name = kw value={{ kw or ''}}
#     </form>
#     ...
#     <center>
#         <label class=btn btn-link alert-light id=search_txt>%s</label>
#     </center>%(kw)
#     '''

#     return render_template_string()(template, question_list=question_list, page=page, kw=kw)














