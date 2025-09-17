from __future__ import annotations
from pathlib import Path
import sys

def get_assets_dir() -> Path:
    """
    Return the directory where runtime assets live.
    - In a PyInstaller onefile build: <_MEIPASS>/assets
    - In dev (python src/main.py):   <project>/src/assets
    """
    base = Path(getattr(sys, "_MEIPASS", Path.cwd()))
    # When frozen, assets are copied to MEIPASS/assets via PyInstaller 'datas'
    # In dev, we keep them under src/assets
    meipass_assets = base / "assets"
    if meipass_assets.exists():
        return meipass_assets
    return Path.cwd() / "src" / "assets"

def get_data_dir() -> Path:
    """
    Return a writable data directory for sessions/config.
    - Prefer <cwd>/data so users see files next to the executable/project.
    """
    d = Path.cwd() / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d
