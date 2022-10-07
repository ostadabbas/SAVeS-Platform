function img = gen_depthmap_func(target_h,target_w,lidar_depth)
%This function generates 16-bit png depthmap based on xyv arrays
% lidar depth show be a (n-by-3) array with width height and depth gt
img = uint16(zeros(target_h,target_w));
dep = lidar_depth;
for j=1:size(dep,1)
    img(ceil(dep(j,2)),ceil(dep(j,1))) = uint16(dep(j,3)*256);
end
end