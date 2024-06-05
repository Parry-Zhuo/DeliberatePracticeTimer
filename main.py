import tkinter as tk
from stopWatchClass import Stopwatch
import time
from plyer import notification  # Import the notification functionality from plyer
import os
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from ttkthemes import ThemedTk
import pygame
from tkinter import ttk

class PomodoroApp:
    def __init__(self, master):
        self.shortDistraction = 0
        self.longDistraction = 0

        self.master = master
        self.master.title("Drip Dropper")
        self.master.geometry('350x250')
        self.master.configure(background='#383838')

        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module
        self.tick_sound = pygame.mixer.Sound("dripdrop.mp3")  # Load your MP3 file
        self.tick_channel = pygame.mixer.find_channel()
        self.sound_enabled = True  # Default to sound being on

        self.setup_frames()
        self.setup_focus_widgets()
        self.setup_contemplation_widgets()
        self.setup_reflection_widgets()
        self.show_contemplation()

    def setup_frames(self):
        style = ttk.Style()
        style.configure('TFrame', background='#383838')
        style.configure('TLabel', font=('Helvetica', 12), foreground='#E0E0E0', background='#383838')
        style.configure('TEntry', font=('Helvetica', 12), foreground='#D0D0D0', background='#505050', fieldbackground='#505050', borderwidth=1, relief='flat')
        style.configure('TButton', font=('Helvetica', 12), foreground='#E0E0E0', background='#404040', borderwidth=0, relief='flat')

        style.map('TButton',
                  foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF')],
                  background=[('pressed', '#333333'), ('active', '#333333')],
                  relief=[('pressed', 'flat'), ('active', 'flat')])
        style.map('TEntry',
                  fieldbackground=[('focus', '#606060')],
                  foreground=[('focus', '#FFFFFF')])

        self.focus_frame = ttk.Frame(self.master, style='TFrame')
        self.contemplation_frame = ttk.Frame(self.master, style='TFrame')
        self.reflection_frame = ttk.Frame(self.master, style='TFrame')

        self.frames = [self.focus_frame, self.contemplation_frame, self.reflection_frame]

        for frame in self.frames:
            frame.pack(fill='both', expand=True)

        self.focus_frame.pack_forget()
        self.reflection_frame.pack_forget()
        self.contemplation_frame.pack_forget()

    def setup_focus_widgets(self):
        self.focus_frame.config(style='TFrame')
        self.focus_frame.pack(fill='both', expand=True, pady=(10, 0), anchor='n')

        self.focus_task_label = ttk.Label(self.focus_frame, text="TASK", style='TLabel')
        self.focus_task_label.pack(pady=(10, 0), anchor='n')

        self.focus_goal_label = ttk.Label(self.focus_frame, text="Goal: Work on the project (1-2 sentences)", style='TLabel')
        self.focus_goal_label.pack(pady=(5, 10))

        self.timer_label = ttk.Label(self.focus_frame, text="25:00", font=('Helvetica', 24), foreground='#E0E0E0', background='#383838')
        self.timer_label.pack(pady=(5, 20))

        button_frame = ttk.Frame(self.focus_frame, style='TFrame')
        button_frame.pack(pady=(5, 5))

        short_distraction_button = ttk.Button(button_frame, text="SHORT DISTRACTION", style='TButton', command=lambda: setattr(self, 'shortDistraction', self.shortDistraction + 1))
        short_distraction_button.pack(side='left', padx=(10, 20))

        long_distraction_button = ttk.Button(button_frame, text="LONG DISTRACTION", style='TButton', command=lambda: setattr(self, 'longDistraction', self.longDistraction + 1))
        long_distraction_button.pack(side='right', padx=(20, 10))

        end_focus_button = ttk.Button(self.focus_frame, text="END FOCUS", style='TButton', command=self.show_reflection)
        end_focus_button.pack(pady=(20, 10))

        discard_focus_button = ttk.Button(self.focus_frame, text="DISCARD", style='TButton', command=self.show_contemplation)
        discard_focus_button.pack(pady=(20, 10))

        self.toggle_sound_button = ttk.Button(self.focus_frame, text="TOGGLE SOUND", style='TButton', command=self.toggle_sound)
        self.toggle_sound_button.pack(pady=(10, 0))


        self.pomodoro = Stopwatch(self.timer_label)

    def setup_contemplation_widgets(self):
        contemplation_label = ttk.Label(self.contemplation_frame, text="REST", style='TLabel', font=('Helvetica', 16))
        contemplation_label.pack(pady=10)

        self.task_label = ttk.Label(self.contemplation_frame, text="TASK", style='TLabel')
        self.task_label.pack(pady=(10, 2), anchor='w')
        self.task_entry = ttk.Entry(self.contemplation_frame, style='TEntry', width=40)
        self.task_entry.pack(pady=(2, 10))
        self.task_entry.bind("<Tab>", lambda e: self.goal_entry.focus_set())

        self.goal_label = ttk.Label(self.contemplation_frame, text="GOAL", style='TLabel')
        self.goal_label.pack(pady=(10, 2), anchor='w')
        self.goal_entry = ttk.Entry(self.contemplation_frame, style='TEntry', width=60)
        self.goal_entry.pack(pady=(2, 10))

        timer_frame = ttk.Frame(self.contemplation_frame, style='TFrame')
        timer_frame.pack(pady=(10, 10))

        pomodoro_label = ttk.Label(timer_frame, text="TIMER(MIN):", style='TLabel')
        pomodoro_label.pack(side='left', padx=(5, 2))
        self.pomodoro_entry = ttk.Entry(timer_frame, style='TEntry', width=5)
        self.pomodoro_entry.pack(side='left', padx=(2, 20))
        self.pomodoro_entry.insert(0, '25')

        break_label = ttk.Label(timer_frame, text="REST TIMER(MIN):", style='TLabel')
        break_label.pack(side='left', padx=(5, 2))
        self.break_entry = ttk.Entry(timer_frame, style='TEntry', width=5)
        self.break_entry.pack(side='left')
        self.break_entry.insert(0, '5')

        contemplation_button = ttk.Button(self.contemplation_frame, text="SWITCH TO FOCUS", style='TButton', command=self.show_focus)
        contemplation_button.pack(pady=(10, 10))

        self.contemplation_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def setup_reflection_widgets(self):
        self.reflection_frame.config(style='TFrame')
        self.reflection_frame.pack(fill='both', expand=True)

        self.reflection_task_label = ttk.Label(self.reflection_frame, text="TASK", style='TLabel')
        self.reflection_task_label.pack(pady=(10, 0), anchor='n')

        self.reflection_goal_label = ttk.Label(self.reflection_frame, text="Goal: Work on the project (1-2 sentences)", style='TLabel')
        self.reflection_goal_label.pack(pady=(5, 10))

        distraction_frame = ttk.Frame(self.reflection_frame, style='TFrame')
        distraction_frame.pack(pady=(5, 10))

        short_label = ttk.Label(distraction_frame, text="Short Distractions:", style='TLabel')
        self.short_value = ttk.Label(distraction_frame, text=str(self.shortDistraction), style='TLabel')
        long_label = ttk.Label(distraction_frame, text="Long Distractions:", style='TLabel')
        self.long_value = ttk.Label(distraction_frame, text=str(self.longDistraction), style='TLabel')

        short_label.pack(side='left')
        self.short_value.pack(side='left')
        long_label.pack(side='left', padx=(20, 0))
        self.long_value.pack(side='left')

        self.break_time_label = ttk.Label(self.reflection_frame, text="00:00", style='TLabel', font=('Helvetica', 24))
        self.break_time_label.pack(pady=(5, 10))

        self.reflection_textbox = tk.Text(self.reflection_frame, height=12, width=70)
        self.reflection_textbox.pack(pady=(5, 5))

        satisfaction_label = ttk.Label(self.reflection_frame, text="SATISFACTION LEVEL (1-10):", style='TLabel')
        satisfaction_label.pack(pady=(5, 2))
        self.satisfaction_entry = ttk.Entry(self.reflection_frame, style='TEntry', width=5)
        self.satisfaction_entry.pack(pady=(2, 10))

        self.satisfaction_entry.bind("<FocusOut>", self.validate_satisfaction)
        button_frame = ttk.Frame(self.reflection_frame, style='TFrame')
        button_frame.pack(pady=(10, 10))
        insert_button = ttk.Button(button_frame, text="INSERT", style='TButton', command=lambda: self.show_contemplation("insert"))
        discard_button = ttk.Button(button_frame, text="DISCARD", style='TButton', command=lambda: self.show_contemplation("discard"))
        insert_button.pack(side='left', padx=10)
        discard_button.pack(side='left')


        self.breakStopwatch = Stopwatch(self.break_time_label)

    def show_focus(self):
        error_present = False

        self.task_entry.config(foreground='white')
        self.pomodoro_entry.config(foreground='white')
        self.break_entry.config(foreground='white')

        if not self.task_entry.get().strip():
            self.task_entry.delete(0, 'end')
            self.task_entry.insert(0, "Error: Task cannot be empty.")
            self.task_entry.config(foreground='red')
            error_present = True

        try:
            pomodoro_time = int(self.pomodoro_entry.get())
            break_time = int(self.break_entry.get())
            if pomodoro_time <= 0 or break_time <= 0:
                raise ValueError("Time must be positive integers.")
        except ValueError:
            self.pomodoro_entry.delete(0, 'end')
            self.pomodoro_entry.insert(0, "Error")
            self.pomodoro_entry.config(foreground='red')
            self.break_entry.delete(0, 'end')
            self.break_entry.insert(0, "Error")
            self.break_entry.config(foreground='red')
            error_present = True

        if not error_present:
            self.toggle_sound(state="ON")
            task_text = self.task_entry.get()
            goal_text = self.goal_entry.get()
            self.focus_task_label.config(text="Task: " + task_text)
            self.focus_goal_label.config(text="Goal: " + goal_text)

            self.pomodoro.running = False
            self.pomodoro.in_bonus = False
            self.pomodoro.set_time(pomodoro_time)
            self.pomodoro.start()
            # Timer update will be handled by the Stopwatch class

            self.contemplation_frame.pack_forget()
            self.reflection_frame.pack_forget()
            self.focus_frame.pack(fill='both', expand=True)

    def show_reflection(self):
        self.tick_channel.stop()
        self.pomodoro.pause()
        data = self.pomodoro.getStopWatchData()
        print(data)
        print("\n distraction counts" + str(self.shortDistraction) + " " + str(self.longDistraction))

        task_text = self.task_entry.get()
        goal_text = self.goal_entry.get()
        self.reflection_task_label.config(text="Task: " + task_text)
        self.reflection_goal_label.config(text="Goal: " + goal_text)

        self.short_value.config(text=str(self.shortDistraction))
        self.long_value.config(text=str(self.longDistraction))

        self.breakStopwatch.running = False
        self.breakStopwatch.in_bonus = False
        self.breakStopwatch.set_time(int(self.break_entry.get()))
        self.breakStopwatch.start()
        # Break timer update will be handled by the Stopwatch class
        data = self.pomodoro.getStopWatchData()

        self.focus_frame.pack_forget()
        self.reflection_frame.pack_forget()
        self.contemplation_frame.pack_forget()
        self.reflection_frame.pack(fill='both', expand=True)
        self.master.update_idletasks()
        self.master.geometry('550x500')

    def show_contemplation(self, action=None):
        error_present = False
        if action == "insert":
            if self.validate_data():
                self.insert_into_database()
            else:
                send_notification("error", "Data validation failed. Not inserting.")
                error_present = True
        elif action == "discard":
            print("Changes discarded.")

        if not error_present:
            self.toggle_sound(state="OFF")
            self.clear_form_fields()
            self.focus_frame.pack_forget()
            self.reflection_frame.pack_forget()
            self.contemplation_frame.pack_forget()
            self.contemplation_frame.pack(fill='both', expand=True)
            self.master.geometry('450x350')

    def validate_satisfaction(self, event=None):
        try:
            val = int(self.satisfaction_entry.get())
            if not 1 <= val <= 10:
                raise ValueError("Satisfaction rating must be between 1 and 10.")
            else:
                return True
        except ValueError:
            self.satisfaction_entry.delete(0, 'end')
            self.satisfaction_entry.insert(0, "Invalid input")
        return False

    def validate_data(self):
        task = self.task_entry.get().strip()
        if not task:
            send_notification("Error", "Task cannot be empty.")
            return False

        time_spent = self.pomodoro.get_time()
        if time_spent <= 0:
            send_notification("Error", "Time spent on task must be greater than zero.")
            return False

        bonus_time_spent = self.pomodoro.bonus_time
        if bonus_time_spent < 0:
            send_notification("Error", "Bonus time cannot be negative.")
            return False

        time_rested = self.breakStopwatch.get_time()
        if time_rested <= 0:
            send_notification("Error", "Time rested must be greater than zero.")
            return False

        bonus_time_rested = self.breakStopwatch.bonus_time
        if bonus_time_rested < 0:
            send_notification("Error", "Bonus time for rest cannot be negative.")
            return False

        short_distractions = self.shortDistraction
        if short_distractions < 0:
            send_notification("Error", "Number of short-term distractions cannot be negative.")
            return False

        long_distractions = self.longDistraction
        if long_distractions < 0:
            send_notification("Error", "Number of long-term distractions cannot be negative.")
            return False

        return True

    def insert_into_database(self):
        filename = 'database.xlsx'
        self.pomodoro.pause()
        self.breakStopwatch.pause()
        data = self.pomodoro.getStopWatchData()
        restingData = self.breakStopwatch.getStopWatchData()
        start_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", self.pomodoro.startLocalTime) if self.pomodoro.startLocalTime else "Not started"
        data = {
            'Start Time': data['Local Time'],
            'Task': self.task_entry.get(),
            'Goal': self.goal_entry.get(),
            'Time Spent on Task': data['Elapsed Time'],
            'Bonus Time Spent on Task': data['Bonus Time'],
            'Time Rested':  restingData['Elapsed Time'],
            'Bonus Time Rested': restingData['Bonus Time'],
            'Number of Short-Term Distractions': self.shortDistraction,
            'Number of Long-Term Distractions': self.longDistraction,
            'Reflection': self.reflection_textbox.get("1.0", "end-1c"),
            'Satisfaction Level': self.satisfaction_entry.get()
        }

        file_exists = os.path.isfile(filename)

        if not file_exists:
            wb = Workbook()
            ws = wb.active
        else:
            wb = load_workbook(filename)
            ws = wb.active

        if not file_exists:
            for col, header in enumerate(data.keys(), start=1):
                ws[f'{get_column_letter(col)}1'] = header

        next_row = ws.max_row + 1 if file_exists else 2

        for col, (key, value) in enumerate(data.items(), start=1):
            ws[f'{get_column_letter(col)}{next_row}'] = value

        wb.save(filename)
        print("Data inserted successfully into Excel.")

    def clear_form_fields(self):
        if hasattr(self, 'task_entry'):
            self.reflection_task_label.config(text=" ")
        if hasattr(self, 'goal_entry'):
            self.reflection_goal_label.config(text=" ")
        if hasattr(self, 'satisfaction_entry'):
            self.satisfaction_entry.delete(0, 'end')
        if hasattr(self, 'reflection_textbox'):
            self.reflection_textbox.delete("1.0", "end")
        self.reset_and_pause_break_stopwatch()
        if hasattr(self, 'short_value'):
            self.shortDistraction = 0
            self.short_value.config(text=str(self.shortDistraction))
        if hasattr(self, 'long_value'):
            self.longDistraction = 0
            self.long_value.config(text=str(self.longDistraction))
        if hasattr(self, 'break_time_label'):
            self.break_time_label.config(text="00:00")

    def reset_and_pause_break_stopwatch(self):
        if self.breakStopwatch.running:
            self.breakStopwatch.pause()
        self.breakStopwatch.remaining_time = 0
        self.breakStopwatch.in_bonus = False
        self.breakStopwatch.bonus_time = 0

    def toggle_sound(self, state=" "):
        if state == " ":
            self.sound_enabled = not self.sound_enabled
            self.toggle_sound_button.config(text="DISABLE SOUND" if self.sound_enabled else "ENABLE SOUND")
        elif state == "ON":
            self.sound_enabled = True
        elif state == "OFF":
            self.sound_enabled = False

        print("sound is " + str(self.sound_enabled))
        if self.sound_enabled:
            if not self.tick_channel.get_busy():
                self.tick_channel.play(self.tick_sound, loops=-1)
        else:
            self.tick_channel.stop()


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Pomodoro Timer"
    )


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = PomodoroApp(root)
    root.mainloop()
