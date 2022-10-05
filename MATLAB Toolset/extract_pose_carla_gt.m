% this script extracts kitti-style trajectory ground truth from carla
% databag

% new_carla_bag = rosbag("D:\LocalProjects\lm-vid2vid\carla-loopv1.bag");
% cam_info = select(new_carla_bag,"Topic", "/carla/ego_vehicle/odometry");
pth = "D:\OneDrive\OneDrive - Northeastern University\databags\";
new_carla_bag = rosbag(strcat(pth,"carla-v2.2-t10.bag"));
cam_info = select(new_carla_bag,"Topic", "/carla/ego_vehicle/odometry");
cam_bag = readMessages(cam_info,'DataFormat','struct');
pth = "D:\LocalProjects\lm-vid2vid\orb-eval\carla_run2\orbslam3\";
% 
% extracts time from bag corresponding to each line in pose
% note that in carla its cam_bag{i}.Pose.Pose, in A-LOAM is
% cam_bag{last}.Poses(i).(Header|Pose)

topic_input = cam_bag;
ts = extract_time_from_topic(cam_bag,pth,"gt_carla_pose_timestamps.txt");

% to-do: swith from world to car spawn as 0 0
new_orig_pt = [topic_input{1}.Pose.Pose.Position.X, topic_input{1}.Pose.Pose.Position.Y, topic_input{1}.Pose.Pose.Position.Z];
new_coords = zeros(3,length(cam_bag));
new_coords_3 = zeros(3,length(cam_bag));

for i=1:length(cam_bag)
    new_coords(1,i) = topic_input{i}.Pose.Pose.Position.X;
    new_coords(2,i) = topic_input{i}.Pose.Pose.Position.Y;
    new_coords(3,i) = topic_input{i}.Pose.Pose.Position.Z;
end
miner = repmat(new_orig_pt.',1,length(cam_bag));
new_coords_2 = new_coords - miner;
save(strcat(pth,"carla_gt_pos.mat"),"new_coords_2","-mat");

% the following process is fixed and should not change
new_coords_3(1,:) = new_coords_2(1,:);
new_coords_3(2,:) = new_coords_2(3,:);
new_coords_3(3,:) = new_coords_2(2,:);

% to-do: extract coords and convert to roll pitch yaw
quaternion_i = zeros(length(cam_bag),4);
qs = zeros(length(cam_bag),1);
for i=1:length(cam_bag)
    quaternion_i(i,1) = topic_input{i}.Pose.Pose.Orientation.W;
    quaternion_i(i,2) = topic_input{i}.Pose.Pose.Orientation.X;
    quaternion_i(i,3) = topic_input{i}.Pose.Pose.Orientation.Y;
    quaternion_i(i,4) = topic_input{i}.Pose.Pose.Orientation.Z;
end
% to-do: switch from rpy to rotation matrix
[yaw, pitch, roll] = quat2angle(quaternion_i);
ypr = [yaw, pitch, roll];
% the following code calibrates orentation with initial orientation
% ypr_new = ypr-ypr(1,:);
ypr_new = ypr;
new_quat = angle2quat(ypr_new(:,1),ypr_new(:,2),ypr_new(:,3));
quaternion_i = new_quat;
save(strcat(pth,"carla_gt_quat.mat"),"ypr","-mat");
transform_q = quaternion([0.7071,0,0,0.7071]);
new_rotm = zeros(3,3,length(cam_bag));
transform_mat = [0,-1,0;1,0,0;0,0,1];

quaternion_i = time_match(strcat(pth,"gt_carla_pose_timestamps.txt"),quaternion_i.',strcat(pth,"timestamps.txt"));
quaternion_i = quaternion_i.';

for i=1:length(quaternion_i)
%     temp_q = quaternion(quaternion_i(i,:)) * transform_q;
    temp_q = quaternion(quaternion_i(i,:));
    new_rotm(:,:,i) = quat2rotm(temp_q);
end
% to-do: generate gt file in kitti fashion
% dest_loc = ".\generated\";

% carla might be more than needed

new_coords_3 = time_match(strcat(pth,"gt_carla_pose_timestamps.txt"),new_coords_3,strcat(pth,"timestamps.txt"));

fileID = fopen(strcat(pth,'gt_carla_pose.txt'),'w');
formatSpec = '%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n';
for i=1:length(quaternion_i)
    fprintf(fileID,formatSpec,...
        new_rotm(1,1,i),new_rotm(1,2,i),new_rotm(1,3,i),new_coords_3(1,i),...
        new_rotm(2,1,i),new_rotm(2,2,i),new_rotm(2,3,i),new_coords_3(2,i),...
        new_rotm(3,1,i),new_rotm(3,2,i),new_rotm(3,3,i),new_coords_3(3,i));
end
fclose(fileID);
