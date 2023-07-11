import os
import subprocess
import signal

class ROSDrivers():
    def __init__(self,is_one_bag,bag_files:[],output_location="."):
        """ 
            Does something with a and b
            :param is_one_bag: specify if all data are recorded into same bag
            :param bag_files: if all data in one bag, pass a array with a location string, otherwise, pass as [imu bag location, lidar bag location]
        """
        self.is_valid = False
        if len(bag_files) == 0:
            print("No bag files specified!")
            return
        if is_one_bag:
            bag_loc = bag_files[0]
            if not os.path.exists(bag_loc):
                print("Specified bag file does not exist.")
                return
            self.is_one_bag = True
            self.bag_loc = bag_loc
        else:
            imu_loc = bag_files[0]
            lidar_loc = bag_files[1]
            if not os.path.exists(imu_loc) or not os.path.exists(lidar_loc):
                print("Specified bag file does not exist.")
                return
            self.is_one_bag = False
            self.imu_loc = imu_loc
            self.lidar_loc = lidar_loc
        if not os.path.isdir(output_location):
            os.mkdir(output_location)
            if not os.path.isdir(output_location):
                print("Output folder path is invalid.")
                return
        self.output_location = output_location
        self.is_valid = self.check_ros_install()
    

    #testing noetic
    def check_ros_install(self):
        direct_output = subprocess.check_output('dpkg -l | grep "ros-noetic" | awk \'{print $2}\'', shell=True)
        if len(direct_output) == 0:
            print("ROS noetic is not installed in this system")
            return False
        else:
            return True

    def check_launch(self,loam_location):
        if not os.path.exists(os.path.join(loam_location,"devel","setup.bash")):
            print("The provided location does not contain necessary file!")
            print(os.path.join(loam_location,"devel","setup.bash"))
            return False
        return True

    def launch_ros(self):
        pass

    def play_bag(self):
        pass

    def collect_result(self):
        pass
