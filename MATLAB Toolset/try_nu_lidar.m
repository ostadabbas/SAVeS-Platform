% this script tries to align nu lidar to image

lidar_file_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\nu-morning\";
pic = imread(strcat(lidar_file_loc,"cam1\1580572316124412421.png"));
lidar_data = load(strcat(lidar_file_loc,"lidar_raw\1.mat")).vel1;
lidar_data = lidar_data(1:3,:).';
ptCloudIn = pointCloud(lidar_data(:,1:3));
img_h = 1024;img_w = 1224;

focalLength = [1888.44515582 1888.40009491];
principalPoint = [613.18976514 482.11894092];
imageSize = [img_h,img_w];
intrinsics = cameraIntrinsics(focalLength,principalPoint,imageSize);

% trans_matrix = [-0.10,-0.0623,0.0];
trans_matrix = [0,0,0.0];
rotation_matrix = [1,0,0;0,0,-1;0,1,0]*[0,0,-1;0,1,0;1,0,0];
tform = rigid3d(rotation_matrix,trans_matrix);

[imPts,inds] = projectLidarPointsOnImage(ptCloudIn,intrinsics,tform);
vert_dist = lidar_data(:,3);
x_dist = lidar_data(:,1); y_dist = lidar_data(:,2);
vert_dist_sel = vert_dist(inds);
x_dist_sel = x_dist(inds);y_dist_sel = y_dist(inds);
z = sqrt(x_dist_sel.^2+y_dist_sel.^2+vert_dist_sel.^2);
% img = [imPts,z];

col = floor((z-min(z))/(max(z)-min(z))*256);
load seamount
figure
imshow(pic)
hold on
scatter(imPts(:,1),imPts(:,2),3,col);
hold off
