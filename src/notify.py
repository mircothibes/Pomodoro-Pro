from pathlib import Path

def play_sound(cfg: dict, assets_dir: Path):
    """Play a 'ding' sound if enabled."""
    if not cfg.get("sound", True):
        return
    try:
        import winsound
        wav = assets_dir / "ding.wav"
        if wav.exists():
            winsound.PlaySound(str(wav), winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            # Fallback: default system beep
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except Exception:
        # Non-Windows or any failure: do nothing (or implement a cross-platform alternative later)
        pass

def show_notification(cfg: dict, title: str, message: str):
    """Show a desktop notification if enabled."""
    if not cfg.get("notify", True):
        return
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Pomodoro",
            timeout=5,   # seconds
        )
    except Exception:
        # If notifications are not supported, fail silently
        pass
