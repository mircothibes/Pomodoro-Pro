from pathlib import Path
import csv
import datetime as dt
import json

DATA_DIR = Path.cwd() / "data"
ASSETS_DIR = Path.cwd() / "src" / "assets"
DATA_DIR.mkdir(exist_ok=True, parents=True)

SESSIONS_CSV = DATA_DIR / "sessions.csv"
CONFIG_JSON = DATA_DIR / "config.json"

DEFAULT_CFG = {
    "work_sec": 25 * 60,
    "short_sec": 5 * 60,
    "long_sec": 15 * 60,
    "sessions_per_long": 4,
    "sound": True,
    "notify": True,
    "theme": "light",
}

def load_config() -> dict:
    if CONFIG_JSON.exists():
        try:
            return json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT_CFG.copy()

def save_config(cfg: dict) -> None:
    CONFIG_JSON.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

def append_session(start_dt: dt.datetime, end_dt: dt.datetime, phase: str, duration_sec: int, tag: str = "") -> None:
    new = not SESSIONS_CSV.exists()
    with SESSIONS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["start", "end", "phase", "duration_sec", "tag"])
        w.writerow([
            start_dt.isoformat(timespec="seconds"),
            end_dt.isoformat(timespec="seconds"),
            phase,
            int(duration_sec),
            tag.strip(),
        ])
