% this scrip reads kitti ground truth file and sorts into 2 mat files:
% position and rotation quat

pth = "D:\LocalProjects\lm-vid2vid\orb-eval\kitti_run3\legoloam\";
gt_file_loc = strcat(pth,"02.txt");
gt_arr = load(gt_file_loc);
pos_arr = gt_arr(:,[4,8,12]).';

rot_flat = gt_arr(:,[1:3,5:7,9:11]);

new_rotm = zeros(3,3,length(gt_arr));
for i=1:length(gt_arr)
    new_rotm(1,:,i) = rot_flat(i,1:3);
    new_rotm(2,:,i) = rot_flat(i,4:6);
    new_rotm(3,:,i) = rot_flat(i,7:9);
end

% rot = reshape(rot_flat,3,3,[]);
rot = new_rotm;
[yaw, pitch, roll] = quat2angle(rotm2quat(rot));
% ypr_gt = [yaw, pitch, roll].*(360/pi);
ypr_gt = [yaw, pitch, roll];

% the following code calibrates orentation with initial orientation
% ypr_new = ypr_gt-ypr_gt(1,:);
ypr_new = ypr_gt;
new_quat = angle2quat(ypr_new(:,1),ypr_new(:,2),ypr_new(:,3));
% new_rotm = quat2rotm(new_quat);

% the following code converts kitti timestamp as ros one and writes back to
% file
kit_time_loc = strcat(pth,"kitti_og_times.txt");
kit_time_og = load(kit_time_loc);
new_kit_time = kit_time_og*1e9;
fileID = fopen(strcat(pth,'kitti_ros_time.txt'),'w');
formatSpec = '%09d\n';
for i=1:length(kit_time_og)
    fprintf(fileID,formatSpec,new_kit_time(i));
end
fclose(fileID);

% the following code converts output kitti timestamp to be aligned with
% what we have by subtracting 1st element
kit_time_loc = strcat(pth,"legoloam_kitti_pose_timestamps.txt");
kit_time_og = load(kit_time_loc);
new_kit_time = kit_time_og-kit_time_og(1);
fileID = fopen(strcat(pth,'legoloam_kitti_pose_timestamps_fixed.txt'),'w');
formatSpec = '%09d\n';
for i=1:length(kit_time_og)
    fprintf(fileID,formatSpec,new_kit_time(i));
end
fclose(fileID);

% the following code matches timestamps from kitti and target
aloam_time_loc = strcat(pth,"legoloam_kitti_pose_timestamps_fixed.txt");
new_coords_3 = time_match(strcat(pth,'kitti_ros_time.txt'),pos_arr,aloam_time_loc);

new_quat = time_match(strcat(pth,'kitti_ros_time.txt'),new_quat.',aloam_time_loc).';
new_rotm = quat2rotm(new_quat);

fileID = fopen(strcat(pth,'gt_kitti_calibrated.txt'),'w');
formatSpec = '%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n';
for i=1:length(new_coords_3)
    fprintf(fileID,formatSpec,...
        new_rotm(1,1,i),new_rotm(1,2,i),new_rotm(1,3,i),new_coords_3(1,i),...
        new_rotm(2,1,i),new_rotm(2,2,i),new_rotm(2,3,i),new_coords_3(2,i),...
        new_rotm(3,1,i),new_rotm(3,2,i),new_rotm(3,3,i),new_coords_3(3,i));
end
fclose(fileID);
