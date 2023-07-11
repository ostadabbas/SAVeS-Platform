import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
import time

from geometric.aloam_driver import aloam_driver
from geometric.legoloam_driver import legoloam_driver
from geometric.orb_driver import orb_driver

class geo_main_frame(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Geometric Result Generation")
        self.tabsystem = ttk.Notebook(self)
        self.tab_aloam = Frame(self.tabsystem)
        self.tab_legoloam = Frame(self.tabsystem)
        self.tab_orbslam = Frame(self.tabsystem)

        # GLOBAL VARS
        self.out_path = "."
        self.out_name = "SAVeS_out_" + str(time.time())
        self.al_drv = None
        self.ros_drv = None
        self.yaml_loc = None
        self.orb_filepath = None
        self.orb_data_pth = None
        self.orb_time_loc = None
        self.orb_drv = None
        self.orb_model_ready = False
        self.orb_data_ready = False

        # -------------- A-LOAM --------------------
        self.abag_txt = Entry(self.tab_aloam)
        self.abag_txt.grid(row=1,column=1)
        self.abag_label = Label(self.tab_aloam,text="Please select bag file location:")
        self.abag_label.grid(row=1,column=0)
        self.abag_btn = Button(self.tab_aloam,text="Browse...",command=lambda:self.select_bag_dia("combined",self.abag_txt))
        self.abag_btn.grid(row=1,column=2)

        self.aoutput_txt = Entry(self.tab_aloam)
        self.aoutput_txt.grid(row=3,column=1)
        self.aout_label = Label(self.tab_aloam,text="Select output destination:")
        self.aout_label.grid(row=3,column=0)
        self.aout_selection_btn = Button(self.tab_aloam,text="Browse...",command=lambda:self.select_fldr_dia("out",self.aoutput_txt))
        self.aout_selection_btn.grid(row=3,column=2)

        self.aros_path_txt = Entry(self.tab_aloam)
        self.aros_path_txt.grid(row=5,column=0,columnspan=2,sticky='ew')
        self.aros_btn = Button(self.tab_aloam, text="2.Load Model",state=DISABLED,command=lambda:self.select_fldr_dia("aloam",self.aros_path_txt))
        self.aros_btn.grid(row=5,column=2)
        self.aloam_ready_label = Label(self.tab_aloam,text="✕",fg='red')
        self.aloam_ready_label.grid(row=5,column=3)
        self.acheck_ros_btn = Button(self.tab_aloam,text="1.Check ROS",command=lambda:self.check_ros("aloam"),state=DISABLED)
        self.acheck_ros_btn.grid(row=4,column=2)
        self.aros_ready_label = Label(self.tab_aloam,text="✕",fg='red')
        self.aros_ready_label.grid(row=4,column=3)

        self.aselect_launch_label = Label(self.tab_aloam,text="Select launch file:")
        self.aselect_launch_label.grid(row=6,column=0)
        self.alaunch_combobox = ttk.Combobox(self.tab_aloam,state="readonly",\
            values=["aloam_velodyne_VLP_16.launch","aloam_velodyne_HDL_32.launch","aloam_velodyne_HDL_64.launch"])
        self.alaunch_combobox.current(0)
        self.alaunch_combobox.grid(row=6,column=1,columnspan=2,sticky='ew')

        self.astart_test_btn = Button(self.tab_aloam,text="Start test",command=lambda:self.start_test(self.aloam_pop_start),state=DISABLED)
        self.astart_test_btn.grid(row=7,column=0,columnspan=3,sticky='ew')

        # -------------- LeGO-LOAM -----------------
        self.is_one_bag = BooleanVar()  
        is_one_bag_btn = Checkbutton(self.tab_legoloam, text="Topics are in seperate bag",
                      variable=self.is_one_bag,onvalue=True,offvalue=False,
                      command=self.show_lidar_imu_location_selection)
        is_one_bag_btn.grid(row=0,column=0)
        self.bag_txt = Entry(self.tab_legoloam)
        self.bag_txt.grid(row=1,column=1)
        self.bag_label = Label(self.tab_legoloam,text="Please select bag file location:")
        self.bag_label.grid(row=1,column=0)
        self.bag_btn = Button(self.tab_legoloam,text="Browse...",command=lambda:self.select_bag_dia("combined",self.bag_txt))
        self.bag_btn.grid(row=1,column=2)

        self.output_txt = Entry(self.tab_legoloam)
        self.output_txt.grid(row=3,column=1)
        self.out_label = Label(self.tab_legoloam,text="Select output destination:")
        self.out_label.grid(row=3,column=0)
        self.out_selection_btn = Button(self.tab_legoloam,text="Browse...",command=lambda:self.select_fldr_dia("out",self.output_txt))
        self.out_selection_btn.grid(row=3,column=2)

        self.ros_path_txt = Entry(self.tab_legoloam)
        self.ros_path_txt.grid(row=5,column=0,columnspan=2,sticky='ew')
        self.ros_btn = Button(self.tab_legoloam, text="2.Load Model",state=DISABLED,command=lambda:self.select_fldr_dia("legoloam",self.ros_path_txt))
        self.ros_btn.grid(row=5,column=2)
        self.loam_ready_label = Label(self.tab_legoloam,text="✕",fg='red')
        self.loam_ready_label.grid(row=5,column=3)
        self.check_ros_btn = Button(self.tab_legoloam,text="1.Check ROS",command=lambda:self.check_ros("lego"),state=DISABLED)
        self.check_ros_btn.grid(row=4,column=2)
        self.ros_ready_label = Label(self.tab_legoloam,text="✕",fg='red')
        self.ros_ready_label.grid(row=4,column=3)

        self.start_test_btn = Button(self.tab_legoloam,text="Start test",command=lambda:self.start_test(self.get_name),state=DISABLED)
        self.start_test_btn.grid(row=6,column=0,columnspan=3,sticky='ew')

        # -------------- ORBSLAM3 -----------------
        self.orb_instr_label = Label(self.tab_orbslam,text="ORBSLAM3 installation location")
        self.orb_instr_label.grid(row=0,column=0)
        self.orb_path_txt = Entry(self.tab_orbslam)
        self.orb_path_txt.grid(row=0,column=1)
        self.orb_sel_btn = Button(self.tab_orbslam,text="Browse...",command=lambda:self.select_fldr_dia("orb-loc",self.orb_path_txt))
        self.orb_sel_btn.grid(row=0,column=2)

        self.orb_yaml_label = Label(self.tab_orbslam,text="YAML descriptor location")
        self.orb_yaml_label.grid(row=1,column=0)
        self.orb_yaml_txt = Entry(self.tab_orbslam)
        self.orb_yaml_txt.grid(row=1,column=1)
        self.orb_yaml_btn = Button(self.tab_orbslam,text="Browse...",\
            command=lambda:self.select_file("Select .yaml file","yaml","orb-yaml"))
        self.orb_yaml_btn.grid(row=1,column=2)

        self.orb_check_btn = Button(self.tab_orbslam,text="Check ORBSLAM3",command=lambda:self.check_orb())
        self.orb_check_btn.grid(row=2,column=2)
        self.orb_ready_label = Label(self.tab_orbslam,text="✕",fg='red')
        self.orb_ready_label.grid(row=2,column=3)

        self.orb_data_label = Label(self.tab_orbslam,text="Dataset Location")
        self.orb_data_label.grid(row=3,column=0)
        self.orb_data_txt = Entry(self.tab_orbslam)
        self.orb_data_txt.grid(row=3,column=1)
        self.orb_data_btn = Button(self.tab_orbslam,text="Browse...",command=lambda:self.select_fldr_dia("orb-dt-loc",self.orb_data_txt))
        self.orb_data_btn.grid(row=3,column=2)
        
        self.orb_time_label = Label(self.tab_orbslam,text="Timestamps file Location")
        self.orb_time_label.grid(row=4,column=0)
        self.orb_time_txt = Entry(self.tab_orbslam)
        self.orb_time_txt.grid(row=4,column=1)
        self.orb_time_btn = Button(self.tab_orbslam,text="Browse...",\
        command=lambda:self.select_file("Select timestamp file","txt","orb-time"))
        self.orb_time_btn.grid(row=4,column=2)
        self.orb_ready_btn = Button(self.tab_orbslam,text="Check Dataset",command=lambda:self.check_orb_dataset())
        self.orb_ready_btn.grid(row=5,column=2)
        self.orb_test_label = Label(self.tab_orbslam,text="✕",fg='red')
        self.orb_test_label.grid(row=5,column=3)

        self.orb_start_btn = Button(self.tab_orbslam,text="Start Test",command=lambda:self.start_orb())
        self.orb_start_btn.grid(row=6,column=0,columnspan=2,sticky='ew')
        # self.orb_save_btn = Button(self.tab_orbslam,text="Save Results")
        # self.orb_save_btn.grid(row=6,column=2,columnspan=2,sticky='ew')

        self.tabsystem.add(self.tab_aloam, text='A-LOAM')
        self.tabsystem.add(self.tab_legoloam, text='LeGO-LOAM')
        self.tabsystem.add(self.tab_orbslam, text='ORB-SLAM3')
        self.tabsystem.pack(expand=1, fill="both")

    def show_lidar_imu_location_selection(self):
        if self.is_one_bag.get() == True:
            self.bag_txt.grid_forget()
            self.bag_label.grid_forget()
            self.bag_btn.grid_forget()
            self.imu_txt = Entry(self.tab_legoloam)
            self.imu_txt.grid(row=1,column=1)
            self.imu_label = Label(self.tab_legoloam, text="Select IMU bag file:")
            self.imu_label.grid(row=1,column=0)
            self.imu_btn = Button(self.tab_legoloam, text="Browse...",command=lambda:self.select_bag_dia("imu",self.imu_txt))
            self.imu_btn.grid(row=1,column=2)
            self.lidar_txt = Entry(self.tab_legoloam)
            self.lidar_txt.grid(row=2,column=1)
            self.lidar_label = Label(self.tab_legoloam, text="Select LiDAR bag file:")
            self.lidar_label.grid(row=2,column=0)
            self.lidar_btn = Button(self.tab_legoloam, text="Browse...",command=lambda:self.select_bag_dia("lidar",self.lidar_txt))
            self.lidar_btn.grid(row=2,column=2)
        else:
            self.imu_txt.grid_forget()
            self.imu_label.grid_forget()
            self.imu_btn.grid_forget()
            self.lidar_label.grid_forget()
            self.lidar_txt.grid_forget()
            self.lidar_btn.grid_forget()
            self.bag_txt.grid(row=1,column=1)
            self.bag_label.grid(row=1,column=0)
            self.bag_btn.grid(row=1,column=2)

    def select_bag_dia(self,do_type,show_widget):
        filetypes = (('ROS Bag Files', '*.bag'),)
        filename = fd.askopenfilename(title='Select Bag file',initialdir='~/Downloads',filetypes=filetypes)
        show_widget.delete(0,END)
        show_widget.insert(0,filename)
        if do_type == "combined":
            self.bag_file = filename
        elif do_type == "imu":
            self.imu_bag = filename
        elif do_type == "lidar":
            self.lidar_bag = filename
        self.check_ros_btn.configure(state=NORMAL)
        self.acheck_ros_btn.configure(state=NORMAL)

    def select_file(self,type_desc,ext,do_type):
        filetypes = ((type_desc, "*.{}".format(ext)),)
        filename = fd.askopenfilename(title=type_desc,initialdir='~/Downloads',filetypes=filetypes)
        if do_type == "orb-yaml":
            self.yaml_loc = filename
            self.orb_yaml_txt.delete(0,END)
            self.orb_yaml_txt.insert(0,filename)
        if do_type == "orb-time":
            self.orb_time_loc = filename
            self.orb_time_txt.delete(0,END)
            self.orb_time_txt.insert(0,filename)

    def select_fldr_dia(self,do_type,show_widget):
        filepath=fd.askdirectory(initialdir=r".",title="Select Folder")
        if type(filepath) is tuple:
            if len(filepath) == 0:
                filepath = "."
            else:
                filepath = filepath[0]
        show_widget.delete(0,END)
        show_widget.insert(0,filepath)
        if do_type == "out":
            self.out_path = filepath
        elif do_type == "legoloam":
            self.loam_path = filepath
            self.loam_ready_label.configure(text="✕",fg='red')
            res = False
            print(self.ros_drv.check_launch(self.loam_path),self.loam_path)
            if self.ros_drv is not None:
                if self.ros_drv.check_launch(self.loam_path):
                    self.loam_ready_label.configure(text="✓",fg='green')
                    res = True
            self.test_ready = (self.is_ready and res)
            if self.test_ready:
                self.start_test_btn.configure(state=NORMAL)
        elif do_type == "aloam":
            self.aloam_path = filepath
            self.aloam_ready_label.configure(text="✕",fg='red')
            res = False
            print(self.al_drv.check_launch(self.aloam_path),self.aloam_path)
            if self.al_drv is not None:
                if self.al_drv.check_launch(self.aloam_path):
                    self.aloam_ready_label.configure(text="✓",fg='green')
                    res = True
            self.atest_ready = (self.is_aloam_ready and res)
            if self.atest_ready:
                self.astart_test_btn.configure(state=NORMAL)
        elif do_type == "orb-loc":
            # orb_filepath = fd.askdirectory(initialdir=r".",title="Select Folder")
            self.orb_filepath = filepath
        elif do_type == "orb-dt-loc":
            self.orb_data_pth = filepath
        elif do_type == "orb-out-loc":
            pass
            
    def check_ros(self,alg):
        if alg == "lego":
            is_ready = True
            if self.is_one_bag.get() == True: # actually 2 bag
                self.ros_drv = legoloam_driver(False,[self.imu_bag, self.lidar_bag],self.out_path)
            else:
                print(self.bag_file) 
                self.ros_drv = legoloam_driver(True,[self.bag_file],self.out_path)
            # print(self.ros_drv.is_valid)
            if not self.ros_drv.check_ros_install():
                tkinter.messagebox.showinfo('Error','ROS Melodic installation not detected')
                is_ready = False
            if not self.ros_drv.is_valid:
                tkinter.messagebox.showinfo('Error','Specified path is not valid')
                is_ready = False
            if is_ready:
                self.is_ready = is_ready
                self.ros_btn.configure(state=NORMAL)
                self.ros_ready_label.configure(text="✓",fg='green')
        elif alg == "aloam":
            is_aloam_ready = True
            self.al_drv = aloam_driver(True,[self.bag_file],self.out_path)
            if not self.al_drv.check_ros_install():
                tkinter.messagebox.showinfo('Error','ROS Melodic installation not detected')
                is_aloam_ready = False
            if not self.al_drv.is_valid:
                tkinter.messagebox.showinfo('Error','Specified path is not valid')
                is_aloam_ready = False
            if is_aloam_ready:
                self.is_aloam_ready = True
                self.aros_btn.configure(state=NORMAL)
                self.aros_ready_label.configure(text="✓",fg='green')

    def check_orb(self):
        if (self.orb_filepath) is None or (self.yaml_loc is None):
            tkinter.messagebox.showinfo('Error','Either YAML is missing or installation is incomplete')
        else:
            self.orb_drv = orb_driver(self.orb_filepath,self.yaml_loc)
            if not self.orb_drv.model_ready:
                tkinter.messagebox.showinfo('Error','Please Check console log.')
                self.orb_ready_label.configure(text="✕",fg='red')
                self.orb_model_ready = False
            else:
                self.orb_ready_label.configure(text="✓",fg='green')
                self.orb_model_ready = True

    def check_orb_dataset(self):
        if (self.orb_time_loc is None) or (self.orb_data_pth is None):
            tkinter.messagebox.showinfo('Error','Either timestamp file is missing or dataset format is incompatible')
            return
        if self.orb_drv is None:
            tkinter.messagebox.showinfo('Error','You haven\'t specified ORBSLAM3 location')
            return
        res = self.orb_drv.set_dataset(self.orb_data_pth,self.orb_time_loc)
        if res != True:
            tkinter.messagebox.showinfo('Error',res)
            self.orb_test_label.configure(text="✕",fg='red')
            self.orb_data_ready = False
            return
        self.orb_test_label.configure(text="✓",fg='green')
        self.orb_data_ready = True

    def start_test(self,go_func):
        top = tk.Toplevel()
        top.wm_title("Output Name")
        l = Label(top,text="Please type in the output file name:")
        l.grid(row=0,column=0)
        t = Entry(top)
        t.grid(row=1,column=0,columnspan=2,sticky='ew')
        tpn_label = Label(top,text="Please type in lidar topic name:")
        tpn_label.grid(row=2,column=0)
        tp_txt = Entry(top)
        tp_txt.grid(row=3,column=0,columnspan=2,sticky='ew')
        b = Button(top,text="Submit",command=lambda:go_func(t,top,tp_txt))
        b.grid(row=4,column=1)

    def start_orb(self):
        if (self.orb_model_ready and self.orb_data_ready) == False:
            tkinter.messagebox.showinfo('Error','Either dataset or model isn\'t ready!')
            return
        top = tk.Toplevel()
        top.wm_title("Output Name")
        l = Label(top,text="Please type in the output file name:")
        l.grid(row=0,column=0)
        t = Entry(top)
        t.grid(row=1,column=0,columnspan=2,sticky='ew')
        tpn_label = Label(top,text="Please select output location:")
        tpn_label.grid(row=2,column=0)
        tp_txt = Entry(top)
        tp_txt.grid(row=3,column=0,columnspan=2,sticky='ew')
        out_btn = Button(top,text="Browse...",command=lambda:self.select_fldr_dia("orb-out-loc",tp_txt))
        out_btn.grid(row=3,column=1)
        b = Button(top,text="Submit",command=lambda:self.start_orb_proc(top,tp_txt,t))
        b.grid(row=4,column=1)

    def start_orb_proc(self,top_wdnw,out_locx,out_namex):
        out_loc = out_locx.get()
        out_name = out_namex.get()
        if len(out_loc) == 0:
            out_loc = "."
        self.orb_drv.run_orbslam3(out_loc,out_name)
        self.orb_drv.copy_to_dest()
        top_wdnw.destroy()

    def aloam_pop_start(self,entryx,windows,topicx):
        out_name = entryx.get()
        topic_name = topicx.get()
        if len(out_name) != 0:
            self.out_name = out_name
        launch_file = self.alaunch_combobox.get()
        self.al_drv.launch_ros(self.aloam_path,launch_file)
        self.al_drv.collect_result(self.out_name)
        self.play_cmd_popup(self.al_drv,topic_name)
        windows.destroy()

    def get_name(self,entryx,windows,topicx):
        out_name = entryx.get()
        topic_name = topicx.get()
        if len(out_name) != 0:
            self.out_name = out_name
        windows.destroy()
        print(self.out_name)
        self.ros_drv.launch_ros(self.loam_path)
        self.ros_drv.collect_result(self.out_name)
        self.play_cmd_popup(self.ros_drv,topic_name)

    def play_cmd_popup(self,driver,topic_name):
        prompt_msg = driver.play_bag(topic_name) # fill topic name
        cmd_window = tk.Toplevel()
        cmd_window.wm_title("rosbag play")
        play_instr = Label(cmd_window,text="If you didn't see anything on the rviz window, open a new terminal and enter the following command, followed by Enter")
        play_instr.grid(row=0,column=0)
        instr_txt = Text(cmd_window)
        instr_txt.insert(tk.END, prompt_msg)
        instr_txt.grid(row=1,column=0)
        close_instr = Label(cmd_window,text="Click Finish after running the rosbag play command to collect results, then close rviz window")
        close_instr.grid(row=2,column=0)
        close_btn = Button(cmd_window,text="Finish",command=lambda:self.close_collect(cmd_window,driver))
        close_btn.grid(row=3,column=0,columnspan=2,sticky='ew')

    def close_collect(self,parent_wdnw,driver):
        driver.close_collect()
        parent_wdnw.destroy()

def main(): 
    geo_main_frame().mainloop()


if __name__ == '__main__':
    main()