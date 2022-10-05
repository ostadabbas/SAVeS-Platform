% plot carla gt pred

% plot carla ground truth
gt_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\carlav2.2\depth_gt\";
seq_len = 1;
% gt_zs = zeros(3922,1);
for i=1:seq_len
    gt1 = load(strcat(gt_loc,sprintf('%06d',i),'.mat')).the_lidar(3,:);
    hist(gt1)
end