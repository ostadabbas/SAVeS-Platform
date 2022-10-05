% this script extracts raw img and lidar data from NUance databags

parent_folder = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\nu-morning\";

% nu_bag = rosbag("D:\LocalProjects\lm-vid2vid\raw_bags\morning_stereo_rgb_ir_lidar_gps.bag");
% img_temp = select(nu_bag,"Topic", "/camera_array/cam0/image_raw");
% img_bag = readMessages(img_temp,'DataFormat','struct');
% img_temp2 = select(nu_bag,"Topic", "/camera_array/cam1/image_raw");
% img_bag2 = readMessages(img_temp2,'DataFormat','struct');
radar = select(nu_bag,'Topic','/ns1/velodyne_points');
radar0 = readMessages(radar,'DataFormat','struct');
% arrs = xtract_img_from_bag(img_bag,strcat(parent_folder,"cam0\"),"png",3);
% arrs2 = xtract_img_from_bag(img_bag2,strcat(parent_folder,"cam1\"),"png",3);
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
    save(strcat(parent_folder,"lidar_raw\",int2str(i),".mat"),"vel1");
    timestamps(i) = strcat(int2str(radar0{i}.Header.Stamp.Sec),sprintf("%09d",radar0{i}.Header.Stamp.Nsec));
end
fileID = fopen(strcat(parent_folder,'lidar_raw_timestamps.txt'),'w');
formatSpec = '%s\n';
for i=1:flir_len
    fprintf(fileID,formatSpec,timestamps(i));
end
fclose(fileID);
