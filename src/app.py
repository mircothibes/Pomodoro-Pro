import tkinter as tk
import datetime as dt
from pathlib import Path

from storage import load_config, append_session
from timer import PomodoroTimer
from notify import play_sound, show_notification  # <-- NOVO


def fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02d}:{s:02d}"


def phase_message(phase: str) -> tuple[str, str]:
    """Return (title, message) for the given new phase."""
    if phase == "WORK":
        return ("Time to Focus", "New work session started. Stay on task! 💪")
    if phase == "SHORT":
        return ("Short Break", "Take a short break. Stretch and hydrate. ☕")
    if phase == "LONG":
        return ("Long Break", "Great job! Enjoy a longer break. 🌿")
    return ("Pomodoro", f"Phase changed: {phase}")


def main():
    root = tk.Tk()
    root.title("Pomodoro — MVP")

    cfg = load_config()
    assets_dir = Path.cwd() / "src" / "assets"

    # --- UI ---
    lbl_mode = tk.Label(root, text="WORK", font=("Segoe UI", 14))
    lbl_time = tk.Label(root, text=fmt_time(cfg["work_sec"]), font=("Segoe UI", 48))

    tag_frame = tk.Frame(root)
    tk.Label(tag_frame, text="Tag:").pack(side="left", padx=(0, 6))
    tag_var = tk.StringVar(value="Python")
    ent_tag = tk.Entry(tag_frame, textvariable=tag_var, width=20)

    btn_frame = tk.Frame(root)
    btn_start = tk.Button(btn_frame, text="Start")
    btn_pause = tk.Button(btn_frame, text="Pause")
    btn_reset = tk.Button(btn_frame, text="Reset")

    # Layout
    lbl_mode.pack(pady=6)
    lbl_time.pack(pady=10)
    tag_frame.pack(pady=4)
    ent_tag.pack(side="left")
    btn_frame.pack(pady=12)
    btn_start.pack(side="left", padx=8)
    btn_pause.pack(side="left", padx=8)
    btn_reset.pack(side="left", padx=8)

    # --- State for persistence ---
    phase_start_dt = {"value": dt.datetime.now()}

    # Timer callbacks
    def on_tick(remaining, state):
        lbl_time.config(text=fmt_time(remaining))

    def persist_previous_phase(prev_phase: str, duration_sec: int):
        start_dt = phase_start_dt["value"]
        end_dt = dt.datetime.now()
        duration = max(0, duration_sec)
        append_session(start_dt, end_dt, prev_phase, duration, tag_var.get())

    def on_phase_change(new_state):
        # UI
        lbl_mode.config(text=new_state)
        # New phase starts now
        phase_start_dt["value"] = dt.datetime.now()
        # Sound + notification for the new phase
        play_sound(cfg, assets_dir)
        title, msg = phase_message(new_state)
        show_notification(cfg, title, msg)

    timer = PomodoroTimer(on_tick, on_phase_change, cfg)

    # Persist the previous phase right before advancing
    original_advance = timer._advance_phase

    def wrapped_advance():
        prev_phase = timer.state
        if prev_phase == "WORK":
            planned = cfg["work_sec"]
        elif prev_phase == "SHORT":
            planned = cfg["short_sec"]
        else:
            planned = cfg["long_sec"]

        persist_previous_phase(prev_phase, planned)
        original_advance()

    timer._advance_phase = wrapped_advance

    # Buttons
    btn_start.config(command=lambda: [
        phase_start_dt.update(value=dt.datetime.now()),
        timer.start(root),
    ])
    btn_pause.config(command=timer.pause)

    def do_reset():
        timer.reset()
        lbl_time.config(text=fmt_time(cfg["work_sec"]))
        lbl_mode.config(text="WORK")
        phase_start_dt["value"] = dt.datetime.now()

    btn_reset.config(command=do_reset)

    root.mainloop()


if __name__ == "__main__":
    main()
