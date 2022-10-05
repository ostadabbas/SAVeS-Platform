lidar_file_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\nu-morning\";
pic = imread(strcat(lidar_file_loc,"cam1\1580572316124412421.png"));
lidar_data = load(strcat(lidar_file_loc,"lidar_raw\1.mat")).vel1;
lidar_data = lidar_data(1:3,:).';
vel1 = lidar_data.';
vel0 = vel1(1:3,:);

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
cam_to_vel0 = [-0.1,0,0.0623,0]';
point_len = length(vel0);
cam_pos = vel0 + repmat(cam_to_vel0,1,point_len);
projection0 = [1888.44515582,0,613.18976514;0,1888.40009491,482.11894092;0,0,1];

unify = [1 0 0 0;0 1 0 0;0 0 1 0];

r = sqrt(cam_pos(1,:).^2+cam_pos(2,:).^2);
theta = atan(r);
thetas = [theta.^2;theta.^4;theta.^6;theta.^8];
ks = [-0.03116674  0.50057031 -7.69105705 41.71286545];
theta_d = theta.*(ks*thetas+1);
coe = repmat(theta_d./r,3,1);

unify = unify*cam_pos;
in_cam = coe.*unify;
in_cam = projection0*in_cam;

in_cam = in_cam ./ in_cam(3,:);
in_cam = in_cam(1:2,:);
% in_cam = in_cam ./ 10; % because different metrics??
rea1 = (0<=in_cam(1,:))&(in_cam(1,:)<=1224);
rea2 = (0<=in_cam(2,:))&(in_cam(2,:)<=1024);
rea = rea1 & rea2 & hid_mask;
x = in_cam(1,:); x=x(rea);
y = in_cam(2,:); y=y(rea);
ground_truth = vel_depth_01(rea);
lidar_img = [x;y];

lidar_file_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\nu-morning\";
pic = imread(strcat(lidar_file_loc,"cam1\1580572316124412421.png"));
z1 = sqrt(x.^2+y.^2+ground_truth.^2);
% img = [imPts,z];

col = floor((z1-min(z1))/(max(z1)-min(z1))*256);
load seamount
figure
imshow(pic)
hold on
scatter(lidar_img(1,:),lidar_img(2,:),3,col);
hold off