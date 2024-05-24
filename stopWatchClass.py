import tkinter as tk
import time
from plyer import notification  # Import the notification functionality from plyer


class Stopwatch:
    def __init__(self):
        self.end_time = 0
        self.start_time = 0
        self.remaining_time = 0
        self.initial_focus_time_minutes = 0  # Store initial set time
        self.bonus_time = 0
        self.running = False
        self.in_bonus = False
        self.startLocalTime = None
        self.timerFinishedFlag = False
    def set_time(self, minutes):
        """Sets the countdown time and stores it as initial focus time in seconds."""
        self.remaining_time = minutes * 60
        self.initial_focus_time_minutes = minutes  # Store initial focus time
        self.timerFinishedFlag = False

    def start(self):
        """Starts or continues the stopwatch depending on conditions."""
        if not self.running:
            self.start_time = time.time()
            self.startLocalTime = time.localtime()
            if self.remaining_time == 0 and not self.in_bonus:
                return
            self.end_time = self.start_time + self.remaining_time
            self.running = True
            

    def pause(self):
        """Pauses the stopwatch, saving elapsed time correctly."""
        if self.in_bonus:
            self.bonus_time += time.time() - self.start_time
        else:
            self.update_remaining_time()
        self.running = False

    def update_remaining_time(self):
        """Updates remaining time and checks if the countdown is complete."""
        current_time = time.time()
        if self.running and not self.in_bonus:
            self.remaining_time = max(0, self.end_time - current_time)
            if self.remaining_time == 0:
                self.running = False
                self.in_bonus = True

    def get_time(self):
        """Returns the current countdown time or bonus time."""
        if self.running:
            if self.in_bonus:
                return time.time() - self.start_time
            self.update_remaining_time()
        return self.remaining_time if not self.in_bonus else self.bonus_time

    def continue_bonus(self):
        """Continues counting in bonus time mode."""
        if not self.running and self.remaining_time == 0:
            self.in_bonus = True
            self.running = True
            self.start_time = time.time()

    def getStopWatchData(self):
        """Returns important properties of the stopwatch, formatted appropriately."""
        bonus_time_minutes = self.bonus_time / 60  # Convert bonus time from seconds to minutes
        formatted_bonus_time = f"{bonus_time_minutes:.2f}"  # Format to two decimal place
        return {
        'Focus Time': self.initial_focus_time_minutes,
        'Bonus Time': formatted_bonus_time,  # Return as a string to preserve formatting
        'Local Time': time.strftime("%Y-%m-%d %H:%M:%S", self.startLocalTime) if self.startLocalTime else "Not started"
        }

def update_display():
    time_elapsed = watch.get_time()
    if watch.in_bonus:
        display_label.config(text=f"Bonus: {format_time(time_elapsed)}")
    else:
        display_label.config(text=format_time(time_elapsed))

    window.after(100, update_display)

def format_time(seconds):
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"

def start():
    try:
        if not watch.running and not watch.in_bonus:
            preset_time = int(entry.get())
            watch.set_time(preset_time)
        watch.start()
    except ValueError:
        display_label.config(text="Invalid input!")

def stop():
    watch.stop()

def pause():
    watch.pause()

def continue_bonus():
    watch.continue_bonus()

def display_stopwatch_data():
    data = watch.getStopWatchData()
    print(data)

def send_notification(title, message):
    """Send a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        app_name="Pomodoro Timer"
    )

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Countdown Timer with Bonus Time")

    watch = Stopwatch()

    entry = tk.Entry(window)
    entry.pack(pady=20)

    display_label = tk.Label(window, text="00:00:00", font=("Helvetica", 24), bg="white", fg="black")
    display_label.pack(pady=20)

    start_button = tk.Button(window, text="Start", command=start)
    start_button.pack(fill='x', expand=True)

    pause_button = tk.Button(window, text="Pause", command=pause)
    pause_button.pack(fill='x', expand=True)

    continue_button = tk.Button(window, text="Continue Bonus", command=continue_bonus)
    continue_button.pack(fill='x', expand=True)

    data_button = tk.Button(window, text="Get Data", command=display_stopwatch_data)
    data_button.pack(fill='x', expand=True)

    data_display_label = tk.Label(window, text="Details will be shown here", font=("Helvetica", 12), bg="white", fg="black")
    data_display_label.pack(pady=10)

    window.after(100, update_display)
    window.mainloop()