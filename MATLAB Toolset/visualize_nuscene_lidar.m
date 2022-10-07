% this script visualize NUSCENES Lidar calibration results
img_loc = "D:\LocalProjects\lm-vid2vid\nuscenes\nuscene_lidar_depth_to_camera_image\nuscene_data\samples\CAM_FRONT";
lidar_loc = "D:\LocalProjects\lm-vid2vid\nuscenes\nuscene_lidar_depth_to_camera_image\nuscene_lidar_2d_depth";
output_loc = "D:\LocalProjects\lm-vid2vid\nuscenes\01\";

if ~exist(strcat(output_loc,"\depthmap\"), 'dir')
       mkdir(strcat(output_loc,"\depthmap\"))
end
if ~exist(strcat(output_loc,"\cam\"), 'dir')
       mkdir(strcat(output_loc,"\cam\"))
end

listing = dir(img_loc);
lid_listing = dir(lidar_loc);
img_len = length(listing);
lid_len = length(lid_listing);
if img_len ~= lid_len
    err = "LIDAR AND IMAGE NUMBER NOT MATCH"
end
ct = 0;
min_val = 10;
for i=1:img_len
    if listing(i,:).isdir ~= 1
        i_res = split(listing(i,:).name,"__");
        i_timestamp = split(i_res(3),'.');
        i_timestamp = cell2mat(i_timestamp(1));
        i_prefix = cell2mat(i_res(1));
        l_res = split(lid_listing(i,:).name,"__");
        l_timestamp = split(l_res(3),'.');
        l_timestamp = cell2mat(l_timestamp(1));
        l_prefix = cell2mat(l_res(1));
        assert(strcmp(i_prefix, l_prefix));
        assert(strcmp(i_timestamp, l_timestamp));
        % now we import and re-orginaze lidar file
        lidar_layer = imread(strcat(lidar_loc,'\',lid_listing(i,:).name));
        [rows,cols,v] = find(lidar_layer);
        rows = rows(v>min_val);
        cols = cols(v>min_val);
        v = v(v>min_val);
        lidar_arr = [rows,cols,v];
        img_w = length(lidar_layer(1,:));
        img_h = length(lidar_layer(:,1));
        output = gen_depthmap_func(img_h,img_w,lidar_arr);
        imwrite(output,strcat(output_loc,"\depthmap\",sprintf('%06d',ct),'.png'))
        % since nuscene uses jpg, we need to convert to png
        a = imread(strcat(listing(i,:).folder,'\',listing(i,:).name));
        imwrite(a,strcat(output_loc,'\cam\',sprintf('%06d',ct),'.png'));
%         copyfile strcat(listing(i,:).folder,'\',listing(i,:).name) strcat(output_loc,'\cam\',sprintf('%06d',ct),'.png')
        ct = ct+1;
    end
end

% load seamount;

% imshow(lidar_layer,Colormap=hot)
imshow(img_layer)
hold on
scatter(cols,rows,7,v,"filled")