function [gt,img] = projection(lidar_data)
vel0 = lidar_data(1:3,:);

% eliminate all y>0 (as not in the camera)
hid_mask = vel0(2,:)<0;
% map z to base footprint for true depth
vel_depth = vel0(3,:);
vel_min = min(vel_depth);vel_max = max(vel_depth);
vel_depth_01 = (vel_depth-vel_min)/(vel_max-vel_min);


new_vel_z = -vel0(2,:);
new_vel_y = vel0(3,:);
new_vel_x = vel0(1,:);
vel0(1,:) = new_vel_x;
vel0(2,:) = new_vel_y;
vel0(3,:) = new_vel_z;
vel0(4,:) = 1;

% matrix for cam0
cam_to_vel0 = [-0.1,0,0.0623,0]';
point_len = length(vel0);
cam_pos = vel0 + repmat(cam_to_vel0,1,point_len);
projection0 = [1888.44515582,0,613.18976514;0,1888.40009491,482.11894092;0,0,1];

in_cam = distortion(cam_pos);
in_cam = projection0*in_cam;

in_cam = in_cam ./ in_cam(3,:);
in_cam = in_cam(1:2,:);

% resolution 1224*1024
rea1 = (0<=in_cam(1,:))&(in_cam(1,:)<=1224);
rea2 = (0<=in_cam(2,:))&(in_cam(2,:)<=1024);
rea = rea1 & rea2 & hid_mask;
x = in_cam(1,:); x=x(rea);
y = in_cam(2,:); y=y(rea);
gt = vel_depth(rea);
img = [x;y;gt];
% scatter3(x,y,ground_truth);
end