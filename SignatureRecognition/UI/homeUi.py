import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from menu import Menu
from Pages import StartPage,AddClassPage,TestSigPage,ResultPage,DisplayTraining

# Styles
LARGE_FONT=("Open Sans",16)
mid_Font=("Open Sans",12)
inner_color= '#4e342e'
outer_color= '#795548'
textbgColor="#d9edf7"
textbdColor="#bce8f1"
divSquareColor_hover="#808080"

#flags
train_flag=1
test_flag=None
result_flag=1

def warn(title,msg):
    messagebox.showwarning(title, msg)
    return

def confirm(title,msg):
    op=messagebox.askokcancel(title, msg)
    return op

def info(title,msg):
    op=messagebox.showinfo(title,msg)
    return op

class HomeGUI(tk.Tk):

    '''initialize the application and tkinter'''

    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.withdraw()  # hide the window
        self.after(0, self.deiconify)

        # Custom styles of widgets
        style = ttk.Style()
        style.configure("b.TButton", background=outer_color,foreground="#eee",font=LARGE_FONT)
        style.map('b.TButton',
                  foreground=[('disabled', '#fff'),
                          ('pressed', '#e0e0e0'),
                          ('active', '#fff')],
                  background=[('disabled', outer_color),
                              ('pressed', '!focus', 'cyan'),
                              ('active', inner_color)],
                  highlightcolor=[('focus', 'green'),
                              ('!focus', 'red')],
                  relief=[('pressed', 'groove'),
                      ('!pressed', 'raised')])

        style.configure("TLabel", foreground="#eee", font=LARGE_FONT, background=outer_color)
        style.configure("inner.TLabel", foreground="#eee", font=LARGE_FONT, background=inner_color)
        style.configure("TLabelframe",highlightbackground="#8d6e63",cursor="hand1",background=outer_color
                        ,highlightthickness=2,relief=tk.FLAT)
        style.configure('InnerFrame.TFrame', background=inner_color, foreground="#fff",
                        highlightbackground=textbdColor, highlightcolor=divSquareColor_hover
                        , highlightthickness=1)
        style.configure('OuterFrame.TFrame', background=outer_color, foreground='#fff')
        style.configure('Treeview',background=inner_color,foreground="#eee",font=mid_Font, rowheight=40)
        style.configure("Treeview.Heading", foreground='#000',font=LARGE_FONT)
        style.configure("Treeview.row",background=inner_color)
        style.configure("TEntry",background=inner_color,fg="#eee", font=LARGE_FONT)

        tk.Tk.configure(self, background=outer_color)
        container=tk.Frame(self)

        tk.Tk.wm_title(self, "Signature verification 1.0")

        container.pack(side="top",fill="both",expand =True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        m=Menu(self,container)
        menuBar=m.getMenu()

        tk.Tk.config(self,menu=menuBar)

        self.frames={}

        for F in (StartPage, AddClassPage, TestSigPage, DisplayTraining, ResultPage):

            frame = F(container,self)

            self.frames[F]=frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)



    def get_page(self,classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None

    def show_frame(self,cont):
        '''Switches the Frame'''

        if(cont.__name__ is 'ResultPage'):
            '''Running tensorboard on different thread'''
            result_page=self.get_page('ResultPage')
            self.tb= result_page.initiate()
            #result_page.start()

        if( cont.__name__ is 'ResultPage'):
            if( result_flag == None):
                warn("Feature not available","Training must be done before checking any result. ")
                return

        if(cont.__name__ is 'testSigPage'):
            if(test_flag==None):
                warn("Feature not available", "Training must be done before testing.")
                return

        if (cont.__name__ is 'DisplayTraining'):
            if (train_flag == None):
                warn("Feature not available", "Datasets must be given before training.")
                return

        frame=self.frames[cont]
        frame.tkraise()


    def quitting(self):
        if messagebox.askokcancel("Quit", "Are you sure to quit the application?"):
            try:

                self.tb.stop()

                print("Exiting")
                quit()
                self.destroy()

            except AttributeError:
                quit()
                self.destroy()

app=HomeGUI()
app.protocol("WM_DELETE_WINDOW", app.quitting)
app.geometry("1376x768")
app.mainloop()