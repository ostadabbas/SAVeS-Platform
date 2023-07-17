from geometric.ros_drivers import ROSDrivers
import subprocess
import os
from threading import Thread
import multiprocessing
import time
import shlex

class legoloam_driver(ROSDrivers):
    def launch_ros(self,loam_location):
        '''
        before launch need to make sure you have configured lidar and catkin_make
        '''
        launch_profile = "run.launch"
        self.new_thread = Thread(target=self.ros_thread,args=(loam_location,launch_profile))
        self.new_thread.start()
        self.ros_record_thread = []
        # consider have some output if anything goes wrong, but not for now
        
    def play_bag(self,lidar_topic,imu_topic=None,do_clock=False):
        # do_clock = True # found out for carla you dont need this option, but for kitti you kinda do??
        if do_clock:
            clock_str = "--clock"
        else:
            clock_str = ""
        if self.is_one_bag:
            bag_loc = self.bag_loc
            play_command = "rosbag play {} {} {}:=/velodyne_points".format(bag_loc,clock_str,lidar_topic)
            if imu_topic is not None:
                play_command += " {}:=/imu/data".format(imu_topic)
        else:
            if imu_topic is not None:
                play_command = "rosbag play {} {} {} {}:=/velodyne_points {}:=/imu/data".format(self.imu_loc,self.lidar_loc,clock_str,lidar_topic,imu_topic)
            else:
                play_command = "rosbag play {} {} {}:=/velodyne_points".format(self.lidar_loc,clock_str,lidar_topic)
        # the threading has some issues, will currently return command to execute
        self.play_bag_thread = Thread(target=self.play_thread,args=(play_command,))
        self.play_bag_thread.start()
        return play_command

    def collect_result(self,result_name):
        self.rec_thread = multiprocessing.Process(target=self.record_thread, args=(result_name,self.ros_record_thread,))
        self.rec_thread.start()

    def ros_thread(self,aloam_location,launch_profile):
        exec_command = "bash -c 'source {} ; roslaunch lego_loam {}'".format(os.path.join(aloam_location,"devel/setup.bash"),launch_profile)
        self.ros_main_thread = subprocess.Popen(exec_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc_stdout = self.ros_main_thread.communicate()[0].strip() 
        # print(proc_stdout)
        self.ros_main_thread.wait()

    def record_thread(self,result_name,proc_list):
        exec_command = "bash -c 'cd {} ; rosbag record -O {} /aft_mapped_to_init __name:=lol_bag'".format(self.output_location, result_name)
        exec_command = shlex.split(exec_command)
        proc = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc_list.append(proc.pid)
        # self.ros_record_thread.wait()

    def play_thread(self,play_command):
        # self.bag_thread = subprocess.Popen(play_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # res = self.bag_thread.communicate()[0].strip()
        # print(res)
        play_command = shlex.split(play_command)
        self.bag_thread = subprocess.Popen(play_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res = self.bag_thread.communicate()[0].strip()
        print(res)

    def close_collect(self):
        end_command = "bash -c 'rosnode kill /lol_bag'"
        end_command = shlex.split(end_command)
        proc = subprocess.call(end_command)
        time.sleep(5)
        end_command = "bash -c 'rosnode kill -a'"
        end_command = shlex.split(end_command)
        proc = subprocess.call(end_command)
        



        

if __name__ == '__main__':
    a = legoloam_driver(True,["/home/petebai/Downloads/carla-v2.2-t05.bag"],"/home/petebai/Downloads")
    a.launch_ros("/home/petebai/lego_loam")
    a.collect_result("lego_try")
    comm = a.play_bag("/carla/ego_vehicle/lidar")
    print(comm)