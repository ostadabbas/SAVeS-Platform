import os
import subprocess
from threading import Thread
import time
import shutil

class orb_driver:
    def __init__(self,orb_location,yaml_location):
        '''
        Note the driver only support stereo setup
        '''
        self.model_ready = True
        self.orb_location = orb_location
        check_stereo_path = os.path.join(orb_location,'Examples','Stereo','stereo_euroc')
        self.check_voc_path = os.path.join(orb_location,'Vocabulary','ORBvoc.txt')
        if not (os.path.exists(check_stereo_path) and os.path.exists(self.check_voc_path)):
            print("ORBSLAM3 is not properly configured")
            self.model_ready = False
            return
        if not os.path.exists(yaml_location):
            print("YAML file not found!")
            self.model_ready = False
            return
        self.yaml = yaml_location
    
    def set_dataset(self,cam_loc,timestamp_loc):
        # check len(cam0)==len(cam1)==len(timestamp)
        cam0_path = os.path.join(cam_loc,'mav0','cam0','data')
        cam1_path = os.path.join(cam_loc,'mav0','cam1','data')
        cam0_content = list(os.listdir(cam0_path))
        cam1_content = list(os.listdir(cam1_path))
        for idx,name in enumerate(cam0_content):
            cam0_content[idx] = int(name[:-4])
        for idx,name in enumerate(cam1_content):
            cam1_content[idx] = int(name[:-4])
        cam0_content.sort()
        cam1_content.sort()
        if not os.path.exists(timestamp_loc):
            return "Timestamp file not found!"
        self.timestamp = timestamp_loc
        with open(timestamp_loc,'r') as f:
            times_content = f.readlines()
        if(len(cam0_content) != len(cam1_content)):
            return "Stereo Images sequence length not equal!"
        if(len(cam0_content) != len(times_content)):
            return "Timestamp file length not match with images!"
        for idx,name in enumerate(cam0_content):
            if(name != cam1_content[idx]):
                return "image {} and {} not match".format(name,cam1_content[idx])
            if(str(name) != times_content[idx][:-1]):
                return "{} and timestamp {} not match".format(name[:-4],times_content[idx][:-1])
        self.cam_loc = cam_loc
        return True

    def run_orbslam3(self,output_location,filename):
        self.exec_path = os.path.join(self.orb_location,'Examples','Stereo')
        command = "bash -c 'cd {}; ./stereo_euroc {} {} {} {}'".format(self.exec_path,self.check_voc_path,self.yaml,self.cam_loc,self.timestamp)
        print("Please wait...")
        if not os.path.isdir(output_location):
            os.mkdir(output_location)
            if not os.path.isdir(output_location):
                print("Output folder path is invalid.")
                return
        self.output_location = output_location
        self.filename = filename + ".txt"
        orb_th = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        orb_th.wait()
        self.copy_to_dest()

    def copy_to_dest(self):
        source_file = os.path.join(self.exec_path,"CameraTrajectory.txt")
        dest_file = os.path.join(self.output_location,self.filename)
        if not os.path.exists(source_file):
            print("No trajectory file detected!")
            return
        res = shutil.copyfile(source_file,dest_file)

if __name__ == '__main__':
    a = orb_driver("/home/petebai/orbslam3/ORB_SLAM3","/home/petebai/orbslam3/ORB_SLAM3/Examples/Stereo/carla2.2.yaml")
    a.set_dataset('/home/petebai/Downloads/carlav2.2-t10_euroc','/home/petebai/Downloads/carlav2.2-t10_euroc/timestamps.txt')
    a.run_orbslam3("/home/petebai/Downloads/saves_output",'orb_test_traj.txt')