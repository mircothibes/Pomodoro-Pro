"""
Notification & Sound Utilities
------------------------------
Lightweight helpers for playing a short sound and showing desktop notifications.

Design notes
- `play_sound`: Uses `winsound` on Windows. If `ding.wav` is missing, falls back to a
  system beep. On non-Windows platforms (or any failure), it silently does nothing.
- `show_notification`: Uses `plyer.notification` if available; otherwise fails silently.

Both functions first check feature flags in the config dict:
  cfg["sound"]  -> enable/disable sound feedback  (default: True)
  cfg["notify"] -> enable/disable notifications    (default: True)
"""

from pathlib import Path

def play_sound(cfg: dict, assets_dir: Path):
    """
    Play a short 'ding' sound if enabled in the configuration.

    Behavior:
        - If cfg["sound"] is falsy, return immediately.
        - On Windows:
            * Tries to play 'ding.wav' located in `assets_dir`.
            * If not found, falls back to a system MessageBeep.
        - On other platforms or on any exception, does nothing.

    Args:
        cfg: Configuration dictionary. If `cfg.get("sound", True)` is False, no sound is played.
        assets_dir: Directory where assets (e.g., 'ding.wav') are stored.

    Returns:
        None. (Side effect: attempts to play a short sound.)

    Notes:
        - `winsound` is only available on Windows. Import is done lazily inside the function.
        - This helper is intentionally fail-safe: any error is swallowed to avoid breaking the UI loop.
    """
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
