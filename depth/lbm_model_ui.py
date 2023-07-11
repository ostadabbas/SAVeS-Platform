import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
import os

class lbm_model_ui:
    def __init__(self):
        self.img_ct = 0

    def get_img_str(self):
        return "{} images(s)".format(str(self.img_ct))

    def update_img_count(self,pth):
        if os.path.isdir(pth):
            counter = 0
            img_list = os.listdir(pth)
            for img in img_list:
                if img[-4:] == ".png":
                    counter += 1
            self.img_ct = counter
        else:
            self.img_ct = 0

    def browse_folder_and_count_img(self,show_widget,count_widget,start_dir=r"."):
        filepath = browse_folder(show_widget,start_dir)
        self.update_img_count(filepath)
        count_widget.configure(text=self.get_img_str())

    def show_env_result(self,res_dict):
        cmd_window = tk.Toplevel()
        cmd_window.wm_title("Check Result")
        widgets = []
        for cont,val in res_dict.items():
            widgets.append(Label(cmd_window,text=cont))
            widgets[-1].pack(side=LEFT)
            widgets.append(checkmark(cmd_window,val))
            widgets[-1].pack(side=LEFT)

    def load_pretrain(self,show_widget,ext):
        # this function works for single weight file (pth) only
        # for DPT, its pt file and for AdaBins its pth
        file_path = browse_file(show_widget,"PyTorch weight file",ext)
        self.single_pretrain = file_path

