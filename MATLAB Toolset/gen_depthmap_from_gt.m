% this script constructs ground truth depth map based on lidar gt.
img_len = 3922;
target_h = 600; target_w = 800;
ground_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t07\depth_gt\";
if ~exist(strcat(ground_loc,"..\depthmap\"), 'dir')
       mkdir(strcat(ground_loc,"..\depthmap\"))
end
for i=1:img_len
    dep = load(strcat(ground_loc,sprintf('%06d',i-1),'.mat')).the_lidar;
    img = uint16(zeros(target_h,target_w));
    for j=1:size(dep,1)
        img(ceil(dep(j,2)),ceil(dep(j,1))) = uint16(dep(j,3)*256);
    end
    imwrite(img,strcat(ground_loc,"..\depthmap\",sprintf('%06d',i-1),'.png'))
% imshow(img)
end
