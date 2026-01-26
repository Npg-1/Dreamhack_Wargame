from __future__ import annotations
import os, json, re, uuid, datetime as dt, urllib.request
from typing import Any, Optional, Dict, List
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

SQLITE_PATH = os.getenv("SQLITE_PATH", "/data/jukebox.db")
DB_URL = os.getenv("DATABASE_URL") or f"sqlite:///{SQLITE_PATH}"

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {},
    future=True,
    pool_pre_ping=True,
)

class Base(DeclarativeBase): pass

class Song(Base):
    __tablename__ = "songs"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[Optional[str]] = mapped_column()
    artist: Mapped[Optional[str]] = mapped_column()
    album: Mapped[Optional[str]] = mapped_column()
    year: Mapped[Optional[int]] = mapped_column()
    duration_seconds: Mapped[Optional[int]] = mapped_column()
    cover_url: Mapped[Optional[str]] = mapped_column()
    source_url: Mapped[Optional[str]] = mapped_column()
    raw_json: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[dt.datetime] = mapped_column(default=lambda: dt.datetime.utcnow())
    updated_at: Mapped[dt.datetime] = mapped_column(default=lambda: dt.datetime.utcnow())

Base.metadata.create_all(engine)

app = Flask(__name__)

ALLOWED_KEYS = ("album","artist","cover_url","duration_seconds","id","title","year")

def i(s: Any) -> Optional[int]:
    try: return int(s)
    except Exception:
        if isinstance(s, str):
            m = re.match(r"^\d{1,6}", s)
            return int(m.group(0)) if m else None
        return None

def pick(d: Dict[str, Any], *keys: str) -> Any:
    for k in keys:
        cur = d; ok = True
        for p in k.split("."):
            if isinstance(cur, dict) and p in cur: cur = cur[p]
            else: ok = False; break
        if ok and cur not in (None, ""): return cur
    return None

def extract(meta: Dict[str, Any]) -> Dict[str, Any]:
    dur = pick(meta, "duration", "duration_ms", "length", "trackTimeMillis", "attributes.durationInMillis")
    dur = i(dur)
    if dur and dur > 1000: dur //= 1000
    year = i(pick(meta, "year", "releaseYear", "release_year", "attributes.releaseDate", "releaseDate"))
    return {
        "title":   pick(meta, "title","name","track","data.title","track.name","attributes.name"),
        "artist":  pick(meta, "artist","artistName","artist_name","by","data.artist","attributes.artistName","artists.0.name"),
        "album":   pick(meta, "album","albumName","collectionName","record","data.album","attributes.albumName"),
        "year": year,
        "duration_seconds": dur,
        "cover_url": pick(meta, "cover","artwork","image","thumbnail","albumArt","artworkUrl100","images.cover"),
    }

def fetch_json(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent":"Jukebox-API/1.0","Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=8) as r:
        txt = r.read().decode("utf-8", errors="replace")
    return json.loads(txt)

def public_song(row: Dict[str, Any]) -> Dict[str, Any]:
    return {k: row.get(k) for k in ALLOWED_KEYS}

seed_songs = [
    {"title":"Bohemian Rhapsody","artist":"Queen","album":"A Night at the Opera","year":1975,"duration_seconds":354,"cover_url":"https://upload.wikimedia.org/wikipedia/en/9/9f/Bohemian_Rhapsody.png"},
    {"title":"Billie Jean","artist":"Michael Jackson","album":"Thriller","year":1982,"duration_seconds":293,"cover_url":"https://upload.wikimedia.org/wikipedia/en/9/9f/Michael_Jackson_-_Billie_Jean.png"},
    {"title":"Smells Like Teen Spirit","artist":"Nirvana","album":"Nevermind","year":1991,"duration_seconds":301,"cover_url":"https://upload.wikimedia.org/wikipedia/en/b/b7/NirvanaNevermindalbumcover.jpg"},
    {"title":"Shape of You","artist":"Ed Sheeran","album":"÷ (Divide)","year":2017,"duration_seconds":233,"cover_url":"https://upload.wikimedia.org/wikipedia/en/4/45/Divide_cover.png"},
    {"title":"Blinding Lights","artist":"The Weeknd","album":"After Hours","year":2019,"duration_seconds":200,"cover_url":"https://upload.wikimedia.org/wikipedia/en/0/09/The_Weeknd_-_Blinding_Lights.png"},
]
with Session(engine) as s:
    count = s.execute(text("SELECT COUNT(*) FROM songs")).scalar_one_or_none() or 0
    if count == 0:
        now = dt.datetime.utcnow()
        for song in seed_songs:
            s.execute(
                text("""INSERT INTO songs
                        (id,title,artist,album,year,duration_seconds,cover_url,source_url,raw_json,created_at,updated_at)
                        VALUES (:id,:title,:artist,:album,:year,:duration,:cover,:src,:raw,:created,:updated)"""),
                {
                    "id": str(uuid.uuid4()),
                    "title": song["title"],
                    "artist": song["artist"],
                    "album": song["album"],
                    "year": song["year"],
                    "duration": song["duration_seconds"],
                    "cover": song["cover_url"],
                    "src": None,
                    "raw": json.dumps(song),
                    "created": now, "updated": now,
                },
            )
        s.commit()

@app.get("/songs")
def list_songs():
    limit = min(i(request.args.get("limit") or 50) or 50, 200)
    offset = i(request.args.get("offset") or 0) or 0
    q = (request.args.get("q") or "").strip()
    with Session(engine) as s:
        if q:
            like = f"%{q.lower()}%"
            rows = s.execute(
                text("""SELECT * FROM songs
                        WHERE (LOWER(COALESCE(title,''))  LIKE :like
                           OR  LOWER(COALESCE(artist,'')) LIKE :like
                           OR  LOWER(COALESCE(album,''))  LIKE :like)
                        ORDER BY created_at DESC
                        LIMIT :limit OFFSET :offset"""),
                {"like": like, "limit": limit, "offset": offset},
            ).mappings().all()
        else:
            rows = s.execute(
                text("""SELECT * FROM songs
                        ORDER BY created_at DESC
                        LIMIT :limit OFFSET :offset"""),
                {"limit": limit, "offset": offset},
            ).mappings().all()
    return jsonify([public_song(dict(r)) for r in rows])

@app.get("/songs/<song_id>")
def get_song(song_id: str):
    with Session(engine) as s:
        row = s.execute(text("SELECT * FROM songs WHERE id=:id"), {"id": song_id}).mappings().first()
        if not row: return jsonify({"error":"not found"}), 404
        return jsonify(public_song(dict(row)))

@app.post("/songs")
def create_song():
    data = request.get_json(silent=True) or {}
    src = data.get("url")
    if isinstance(src, str) and re.match(r"^https?://", src, re.I):
        try:
            blob = fetch_json(src)
        except Exception as e:
            return jsonify({"error": f"fetch failed: {e}"}), 400
    else:
        blob = data if isinstance(data, dict) else {}

    norm = extract(blob)
    new_id = str(uuid.uuid4())
    now = dt.datetime.utcnow()
    with Session(engine) as s:
        s.execute(
            text("""INSERT INTO songs
                    (id,title,artist,album,year,duration_seconds,cover_url,source_url,raw_json,created_at,updated_at)
                    VALUES (:id,:title,:artist,:album,:year,:duration,:cover,:src,:raw,:created,:updated)"""),
            {
                "id": new_id,
                "title": norm["title"],
                "artist": norm["artist"],
                "album": norm["album"],
                "year": norm["year"],
                "duration": norm["duration_seconds"],
                "cover": norm["cover_url"],
                "src": src if isinstance(src, str) else None,
                "raw": json.dumps(blob),
                "created": now, "updated": now,
            },
        )
        s.commit()
        row = s.execute(text("SELECT * FROM songs WHERE id=:id"), {"id": new_id}).mappings().first()
    return jsonify(public_song(dict(row))), 201
