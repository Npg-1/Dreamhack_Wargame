def _now():
    return int(time.time())

def _ensure_session():              # _ensure_session()는 sid, csrf, last_hb로 세션 딕셔너리를 초기화함. 이후로 실행되면 이미 있으니까 if문에서 막혀서 그냥 넘어감
    if "sid" not in session:
        session["sid"] = secrets.token_urlsafe(16)
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(24)
    if "last_hb" not in session:
        session["last_hb"] = _now()


@app.route("/", methods=["GET"])        
def index():
    _ensure_session()       # 처음에 세션을 생성함
    # 이 부분이 의미가 있나? => 라고 생각했던 시기가 저에게도 있었지요.. => 근데 index는 최초에 사이트 접속할 때마 실행되는 게 아니라 
    # 그냥 index페이지에 접속할 때마다 실행되는 거임, 근데 _ensure_session()에서 last_hb을 초기화하는 건 처음에만 그런 것이어서 last_hb을 최신화 하고 싶으면 이렇게 따로 해줘야함
    session["last_hb"] = _now()     
    return render_template(...)

@app.route("/hb", methods=["POST"])
def hb():
    if "sid" not in session:
        return ("", 204)
    session["last_hb"] = _now()
    return ("", 204)

@app.route("/claim", methods=["POST"])
def claim():
    _ensure_session()        # 세션을 생성함, 근데 index()에서 이미 했으니까 이 줄은 주석처리해도 상관없어 보임

    last_hb = session.get("last_hb", 0) # last_hb을 session에서 가져오는데 
    age = _now() - last_hb      # last_hb은 마지막으로 활동했던 시간인데 _now()에서 뺐으니까 claim()이 실행된 시간(나이)를 나타냄

    if age < 5:
        msg = f"You're still in ads, kill all ads"
        return render_template(...)
    
    # else 일 때 실행되는 부분
    ...

이 코드에서 session["last_hb"]을 수정하는 부분은 _ensure_session()와 16번, 23번줄에서 수정하는 것 말고는 없음
33번줄이 True가 되기 위해서는 /페이지에 들어가 index()가 실행되고 나면 session["last_hb"]이 수정되고 5초이상 시간이 지난 다음에 /claim 으로 들어가서 claim()이 실행되면 
30번줄의 last_hb에는 5초 이상 이전에 /에서 기록된 마지막 활동했던 시간이 기록될테니까 age는 5 이상이 돼서 33번줄의 if문이 False가 돼야하는 거 아니야?