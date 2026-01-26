#!/usr/bin/python3
from flask import Flask, request, render_template
import re

app = Flask(__name__)

try:
    FLAG = open("./flag.txt", "r").read()
except:
    FLAG = "[**FLAG**]"

@app.route("/", methods = ["GET", "POST"])
def index():
    input_val = ""
    if request.method == "POST":
        input_val = request.form.get("input_val", "")
        m = re.match(r'@[a-z]{3,7}\.\w+', input_val)     # dreeeeee0am@hack
        # dreeeeee1am@hack\.lust
        if m:
            return render_template("index.html", pre_txt=input_val, flag=FLAG)
    return render_template("index.html", pre_txt=input_val, flag='?')

app.run(host="0.0.0.0", port=8000)


re.match(r'al\w{1,3}', input)

