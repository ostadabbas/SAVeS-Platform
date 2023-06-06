import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
import time

from depth_ana_ui import depth_ana_ui

class analysis_frame(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Analysis Control")
       
        self.tabsystem = ttk.Notebook(self)
        self.tab_loam = Frame(self.tabsystem)
        self.tab_depth = Frame(self.tabsystem)

        self.depth = depth_ana_ui(self.tab_depth)


        self.tabsystem.add(self.tab_loam, text='Odometry')
        self.tabsystem.add(self.tab_depth, text='Depth')
        self.tabsystem.pack(expand=1, fill="both")


if __name__ == '__main__':
    analysis_frame().mainloop()