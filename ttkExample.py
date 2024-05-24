from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk

def submit_action():
    print("Name entered:", name_entry.get())  # This will print to console

def main():
    # Create a themed Tkinter window with the Equilux theme
    root = ThemedTk(theme="equilux")
    root.title("Styled Equilux Theme Example")
    root.geometry("400x250")  # Set the window size

    # Set the background color of the root window to match the theme's color
    root.configure(background='#383838')  # Equilux background color, adjust as needed

    # Customizing style for Entry widget
    style = ttk.Style()
    style.configure('TEntry', font=('Helvetica', 10), borderwidth=1, relief="solid", foreground='#FFF', background='#505050', insertbackground='white')  # Light text cursor
    style.configure('TButton', font=('Helvetica', 10), borderwidth=1, relief="solid", foreground='#FFF', background='#505050')
    style.configure('TLabel', font=('Helvetica', 10), background='#383838', foreground='white')

    # Use frames to organize the layout, setting the frame background to match
    main_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Create a label
    label = ttk.Label(main_frame, text="Enter your name:", style='TLabel')
    label.pack(side=tk.TOP, pady=(0, 10))

    # Entry widget for name input
    name_entry = ttk.Entry(main_frame, style='TEntry')
    name_entry.pack(side=tk.TOP, fill=tk.X)

    # Submit button
    submit_button = ttk.Button(main_frame, text="Submit", style='TButton', command=submit_action)
    submit_button.pack(side=tk.TOP, pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    main()