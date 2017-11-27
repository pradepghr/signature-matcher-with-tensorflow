import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from SignatureRecognition.image_retraining.Graphs import Graphs

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

LARGE_FONT = ("Albertus Extra Bold", 16)
mid_Font = ("Albertus Extra Bold", 12)
NORM_FONT = ("Albertus Extra Bold", 16, "underline")
SMALL_FONT = ("Arial", 8)
bgColor = "#000000"
fgColor = "#d7ccc8"
Color2 = '#212121'
btnColor = "#9e9e9e"


# Output frame--for accuracy
class AccuracyFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=bgColor)

        graph = Graphs()
        figure = graph.graph_of_accuracy()

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# Output frame-- for cross entropy
class CrossFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=bgColor)

        graph = Graphs()
        figure = graph.graph_of_cross_entropy()

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# Output frame--for final_ops
class FinalOutputsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=bgColor)

        graph = Graphs()
        figure = graph.graph_of_final_outputs()

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
