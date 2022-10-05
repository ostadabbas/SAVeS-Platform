% bag = rosbag("E:\Migration\LocalProjects\lm-vid2vid\DAC_data_bags\from_teams\ir_rgb_lidar_data\calibration_info\meta\2019-07-26-18-19-21_car_selected.bag");
% bag = rosbag("D:\LocalProjects\lm-vid2vid\carla\output\CARLA_2022-05-30-12-48-41.bag");
% gt_bag0 = rosbag("D:\LocalProjects\lm-vid2vid\carla\output\campus_small_dataset.bag");
% gt_bag = rosbag("D:\LocalProjects\lm-vid2vid\carla\output\CAR_LIG_RENAME_2022-06-03-11-38-46.bag");
% offroad_bag = rosbag("F:\woodshore_drive_05_05_02\calibration_2022-05-05-18-37-43_0.bag");
% chk_lidar_bag = rosbag("F:\woodshore_drive_05_05_02\calibration_2022-05-05-18-37-43_0.bag");
new_carla_bag = rosbag("D:\OneDrive\OneDrive - Northeastern University\databags\carla-v2.2-t10.bag");
% new_carla_bag = rosbag("D:\OneDrive\OneDrive - Northeastern University\carla-v2.2.bag");
% kitti_bag = rosbag("F:/kitti.bag");
% nu_bag = rosbag("D:\LocalProjects\lm-vid2vid\raw_bags\morning_stereo_rgb_ir_lidar_gps.bag");
% ca_info_temp = select(bag,"Topic","/camera_array/cam0/image_raw");
% ca_info = readMessages(ca_info_temp,'DataFormat','struct');
% img_temp = select(new_carla_bag,"Topic", "/carla/ego_vehicle/rgb_front/image");
% depth_temp = select(new_carla_bag,"Topic", "/carla/ego_vehicle/depth_front/image");
% depth_bag = readMessages(depth_temp,'DataFormat','struct');
img_temp = select(new_carla_bag,"Topic", "/carla/ego_vehicle/rgb_front/image");
img_bag = readMessages(img_temp,'DataFormat','struct');
img_temp2 = select(new_carla_bag,"Topic", "/carla/ego_vehicle/rgb_2/image");
img_bag2 = readMessages(img_temp2,'DataFormat','struct');
% offroad_temp = select(offroad_bag,"topic","/os_cloud_node/points");
% offroad_lidar = readMessages(offroad_temp,'DataFormat','struct');
% cam_info = select(new_carla_bag,"Topic", "/carla/ego_vehicle/odometry");
% cam_bag = readMessages(cam_info,'DataFormat','struct');
% nu_info_temp = select(nu_bag,"Topic","/imu/imu");
% nu_info = readMessages(nu_info_temp,'DataFormat','struct');

% imu_gt_temp = select(gt_bag0,'Topic',"/imu_correct");
% imu_gt = readMessages(imu_gt_temp,'DataFormat','struct');
% carla_imu_temp = select(new_carla_bag,'Topic','/carla/ego_vehicle/imu');
% carla_imu = readMessages(carla_imu_temp,'DataFormat','struct');
% imu_gt1 = select(gt_bag,'Topic',"/points_raw");
% imu_gt01 = readMessages(imu_gt1,'DataFormat','struct');
radar = select(new_carla_bag,'Topic','/carla/ego_vehicle/lidar');
radar0 = readMessages(radar,'DataFormat','struct');

% bSel = select(nu_bag,'Topic','/camera_array/cam0/camera_info');
% msgStructs = readMessages(bSel,'DataFormat','struct');
% bSel = select(new_carla_bag,'Topic','/carla/ego_vehicle/rgb_front/camera_info');
% msgStructs = readMessages(bSel,'DataFormat','struct');
% fig_1d = msgStructs{1}.Data;
% r = reshape(fig_1d,msgStructs{1}.Width,msgStructs{1}.Height);
% % we first extract images from flir_boston
arrs = xtract_img_from_bag(img_bag,"D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\cam0\","png",4);
arrs2 = xtract_img_from_bag(img_bag2,"D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\cam1\","png",4);
% loc = "D:\LocalProjects\lm-vid2vid\proc_bags\";
% bSel = select(bag,'Topic','/flir_boson/image_raw');
% msgStructs = readMessages(bSel,'DataFormat','struct');
% flir_len = 36120;
% img_w = msgStructs{1}.Width;
% img_h = msgStructs{1}.Height;
% for i=1:flir_len
%     fig_1d = msgStructs{i}.Data;
%     r = reshape(fig_1d,img_w,img_h);
%     imwrite(r,strcat(loc,string(i),".jpg"));
% end

% cam0 = select(bag,'Topic','/carla/ego_vehicle/radar_front/cam0/image');
% cam0s = readMessages(cam0,'DataFormat','struct');
% flir_len = 3760;
% img_w = cam0s{1}.Width;
% img_h = cam0s{1}.Height;
% for i=1:flir_len
%     fig_1d = cam0s{i}.Data;
%     temp = reshape(fig_1d,4,[]).';
%     fig = reshape(temp,img_w,img_h,4);
%     r = fig(:,:,3);
%     g = fig(:,:,2);
%     b = fig(:,:,1);
%     new_fig = cat(3,r,g,b);
%     r = imrotate(new_fig,-90);
%     imshow(r)
%     imwrite(r,strcat(loc,"raw0\",sprintf('%06d',i-1),".jpg"));
% end

% bSel = select(nu_bag,'Topic','/camera_array/cam0/image_raw');
% msgStructs = readMessages(bSel,'DataFormat','struct');
% flir_len = 5252;
% img_w = msgStructs{1}.Width;
% img_h = msgStructs{1}.Height;
% for i=1:flir_len
%     fig_1d = msgStructs{i}.Data;
%     temp = reshape(fig_1d,3,[]).';
%     fig = reshape(temp,img_w,img_h,3);
%     r = fig(:,:,3);
%     g = fig(:,:,2);
%     b = fig(:,:,1);
%     new_fig = cat(3,r,g,b);
%     r = imrotate(new_fig,-90);
%     imwrite(r,strcat(loc,"NUance\raw0\",string(i),".jpg"));
% end
% timestamps_raw2 = {};
% for i=1:flir_len
%     timestamps_raw2{i} = msgStructs{i}.Header;
% end

% bSel = select(bag,'Topic','/ns1/velodyne_points');
% msgStructs = readMessages(bSel,'DataFormat','struct');

flir_len = length(radar0);
timestamps = strings(flir_len,1);
vel2_raw = {};
for i=1:flir_len
    lol = reshape(radar0{i}.Data,16,[]);
    u8x = lol(1:4,:);f32x = typecast(reshape(u8x,1,[]),'single');
    u8y = lol(5:8,:);f32y = typecast(reshape(u8y,1,[]),'single');
    u8z = lol(9:12,:);f32z = typecast(reshape(u8z,1,[]),'single');
    u8intense = lol(13:16,:);f32in = typecast(reshape(u8intense,1,[]),'single');
%     u8ring = lol(21:22,:);u16ring = typecast(reshape(u8ring,1,[]),'uint16');
    vel1 = zeros(4,length(f32x));
    vel1(1,:)=f32x;vel1(2,:)=f32y;vel1(3,:)=f32z;vel1(4,:)=f32in;
    save(strcat("D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\lidar_raw\",int2str(i),".mat"),"vel1");
    timestamps(i) = strcat(int2str(radar0{i}.Header.Stamp.Sec),sprintf("%09d",radar0{i}.Header.Stamp.Nsec));
end
dest_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\";
fileID = fopen(strcat(dest_loc,'lidar_raw_timestamps.txt'),'w');
formatSpec = '%s\n';
for i=1:flir_len
    fprintf(fileID,formatSpec,timestamps(i));
end
fclose(fileID);

% validate which image is usable (ridar time = img time)
% do_loop = min(length(cam0s),length(radar0));
% cams_time = zeros(length(cam0s),1); vels_time = zeros(length(radar0),1);
% cams_nano = zeros(length(cam0s),1); vels_nano = zeros(length(radar0),1);
% validate_pics = zeros(length(cam0s),1);
% for i=1:length(cam0s)
%     cams_time(i) = cam0s{i}.Header.Stamp.Sec;
%     cams_nano(i) = cam0s{i}.Header.Stamp.Nsec;
% end
% for i=1:length(radar0)
%     vels_time(i) = radar0{i}.Header.Stamp.Sec;
%     vels_nano(i) = radar0{i}.Header.Stamp.Nsec;
% end
% for i=1:do_loop
%     idxs = find(vels_time==cams_time(i));
%     if isempty(idxs)
%         continue
%     end
%     look_in = vels_nano(idxs); target = cams_nano(i);
%     temp = abs(target-look_in);
%     closest = look_in(temp == min(temp));
%     validate_pics(i) = idxs(look_in==closest(1));
% end
% writematrix(validate_pics,'D:\LocalProjects\lm-vid2vid\proc_bags\hanu_dataset_cv_ready\gt_loc.csv');
% pic_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\raw1\";
% vel_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\vels\";
% sav_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\hanu_dataset_cv_ready\imgs\";
% vel_save_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\hanu_dataset_cv_ready\gts\";
% % pic_num = length(cam0s);
% validate_pics = table2array(gtloc)';
% pic_num = length(validate_pics);
% for i=1:pic_num
% %     x1 = imread(strcat(pic_loc,int2str(i),".jpg"));
% %     x1 = fix_img_distortion(x1);
% %     imwrite(x1,strcat(sav_loc,sprintf('%06d',i-1),".jpg"));
%     v1 = load(strcat(vel_loc,string(validate_pics(i)),".mat")).vel1;
%     [gt,img] = projection(v1);
%     save(strcat(vel_save_loc,sprintf('%06d',i-1),'.mat'),"img",'-mat');
% end




