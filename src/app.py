import tkinter as tk
from storage import DEFAULT_CFG
from timer import PomodoroTimer

def fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02d}:{s:02d}"

def main():
    root = tk.Tk()
    root.title("Pomodoro — MVP")

    # Widgets principais
    lbl_mode = tk.Label(root, text="WORK", font=("Segoe UI", 14))
    lbl_time = tk.Label(root, text="25:00", font=("Segoe UI", 48))
    btn_start = tk.Button(root, text="Start")
    btn_pause = tk.Button(root, text="Pause")
    btn_reset = tk.Button(root, text="Reset")

    # Layout simples (ajuste depois)
    lbl_mode.pack(pady=6)
    lbl_time.pack(pady=12)
    btn_start.pack(side="left", padx=8, pady=12)
    btn_pause.pack(side="left", padx=8, pady=12)
    btn_reset.pack(side="left", padx=8, pady=12)

    # Callbacks do timer
    def on_tick(remaining, state):
        lbl_time.config(text=fmt_time(remaining))

    def on_phase_change(state):
        lbl_mode.config(text=state)

    timer = PomodoroTimer(on_tick, on_phase_change, DEFAULT_CFG)

    # Ações dos botões
    btn_start.config(command=lambda: timer.start(root))
    btn_pause.config(command=timer.pause)
    btn_reset.config(command=lambda: [timer.reset(), lbl_time.config(text=fmt_time(DEFAULT_CFG["work_sec"])), lbl_mode.config(text="WORK")])

    root.mainloop()

if __name__ == "__main__":
    main()
