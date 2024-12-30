import tkinter as tk
import operator
import json
# import pdb
#from settings import storemetaBox
from textBox import AutoResizedText
# from customNotebook import CustomNotebook
import copy
import sys
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk

class MetaBox:# so our bug exists on the first nodes siblings.
    def __init__(self, master,height=0,width=0,word= "",child= None,parent = None, sibling= None,head = None, app=None):
        self.master = master
        self.child = child 
        self.parent = parent
        self.sibling = sibling
        self.width=width
        self.height=height
        self.head = self if head is None else head
        self.app = app
        self.txtBox(word)
        
        # frame.grid_columnconfigure(width*2,minsize=40)
        # print(self.txt.grid_info())
    def txtBox(self,word):
        self.word = word.strip("\r\n") 
        nlines = word.count('\n')
        nlines = (nlines * 25)+25
        nWidth = word.split("\n")
        maxLineLength = findMaxLine(nWidth)
        self.txt = AutoResizedText(self.master, family="Arial",size=8, width = maxLineLength , height = nlines,background = "black",foreground = "white") #how to make int go by characters or something similar
        self.txt.grid(row = self.height, column = self.width,sticky = "ew")
        self.txt._fit_to_size_of_text(word)
        self.txt.bind("<Shift-Delete>",self.deleteSelf)
        self.txt.bind('<Shift-Up>',self.moveUp)
        self.txt.bind('<Shift-Down>',self.insertSibling)
        self.txt.bind('<Shift-Right>',self.insertChild)

    def moveUp(self,event):
        if(self.parent):
            self.parent.txt.focus()
            self.app.scroll_to_widget(self.parent.txt)
            

    def moveDown(self):
        curr = self
        while curr.parent is not None:
            curr = curr.parent
        sortButtons(curr,0,0)

    def insertSibling(self,event):
        # head = notebook.get_head(notebook.select())  # Get the current head
        if(self.sibling):
            #self=self.sibling
            # print("sibling")
            self.sibling.txt.focus()
            self.app.scroll_to_widget(self.sibling.txt)
            return
        newNode = MetaBox(self.master,self.height+1,self.width,parent = self,head = self.head, app = self.app)
        self.sibling = newNode
        # mainCanvas.yview_scroll(100, "units")
        
        sortButtons(self.head,0,0)
        self.app.scroll_to_widget(newNode.txt)

    def insertChild(self,event):
        # head = notebook.get_head(notebook.select())  # Get the current head
        if (self.child):
            self.child.txt.focus() 
            self.app.scroll_to_widget(self.child.txt)
            return
            
        nextNode = MetaBox(self.master,self.height+1,self.width+1,parent = self,head = self.head, app = self.app)
        self.child = nextNode
        sortButtons(self.head,0,0)#what's the purpose of this? Well looks through all the buttons EVERY SINGLE ONE. Determines the num of descendents then can you  you know.
        self.app.scroll_to_widget(nextNode.txt)

    def deleteSelf(self,event):#deletes itself as well as all descendents of self
        # head = notebook.get_head(notebook.select())  # Get the current head
        #to simplify program we are removing DFS/BFS in delete self and simply not allowing
        #NODE NOT ALLOWED TO BE DELETED IF HAS CHILDREN
        if(self.child is not None or self is self.head):#here we are seeing if it has children so we can delete it and the rest of it's descendents using dfs
            # deleteThis.append(self.child)
            # self.child=None
            return;
        else:
             self.txt.destroy()

        # deleteThis = []
        # curr = self
        
        if(self.sibling is not None):#here we replace the link between the parent and the self with either none or it's sibling.
            if self.parent.child == self:#eldest sibling
                self.parent.child = self.sibling
                self.sibling.parent = self.parent
                # print("eldest sibling")
            else:#middle child
                self.parent.sibling = self.sibling
                self.sibling.parent = self.parent
                # print("normal sibling")
        elif self.parent.sibling == self:#youngest sibling
            self.parent.sibling =None
            # self.parent.child = None
            # print("youngest child")
        elif self.parent.child == self:#only child
            # self.parent.sibling =None
            self.parent.child = None
            # print("no sibling")
        # while deleteThis:
        #     curr = deleteThis.pop(0)
        #     curr.txt.destroy()
        #     if(curr.child is not None):
        #         deleteThis.append(curr.child)
        #     if(curr.sibling is not None):
        #         deleteThis.append(curr.sibling)
        #     curr = None # DELETES REFERENCE To child
        #     curr.parent = None

        sortButtons(self.head,0,0) #reorganizes GUI to fit the new structure created
        self.parent.txt.focus()


def ancestor(curr,width):#traverses up until curr.width = width
    while(curr.width !=width):
        curr = curr.parent
    return curr

def traverse(curr,diction):#sorts in preorder
	# if((curr.child is None) and (curr.sibling is None) and (curr is not None)):#deals with the end of a tree branch
	# 	diction.append({"height": curr.height,"width": curr.width, "word": curr.word})
    if(curr.child is not None):
        word= curr.child.txt.get("1.0",tk.END)
        diction.append({"height": curr.child.height,"width": curr.child.width, "word": word.strip("\r\n")})
        traverse(curr.child,diction)
    if(curr.sibling is not None):
        word= curr.sibling.txt.get("1.0",tk.END)
        diction.append({"height": curr.sibling.height,"width": curr.sibling.width, "word": word.strip("\r\n")})
        traverse(curr.sibling,diction)
    return diction	
def sortButtons(curr,height,width):#this sorts out bobs starting from curr(usually head)
	if curr.child is not None:
		sortButtons(curr.child,height+1,width+1)#for each bob created from this child temp will increase by
	if curr.sibling is not None:
		temp1=countChildren(curr)+1
		sortButtons(curr.sibling,height+temp1,width)

	curr.height = height
	curr.width = width
	curr.txt.grid_configure(row = height, column = width,sticky = "w")
def conversion(converting):#this method converts string to int, or int to string
    try:
	#if it is a string with a number it will run this, changing it to an int
        converted = converting + ""
        converted = int(converting)
    except :# if it is a int, it'll convert to a string
        converted = str(converting)
    return converted

def findMaxLine(myList):
    try:
        for x in range(1,len(myList)):
            if myList[0] < myList[x]:
                myList[0] = myList[x]
                return int(myList[0])
    except ValueError:
        return 100
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def _on_mousewheel(event):
    mainCanvas.yview_scroll(-1*(int)(event.delta/40), "units")

def initializeScollbar(master):
    mainCanvas.grid(row = 1,column = 0,sticky = "ew")
    mainCanvas.bind_all("<MouseWheel>", _on_mousewheel)
    vsb.grid(column = 1,row = 1,sticky = "news")	
    hsb.grid(column=0,row = 2,sticky = "ew")
    vsb.rowconfigure(0, weight=1)
    hsb.columnconfigure(0, weight=1)
    mainCanvas.configure(yscrollcommand=vsb.set,xscrollcommand = hsb.set,height = master.winfo_screenheight()-120,width = master.winfo_screenwidth()-20,yscrollincrement = '2',xscrollincrement = '2')	
    mainCanvas.create_window((12,12), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=mainCanvas: onFrameConfigure(mainCanvas))
	# mainCanvas.configure(yscrollincrement='2')
def moveFocus(curr):
    curr.txt.focus_set()
def printLinked(head):
    print(str(self.head.height) + " " + str(selffhead.width) + " " + self.head.word)
    if selfhead.child is not None:
        printLinked(self.head.child)
    if self.head.sibling is not None:
        printLinked(self.head.sibling)
def countChildren(curr):#counts number of descendents 
	count = 0
	stack = []
	if curr.child is not None:
		count+=1
		stack.append(curr.child)
	while stack:#uses dfs
		noder = stack.pop(0)
		if noder.child is not None:
			stack.append(noder.child)
			count+=1
		if noder.sibling is not None:
			stack.append(noder.sibling)
			count+=1
	return count

# @@@@@@@@@@@@@@@@@ THIS IS WHERE MENU METHODS START@@@@@@@@@@@@@@@@
def initializeBorderButtons(master,frame):
    menu = tk.Menu(master)
    master.config(menu = menu) 

    subMenu = tk.Menu(menu,tearoff = 0) # creating a menu item within the menu
    transparentMenu = tk.Menu(menu,tearoff = 0)

    menu.add_cascade(label = "Edit", menu = subMenu) #Name of drop down menu
    menu.add_cascade(label = "Transparancy",  menu = transparentMenu)
    # subMenu.add_command(label = "new Tab", command = lambda: newTab(master))
    # subMenu.add_command(label="new Tab", command=lambda: newTab(notebook))
    subMenu.add_command(label = "save", command = save)
    subMenu.add_command(label = "Open", command = lambda: openTheFile(frame))
    subMenu.add_separator()
    subMenu.add_command(label = "Exit", command =lambda: sys.exit(1))

    transparentMenu.add_command(label = "30%",command = lambda: changeRootTransparency(master,0.3))
    transparentMenu.add_command(label = "50%",command =lambda: changeRootTransparency(master,0.5) )
    transparentMenu.add_command(label = "60%",command = lambda: changeRootTransparency(master,0.6))
    transparentMenu.add_command(label = "70%",command = lambda: changeRootTransparency(master,0.7))
    transparentMenu.add_command(label = "80%",command = lambda: changeRootTransparency(master,0.8))
    transparentMenu.add_command(label = "100%",command = lambda: changeRootTransparency(master,1.0))	
def changeRootTransparency(master,percentage):
    root.attributes("-alpha",percentage)
def newTab(notebook):
    # Create a new frame for the new tab
    new_frame = tk.Frame(notebook)

    # Create a new head for this tab
    new_head = MetaBox(new_frame)

    # Add the new tab and associate the head
    notebook.add_tab(new_frame, new_head)


# @@@@@@@@@@@@@@@@@ THIS IS WHERE MENU METHODS END@@@@@@@@@@@@@@@@
# def createToolBar(master):
#     toolbar = tk.Frame(master, bg = "yellow")
#     insertButt= tk.Button(toolbar,text="button")
#     insertButt.pack(side = tk.LEFT)
#     toolbar.grid(row=0,column=0)
######METHOD

# if __name__ == "__main__":
#     root = tk.Tk() 
#     root.geometry('%sx%s' % (root.winfo_screenwidth(), root.winfo_screenwidth()))

#     mainCanvas = tk.Canvas(root, background="black")
#     frame = tk.Frame(mainCanvas, background="black")

#     vsb = tk.Scrollbar(root, orient="vertical", command=mainCanvas.yview)
#     hsb = tk.Scrollbar(root, orient="horizontal", command=mainCanvas.xview)

#     mainCanvas.configure(scrollregion=mainCanvas.bbox("all"))
#     root.attributes("-alpha", 0.8)

#     initializeScollbar(root)
#     newHead = MetaBox(frame)

#     # Initialize the notebook
#     # notebook = CustomNotebook(frame)
#     # notebook.pack()

#     # Pass the notebook to initializeBorderButtons
#     initializeBorderButtons(root, frame)

#     # Create the first tab
#     # newTab(notebook)

#     root.mainloop()

class MetaBoxApp:
    def __init__(self, parent):
        # Use parent instead of root
        self.parent = parent

        # Configure the ttk theme styles
        style = ttk.Style()
        style.configure('TCanvas', background='#383838')
        style.configure('TFrame', background='#383838')

        self.canvas = tk.Canvas(self.parent, background="black")
        self.frame = tk.Frame(self.canvas, background="black")

        # Apply the theme to Canvas and Frame
        self.canvas = tk.Canvas(self.parent, background='#383838', highlightthickness=0)
        self.frame = ttk.Frame(self.canvas, style='TFrame')

        self.vsb = tk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(self.parent, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.head = MetaBox(self.frame,app = self)  

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Windows/macOS
        
        # self.initialize_menu()


    def on_mousewheel(self, event):
        # Adjust scrolling based on platform
        if event.delta:  # Windows and macOS
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def initialize_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def save(self,head):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".pz")
        if not file:
            return

        data = []
        word = head.txt.get("1.0", tk.END).strip("\r\n")
        data.append({"height": head.height, "width": head.width, "word": word})
        traverse(head,data)
        json.dump(data, file, indent=4)
        file.close()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        # # self.head = MetaBox(self.frame, word=data[0]['word'],app=self)
        # self.head.txt.text_box.delete("1.0", tk.END)  # Clear any existing text in the head
        # self.head.txt.text_box.insert("1.0", data[0]["word"])  # Set the new word
        # Delete the existing tree
        self.delete_tree(self.head)
        self.head = MetaBox(self.frame,data[0]["height"],data[0]["width"],data[0]["word"],app = self)
        curr = self.head

        descendentCounter = 0
        for index in range(1,len(data)):
            if((curr.height+1 == data[index]["height"]) and (curr.width+1==data[index]["width"])):#if the next node is a child to curr
                bob = MetaBox(self.frame,data[index]["height"],data[index]["width"],data[index]["word"],parent = curr,head = self.head,app = self)
                curr.child = bob
                curr = curr.child
                print("child found")
            elif(curr.width+1 != data[index]["width"]):#it's a sibling to someone therefore width between curr and next node are the same
                curr = ancestor(curr,data[index]["width"])
                bob = MetaBox(self.frame,data[index]["height"],data[index]["width"],data[index]["word"],parent = curr,head = self.head,app = self)
                bob.parent.sibling = bob
                curr = curr.sibling
                print("sibling found")
            else:
                print("ERROR IN   " + str(data[index]["height"]) + " " + str(data[index]["width"]) +" " + str(data[index]["word"]) )
        self.on_frame_configure()
    def delete_tree(self, node):
        """Recursively delete all nodes starting from the given node."""
        if node is None:
            return

        # Delete children and siblings recursively
        if node.child:
            self.delete_tree(node.child)
        if node.sibling:
            self.delete_tree(node.sibling)

        # Destroy the node's widget (e.g., text box)
        if hasattr(node, "txt") and node.txt:
            node.txt.destroy()

        # Disconnect the node
        node.child = None
        node.sibling = None
        node.parent = None
        print(f"Deleted node at height {node.height}, width {node.width}")
    def on_frame_configure(self, event=None):
        """Update the scroll region to encompass all content."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # def scroll_to_widget(self, widget = None,xMovement = 0,yMovement = 0):
    #     # self.canvas.update_idletasks()
    #     self.canvas.yview_scroll(yMovement, "page")
    #     self.canvas.xview_scroll(xMovement, "units")
    def scroll_to_widget(self, widget):
        # Ensure the canvas and elements are updated
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()


        # Get canvas dimensions (viewport dimensions)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Get the bounding box of all canvas content
        canvas_bbox = self.canvas.bbox("all")
        if not canvas_bbox:
            return  # No content in canvas, do nothing

        canvas_total_width = canvas_bbox[2]  # Total content width
        canvas_total_height = canvas_bbox[3]  # Total content height

        # Calculate the target scroll positions to center the widget
        widget_center_x = widget.winfo_x() + widget.winfo_width() / 2
        scroll_x = max(0, min((widget_center_x) / canvas_total_width, 1))

        widget_center_y = widget.winfo_y() + widget.winfo_height() / 2
        scroll_y = max(0, min((widget_center_y) / canvas_total_height, 1))


        # Scroll canvas to center the widget
        self.canvas.xview_moveto(scroll_x)
        self.canvas.yview_moveto(scroll_y)


if __name__ == "__main__":
    # Use ThemedTk to apply the "equilux" theme
    root = ThemedTk(theme="equilux")
    root.title("MetaBox App")
    root.configure(background='#383838')  # Ensure root background matches the theme

    app = MetaBoxApp(root)
    root.mainloop()
