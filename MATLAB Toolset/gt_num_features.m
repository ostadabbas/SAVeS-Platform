% numerical features of depth truth

% kit_gt_loc = "D:\LocalProjects\lm-vid2vid\dep-eval\2011_09_30_drive_0018_sync\image_02\";
% kit_gt_loc = "D:\LocalProjects\lm-vid2vid\dep-eval\2011_09_30_drive_0018_sync\image_02\";
% kit_pred_loc = "D:\LocalProjects\lm-vid2vid\dep-eval\adabins\ada_kitti_extract_png_18\";
kit_gt_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\depthmap\";
kit_pred_loc = "D:\LocalProjects\lm-vid2vid\dep-eval\adabins\ada_carla_extract_png_10\";
listing = dir(kit_gt_loc);
% plist = dir(kit_pred_loc);
thre = zeros(length(listing),1);
gtre = zeros(length(listing),1);
for i=1:length(listing)
    if listing(i,:).isdir ~= 1  
        a = imread(strcat(kit_gt_loc,listing(i,:).name));
        b = imread(strcat(kit_pred_loc,listing(i,:).name));
        prt = prctile(b(a>0),90,"all");
        thre(i) = mean(b(b>prt));
        gt_prt = prctile(a(a>0),90,"all");
        gtre(i) = mean(a(a>gt_prt));
    end
end
mean(thre/256.0)
mean(gtre/256.0)
