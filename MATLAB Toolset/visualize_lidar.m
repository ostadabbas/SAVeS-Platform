% is_init = true;
% if is_init
%     bag_loc = "D:\LocalProjects\lm-vid2vid\carla\output\";
% %     carla_loc = bag_loc+"carla-long-16.bag";
%     carla_loc = bag_loc+"carla-n720.bag";
% %     demo_loc = bag_loc+"2018-05-18-14-49-12_0.bag";
%     demo_loc = "D:\LocalProjects\lm-vid2vid\raw_bags\woodshole_drive_2022-05-05-18-48-57_0.bag";
%     
%     carla_bag = rosbag(carla_loc);
%     demo_bag = rosbag(demo_loc);
%     carla_lidar_temp = select(carla_bag,'Topic',"/carla/ego_vehicle/lidar");
%     carla_lidar = readMessages(carla_lidar_temp,'DataFormat','struct');
% %     demo_lidar_temp = select(demo_bag,'Topic',"/velodyne_points");
%     demo_lidar_temp = select(demo_bag,'Topic',"/ns1/velodyne_points");
%     demo_lidar = readMessages(demo_lidar_temp,'DataFormat','struct');
% end
% figure
% rosPlot(carla_lidar{1})
% figure
% rosPlot(carla_lidar{2})
% figure;
% rosPlot(demo_lidar{1})

seq_name = "003000";
img_path = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\cam0\";
lidar_path = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\depth_gt\";

p_img_path = strcat(img_path,seq_name,".png");
p_lidar_path = strcat(lidar_path,seq_name,".mat");

hl_img = imread(p_img_path);
hl_depth = load(p_lidar_path).the_lidar.';

load seamount
s = 3;
c = hot;
z = hl_depth(3,:);
% hist(z,100)
% assert false
new_z = floor((z-min(z))/(max(z)-min(z))*256);
color_z = zeros(length(new_z),3);
new_depth_x = [];
new_depth_y = [];
new_depth_z = [];

for i=1:length(new_z)
%     if new_z(i) <= 10
%         continue
%     end
%     color_z(i,:) = c(new_z(i),:);
    new_depth_x = [new_depth_x,hl_depth(1,i)];
    new_depth_y = [new_depth_y,hl_depth(2,i)];
    new_depth_z = [new_depth_z,new_z(i)];
end


figure;
imshow(hl_img);
hold on;
scatter(new_depth_x,new_depth_y,s,new_depth_z);