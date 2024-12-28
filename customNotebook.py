from tkinter import ttk
import tkinter as tk
class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab and head management for each tab."""
    
    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__initialized = True

        kwargs["style"] = "CustomNotebook"
        super().__init__(*args, **kwargs)

        self._active = None
        self.tab_heads = {}  # Maps tab IDs to their head nodes
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button."""
        try:
            element = self.identify(event.x, event.y)
            index = self.index("@%d,%d" % (event.x, event.y))
            if "close" in element:
                self.state(['pressed'])
                self._active = index
        except tk.TclError:
            print("No valid tab identified at the clicked position.")

    def on_close_release(self, event):
        """Called when the button is released over the close button."""
        try:
            index = self.index("@%d,%d" % (event.x, event.y))
            element = self.identify(event.x, event.y)
            if "close" in element and self._active == index:
                tab_id = self.tabs()[index]
                self.forget(index)
                self.event_generate("<<NotebookTabClosed>>")

                # Remove the head associated with the closed tab
                if tab_id in self.tab_heads:
                    del self.tab_heads[tab_id]

        except tk.TclError:
            pass

        self.state(["!pressed"])
        self._active = None

    def on_tab_change(self, event):
        """Updates the current head when switching tabs."""
        selected_tab = self.select()
        global head
        head = self.tab_heads.get(selected_tab, None)  # Update the global head to match the current tab

    def set_head(self, tab, head_node):
        """Associates a head node with a tab."""
        self.tab_heads[tab] = head_node

    def get_head(self, tab):
        """Retrieves the head node associated with a tab."""
        return self.tab_heads.get(tab, None)

    def add_tab(self, tab_frame, head_node, title="Untitled"):
        """Adds a new tab and associates it with a head node."""
        self.add(tab_frame, text=title)
        self.set_head(self.tabs()[-1], head_node)  # Associate the new tab with its head
        
    def getIndex(self,event):
        try:
            return self.index("@%d,%d" % (event.x, event.y))
        except:
            return -1
    def newCustomWidget(self):#SO I'M GOING TO TRY TO BE ABLE TO SWITCH BETWEEN STATES.
        style = ttk.Style()
        style.layout("new.Tab", [
            ("new.tab", {
            "sticky": "w", 
            "children": [
                ("new.padding", {
                "side": "bot", 
                "sticky": "w",
                "children": [
                    ("new.focus", {
                    "side": "top", 
                    "sticky": "w",
                    "children": [
                        ("new.label", {"side": "left", "sticky": ''}),
                        # ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                    ]
                })
                ]
            })
            ]
        })
        ])
    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
            R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
            d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
            5kEJADs=
            '''),
            tk.PhotoImage("img_closeactive", data='''
            R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
            AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
            '''),
            tk.PhotoImage("img_closepressed", data='''
            R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
            d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
            5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",("active", "pressed", "!disabled", "img_closepressed"),("active", "!disabled", "img_closeactive"), border=8, sticky='')#so this creates the x
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [("CustomNotebook.tab", {
            "sticky": "nswe", 
            "children": [
                ("CustomNotebook.padding", {
                "side": "top", 
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.focus", {
                    "side": "top", 
                    "sticky": "nswe",
                    "children": [
                        ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                        ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                    ]
                })
                ]
            })
            ]
        })
        ])
        style.map('CustomNotebook.tab',image = [('disabled',[("CustomNotebook.tab", {
            "sticky": "nswe", 
            "children": [
                ("CustomNotebook.padding", {
                "side": "top", 
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.focus", {
                    "side": "top", 
                    "sticky": "nswe",
                    "children": [
                        ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                    ]
                })
                ]
            })
            ]
        })
        ] )])