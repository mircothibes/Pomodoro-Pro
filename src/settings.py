import tkinter as tk
from tkinter import ttk, messagebox

def apply_theme(root: tk.Tk, theme: str):
    """Very simple theme switcher for tk widgets."""
    if theme == "dark":
        bg = "#1f2937"   # slate-800
        fg = "#e5e7eb"   # gray-200
        btn_bg = "#374151"
        entry_bg = "#111827"
        entry_fg = fg
    else:
        bg = "#ffffff"
        fg = "#111827"
        btn_bg = "#f3f4f6"
        entry_bg = "#ffffff"
        entry_fg = fg

    root.configure(bg=bg)
    # apply to all direct children (simple pass)
    for w in root.winfo_children():
        try:
            if isinstance(w, (tk.Label, tk.Button, tk.Frame, tk.Entry)):
                w.configure(bg=bg, fg=fg)
                if isinstance(w, tk.Button):
                    w.configure(bg=btn_bg)
                if isinstance(w, tk.Entry):
                    w.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        except Exception:
            pass


def open_settings_window(parent, cfg: dict, save_fn, apply_theme_fn):
    """Open a modal window to edit settings.

    parent: root window
    cfg: dict (will be mutated on save)
    save_fn: function(cfg) -> None (e.g., storage.save_config)
    apply_theme_fn: function(root, theme) -> None
    """
    win = tk.Toplevel(parent)
    win.title("Settings")
    win.geometry("360x360")
    win.transient(parent)
    win.grab_set()

    # ensure ttk looks ok on dark
    style = ttk.Style(win)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Vars
    work_var = tk.IntVar(value=int(cfg.get("work_sec", 25*60) // 60))
    short_var = tk.IntVar(value=int(cfg.get("short_sec", 5*60) // 60))
    long_var = tk.IntVar(value=int(cfg.get("long_sec", 15*60) // 60))
    sessions_var = tk.IntVar(value=int(cfg.get("sessions_per_long", 4)))
    sound_var = tk.BooleanVar(value=bool(cfg.get("sound", True)))
    notify_var = tk.BooleanVar(value=bool(cfg.get("notify", True)))
    theme_var = tk.StringVar(value=cfg.get("theme", "light"))

    pad = {"padx": 10, "pady": 6}

    frm = ttk.Frame(win)
    frm.pack(fill="both", expand=True, **pad)

    ttk.Label(frm, text="Work (minutes)").grid(row=0, column=0, sticky="w")
    ttk.Entry(frm, textvariable=work_var, width=10).grid(row=0, column=1, sticky="w")

    ttk.Label(frm, text="Short break (minutes)").grid(row=1, column=0, sticky="w")
    ttk.Entry(frm, textvariable=short_var, width=10).grid(row=1, column=1, sticky="w")

    ttk.Label(frm, text="Long break (minutes)").grid(row=2, column=0, sticky="w")
    ttk.Entry(frm, textvariable=long_var, width=10).grid(row=2, column=1, sticky="w")

    ttk.Label(frm, text="Sessions per long break").grid(row=3, column=0, sticky="w")
    ttk.Entry(frm, textvariable=sessions_var, width=10).grid(row=3, column=1, sticky="w")

    ttk.Checkbutton(frm, text="Sound", variable=sound_var).grid(row=4, column=0, columnspan=2, sticky="w")
    ttk.Checkbutton(frm, text="Notifications", variable=notify_var).grid(row=5, column=0, columnspan=2, sticky="w")

    ttk.Label(frm, text="Theme").grid(row=6, column=0, sticky="w")
    theme_combo = ttk.Combobox(frm, textvariable=theme_var, values=["light", "dark"], width=8, state="readonly")
    theme_combo.grid(row=6, column=1, sticky="w")

    btns = ttk.Frame(frm)
    btns.grid(row=7, column=0, columnspan=2, sticky="e", pady=(12, 0))

    def on_save():
        try:
            w = max(1, int(work_var.get()))
            s = max(1, int(short_var.get()))
            l = max(1, int(long_var.get()))
            sp = max(1, int(sessions_var.get()))
        except Exception:
            messagebox.showerror("Invalid input", "Please enter valid integer values.")
            return

        cfg.update({
            "work_sec": w * 60,
            "short_sec": s * 60,
            "long_sec": l * 60,
            "sessions_per_long": sp,
            "sound": bool(sound_var.get()),
            "notify": bool(notify_var.get()),
            "theme": theme_var.get(),
        })
        save_fn(cfg)
        apply_theme_fn(parent, cfg["theme"])
        messagebox.showinfo("Saved", "Settings saved successfully.")
        win.destroy()

    ttk.Button(btns, text="Save", command=on_save).pack(side="right", padx=6)
    ttk.Button(btns, text="Cancel", command=win.destroy).pack(side="right")

    # Try to reflect current theme on this window as well (optional)
    apply_theme_fn(win, cfg.get("theme", "light"))
