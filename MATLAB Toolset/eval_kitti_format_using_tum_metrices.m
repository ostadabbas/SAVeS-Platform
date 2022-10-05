% this script evaluates ate and rpe using 2 same length kitti-style txt
% file
pth = "D:\LocalProjects\lm-vid2vid\orb-eval\carla_run1\orbslam3\";
gt_loc = strcat(pth,"gt_carla_pose.txt");
gts = load(gt_loc);
gt_tra = gts(:,[4,8,12]).';
rot_flat = gts(:,[1:3,5:7,9:11]);
rotm = zeros(3,3,length(gt_tra));
for i=1:length(gt_tra)
    rotm(1,:,i) = rot_flat(i,1:3);
    rotm(2,:,i) = rot_flat(i,4:6);
    rotm(3,:,i) = rot_flat(i,7:9);
end

pred_loc = strcat(pth,"eval_carla_stereo_tum.txt");
preds = load(pred_loc);
pred_tra = preds(:,[4,8,12]).';
pred_rot_flat = preds(:,[1:3,5:7,9:11]);
pred_rotm = zeros(3,3,length(pred_tra));
for i=1:length(pred_tra)
    pred_rotm(1,:,i) = pred_rot_flat(i,1:3);
    pred_rotm(2,:,i) = pred_rot_flat(i,4:6);
    pred_rotm(3,:,i) = pred_rot_flat(i,7:9);
end

[yaw_gt, pitch_gt, roll_gt] = quat2angle(rotm2quat(rotm));
[yaw_pred,pitch_pred,roll_pred] = quat2angle(rotm2quat(pred_rotm));
gt_ypr = [pitch_gt, roll_gt, pitch_gt];
ypr = [pitch_pred,roll_pred,yaw_pred];

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
hold off
% calc Absolute Translation Error
diff = pred_tra - gt_tra;
diff_sum_arr = sqrt(sum(diff.*diff,1));
diff_mean = mean(diff_sum_arr);
diff_std = std(diff_sum_arr);
% calc Relative Pose Error
diffr = abs(cos(gt_ypr)) - abs(cos(ypr));
diffr_sum_arr = sqrt(sum(diffr.*diffr,2));
diffr_mean = mean(diffr_sum_arr);
diffr_std = std(diffr_sum_arr);