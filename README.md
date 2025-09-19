# ⏱️ Pomodoro Timer with Reports

A simple **Pomodoro timer app** with a graphical interface built in Python.  
Perfect for study and focused work, with automatic session logging and **weekly reports** in charts.  

---

## 📖 What is the Pomodoro Technique?  
The **Pomodoro Technique** was created by Francesco Cirillo in the late 1980s.  
The name comes from a **tomato-shaped kitchen timer (*pomodoro* in Italian)** he used to manage his study time.  

The method works in cycles:  
- **25 minutes of focused work**  
- **5 minutes of short break**  
- After 4 cycles → **long break (15–30 minutes)**  

This routine helps improve concentration, reduces mental fatigue, and boosts consistency.

---

## 🚀 Features
- Graphical interface with **Tkinter**  
- Automatic cycles: **Work / Short break / Long break**  
- **Start / Pause / Reset** timer controls  
- Logs each session into a **CSV file** with start, end, duration, and type  
- Reports with **charts (matplotlib + pandas)**  
- Saved settings (cycle durations, theme, sound, notifications)  
- Sounds and notifications when switching phases  
- Export session data + open data folder  
- Keyboard shortcuts (**Ctrl+S** start, **Ctrl+P** pause, **Ctrl+R** reset)

---

## 🛠️ Technologies
- Python 3.10+  
- Tkinter (GUI)  
- Pandas + Matplotlib (reports)  
- Plyer (notifications)  
- Winsound (sound on Windows)  

---

## 📂 Project Structure
```
pomodoro-pro/
├─ src/
│ ├─ app.py # entry point
│ ├─ ui.py # Tkinter interface
│ ├─ timer.py # timer logic
│ ├─ storage.py # save/load sessions
│ ├─ reports.py # reports and charts
│ └─ assets/ # sounds, icons
├─ data/ # CSV + config.json
├─ README.md
├─ requirements.txt
└─ pyproject.toml
```
---

## 📦 Installation
Clone the repository and create a virtual environment:
```
git clone https://github.com/mircothibes/pomodoro-pro.git
cd pomodoro-pro
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```
---

💻 Windows Executable

You can also download the latest ready-to-use .exe from the Releases page.
Just extract and double-click PomodoroPro.exe.
All session data will be saved in the data/ folder next to the executable.

---

## ▶️ Usage

Run the app:

- Click Start to begin a cycle.
- The timer automatically moves to the next phase.
- Each completed session is saved to the log.
- Access Reports in the menu to view daily/weekly productivity.
- Use Settings to customize durations, sounds, and theme.

---

📜 License

This project is open-source, licensed under the MIT License.

---

## 👨‍💻 Author

Developed by Marcos Vinicius Thibes Kemer

---