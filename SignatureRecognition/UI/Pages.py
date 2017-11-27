import subprocess
import  webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from pathlib import Path

from graphFrames import CrossFrame,AccuracyFrame,FinalOutputsFrame
from ListSearch import ListBox
from cLabelFrame import CustomLabelButtom
from TensorBoard import TensorBoard

from SignatureRecognition.image_retraining.createClassDir import CreateClassDir
from SignatureRecognition.image_retraining.test_Signature import TestSignature

LARGE_FONT=("Open Sans",16)
mid_Font=("Open Sans",12)
outer_color= '#795548'
inner_color= '#4e342e'
textbgColor="#d9edf7"
textbdColor="#bce8f1"
textFont="#31708f"
divSquareColor_hover="#808080"


def warn(title,msg):
    messagebox.showwarning(title, msg)
    return

def confirm(title,msg):
    op=messagebox.askokcancel(title, msg)
    return op

def info(title,msg):
    op=messagebox.showinfo(title,msg)
    return op

def link_tensorboard():
    webbrowser.open_new(r"http://0.0.0.0:6006")

def makeImage(imagePath='',width=200,height=200):
    addClassImage = Image.open(imagePath)
    resized = addClassImage.resize((width, height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized)
    return img


class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller
        ttk.Frame.__init__(self,parent,style='OuterFrame.TFrame')

        # Software Info Message
        var=StringVar()
        Info=tk.Message(self,textvariable=var,width=850,font=LARGE_FONT,fg=textFont,bg=textbgColor,
                        relief=GROOVE,highlightbackground=textbdColor,highlightcolor=divSquareColor_hover
                        ,highlightthickness=1 )
        var.set("Signature Verification 1.0 is a prototype software where you can "
                "train the machine to identify and verify handwritten signatures.\n"
                "Choose the any of following options to begin your machine learning experiments.")
        Info.pack(pady=10,padx=10)

        # Container for options
        buttonFrame = tk.LabelFrame(self,relief=FLAT,width=850,background="#4e342e" )
        buttonFrame.pack(pady=5)

        # Images for button
        p = Path(__file__).parents[2]
        #path = os.path.join(p, 'Signature Resources and Data/retrain_logs')
        add_class_image=makeImage("Images/addclass.png",200,200)

        train_image = makeImage("Images/addSignature.png",200,200)

        test_sig_image =makeImage("Images/check.png",200,200)

        check_result_image =makeImage("Images/checkResult.jpeg",200,200)

        addClassButton=CustomLabelButtom(buttonFrame,add_class_image,"Add New Class")
        addClassButton.grid(row=0,column=0,padx=15,pady=10)
        addClassButton.bind("<Button-1>",lambda f:controller.show_frame(AddClassPage))

        trainModelButton = CustomLabelButtom(buttonFrame, train_image, "Train The Model")
        trainModelButton.grid(row=0, column=1, padx=15, pady=10)
        trainModelButton.bind("<Button-1>", lambda f: controller.show_frame(DisplayTraining))

        testSigButton = CustomLabelButtom(buttonFrame, test_sig_image, "Check Signature")
        testSigButton.grid(row=1, column=0, padx=15, pady=10)
        testSigButton.bind("<Button-1>", lambda f: controller.show_frame(TestSigPage))

        checkResultButton = CustomLabelButtom(buttonFrame, check_result_image, "Training Result")
        checkResultButton.grid(row=1, column=1, padx=15, pady=10)
        checkResultButton.bind("<Button-1>", lambda f: controller.show_frame(ResultPage))


class AddClassPage(ttk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller
        ttk.Frame.__init__(self,parent,style='OuterFrame.TFrame')

        goHomebtn = ttk.Button(self, text="Back to home",style="b.TButton",cursor="hand1",
                              command=lambda:[self.dirLabel.grid_remove(), controller.show_frame(StartPage)])

        goHomebtn.pack(side=LEFT, anchor=N,padx=5,pady=5)

        innerFrame = ttk.Frame(self, width=820,relief=GROOVE,style="InnerFrame.TFrame")
        innerFrame.pack()

        addLabel = tk.Label(innerFrame,text="Add New Class\n\nUpload signature images (at least 100) and provide appropriate name.",
                         font=LARGE_FONT, fg=textFont, bg=textbgColor,relief=GROOVE, highlightbackground=textbdColor,
                            highlightcolor=divSquareColor_hover, highlightthickness=1)
        addLabel.grid(row=0,pady=10,padx=10)

        browseLabel=ttk.Label(innerFrame, text="Browse the folder containing your dataset:",style="inner.TLabel")
        browseLabel.grid(row=1,column=0,pady=10,padx=10,sticky=W)

        self.filename = ''
        self.className = ''

        browseBtn=ttk.Button(innerFrame, text="Browse", command=self.select_dir, cursor="hand1", style="b.TButton")
        browseBtn.grid(row=2,column=0,pady=10,padx=10,sticky=W)

        self.dir_var = StringVar()
        self.dirLabel = tk.Message(innerFrame, textvariable=self.dir_var, width=400, relief=FLAT, font=LARGE_FONT,bg=inner_color)

        classlabel=ttk.Label(innerFrame, text="Give name for signature holder (ie. class name):",style="inner.TLabel")
        classlabel.grid(row=4,column=0,padx=10,pady=10,sticky=W)

        self.classNameEntry=tk.Entry(innerFrame,fg="#eee",bg=inner_color,font=LARGE_FONT)
        self.classNameEntry.grid(row=5,column=0,pady=5,padx=10,sticky=W,ipadx=20,ipady=5)

        confirmbtn=ttk.Button(innerFrame, text="Add the Data for training", cursor="hand1", style="b.TButton",command =self.add_files)
        confirmbtn.grid(row=6,pady=20)

    def select_dir(self):
        self.filename = filedialog.askdirectory()
        self.dir_var.set(self.filename)
        self.dirLabel.grid(row=3,pady=5,padx=10,sticky=W)
        print(self.filename)

    def add_files(self):
        self.className = self.classNameEntry.get().lower()

        if(self.filename == ''):
            warn("Files not selected.","You need to select Folder first!")
            return
        if (self.className == ''):
            warn("Class name not given.", "You need to give class name first!")
            return

        if(confirm("Confirm Adding Files.","Are you sure to add selected datasets.")):

            try:
                c = CreateClassDir(self.filename,self.className)
                c.make_class()

                info("Sucess","Files in {} Added.\n\n Class \"{}\" created\n\n Repeat same steps to add other data.".format(self.filename,self.className))

            except FileNotFoundError:
                warn("File not Found","No any jpg files were found in given directory")

            self.classNameEntry.delete(0, 'end')
            self.filename = ''
            self.className = ''
            self.dirLabel.grid_remove()


class TestSigPage(ttk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller

        ttk.Frame.__init__(self,parent,style='OuterFrame.TFrame')

        goHomebtn = ttk.Button(self, text="Back to home", style="b.TButton", cursor="hand1",command=lambda: [self.reset(), controller.show_frame(StartPage)])
        goHomebtn.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.innerFrame = ttk.Frame(self, width=820, relief=GROOVE, style="InnerFrame.TFrame")
        self.innerFrame.pack()

        self.resultFrame = ttk.Frame(self, width=820, relief=GROOVE, style="InnerFrame.TFrame")
        self.resultFrame.pack()
        self.resultFrame.forget()

        self.Info = tk.Label(self.innerFrame,
                 text="Check Signature\n\nChoose the signature you want to test,Select the name of signature"
                 "holder from the list for further \ninformation.Click initialize button to begin testing"
                 "process.",
                 font=LARGE_FONT, fg=textFont, bg=textbgColor,
                 relief=GROOVE, highlightbackground=textbdColor, highlightcolor=divSquareColor_hover
                 , highlightthickness=1)

        self.Info.pack(pady=10, padx=10)

        self.mid_frame = ttk.Frame(self.innerFrame, relief=FLAT,style='InnerFrame.TFrame')
        self.mid_frame.pack(side=LEFT,fill=BOTH,padx=10)

        self.right_frame = ttk.Frame(self.innerFrame,relief=FLAT,style='InnerFrame.TFrame')
        self.right_frame.pack(side=RIGHT,fill=BOTH, padx=10)

        self.filename = ''
        self.className = ''

        self.listbox=ListBox(self.right_frame)
        self.listbox.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.browse_btn = ttk.Button(self.mid_frame, text="Choose the image", command=self.select_dir, cursor="hand1",style="b.TButton")
        self.browse_btn.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        img = Image.new('RGBA', (300, 300), (255, 0, 0, 0))
        #resized = img.resize((300, 300), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(img)
        self.myvar = ttk.Label(self.mid_frame, image=tkimage,style="inner.TLabel")
        self.myvar.image = tkimage
        self.myvar.grid(row=1)

        self.dir_var = StringVar()
        self.dirLabel = tk.Message(self.mid_frame, textvariable=self.dir_var, width=400, relief=FLAT, font=mid_Font
                                    ,fg = '#eee', bg = inner_color)

        self.confirm_btn = ttk.Button(self.mid_frame, text="Check The Signature", cursor="hand1", style="b.TButton",
                                 command=lambda :self.check_signature())

    def select_dir(self):

        self.file=filedialog.askopenfilename()

        self.myvar.grid_remove()

        self.dir_var.set(self.file)
        self.dirLabel.grid(row=2, pady=5, padx=5, sticky=W)

        self.img = Image.open(self.file)
        resized = self.img.resize((300, 300), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        self.myvar = tk.Label(self.mid_frame, image=tkimage,width=300,height=300)
        self.myvar.image = tkimage
        self.myvar.grid(row=3)

        self.confirm_btn.grid(row=4, pady=30)

    def check_signature(self):

        check = TestSignature(self.file)
        predictions, top_k, labels = check.run_inference_on_image()

        # Clearing inner Frame
        for child in self.innerFrame.winfo_children():
            child.forget()

        self.confirm_btn.destroy()
        self.myvar.destroy()
        self.listbox.destroy()
        self.innerFrame.forget()

        #Addind new child widgets
        self.resultFrame.pack()
        self.result_label=tk.Label(self.resultFrame,text="Test Result",relief=GROOVE,font=LARGE_FONT, fg=textFont,
                           bg=textbgColor, highlightbackground=textbdColor,highlightcolor=divSquareColor_hover, highlightthickness=1)

        self.result_label.pack(pady=20, padx=10,ipady=5,ipadx=5)

        self.tree = ttk.Treeview(self.resultFrame, columns=('Match score'))
        self.tree.heading('#0', text='Signature Holder')
        self.tree.heading('#1', text='Match score')
        self.tree.heading('#2', text='Remarks')

        id=0
        for node_id in top_k:
            human_string = labels[node_id]

            score = predictions[node_id]

            self.tree.insert("",id, text=human_string.title(), values=(score,"{0:.2f}% matched".format(score*100)))
            id+=1
            self.tree.pack()

    def reset(self):
        for child in self.resultFrame.winfo_children():
            child.destroy()
        self.resultFrame.forget()

        # self.result_label.destroy()
        # self.tree.destroy()

        self.myvar.destroy()
        self.listbox.destroy()
        self.confirm_btn.destroy()
        # Recreate childs
        self.innerFrame.pack()
        self.Info.pack(pady=10, padx=10)
        self.mid_frame.pack(side=LEFT, fill=BOTH, padx=10)
        self.right_frame.pack(side=RIGHT, fill=BOTH, padx=10)
        self.listbox = ListBox(self.right_frame)
        self.listbox.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.browse_btn.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        img = Image.new('RGBA', (300, 300), (255, 0, 0, 0))

        tkimage = ImageTk.PhotoImage(img)
        self.myvar = ttk.Label(self.mid_frame, image=tkimage, style="inner.TLabel")
        self.myvar.image = tkimage
        self.myvar.grid(row=1)

        self.confirm_btn = ttk.Button(self.mid_frame, text="Check The Signature", cursor="hand1", style="b.TButton",
                                      command=lambda: self.check_signature())

        self.dir_var.set('')

        self.filename = ''
        self.className = ''


class ResultPage(ttk.Frame):

    def __init__(self,parent,controller):
        self.controller=controller

        ttk.Frame.__init__(self,parent,style='OuterFrame.TFrame')

        goHomebtn = ttk.Button(self, text="Back to home",command=lambda: [self.tb.stop(), controller.show_frame(StartPage)],
                                style = "b.TButton", cursor="hand1")
        goHomebtn.pack(side=LEFT,anchor=N,padx=5,pady=5)

        innerFrame = ttk.Frame(self, width=820, relief=GROOVE,style="InnerFrame.TFrame")
        innerFrame.pack()

        label1 = tk.Label(innerFrame, text="Check Results\n\nFor detail Analysis check TensorBoard.To Open TensorBoard Click this link:",
                          font=LARGE_FONT, fg=textFont, bg=textbgColor,relief=GROOVE, highlightbackground=textbdColor,
                          highlightcolor=divSquareColor_hover,highlightthickness=1)
        label1.pack(pady=10, padx=10)

        optionFrame = ttk.Frame(innerFrame, relief=FLAT, style="InnerFrame.TFrame")
        optionFrame.pack(pady=10)

        accuracy=ttk.Button(optionFrame,text="Accuracy",style="b.TButton",cursor="hand1",command=lambda :self.show_output_frame(AccuracyFrame))
        accuracy.pack(pady=10,padx=25,side=LEFT)

        cross =ttk.Button(optionFrame,text="Cross Entropy",style="b.TButton",cursor="hand1",command=lambda:self.show_output_frame(CrossFrame))
        cross.pack(pady=10, padx=10,side=LEFT)

        final =ttk.Button(optionFrame,text="Final train_ops",style="b.TButton",cursor="hand1",command=lambda: self.show_output_frame(FinalOutputsFrame))
        final.pack(pady=10, padx=10,side=LEFT)

        tensorboardbtn = ttk.Button(optionFrame, text="Check TensorBoard", cursor="hand1",style="b.TButton",command=link_tensorboard)
        tensorboardbtn.pack(pady=10, padx=10,side=LEFT)

        outputFrame=tk.Frame(innerFrame)
        outputFrame.pack()

        self.frames = {}

        for F in (AccuracyFrame,CrossFrame,FinalOutputsFrame):
            frame = F(outputFrame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_output_frame(AccuracyFrame)


    def show_output_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

    def initiate(self):
        self.tb = TensorBoard()
        self.tb.start()
        return self.tb


class DisplayTraining(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller

        ttk.Frame.__init__(self,parent,style='OuterFrame.TFrame')

        goHomebtn = ttk.Button(self, text="Back to home", style="b.TButton",
                               command=lambda: [self.clear(),self.show(),controller.show_frame(StartPage)], cursor="hand1")
        goHomebtn.pack(side=LEFT, anchor=N, padx=5, pady=5)

        innerFrame = ttk.Frame(self, width=820, relief=GROOVE, style="InnerFrame.TFrame")
        innerFrame.pack()

        label1 = tk.Label(innerFrame,
                          text="Train The Model\n\n"
                "Training is done on recently uploaded data.Click train button to initiate Training process.\n"
                "This may take some time depending upon training data and your CPU.",
                          font=LARGE_FONT, fg=textFont, bg=textbgColor,
                          relief=GROOVE, highlightbackground=textbdColor, highlightcolor=divSquareColor_hover
                          , highlightthickness=1)
        label1.pack(pady=20, padx=10)


        upperFrame=ttk.Frame(self,style="InnerFrame.TFrame")
        upperFrame.pack(pady=10)

        var = StringVar()
        self.Info = tk.Message(innerFrame,width=850, textvariable=var,font=LARGE_FONT, fg='#eee', bg=outer_color)
        var.set("Observe progress in console below.\nDo not quit or click 'Back to home' until the training process completes.\n"
               "Quiting or tampering during training may results errors and corruption.")
        #self.Info.pack(pady=20, padx=10)

        self.initiate = ttk.Button(self,text="Initiate Training", command=lambda :[self.hide(),self.start()]
                              ,cursor="hand1",style="b.TButton",)
        self.initiate.pack(pady=20,ipadx=50,ipady=10)

        self.output = tk.Text(self, background = '#4e342e', fg='#fff')
        self.output.pack(ipadx=100,ipady=50)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command = self.output.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.output['yscrollcommand'] = self.scrollbar.set
        self.pack()

    def hide(self):
        self.initiate.pack_forget()
        self.Info.pack(pady=20,padx=10)

    def show(self):
        self.initiate.pack(pady=20,ipadx=50,ipady=10)
        self.Info.pack_forget()

    def start(self):
        p = Path(__file__).parents[2]
        # print(p)
        path = os.path.join(p, 'SignatureRecognition/image_retraining/retrain.py')
        proc = subprocess.Popen(['python', path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in proc.stdout:
            #print(line.decode("utf8").strip())
            self.write(line.decode("utf8"))

        for err in proc.stderr:
            self.write(err.decode("utf8"))

    def write(self, txt):
        self.output.insert(tk.END,str(txt))
        self.output.see(tk.END)
        self.update_idletasks()

    def clear(self):
        self.output.delete('1.0',END)