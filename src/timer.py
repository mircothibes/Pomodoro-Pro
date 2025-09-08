# timer.py 
class PomodoroTimer:
    def __init__(self, on_tick, on_phase_change, cfg):
        self.on_tick = on_tick                # callback para atualizar UI a cada segundo
        self.on_phase_change = on_phase_change
        self.cfg = cfg                        # dict com durações, etc.
        self.state = "WORK"                   # WORK | SHORT | LONG | IDLE
        self.remaining = self.cfg["work_sec"]
        self.completed_work_sessions = 0
        self.running = False

    def start(self, tk_root):
        if not self.running:
            self.running = True
            self._tick(tk_root)

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.state = "WORK"
        self.remaining = self.cfg["work_sec"]

    def _tick(self, tk_root):
        if not self.running:
            return
        self.on_tick(self.remaining, self.state)
        if self.remaining <= 0:
            self._advance_phase()
            self.on_phase_change(self.state)
        else:
            self.remaining -= 1
        tk_root.after(1000, lambda: self._tick(tk_root))

    def _advance_phase(self):
        if self.state == "WORK":
            self.completed_work_sessions += 1
            if self.completed_work_sessions % self.cfg["sessions_per_long"] == 0:
                self.state = "LONG"
                self.remaining = self.cfg["long_sec"]
            else:
                self.state = "SHORT"
                self.remaining = self.cfg["short_sec"]
        else:
            self.state = "WORK"
            self.remaining = self.cfg["work_sec"]
