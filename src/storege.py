DEFAULT_CFG = {
    "work_sec": 25*60,
    "short_sec": 5*60,
    "long_sec": 15*60,
    "sessions_per_long": 4,
    "sound": True,
    "notify": True,
    "theme": "light",
}

# storage.py 
from pathlib import Path
import csv, datetime as dt

DATA_DIR = Path.cwd() / "data"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
DATA_DIR.mkdir(exist_ok=True)

def append_session(start_dt, end_dt, phase, duration, tag=""):
    new = not SESSIONS_CSV.exists()
    with SESSIONS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["start", "end", "phase", "duration_sec", "tag"])
        w.writerow([start_dt.isoformat(), end_dt.isoformat(), phase, duration, tag])
