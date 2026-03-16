from flask import Flask, request, render_template_string
import re
import unicodedata

app = Flask(__name__)

# 페이지에서 사용자 입력을 출력하는 부분
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        message = request.form["message"]

        # 사용자 입력값에 영어가 포함되어 있다면
        if re.search("[a-zA-Z]", message):
            message = "한글을 사용합시다!"
        
        # 사용자 입력값에 !@#$%^&*=;,<>?1234567890 가 들어있다면 해킹하지 말아다오
        for i in "!@#$%^&*=;,<>?1234567890":
            if i in message:
                message = "해킹을 하지 맙시다!"
        message = unicodedata.normalize("NFKC", message)    # for normalize Windows and Mac Hangul implementation
    return render_template_string('''
        <form method="POST">
            입력: <input type="text" name="message">
            <input type="submit">
        </form>
        <p>출력:</p>
        <div>%s</div>
    ''' % message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

cat /home/hangul/flag