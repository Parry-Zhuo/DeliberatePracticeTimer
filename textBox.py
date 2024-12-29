from tkinter import Frame, Text
from tkinter.constants import *
from tkinter import font as tkFont
import tkinter as tk 
from tkinter import ttk

class AutoResizedText(tk.Frame):
	def __init__(self,master, width=6, height=1, family = None, size=None,*args, **kwargs):
		tk.Frame.__init__(self,master,width=2,height=1)
		
		self.height = height
		self.width = width
		self.text_box = tk.Text(
			self,
			height = self.height,
			width = self.width,
			font=('Helvetica', 10),  # Match font style
			fg="#E0E0E0",  # Light gray text color
			bg="#505050",  # Dark gray background
			insertbackground="#E0E0E0",  # Cursor color
			highlightthickness=0  # Remove border highlight)
		)
		self.text_box.pack(expand = True,fill = "both")
		# if family != None and size != None:
		# 	self._font = tkFont.Font(family=family,size=size)
		# else:
		# 	self._font = tkFont.Font(family=self.text_box.cget("font"))
		# self.text_box.config(font=self._font)
		self.text_box.bind("<Key>", self.updateBox)

	def updateBox(self,event=None):#so the reason why this method is kinda bad is because we insert the character. THEN we reorganize the text.
		#the only way to deal with this is reorganize text, THEN we insert into text.
		self.text = event.widget.get("1.0",tk.END).split("\n")
		self.height = len(self.text)
		self.width = 0
		for width in self.text:
			if len(width) > self.width:
				self.width = len(width)
		self.text_box.config(height = self.height,width = self.width+2)
	def changeLocation(self,row,column):
		self.row = row
		self.column = column
		self.text_box.configure(column = self.column,row = self.row)
	# def update_size(self, event):
	# 	print(event)
	# 	widget_width = 0
	# 	widget_height = float(event.widget.index(tk.END))
	# 	for line in event.widget.get("1.0", tk.END).split("\n"):
	# 		if len(line) > widget_width:
	# 			widget_width = len(line)+1
	# 		event.widget.config(width=widget_width, height=widget_height)
	def update_size(self):
		# print(event)
		widget_width = 0#
		widget_height = float(self.text_box.index(tk.END))
		for line in self.text_box.get("1.0", tk.END).split("\n"):
			if len(line) > widget_width:
				widget_width = len(line)+1
			self.text_box.config(width=widget_width, height=widget_height)

	def _fit_to_size_of_text(self, text):
		self.focus()
		self.text_box.insert(END, text)
		self.update_size()

	def insert(self,word):
		self.focus()
		old_text = 'hi'
		print(word)

		for x in range(0,len(word)):
			# old_text=self._insert_character_into_message(old_text, self.text_box.index(INSERT),word[x])
			self.text_box.insert(INSERT, word[x])

	@property
	def bbox(self):
		return self.text_box.bbox()

	def tag(self):
		return self._autoresize_text_tag

	def focus(self):
		self.text_box.focus()

	def bind(self, event, handler, add=None):
		self.text_box.bind(event, handler, add)

	def get(self, start, end=None):
		return self.text_box.get(start, end)

	def update(self, text):
		self.text_box.delete('1.0', 'end')
		self._fit_to_size_of_text(text)
		self.text_box.insert('1.0', text)

#
# root = tk.Tk()
# hi=AutoResizedText(root)
# hi.grid(row=0,column=0)
# hi=AutoResizedText(root)
# hi._fit_to_size_of_text("hello\n\n")
# hi.grid(row=5,column=2)
# root.mainloop()

# #planning AutoResiedText