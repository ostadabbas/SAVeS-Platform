% this scripts converts predicted tum format trajectory output from orbslam3 to kitti
% gt format for evaluation

tum_pth = "D:\LocalProjects\lm-vid2vid\orb-eval\carla_run3\orbslam3\CameraTrajectory-carlat10.txt";
dest_loc = "D:\LocalProjects\lm-vid2vid\orb-eval\carla_run3\orbslam3\";
tum = readtable(tum_pth);
% timestamp translation 012 r-xyzw
quat_xyz = tum(:,5:7); quat_w = tum(:,8);
quat = [quat_w,quat_xyz];
quat = table2array(quat);
% [yaw, pitch, roll] = quat2angle(quat);
% ypr = [yaw, pitch, roll];
% new_rotm = zeros(3,3,length(pitch));
new_rotm = quat2rotm(quat);
trans = table2array(tum(:,2:4)).';
tum_time = round(table2array(tum(:,1)),3);
% og_gt_pth = ;
% og_time_pth = "D:\LocalProjects\lm-vid2vid\orb-eval\carla_run1\orbslam3\gt_carla_pose_timestamps.txt";
% og_gt = table2array(readtable(og_gt_pth));
% timex = (round(table2array(readtable(og_time_pth)),3));

% fileID = fopen(strcat(dest_loc,'orb_og_timestamps.txt'),'w');
pred_file = fopen(strcat(dest_loc,'orb_carla_pose.txt'),'w');
formatSpec = '%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n';
timeSpec = "%s";
for i=1:length(tum_time)
%     result = find(timex == tum_time(i));
%     if(isempty(result))
%         continue
%     end
%     fprintf(fileID,formatSpec,);
    fprintf(pred_file,formatSpec,...
        new_rotm(1,1,i),new_rotm(1,2,i),new_rotm(1,3,i),trans(3,i),...
        new_rotm(2,1,i),new_rotm(2,2,i),new_rotm(2,3,i),trans(2,i),...
        new_rotm(3,1,i),new_rotm(3,2,i),new_rotm(3,3,i),trans(1,i) ...
        );
end
fclose(pred_file);