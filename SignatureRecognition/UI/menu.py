import tkinter as tk

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

LARGE_FONT=("Albertus Extra Bold",16)
mid_Font=("Albertus Extra Bold",12)
NORM_FONT=("Albertus Extra Bold",16,"underline")
SMALL_FONT=("Arial",8)
bgColor="#f3f3f3"
fgColor="#d7ccc8"
Color2='#212121'
btnColor="#9e9e9e"

# menuColor='#214761'
menuColor='#4e342e'
btncolor="#4e342e"

def warn(title,msg):
    messagebox.showwarning(title, msg)
    return


class Menu:
    def __init__(self,parent,container):
        self.container=container
        self.parent=parent

    def getMenu(self):
        menuBar = tk.Menu(self.container, background=menuColor, fg=fgColor, activebackground=fgColor)
        fileMenu = tk.Menu(menuBar, tearoff=0, bg=menuColor, fg=fgColor, activebackground=fgColor)
        fileMenu.add_command(label="Save Results", command=lambda: warn("Not available", "Function not available yet."))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.parent.quitting)
        menuBar.add_cascade(label="File", menu=fileMenu)

        editMenu = tk.Menu(menuBar, tearoff=0, bg=menuColor, fg=fgColor, activebackground=fgColor)
        menuBar.add_cascade(label="Edit", menu=editMenu)

        viewMenu = tk.Menu(menuBar, tearoff=0, bg=menuColor, fg=fgColor, activebackground=fgColor)
        menuBar.add_cascade(label="View", menu=viewMenu)

        windowMenu = tk.Menu(menuBar, tearoff=0, bg=menuColor, fg=fgColor, activebackground=fgColor)
        menuBar.add_cascade(label="Window", menu=windowMenu)

        helpMenu = tk.Menu(menuBar, tearoff=0, bg=menuColor, fg=fgColor, activebackground=fgColor)
        helpMenu.add_command(label="About", command=lambda: warn("Not available", "Function not available yet."))
        menuBar.add_cascade(label="Help", menu=helpMenu)

        return menuBar

