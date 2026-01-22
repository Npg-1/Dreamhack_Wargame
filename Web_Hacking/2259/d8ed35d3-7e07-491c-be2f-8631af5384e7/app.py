from flask import Flask, render_template, request, session, abort
import os, time, secrets, json
from pathlib import Path
import random

app = Flask(__name__)
app.secret_key = os.environ.get("???", "???")

BASE_DIR = Path(__file__).resolve().parent
FLAG_PATH = BASE_DIR / "flag.txt"
ADS_JSON = BASE_DIR / "static" / "ads.json"


def read_flag():
    return FLAG_PATH.read_text(encoding="utf-8").strip()

def _now():
    return int(time.time())

def _ensure_session():              # _ensure_session()는 sid, csrf, last_hb로 세션 딕셔너리를 초기화함. 이후로 실행되면 이미 있으니까 if문에서 막혀서 그냥 넘어감
    if "sid" not in session:
        session["sid"] = secrets.token_urlsafe(16)
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(24)
    if "last_hb" not in session:
        session["last_hb"] = _now()

def load_ads():
    data = json.loads(ADS_JSON.read_text(encoding="utf-8"))

    ads = []
    for item in data:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "Sponsored Ad"))
        body = str(item.get("body", "Best deal of your life."))
        ads.append({"title": title, "body": body})
    return ads


@app.after_request
def security_headers(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp

@app.route("/", methods=["GET"])        # 메인화면선서에서는 대충 세션, 광고 생성하고 index.html 표시함
def index():
    _ensure_session()       # 처음에 세션을 생성함
    session["last_hb"] = _now()     # 얘는 뭐지? _ensure_session()에서 똑같은 걸 이미 했는데 또 하는 이유가 있나? 일단은 pass
    ads = load_ads()        # 광고들을 생성해서 반환
    return render_template(
        "index.html",
        csrf=session["csrf"],       # 
        max_ads=min(20, len(ads)) if ads else 20,   # 광고 최대 개수는 20
        hb_ms=1000,
        stale_seconds=5,
        ads=ads,
        flag=None
    )

@app.route("/hb", methods=["POST"])
def hb():
    if "sid" not in session:
        return ("", 204)
    session["last_hb"] = _now()
    return ("", 204)

@app.route("/claim", methods=["POST"])
def claim():
    _ensure_session()        # 세션을 생성함, 근데 이 부분은 의미없을 거 같으니까 일단 무시
    csrf = request.form.get("csrf", "")     # claim으로 들어올 때의 사이트의 csrf값을 받아서 csrf 변수에 저장함
    if csrf != session.get("csrf"):         # session딕셔너리 csrf의 값을 받아와서 사이트의 csrf와 비교함
        abort(400, description="Bad CSRF")

    last_hb = session.get("last_hb", 0)
    age = _now() - last_hb      # last_hb은 마지막으로 활동했던 시간인데 _now()에서 뺐으니까 claim()이 실행된 시간(나이)를 나타냄
    ads = load_ads()

    # age가 5이상이어서 아래의 if문을 안 들어가기만 하면 됨, 그러면 age가 5이상이 되려면 어떻게 하면 되느냐
    # age는 _now()와 last_hb 두 값의 차이로 생김, _now() 값은 time.time()이어서 클라이언트가 어떻게 건들일 수 있는 부분은 없어보이고
    # 그러러면 last_hb을 수정해야하는데 last_hb은 session에서 last_hb값을 가져옴 session["last_hb"]의 값은 _ensure_session()와, '/', /'hb'에서 수정함
    # 여기서 '/hb'에서 sid가 session에 없으면 session["last_hb"]=_now() 가 실행이 안 돼서 어떻게 될 것도 같은데.데데데데데데
    if age < 5:
        msg = f"You're still in ads, kill all ads"
        return render_template( 
            "index.html",   
            csrf=session["csrf"],   
            max_ads=min(20, len(ads)) if ads else 20,   
            hb_ms=1000, 
            stale_seconds=5,    
            ads=ads,    
            flag=None,  
            error=msg
        ), 403

    flag = read_flag()
    return render_template(
        "index.html",
        csrf=session["csrf"],
        max_ads=min(20, len(ads)) if ads else 20,
        hb_ms=1000,
        stale_seconds=5,
        ads=ads,
        flag=flag
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
