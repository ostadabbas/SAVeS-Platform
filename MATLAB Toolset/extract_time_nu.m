% this script extract timestamp from NUance databag and output it into txt
% file, the format is SecNsec

% nu_bag = rosbag("D:\LocalProjects\lm-vid2vid\raw_bags\morning_stereo_rgb_ir_lidar_gps.bag");
% bSel = select(nu_bag,'Topic','/camera_array/cam0/camera_info');
% msgStructs = readMessages(bSel,'DataFormat','struct');
nu_len = length(msgStructs);
timestamps = strings(nu_len,1);

for i=1:nu_len
    timestamps(i) = strcat(int2str(msgStructs{i}.Header.Stamp.Sec),sprintf("%09d",msgStructs{i}.Header.Stamp.Nsec));
end

dest_loc = ".\generated\";
fileID = fopen(strcat(dest_loc,'NUance_timestamps.txt'),'w');
formatSpec = '%s\n';
for i=1:nu_len
    fprintf(fileID,formatSpec,timestamps(i));
end
fclose(fileID);