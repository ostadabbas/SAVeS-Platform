import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
import time
from util import *
import os
import json

from extract_from_bag import bag_transform
from analysis.geo_analysis import geo_ana
import numpy as np
import copy

class args_pl():
    def __init__(self,bag_file,model,datasets,output_location):
        self.bag_file = bag_file
        self.model = model
        self.datasets = datasets
        self.output_location = output_location

class geo_ana_frame(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Geometric Analysis")

        # GLOBAL VARIABLES
        self.bt = bag_transform()

        # BAG EXTRACTION
        self.extract_sep = ttk.Labelframe(self, text='Extract Trajectory from bag')
        self.extract_sep.grid(row=0,column=0,sticky='ew')
        sel_bag_label = Label(self.extract_sep,text="Please select bag file location:")
        sel_bag_label.grid(row=1,column=0,columnspan=3)
        self.bag_txt = Entry(self.extract_sep)
        self.bag_txt.grid(row=2,column=0,columnspan=2,sticky='ew')
        bag_btn = Button(self.extract_sep,text="Browse...",command=lambda:browse_file(self.bag_txt,"ROS Bag file","bag"))
        bag_btn.grid(row=2,column=2)
        out_loc_label = Label(self.extract_sep, text="Select output file location:")
        out_loc_label.grid(row=3,column=0,columnspan=3)
        self.out_loc_txt = Entry(self.extract_sep)
        self.out_loc_txt.grid(row=4,column=0,columnspan=2,sticky='ew')
        out_loc_btn = Button(self.extract_sep,text="Browse...",command=lambda:browse_folder(self.out_loc_txt))
        out_loc_btn.grid(row=4,column=2)
        self.out_name_txt = Entry(self.extract_sep)
        # self.out_name_txt.grid(row=5,column=0,columnspan=3,sticky='ew')
        set_entry_txt(self.out_name_txt,"Extraction files name")
        self.extract_combobox = ttk.Combobox(self.extract_sep,state="readonly",\
            values=["A-LOAM","LeGO-LOAM"])
        self.extract_combobox.current(0)
        self.extract_combobox.grid(row=6,column=0,columnspan=1,sticky='ew')
        self.dataset_combobox = ttk.Combobox(self.extract_sep,state="readonly",\
            values=["CARLA","KITTI","nuScenes"])
        self.dataset_combobox.current(0)
        self.dataset_combobox.grid(row=6,column=1,columnspan=1,sticky='ew')
        extraction_start_btn = Button(self.extract_sep,text="Start",command=lambda:self.start_extract())
        extraction_start_btn.grid(row=6,column=2)

        # Traj analysis
        self.ana_sep = ttk.Labelframe(self, text='Analysis Trajectory')
        self.ana_sep.grid(row=7,column=0,sticky='ew')
        gt_label = Label(self.ana_sep,text="Select ground truth trajectory file:")
        gt_label.grid(row=8,column=0,columnspan=3)
        self.gt_txt = Entry(self.ana_sep)
        self.gt_txt.grid(row=9,column=0,columnspan=2,sticky='ew')
        gt_btn = Button(self.ana_sep,text="Browse...",command=lambda:browse_file(self.gt_txt,"Trajectory KITTI format txt file","txt"))
        gt_btn.grid(row=9,column=2)
        pred_label = Label(self.ana_sep,text="Select calculated trajectory file:")
        pred_label.grid(row=10,column=0,columnspan=3)
        self.pred_txt = Entry(self.ana_sep)
        self.pred_txt.grid(row=11,column=0,columnspan=2,sticky='ew')
        pred_btn = Button(self.ana_sep,text="Browse...",command=lambda:browse_file(self.pred_txt,"Trajectory KITTI format txt file","txt"))
        pred_btn.grid(row=11,column=2)
        self.metrics_sep = ttk.Labelframe(self.ana_sep, text='Metrics')
        self.metrics_sep.grid(row=12,column=0)
        self.is_ape = BooleanVar()
        self.check_ape = Checkbutton(self.metrics_sep, text='APE',variable=self.is_ape)
        self.check_ape.grid(row=13,column=0,sticky='w')
        self.is_rpe = BooleanVar()
        self.check_rpe = Checkbutton(self.metrics_sep, text='RPE',variable=self.is_rpe)
        self.check_rpe.grid(row=14,column=0,sticky='w')
        self.options_sep = ttk.Labelframe(self.ana_sep, text='Options')
        self.options_sep.grid(row=12,column=1)
        self.adj_sep = ttk.Labelframe(self.ana_sep, text='Manual Adjust (w/ Align Origin)')
        self.adj_sep.grid(row=15,column=0,columnspan=2)
        x_to_label = Label(self.adj_sep,text="x ➡️ ")
        x_to_label.grid(row=16,column=0)
        self.x_dest = Entry(self.adj_sep)
        self.x_dest.grid(row=16,column=1)
        y_to_label = Label(self.adj_sep,text="y ➡️ ")
        y_to_label.grid(row=17,column=0)
        self.y_dest = Entry(self.adj_sep)
        self.y_dest.grid(row=17,column=1)
        z_to_label = Label(self.adj_sep,text="z ➡️ ")
        z_to_label.grid(row=18,column=0)
        self.z_dest = Entry(self.adj_sep)
        self.z_dest.grid(row=18,column=1)

        self.is_align = BooleanVar()
        self.check_align = Checkbutton(self.options_sep, text='Automatic Align (first 10 poses)',variable=self.is_align,command=self.show_manual_align)
        self.check_align.grid(row=13,column=1,sticky='w')
        self.is_plot = BooleanVar()
        self.check_plot = Checkbutton(self.options_sep, text='Plot Trajectory',variable=self.is_plot)
        self.check_plot.grid(row=14,column=1,sticky='w')
        self.do_ts_align = BooleanVar()
        self.check_ts = Checkbutton(self.options_sep,text='Align No. of Poses',\
                                    variable=self.do_ts_align,command=lambda:self.show_ts_selection_window())
        self.check_ts.grid(row=13,column=2,sticky="w")
        check_start_btn = Button(self.ana_sep,text="Start",command=lambda:self.start_analysis())
        check_start_btn.grid(row=15,column=2)

        self.gt_ts_file = ""
        self.pred_ts_file = ""

    def start_extract(self):
        model = self.extract_combobox.get()
        bag_file = self.bag_txt.get()
        if not os.path.exists(bag_file):
            tkinter.messagebox.showinfo('Error','Bag file not correctly selected!')
            return
        datasets = self.dataset_combobox.get()
        output_location = self.out_loc_txt.get()
        if not os.path.isdir(output_location):
            tkinter.messagebox.showinfo('Error','Not valid path!')
            return
        args = args_pl(bag_file,model,datasets,output_location)
        try:
            if model == "A-LOAM":
                self.bt.extract_from_aloam_bag(args)
                tkinter.messagebox.showinfo('Completed','Extraction process has sucessfully returned.')
                # tkinter.messagebox.showinfo('Error','Bag file does not match with model.')
            elif model == "LeGO-LOAM":
                self.bt.extract_from_lego_bag(args)
                tkinter.messagebox.showinfo('Completed','Extraction process has sucessfully returned.')
        except:
            tkinter.messagebox.showinfo('Error','Bag file does not match with model.')

    def start_analysis(self):
        gt_file = self.gt_txt.get()
        pred_file = self.pred_txt.get()
        if not os.path.exists(gt_file):
            tkinter.messagebox.showinfo('Error','Not valid ground truth path!')
            return
        if not os.path.exists(pred_file):
            tkinter.messagebox.showinfo('Error','Not valid prediction path!')
            return
        if self.is_align.get() == True:
            temp_pred_file = self.adjust_xyz(pred_file)
        else:
            temp_pred_file = pred_file
        if self.do_ts_align.get() == True:
            res = geo_ana(gt_file,temp_pred_file,self.is_rpe.get(),self.is_ape.get(),self.is_align.get(),self.is_plot.get(),True,self.gt_ts_file,self.pred_ts_file)
        else:
            res = geo_ana(gt_file,temp_pred_file,self.is_rpe.get(),self.is_ape.get(),self.is_align.get(),self.is_plot.get(),False)
        if res[0] == False:
            tkinter.messagebox.showinfo('Error',res[1])
            return
        else:
            res = res[1]
        # disp = json.dumps(res)
        disp = ""
        for key, val in res.items():
            disp += "{}: {}\n".format(key,val)
        cmd_window = tk.Toplevel()
        cmd_window.wm_title("Analysis Result")
        t = Text(cmd_window)
        t.insert(tk.END, disp)
        t.grid(row=0,column=0)
    
    def adjust_xyz(self,pred_file):
        the_dict = {"x":3,"y":7,"z":11}
        new_rule= []
        file_data = np.loadtxt(pred_file,dtype=float)
        if len(self.x_dest.get()) == 0:
            new_rule.append(3)
        else:
            new_rule.append(the_dict[self.x_dest.get()[-1]])
        if len(self.y_dest.get()) == 0:
            new_rule.append(7)
        else:
            new_rule.append(the_dict[self.y_dest.get()[-1]])
        if len(self.z_dest.get()) == 0:
            new_rule.append(11)
        else:
            new_rule.append(the_dict[self.z_dest.get()[-1]])

        new_x = copy.deepcopy(file_data[:,new_rule[0]])
        if not len(self.x_dest.get()) == 0:
            if self.x_dest.get()[0] == "-":
                new_x = -new_x
        new_y = copy.deepcopy(file_data[:,new_rule[1]])
        if not len(self.y_dest.get()) == 0:
            if self.y_dest.get()[0] == "-":
                new_y = -new_y
        new_z = copy.deepcopy(file_data[:,new_rule[2]])
        if not len(self.z_dest.get()) == 0:
            if self.z_dest.get()[0] == "-":
                new_z = -new_z
        file_data[:,3] = new_x
        file_data[:,7] = new_y
        file_data[:,11] = new_z
        temp_pred_file_dir = os.path.join(".","extracted")
        if not os.path.exists(temp_pred_file_dir):
            os.makedirs(temp_pred_file_dir)
        temp_pred_file = os.path.join(temp_pred_file_dir,"alt_pred.txt")
        np.savetxt(temp_pred_file,file_data,delimiter=" ",newline="\n")
        return temp_pred_file
    
    def show_manual_align(self):
        if self.is_align.get() == True:
            self.adj_sep.grid_forget()
        else:
            self.adj_sep.grid(row=15,column=0,columnspan=2)

    def show_ts_selection_window(self):
        if self.do_ts_align.get() == True:
            top = tk.Toplevel()
            top.wm_title("Timestamp File Selection")
            gt_ts_label = Label(top,text="Select ground truth timestamp file:")
            gt_ts_label.grid(row=0,column=0)
            gt_ts_txt = Entry(top)
            gt_ts_txt.grid(row=1,column=0,sticky="ew")
            gt_ts_btn = Button(top,text="Browse...",command=lambda:self.browse_ts(True,gt_ts_txt))
            gt_ts_btn.grid(row=1,column=1)

            pred_ts_label = Label(top,text="Select prediction timestamp file:")
            pred_ts_label.grid(row=2,column=0)
            pred_ts_txt = Entry(top)
            pred_ts_txt.grid(row=3,column=0,sticky="ew")
            pred_ts_btn = Button(top,text="Browse...",command=lambda:self.browse_ts(False,pred_ts_txt))
            pred_ts_btn.grid(row=3,column=1)
    
    def browse_ts(self,is_gt,show_widget):
        if is_gt:
            self.gt_ts_file = browse_file(show_widget,"Timestamp File","txt")
        else:
            self.pred_ts_file = browse_file(show_widget,"Timestamp File","txt")

if __name__ == '__main__':
    geo_ana_frame().mainloop()