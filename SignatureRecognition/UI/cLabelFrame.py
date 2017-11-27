import os
import glob
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

frame_color='#795548'
divSquareColor="#8d6e63"
divSquareColor_hover="#808080"

custom_font=("Open Sans",16)

class CustomLabelButtom(tk.Button):

    def __init__(self, master=None,photo='',label=''):
        tk.Button.__init__(self, master,text=label,compound='top',image=photo,width=280,height=230,relief=FLAT,
                            highlightbackground=divSquareColor, cursor="hand1",background=frame_color,
                           highlightcolor=divSquareColor_hover,highlightthickness=2,fg='#fff',font=custom_font
                           , activebackground='#4e342e')
        self.image=photo



