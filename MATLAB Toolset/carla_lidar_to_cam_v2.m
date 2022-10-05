function img = carla_lidar_to_cam_v2(points_raw,fov,img_w,img_h)
%This is the updated version of the original lidar to cam function
%   Fixed issue of duplicated dots
%   Improved robustness and speed
points_raw = points_raw.';
ptCloudIn = pointCloud(points_raw(:,1:3));
focal = img_w/(2.0*tan(fov*pi/360.0));
focalLength = [focal,focal];
principalPoint = [img_w / 2.0,img_h / 2.0];
imageSize = [img_h,img_w];
intrinsics = cameraIntrinsics(focalLength,principalPoint,imageSize);
rotation_matrix = [0,1,0;-1,0,0;0,0,1] * [1,0,0;0,0,1;0,-1,0];
trans_matrix = [0,-0.4,-2.0];
tform = rigid3d(rotation_matrix,trans_matrix);
[imPts,inds] = projectLidarPointsOnImage(ptCloudIn,intrinsics,tform);
vert_dist = points_raw(:,3);
x_dist = points_raw(:,1); y_dist = points_raw(:,2);
vert_dist_sel = vert_dist(inds);
x_dist_sel = x_dist(inds);y_dist_sel = y_dist(inds);
z = sqrt(x_dist_sel.^2+y_dist_sel.^2+vert_dist_sel.^2);
img = [imPts,z];
end