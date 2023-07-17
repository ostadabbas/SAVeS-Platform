from geometric.ros_drivers import ROSDrivers
import subprocess
import os
from threading import Thread
import time
import shlex

class aloam_driver(ROSDrivers):
    def launch_ros(self,loam_location, launch_profile="aloam_velodyne_VLP_16.launch"):
        '''
        :param launch_profile: choose from aloam_velodyne_VLP_16.launch (default) or aloam_velodyne_HDL_64.launch
        '''
        if not os.path.isdir(os.path.join(loam_location,"devel")):
            print("The provided location does not contain necessary file!")
        self.new_thread = Thread(target=self.ros_thread,args=(loam_location,launch_profile))
        self.new_thread.start()
        
    def play_bag(self,lidar_topic,do_clock=False):
        lidar_loc = self.bag_loc if self.is_one_bag else self.lidar_loc
        play_command = "rosbag play {} {}:=/velodyne_points".format(lidar_loc,lidar_topic)
        # the threading has some issues, will currently return command to execute
        self.play_bag_thread = Thread(target=self.play_thread,args=(play_command,))
        self.play_bag_thread.start()
        return play_command

    def collect_result(self,result_name):
        self.rec_thread = Thread(target=self.record_thread,args=(result_name,))
        self.rec_thread.start()

    def ros_thread(self,loam_location,launch_profile):
        exec_command = "bash -c 'source {} ; roslaunch aloam_velodyne {}'".format(os.path.join(loam_location,"devel/setup.bash"),launch_profile)
        self.ros_main_thread = subprocess.Popen(exec_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc_stdout = self.ros_main_thread.communicate()[0].strip() 
        print(proc_stdout)
        # self.ros_main_thread.wait()

    def record_thread(self,result_name):
        exec_command = "bash -c 'cd {} ; rosbag record -O {} /aft_mapped_path __name:=lol_bag2'".format(self.output_location, result_name)
        exec_command = shlex.split(exec_command)
        self.ros_record_thread = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # self.ros_record_thread.wait()

    def play_thread(self,play_command):
        play_command = shlex.split(play_command)
        self.bag_thread = subprocess.Popen(play_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res = self.bag_thread.communicate()[0].strip()
        print(res)
    
    def close_collect(self):
        end_command = "bash -c 'rosnode kill /lol_bag2'"
        end_command = shlex.split(end_command)
        proc = subprocess.call(end_command)
        time.sleep(5)
        end_command = "bash -c 'rosnode kill -a'"
        end_command = shlex.split(end_command)
        proc = subprocess.call(end_command)
        

if __name__ == '__main__':
    a = aloam_driver(True,["/home/petebai/Downloads/carla-v2.2-t05.bag"],"/home/petebai/Downloads")
    a.launch_ros("/home/petebai/aloam")
    a.collect_result("first_try")
    comm = a.play_bag("/carla/ego_vehicle/lidar")
    print(comm)