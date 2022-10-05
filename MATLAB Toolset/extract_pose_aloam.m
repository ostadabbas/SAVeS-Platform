% this script extracts kitti-style trajectory prediction from A-LOAM

% new_carla_bag = rosbag("D:\LocalProjects\lm-vid2vid\carla-loopv1.bag");
% cam_info = select(new_carla_bag,"Topic", "/carla/ego_vehicle/odometry");
pth = "D:\LocalProjects\lm-vid2vid\orb-eval\kitti_run3\aloam\";
new_carla_bag = rosbag(strcat(pth,"kitti_0034.bag"));
cam_info = select(new_carla_bag,"Topic", "/aft_mapped_path");
cam_bag = readMessages(cam_info,'DataFormat','struct');
% 
% extracts time from bag corresponding to each line in pose
% note that in carla its cam_bag{i}.Pose.Pose, in A-LOAM is
% cam_bag{last}.Poses(i).(Header|Pose)
topic_input = cam_bag{length(cam_bag)}.Poses;
ts = extract_time_from_topic(cam_bag,pth,"aloam_kitti_pose_timestamps.txt");

% to-do: swith from world to car spawn as 0 0
new_orig_pt = [topic_input(1).Pose.Position.X, topic_input(1).Pose.Position.Y, topic_input(1).Pose.Position.Z];
new_coords = zeros(3,length(cam_bag));
new_coords_3 = zeros(3,length(cam_bag));

for i=1:length(cam_bag)
    new_coords(1,i) = topic_input(i).Pose.Position.X;
    new_coords(2,i) = topic_input(i).Pose.Position.Y;
    new_coords(3,i) = topic_input(i).Pose.Position.Z;
end
miner = repmat(new_orig_pt.',1,length(cam_bag));
new_coords_2 = new_coords - miner;
save(strcat(pth,"aloam_og_pos.mat"),"new_coords_2","-mat");

% note that for aloam-kitti
% new_coords_3(1,:) = -new_coords_2(2,:);
% new_coords_3(2,:) = -new_coords_2(3,:);
% new_coords_3(3,:) = new_coords_2(1,:);

% while in aloam-carla
new_coords_3(1,:) = -new_coords_2(2,:);
new_coords_3(2,:) = -new_coords_2(3,:);
new_coords_3(3,:) = new_coords_2(1,:);

% to-do: extract coords and convert to roll pitch yaw
quaternion_i = zeros(length(cam_bag),4);
qs = zeros(length(cam_bag),1);
for i=1:length(cam_bag)
    quaternion_i(i,1) = topic_input(i).Pose.Orientation.W;
    quaternion_i(i,2) = topic_input(i).Pose.Orientation.X;
    quaternion_i(i,3) = topic_input(i).Pose.Orientation.Y;
    quaternion_i(i,4) = topic_input(i).Pose.Orientation.Z;
end
% to-do: switch from rpy to rotation matrix
[yaw, pitch, roll] = quat2angle(quaternion_i);
ypr = [yaw, pitch, roll];
save(strcat(pth,"aloam_og_quat.mat"),"ypr","-mat");
transform_q = quaternion([0.7071,0,0,0.7071]);
rotmZYX = quat2rotm(quaternion_i);
new_rotm = zeros(3,3,length(cam_bag));
transform_mat = [0,-1,0;1,0,0;0,0,1];

% its worth noting that you dont need to rotate 90 deg, its gt that needs to
% be processed
for i=1:length(cam_bag)
%     temp_q = quaternion(quaternion_i(i,:)) * transform_q;
    temp_q = quaternion(quaternion_i(i,:));
    new_rotm(:,:,i) = quat2rotm(temp_q);
end
% to-do: generate gt file in kitti fashion
% dest_loc = ".\generated\";
fileID = fopen(strcat(pth,'aloam_kitti_pose.txt'),'w');
formatSpec = '%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n';
for i=1:length(cam_bag)
    fprintf(fileID,formatSpec,...
        new_rotm(1,1,i),new_rotm(1,2,i),new_rotm(1,3,i),new_coords_3(1,i),...
        new_rotm(2,1,i),new_rotm(2,2,i),new_rotm(2,3,i),new_coords_3(2,i),...
        new_rotm(3,1,i),new_rotm(3,2,i),new_rotm(3,3,i),new_coords_3(3,i));
end
fclose(fileID);

% the following codes calculates ATE & RPE, be sure to run read_kitti_gt first
% and then toggle eval part!
do_eval = false;
if do_eval
    gt_loc = strcat(pth,"gt_carla_calibrated.txt");
    gts = load(gt_loc);
    gt_tra = gts(:,[4,8,12]).';
    rot_flat = gts(:,[1:3,5:7,9:11]);
    rotm = zeros(3,3,length(gt_tra));
    for i=1:length(gt_tra)
        rotm(1,:,i) = rot_flat(i,1:3);
        rotm(2,:,i) = rot_flat(i,4:6);
        rotm(3,:,i) = rot_flat(i,7:9);
    end
    
    [yaw_gt, pitch_gt, roll_gt] = quat2angle(rotm2quat(rotm));
    gt_ypr = [pitch_gt, roll_gt, pitch_gt];
    figure(1); hold on
%     plot(yaw_gt);
%     plot(ypr(:,1));
    plot(abs(cos(yaw_gt)));
    plot(abs(cos(pitch_gt)));
    plot(abs(cos(roll_gt)));
    plot(abs(cos(ypr(:,1))));
    plot(abs(cos(ypr(:,2))));
    plot(abs(cos(ypr(:,3))));
    legend("yaw-gt","pitch-gt","roll-gt","yaw-pred","pitch-pred","roll-pred")
    % aloam-kitti
    % yaw-pred -> pitch-gt;
    % pitch-pred -> roll-gt;
    hold off
    % calc Absolute Translation Error
    diff = new_coords_3 - gt_tra;
    diff_sum_arr = sqrt(sum(diff.*diff,1));
    diff_mean = mean(diff_sum_arr);
    diff_std = std(diff_sum_arr);
    % calc Relative Pose Error
    diffr = abs(cos(gt_ypr)) - abs(cos(ypr));
    diffr_sum_arr = sqrt(sum(diffr.*diffr,2));
    diffr_mean = mean(diffr_sum_arr);
    diffr_std = std(diffr_sum_arr);
end

