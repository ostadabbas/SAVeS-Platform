import tkinter as tk
from tkinter import *
from tkinter import ttk

from analysis.depth_ana_ui import depth_ana_ui
from analysis.geo_analysis_ui import geo_ana_frame

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
        self.odo_link = Button(self.tab_loam,text="Open Geomeric Algorithm Analysis in a New Window ⇱",command=lambda:self.open_geo_ana())
        self.odo_link.pack(side=TOP)

    def open_geo_ana(self):
        self.destroy()
        self.odometry = geo_ana_frame()
        self.odometry.mainloop()


if __name__ == '__main__':
    analysis_frame().mainloop()