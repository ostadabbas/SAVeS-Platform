import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
import os
import numpy as np
from PIL import Image,ImageTk
import imageio
import cv2
import math
import threading
import time
import shlex

class depth_ana_ui:
    def __init__(self, tab) -> None:
        super().__init__()
        # check kitti file valid
        if not os.path.exists("./kitti_eval_tools/evaluate_depth"):
            tkinter.messagebox.showinfo('Error','KITTI Evaluation toolchain not detected! Program will not work!')
        self.dest_fldr = None
        self.cut_head = False
        img = Image.open("./images/warn.png")
        self.img = ImageTk.PhotoImage(img)
        npy_loc_label = Label(tab,text="Please select depth prediction file (*.npy):")
        npy_loc_label.grid(row=0,column=0,columnspan=2,sticky='w')
        self.npy_loc_txt = Entry(tab)
        self.npy_loc_txt.grid(row=1,column=0,columnspan=3,sticky='ew')
        npy_loc_btn = Button(tab,text="Browse...",command=lambda:self.validate_ct(True))
        npy_loc_btn.grid(row=1,column=3)

        gt_loc_label = Label(tab,text="Please select folder of ground truth:")
        gt_loc_label.grid(row=2,column=0,columnspan=2,sticky='w')
        self.gt_loc_txt = Entry(tab)
        self.gt_loc_txt.grid(row=3,column=0,columnspan=3,sticky='ew')
        gt_loc_btn = Button(tab,text="Browse...",command=lambda:self.validate_ct(False))
        gt_loc_btn.grid(row=3,column=3)

        self.ct_eql_mark = checkmark(tab,False)
        self.ct_eql_mark.grid(row=4,column=0)
        self.ct_desc_label = Label(tab,text="0 images from prediction file, 0 in ground truth folder")
        self.ct_desc_label.grid(row=4,column=1)

        self.extract_btn = Button(tab,text="Extract",command=lambda:self.extract_img())
        self.extract_btn.grid(row=5,column=0)
        next_label = Label(tab,text=">>>>>>>>>>>>>>>>>>>>>>>")
        next_label.grid(row=5,column=1)
        self.analysis_btn = Button(tab,text="Analysis",command=lambda:self.call_kitti())
        self.analysis_btn.grid(row=5,column=2)
    
    def extract_img(self,extract_loc=None):
        if self.npy_loc_txt.get() == "" or self.gt_loc_txt.get() == "":
            print("empty container")
            return
        top = tk.Toplevel()
        top.wm_title("Halt")
        top.protocol("WM_DELETE_WINDOW", self.on_close)
        wait_img = Label(top,image=self.img)
        wait_img.image = self.img
        wait_img.grid(row=0,column=0)
        wait_label = Label(top, text="Extraction in progress, this window will close itself when done.")
        wait_label.grid(row=1,column=0)
        top.update()
        # do something time consuming but exact time can't be determined
            
        if extract_loc is None:
            self.fldr_name = self.npy_loc_txt.get().split("/")[-1] + "_extract"
            self.fldr_path = os.path.join(".","extracted",self.fldr_name)
            if not os.path.exists(self.fldr_path):
                os.makedirs(self.fldr_path)
            self.dest_fldr = self.fldr_path
        else:
            self.dest_fldr = extract_loc

        self.img_coll = np.load(self.npy_loc_txt.get())
        self.num_img = self.img_coll.shape[0]
        # start assign workload
        thread_ct = 8
        each_thread_ct = math.ceil((self.num_img-10)/thread_ct)
        threads_handle = []
        name_arr = list(os.listdir(self.gt_loc_txt.get()))
        name_arr.sort()
        # with open("img_seq.txt",'r') as f:
        #     name_arr = f.readlines()
        # tkinter.messagebox.showinfo('Attention','This window will close itself when extraction is finished!')
        for th_ct in range(thread_ct):
            if self.cut_head:
                start = 5 + th_ct * each_thread_ct
                end = 5+(th_ct+1)*each_thread_ct
                # for the last thread
                if th_ct == thread_ct-1:
                    if end != self.num_img - 5:
                        end = self.num_img - 5
            else:
                start = th_ct * each_thread_ct
                end = (th_ct+1)*each_thread_ct
                # for the last thread
                if th_ct == thread_ct-1:
                    if end != self.num_img:
                        end = self.num_img
            print(start,end)
            
            threads_handle.append(threading.Thread(target=self.__open_and_cvt,args=(self.gt_loc_txt.get(),start,end,name_arr,)))
            threads_handle[-1].start()

        for th_ct in range(thread_ct):
            threads_handle[th_ct].join()
            
        top.destroy()
    
    # must be called by extract_img
    def __open_and_cvt(self,gt_folder,start,end,name_arr):
        reshape = (1216,352)
        for i in range(start, end):
            if i % 100 == 0:
                print(i)
            gt = np.array(Image.open(gt_folder+"/"+name_arr[i]))
            interm_img = cv2.resize(self.img_coll[i],reshape,interpolation=cv2.INTER_LINEAR)
            new_img = scale_matching(gt,interm_img)
            imageio.imwrite(self.dest_fldr+"/"+name_arr[i], new_img.astype(np.uint16))

    def validate_ct(self,is_npy):
        if is_npy:
            browse_file(self.npy_loc_txt,"Numpy File","npy")
            self.fldr_name = self.npy_loc_txt.get().split("/")[-1] + "_extract"
            self.fldr_path = os.path.join(".","extracted",self.fldr_name)
            self.dest_fldr = self.fldr_path
        else:
            browse_folder(self.gt_loc_txt)
        try:
            pred_arr = np.load(self.npy_loc_txt.get())
            pred_len = pred_arr.shape[0]
        except:
            pred_len = 0
        try:
            gt_dir = self.gt_loc_txt.get()
            gt_len = len(list(os.listdir(gt_dir)))
        except:
            gt_len = 0
        if pred_len != 0 and gt_len != 0:
            if pred_len == gt_len:
                self.cut_head = False
                set_checkmark(self.ct_eql_mark, True)
            elif pred_len == (gt_len + 10):
                set_checkmark(self.ct_eql_mark, True)
                self.cut_head = True
        
        ct_str = "{} images from prediction file, {} in ground truth folder".format(pred_len,gt_len)
        self.ct_desc_label.config(text=ct_str)

    def call_kitti(self):
        pred_pth = self.dest_fldr
        gt_pth = self.gt_loc_txt.get()
        exec_command = "bash -c './kitti_eval_tools/evaluate_depth {} {}'".format(gt_pth,pred_pth)
        exec_command = shlex.split(exec_command)
        
        try:
            top = tk.Toplevel()
            top.wm_title("Halt")
            top.protocol("WM_DELETE_WINDOW", on_close)
            wait_label = Label(top,image=self.img)
            wait_label.image = self.img
            wait_label.grid(row=0,column=0)
            wait_label2 = Label(top,text="Analysis is in progress, this window will close itself when done.")
            wait_label2.grid(row=1,column=0)
            top.update()
            proc = subprocess.check_output(exec_command,stderr=subprocess.STDOUT)
            top.destroy()
            print(proc.decode("utf-8").split('\n')[-12:])
            stats_str = ""
            with open(os.path.join(pred_pth,"stats_depth.txt"),'r') as f:
                stats = f.readlines()
                for idx, items in enumerate(stats):
                    stats_str += items
            results_wd = tk.Toplevel()
            results_wd.wm_title("The results are in!")
            stats_text = tkinter.Text(results_wd)
            stats_text.insert(tkinter.END, stats_str)
            stats_text.grid(row=0,column=0)

        except Exception as e: 
            print(e)
        
        
