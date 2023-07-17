import bagpy
import os
import argparse
from bagpy import bagreader
import pandas as pd
from scipy.spatial.transform import Rotation as R

class bag_transform():
    def extract_time_from_topic(self,topic_pd,out_loc,out_filename):
        len_topic = topic_pd.shape[0]
        if not os.path.exists(out_loc):
            os.mkdir(out_loc)
            if not os.path.exists(out_loc):
                return False
        with open(os.path.join(out_loc,out_filename),'w') as f:
            nsec_str = topic_pd['header.stamp.nsecs'].apply(lambda num: "{:09d}".format(num))
            sec_str = topic_pd['header.stamp.secs'].apply(lambda num: str(num))
            res = sec_str + nsec_str
            dfAsString = res.to_string(header=False, index=False)
            f.write(dfAsString)

    def custom_xyz(self,x,y,z):
        return (x,y,z)

    def write_to_txt(self,f,rot,xyz):
        panel = "{:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f} {:.9f}\n"
        panel = panel.format(rot[0][0],rot[0][1],rot[0][2],xyz[0], \
                    rot[1][0],rot[1][1],rot[1][2],xyz[1], \
                    rot[2][0],rot[2][1],rot[2][2],xyz[2])
        f.write(panel)

    def extract_from_lego_bag(self,args):
        if not os.path.exists(args.bag_file):
            return False
        b = bagreader(args.bag_file)
        odo_msg = b.message_by_topic('/aft_mapped_to_init')
        df_odo = pd.read_csv(odo_msg)
        # print(df_odo.dtypes)
        self.extract_time_from_topic(df_odo,args.output_location,"{}_{}_timestamps.txt".format(args.model,args.datasets))
        matters = df_odo[['pose.pose.orientation.x','pose.pose.orientation.y',\
                                'pose.pose.orientation.z','pose.pose.orientation.w',\
                'pose.pose.position.x','pose.pose.position.y','pose.pose.position.z']]
        f = open(os.path.join(args.output_location,"{}_{}_traj.txt".format(args.model,args.datasets)),'w')
        for idx, val in matters.iterrows():
            # print(idx,val)
            quat = [val['pose.pose.orientation.x'],val['pose.pose.orientation.y'],\
                val['pose.pose.orientation.z'],val['pose.pose.orientation.w']]
            r = R.from_quat(quat).as_matrix()
            get_xyz = self.custom_xyz(val['pose.pose.position.x'],val['pose.pose.position.y'],val['pose.pose.position.z'])
            self.write_to_txt(f,r,get_xyz)
        f.close()

    def extract_from_aloam_bag(self,args):
        if not os.path.exists(args.bag_file):
            return False
        b = bagreader(args.bag_file)
        odo_msg = b.message_by_topic('/aft_mapped_path')
        df_odo = pd.read_csv(odo_msg)['poses'].iloc[-1]
        odo_split = df_odo.split('\n')
        odo_split.pop(0)
        secs = []
        nsecs = []
        px = []
        py = []
        pz = []
        qx = []
        qy = []
        qz = []
        qw = []
        for idx, entry in enumerate(odo_split):
            shift = idx % 15
            # print(entry)
            if shift == 2:
                secs.append(int(entry[10:]))
            elif shift == 3:
                nsecs.append(int(entry[11:]))
            elif shift == 7:
                px.append(float(entry[7:]))
            elif shift == 8:
                py.append(float(entry[7:]))
            elif shift == 9:
                pz.append(float(entry[7:]))
            elif shift == 11:
                qx.append(float(entry[7:]))
            elif shift == 12:
                qy.append(float(entry[7:]))
            elif shift == 13:
                qz.append(float(entry[7:]))
            elif shift == 14:
                temp = entry[7:].split(',')
                qw.append(float(temp[0][:-1]))
        stime_odo = pd.DataFrame(secs,columns=['header.stamp.secs']).astype(int)
        ns_time_odo = pd.DataFrame(nsecs,columns=['header.stamp.nsecs']).astype(int)
        time_odo = pd.concat([stime_odo,ns_time_odo],axis=1,join='inner')
        self.extract_time_from_topic(time_odo,args.output_location,"{}_{}_timestamps.txt".format(args.model,args.datasets))
        # matters = df_odo[['pose.pose.orientation.x','pose.pose.orientation.y',\
        #                         'pose.pose.orientation.z','pose.pose.orientation.w',\
        #         'pose.pose.position.x','pose.pose.position.y','pose.pose.position.z']]
        f = open(os.path.join(args.output_location,"{}_{}_traj.txt".format(args.model,args.datasets)),'w')
        for idx in range(len(px)):
            quat = [qx[idx],qy[idx],qz[idx],qw[idx]]
            r = R.from_quat(quat).as_matrix()
            get_xyz = self.custom_xyz(px[idx],py[idx],pz[idx])
            self.write_to_txt(f,r,get_xyz)
        f.close()     

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    bt = bag_transform()
    parser.add_argument('-b','--bag-file',dest='bag_file',help="the bag file that contains extraction topic")
    parser.add_argument('-m','--model',help="the model used to produce the result, either aloam or legoloam")
    parser.add_argument('-d','--datasets',help="choose from carla kitti and nuscenes")
    parser.add_argument('-o','--output_location',default='.',help="output location of extracted trajectory, defaults to current folder")
    args = parser.parse_args()
    if args.model == "aloam":
        bt.extract_from_aloam_bag(args)
    elif args.model == "legoloam":
        bt.extract_from_lego_bag(args)
