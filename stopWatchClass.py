import tkinter as tk
import time
from plyer import notification  # Import the notification functionality from plyer
from tkinter import ttk

class Stopwatch:
    def __init__(self, display_label):
        self.end_time = 0
        self.start_time = 0
        self.remaining_time = 0
        self.initial_focus_time_minutes = 0
        self.bonus_time = 0
        self.running = False
        self.in_bonus = False
        self.startLocalTime = None
        self.timerFinishedFlag = False
        self.display_label = display_label
        self.total_elapsed_time = 0

    def set_time(self, minutes):
        self.remaining_time = minutes * 60
        self.initial_focus_time_minutes = minutes
        self.timerFinishedFlag = False
        self.total_elapsed_time = 0

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.startLocalTime = time.localtime()
            if self.remaining_time == 0 and not self.in_bonus:
                return
            self.end_time = self.start_time + self.remaining_time
            self.running = True
            self.update_display()

    def pause(self):
        if self.in_bonus and self.running:
            self.bonus_time += time.time() - self.start_time
        elif self.running:
            self.update_remaining_time()
        self.running = False

    def update_remaining_time(self):
        current_time = time.time()
        if self.running and not self.in_bonus:
            self.remaining_time = max(0, self.end_time - current_time)
            self.total_elapsed_time += current_time - self.start_time
            self.start_time = current_time  # Reset start time
            if self.remaining_time == 0:
                self.running = False
                self.in_bonus = True
                self.send_notification("Timer Finished", "Bonus time started!")
                self.continue_bonus()

    def get_time(self):
        if self.running:
            if self.in_bonus:
                return time.time() - self.start_time
            self.update_remaining_time()
        return self.remaining_time if not self.in_bonus else self.bonus_time

    def continue_bonus(self):
        if not self.running and self.remaining_time == 0:
            self.in_bonus = True
            self.running = True
            self.start_time = time.time()
            self.update_display()

    def getStopWatchData(self):
        bonus_time_minutes = self.bonus_time / 60
        formatted_bonus_time = f"{bonus_time_minutes:.2f}"
        elapsed_time_minutes = self.total_elapsed_time / 60
        formatted_elapsed_time = f"{elapsed_time_minutes:.2f}"
        return {
            'Focus Time': self.initial_focus_time_minutes,
            'Elapsed Time': formatted_elapsed_time,
            'Bonus Time': formatted_bonus_time,
            'Local Time': time.strftime("%Y-%m-%d %H:%M:%S", self.startLocalTime) if self.startLocalTime else "Not started"
        }

    def update_display(self):
        time_elapsed = self.get_time()
        if self.in_bonus:
            self.display_label.config(text=f"Bonus: {self.format_time(time_elapsed)}")
        else:
            self.display_label.config(text=self.format_time(time_elapsed))
        if self.running:
            self.display_label.after(1000, self.update_display)

    def format_time(self, seconds):
        return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"

    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Pomodoro Timer"
        )

class PomodoroApp:
    def __init__(self, root):
        self.window = root
        self.window.title("Countdown Timer with Bonus Time")

        self.entry = tk.Entry(self.window)
        self.entry.pack(pady=20)

        self.display_label = tk.Label(self.window, text="00:00:00", font=("Helvetica", 24), bg="white", fg="black")
        self.display_label.pack(pady=20)

        self.watch = Stopwatch(self.display_label)

        start_button = tk.Button(self.window, text="Start", command=self.start)
        start_button.pack(fill='x', expand=True)

        pause_button = tk.Button(self.window, text="Pause", command=self.pause)
        pause_button.pack(fill='x', expand=True)

        continue_button = tk.Button(self.window, text="Continue Bonus", command=self.continue_bonus)
        continue_button.pack(fill='x', expand=True)

        data_button = tk.Button(self.window, text="Get Data", command=self.display_stopwatch_data)
        data_button.pack(fill='x', expand=True)

    def start(self):
        try:
            if not self.watch.running and not self.watch.in_bonus:
                preset_time = int(self.entry.get())
                self.watch.set_time(preset_time)
            self.watch.start()
        except ValueError:
            self.display_label.config(text="Invalid input!")

    def pause(self):
        self.watch.pause()

    def continue_bonus(self):
        self.watch.continue_bonus()

    def display_stopwatch_data(self):
        data = self.watch.getStopWatchData()
        print(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
