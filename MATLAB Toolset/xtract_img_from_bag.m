function ts_arr = xtract_img_from_bag(bag_file,dest_loc,file_type,img_channel)
%extract images from bag and save them to folder
img_seq_len = length(bag_file);
ts_arr = zeros(img_seq_len,1);
fileID = fopen(strcat(dest_loc,"..\",'img_timestamps.txt'),'w');
formatSpec = '%d\n';
img_w = bag_file{1}.Width;
img_h = bag_file{1}.Height;
for i=1:img_seq_len
    fig_1d = bag_file{i}.Data;
    temp = reshape(fig_1d,img_channel,[]).';
    fig = reshape(temp,img_w,img_h,img_channel);
    r = fig(:,:,3);
    g = fig(:,:,2);
    b = fig(:,:,1);
    new_fig = cat(3,r,g,b);
    r = imrotate(new_fig,-90);
    r = flip(r,2);
%     n_timestamp = bag_file{i}.Header.Stamp.Nsec * 1e-6;
%     ns_with_0 = sprintf('%03d',floor(n_timestamp));
%     s_timestamp = strcat(int2str(bag_file{i}.Header.Stamp.Sec),ns_with_0);
    s_timestamp = strcat(int2str(bag_file{i}.Header.Stamp.Sec),sprintf("%09d",bag_file{i}.Header.Stamp.Nsec));
    imwrite(r,strcat(dest_loc,string(s_timestamp),".",file_type));
    ts_arr(i) = string(s_timestamp);
    fprintf(fileID,formatSpec,ts_arr(i));
end
fclose(fileID);
end