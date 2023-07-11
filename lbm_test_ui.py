import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
import time

from depth.geonet_ui import geonet_test_ui
from depth.adabins_ui import adabins_ui
from depth.dpt_ui import dpt_ui

class lbm_test_frame(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Learning-based Models")
       
        self.tabsystem = ttk.Notebook(self)
        self.tab_geo = Frame(self.tabsystem)
        self.tab_ada = Frame(self.tabsystem)
        self.tab_dpt = Frame(self.tabsystem)

        self.geo = geonet_test_ui(self.tab_geo)
        self.ada = adabins_ui(self.tab_ada)
        self.dpt = dpt_ui(self.tab_dpt)

        # self.tabsystem.add(self.tab_geo, text='GeoNet')
        self.tabsystem.add(self.tab_ada, text='AdaBins')
        self.tabsystem.add(self.tab_dpt, text='DPT')
        self.tabsystem.pack(expand=1, fill="both")


if __name__ == '__main__':
    lbm_test_frame().mainloop()