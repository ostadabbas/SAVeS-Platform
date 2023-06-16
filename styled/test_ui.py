import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
import os

class style_test_ui:
    def __init__(self,tab) -> None:
        self.combo_list = []
        pretrained_fldr_label = Label(tab,text="Please Select Pretrained Weights Folder:")
        pretrained_fldr_label.grid(row=0,column=0)
        self.pre_fldr_txt = Entry(tab)
        self.pre_fldr_txt.grid(row=1,column=0,sticky="ew")
        self.pre_fldr_btn = Button(tab,text="Browse...",command=lambda:self.browse_weights(self.pre_fldr_txt))
        self.pre_fldr_btn.grid(row=1,column=1)
        self.model_sel_combo = ttk.Combobox(tab,state="readonly",values=self.combo_list)
        self.model_sel_combo.grid(row=2,column=0,sticky="ew",columnspan=2)

    def browse_weights(self,txt_widget):
        the_path = browse_folder(txt_widget)
        the_list = list(os.listdir(the_path))
        self.combo_list = []
        for entry in the_list:
            if len(entry) <= 5:
                continue
            else:
                if entry[-4:] == "ckpt":
                    self.combo_list.append(entry)
        self.model_sel_combo['value'] = self.combo_list
        if len(self.combo_list) != 0:
            self.model_sel_combo.set(self.combo_list[0])