# src/reports.py
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import datetime as dt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_sessions_df(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError("sessions.csv not found")
    df = pd.read_csv(csv_path, parse_dates=["start", "end"])
    # Normalize / guard
    if "phase" not in df.columns or "duration_sec" not in df.columns:
        raise ValueError("Invalid CSV schema")
    return df


def daily_work_minutes(df: pd.DataFrame) -> pd.DataFrame:
    work = df[df["phase"] == "WORK"].copy()
    if work.empty:
        return pd.DataFrame(columns=["date", "minutes"])
    work["date"] = work["start"].dt.date
    g = work.groupby("date")["duration_sec"].sum().reset_index()
    g["minutes"] = (g["duration_sec"] / 60).round(1)
    return g[["date", "minutes"]].sort_values("date")


def weekly_work_minutes(df: pd.DataFrame) -> pd.DataFrame:
    """ISO week aggregation: year-week vs total minutes of WORK."""
    work = df[df["phase"] == "WORK"].copy()
    if work.empty:
        return pd.DataFrame(columns=["year_week", "minutes"])
    work["year"] = work["start"].dt.isocalendar().year
    work["week"] = work["start"].dt.isocalendar().week
    g = work.groupby(["year", "week"])["duration_sec"].sum().reset_index()
    g["minutes"] = (g["duration_sec"] / 60).round(1)
    g["year_week"] = g["year"].astype(str) + "-W" + g["week"].astype(str)
    return g[["year_week", "minutes"]].sort_values(["year", "week"])


def top_tags(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    if "tag" not in df.columns or df.empty:
        return pd.DataFrame(columns=["tag", "count"])
    w = df[df["phase"] == "WORK"]
    if w.empty:
        return pd.DataFrame(columns=["tag", "count"])
    g = w["tag"].fillna("").str.strip()
    g = g[g != ""]
    if g.empty:
        return pd.DataFrame(columns=["tag", "count"])
    out = g.value_counts().head(n).reset_index()
    out.columns = ["tag", "count"]
    return out


def build_bar_figure(x_labels, y_values, title: str) -> Figure:
    fig = Figure(figsize=(7, 3.8), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(x_labels, y_values)  # (não especificamos cores)
    ax.set_title(title)
    ax.set_ylabel("Minutes")
    ax.set_xlabel("")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    return fig


def open_reports_window(parent: tk.Tk, data_dir: Path):
    csv_path = data_dir / "sessions.csv"

    win = tk.Toplevel(parent)
    win.title("Reports — Pomodoro")
    win.geometry("820x520")
    win.transient(parent)
    win.grab_set()

    # Frames
    top = ttk.Frame(win)
    top.pack(fill="x", padx=10, pady=8)

    body = ttk.Frame(win)
    body.pack(fill="both", expand=True, padx=10, pady=4)

    status = ttk.Label(win, text="", anchor="w")
    status.pack(fill="x", padx=10, pady=(0, 8))

    # Buttons
    btn_refresh = ttk.Button(top, text="Refresh")
    btn_open_folder = ttk.Button(top, text="Open data folder")
    btn_refresh.pack(side="left", padx=(0, 6))
    btn_open_folder.pack(side="left", padx=6)

    # Tabs
    nb = ttk.Notebook(body)
    tab_daily = ttk.Frame(nb)
    tab_weekly = ttk.Frame(nb)
    tab_tags = ttk.Frame(nb)
    nb.add(tab_daily, text="Daily")
    nb.add(tab_weekly, text="Weekly")
    nb.add(tab_tags, text="Top Tags")
    nb.pack(fill="both", expand=True)

    # Canvas placeholders
    daily_canvas = None
    weekly_canvas = None

    # Tables
    daily_table = ttk.Treeview(tab_daily, columns=("date", "minutes"), show="headings", height=8)
    daily_table.heading("date", text="Date")
    daily_table.heading("minutes", text="Minutes")
    daily_table.pack(fill="x", padx=6, pady=(6, 0))

    weekly_table = ttk.Treeview(tab_weekly, columns=("year_week", "minutes"), show="headings", height=8)
    weekly_table.heading("year_week", text="Year-Week")
    weekly_table.heading("minutes", text="Minutes")
    weekly_table.pack(fill="x", padx=6, pady=(6, 0))

    tags_table = ttk.Treeview(tab_tags, columns=("tag", "count"), show="headings", height=12)
    tags_table.heading("tag", text="Tag")
    tags_table.heading("count", text="Count")
    tags_table.pack(fill="both", expand=True, padx=6, pady=6)

    chart_frame_daily = ttk.Frame(tab_daily)
    chart_frame_daily.pack(fill="both", expand=True, padx=6, pady=6)

    chart_frame_weekly = ttk.Frame(tab_weekly)
    chart_frame_weekly.pack(fill="both", expand=True, padx=6, pady=6)

    def refresh():
        nonlocal daily_canvas, weekly_canvas
        try:
            df = load_sessions_df(csv_path)
        except FileNotFoundError:
            messagebox.showinfo("No data", "No sessions.csv found yet.")
            status.config(text="No sessions.csv found.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            status.config(text=f"Error: {e}")
            return

        # clear previous charts if any
        if daily_canvas:
            daily_canvas.get_tk_widget().destroy()
            daily_canvas = None
        if weekly_canvas:
            weekly_canvas.get_tk_widget().destroy()
            weekly_canvas = None

        # Daily
        ddf = daily_work_minutes(df)
        for row in daily_table.get_children():
            daily_table.delete(row)
        if not ddf.empty:
            for _, r in ddf.iterrows():
                daily_table.insert("", "end", values=(r["date"], r["minutes"]))
            fig_d = build_bar_figure(ddf["date"].astype(str).tolist(), ddf["minutes"].tolist(), "Daily Focus Minutes")
            daily_canvas = FigureCanvasTkAgg(fig_d, master=chart_frame_daily)
            daily_canvas.draw()
            daily_canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(chart_frame_daily, text="No WORK data to display yet.").pack(pady=10)

        # Weekly
        wdf = weekly_work_minutes(df)
        for row in weekly_table.get_children():
            weekly_table.delete(row)
        if not wdf.empty:
            for _, r in wdf.iterrows():
                weekly_table.insert("", "end", values=(r["year_week"], r["minutes"]))
            fig_w = build_bar_figure(wdf["year_week"].tolist(), wdf["minutes"].tolist(), "Weekly Focus Minutes")
            weekly_canvas = FigureCanvasTkAgg(fig_w, master=chart_frame_weekly)
            weekly_canvas.draw()
            weekly_canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(chart_frame_weekly, text="No WORK data to display yet.").pack(pady=10)

        # Tags
        tdf = top_tags(df, n=8)
        for row in tags_table.get_children():
            tags_table.delete(row)
        if not tdf.empty:
            for _, r in tdf.iterrows():
                tags_table.insert("", "end", values=(r["tag"], int(r["count"])))
        status.config(text=f"Loaded {len(df)} sessions.")

    def open_folder():
        try:
            import os
            os.startfile(str(data_dir))  # Windows
        except Exception:
            try:
                import subprocess, sys
                if sys.platform == "darwin":
                    subprocess.Popen(["open", str(data_dir)])
                else:
                    subprocess.Popen(["xdg-open", str(data_dir)])
            except Exception:
                messagebox.showinfo("Folder", f"Data folder: {data_dir}")

    btn_refresh.config(command=refresh)
    btn_open_folder.config(command=open_folder)

    refresh()
