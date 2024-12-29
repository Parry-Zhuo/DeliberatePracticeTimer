import tkinter as tk

root = tk.Tk()

# Tkinter widgets needed for scrolling. The only native scrollable container that Tkinter provides is a canvas.
# A Frame is needed inside the Canvas so that widgets can be added to the Frame and the Canvas makes it scrollable.
cTableContainer = tk.Canvas(root)
fTable = tk.Frame(cTableContainer)
sbHorizontalScrollBar = tk.Scrollbar(root)
sbVerticalScrollBar = tk.Scrollbar(root)

# Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
def updateScrollRegion():
    cTableContainer.update_idletasks()
    cTableContainer.config(scrollregion=cTableContainer.bbox("all"))

# Scrolls to a specific widget to ensure it is visible in the canvas
def scrollToWidget(widget):
    cTableContainer.update_idletasks()
    # Get widget position relative to canvas
    widget_x = widget.winfo_rootx() - cTableContainer.winfo_rootx()
    widget_y = widget.winfo_rooty() - cTableContainer.winfo_rooty()

    # Calculate how much to scroll
    canvas_width = cTableContainer.winfo_width()
    canvas_height = cTableContainer.winfo_height()

    # Scroll horizontally if needed
    if widget_x < 0 or widget_x > canvas_width:
        cTableContainer.xview_moveto(widget_x / cTableContainer.bbox("all")[2])
    # Scroll vertically if needed
    if widget_y < 0 or widget_y > canvas_height:
        cTableContainer.yview_moveto(widget_y / cTableContainer.bbox("all")[3])

# Sets up the Canvas, Frame, and scrollbars for scrolling
def createScrollableContainer():
    cTableContainer.config(xscrollcommand=sbHorizontalScrollBar.set, yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    sbHorizontalScrollBar.config(orient=tk.HORIZONTAL, command=cTableContainer.xview)
    sbVerticalScrollBar.config(orient=tk.VERTICAL, command=cTableContainer.yview)

    sbHorizontalScrollBar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
    sbVerticalScrollBar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    cTableContainer.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
    cTableContainer.create_window(0, 0, window=fTable, anchor=tk.NW)

# Adds labels diagonally across the screen to demonstrate the scrollbar adapting to the increasing size
i = 0

def addNewLabel():
    global i
    new_label = tk.Label(fTable, text=f"Hello World {i}")
    new_label.grid(row=i, column=i)
    i += 1

    # Update the scroll region after new widgets are added
    updateScrollRegion()

    # Automatically scroll to the new widget
    scrollToWidget(new_label)

    root.after(1000, addNewLabel)

createScrollableContainer()
addNewLabel()

root.mainloop()
