# reports.py (trecho)
import pandas as pd

def weekly_summary(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["start","end"])
    df["date"] = df["start"].dt.date
    work = df[df["phase"]=="WORK"]
    daily = work.groupby("date")["duration_sec"].sum().reset_index()
    daily["minutes"] = (daily["duration_sec"]/60).round(1)
    return daily.sort_values("date")
