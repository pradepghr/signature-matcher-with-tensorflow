import os
import glob
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
# First create application class
LARGE_FONT=("Open Sans",16)
mid_Font=("Open Sans",12)
fgColor="#31708f"
frame_color='#eeeeee'

textbgColor="#d9edf7"
textbdColor="#bce8f1"
textFont="#31708f"


inner_color= '#4e342e'
outer_color= '#795548'


divSquareColor="#bdbdbd"
divSquareColor_hover="#808080"

class ListBox(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master,style="InnerFrame.TFrame")

        self.create_widgets()
        self.selected_name=""

    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())

        classlabel = ttk.Label(self, text="Select signature holder",style="inner.TLabel")

        self.search_label=ttk.Label(self, text="Search:",style="inner.TLabel")
        self.entry = Entry(self, textvariable=self.search_var, width=13,font=LARGE_FONT,fg="#eee",bg=inner_color)
        self.lbox = Listbox(self, width=45, height=15,font=mid_Font,bg=inner_color,fg="#eee")
        self.lbox.bind('<<ListboxSelect>>', self.onselect)
        self.profile=tk.LabelFrame(self,bg=inner_color)

        self.var = StringVar()
        self.Name = tk.Message(self, textvariable=self.var,width=400,font=mid_Font,bg=inner_color,fg="#eee")

        classlabel.grid(row=0,columnspan=2,padx=10, pady=5)
        self.search_label.grid(row=1,padx=10, column=0, pady=5,ipady=5,sticky=W)
        self.entry.grid(row=1, column=1, pady=5,ipady=5,sticky=W)
        self.lbox.grid(row=2,columnspan=2, padx=10, pady=5)


        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self):
        search_term = self.search_var.get()

        #self.read_label_file()
        # Just a generic list to populate the listbox
        lbox_list=self.read_label_file()

        self.lbox.delete(0, END)

        for item in lbox_list:
                if search_term.lower() in item.lower():
                    self.lbox.insert(END, item)

    def onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        #print( 'You selected item %d: "%s"' % (index, value))
        self.selected_name=value

        self.profile_clear()

        self.Name.grid(row=3, column=0, columnspan=2,pady=5)

        self.profile.grid(row=4, columnspan=2, padx=10, pady=5)
        self.var.set(self.selected_name+"'s few stored signatures.")

        self.profile_images()


    def read_label_file(self):
        p = Path(__file__).parents[2]

        file = os.path.join(p, 'Signature Resources and Data/Train_resource/Label_signature/labels.txt')
        #file="/home/pradeep/pythonProjects/Signature Resources and Data/Train_resource/Label_signature/labels.txt"
        with open(file) as f:
            content=f.readlines()

        content=[x.strip() for x in content]

        return content

    def profile_clear(self):
        self.profile.grid_remove()
        self.Name.grid_remove()

    def profile_images(self):

        self.Name.grid()
        p = Path(__file__).parents[2]
        filepath = os.path.join(p, 'Signature Resources and Data/Data/DataSets/Training_Sets/'+self.selected_name)
        #filepath="/home/pradeep/pythonProjects/Signature Resources and Data/Data/DataSets/Training_Sets/"+self.selected_name

        COLUMNS = 5
        image_count = 0
        for filename in glob.glob(os.path.join(filepath, '*.jpg')):
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)

            img = Image.open(filename)
            resized = img.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = ttk.Label(self.profile, image=tkimage,style="inner.TLabel")
            myvar.image = tkimage
            myvar.grid(row=r, column=c)
            if(image_count==5):
                break