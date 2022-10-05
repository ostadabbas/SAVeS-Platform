is_init = true;
if is_init
    bag_loc = "D:\LocalProjects\lm-vid2vid\carla\output\";
%     carla_loc = bag_loc+"carla-long-16.bag";
    carla_loc = bag_loc+"carla-modint.bag";
%     demo_loc = bag_loc+"2018-05-18-14-49-12_0.bag";
    demo_loc = "D:\LocalProjects\lm-vid2vid\raw_bags\woodshole_drive_2022-05-05-18-48-57_0.bag";
    
    carla_bag = rosbag(carla_loc);
    demo_bag = rosbag(demo_loc);
    carla_lidar_temp = select(carla_bag,'Topic',"/carla/ego_vehicle/lidar");
    carla_lidar = readMessages(carla_lidar_temp,'DataFormat','struct');
%     demo_lidar_temp = select(demo_bag,'Topic',"/velodyne_points");
    demo_lidar_temp = select(demo_bag,'Topic',"/ns1/velodyne_points");
    demo_lidar = readMessages(demo_lidar_temp,'DataFormat','struct');
end
% extract xyzi in each frame and compare
carla_len = 10295; demo_len = 573;
demo_ifeature = zeros(6,0);
carla_ifeature = zeros(6,0);
demo_xfeature = zeros(6,0);
carla_xfeature = zeros(6,0);
demo_yfeature = zeros(6,0);
carla_yfeature = zeros(6,0);
demo_zfeature = zeros(6,0);
carla_zfeature = zeros(6,0);
demo_dfeature = zeros(6,0);
carla_dfeature = zeros(6,0);
for i=1:demo_len
    demo_readable = extract_xyzi(demo_lidar{i},32,16);
    carla_readable = extract_xyzi(carla_lidar{500+i},16,12);
    carla_x_arr = carla_readable(1,:); carla_y_arr = carla_readable(2,:); carla_z_arr = carla_readable(3,:);
    carla_d_arr = sqrt(carla_x_arr.*carla_x_arr+carla_y_arr.*carla_y_arr+carla_z_arr.*carla_z_arr);
    demo_x_arr = demo_readable(1,:); demo_y_arr = demo_readable(2,:); demo_z_arr = demo_readable(3,:);
    demo_d_arr = sqrt(demo_x_arr.*demo_x_arr+demo_y_arr.*demo_y_arr+demo_z_arr.*demo_z_arr);
    demo_ifeature = cat(2,demo_ifeature,feature_box(demo_readable(4,:)));
    carla_ifeature = cat(2,carla_ifeature,feature_box(carla_readable(4,:)));
    demo_xfeature = cat(2,demo_xfeature,feature_box(demo_readable(1,:)));
    carla_xfeature = cat(2,carla_xfeature,feature_box(carla_readable(1,:)));
    demo_yfeature = cat(2,demo_yfeature,feature_box(demo_readable(2,:)));
    carla_yfeature = cat(2,carla_yfeature,feature_box(carla_readable(2,:))); 
    demo_zfeature = cat(2,demo_zfeature,feature_box(demo_readable(3,:)));
    carla_zfeature = cat(2,carla_zfeature,feature_box(carla_readable(3,:))); 
    demo_dfeature = cat(2,demo_dfeature,feature_box(demo_d_arr));
    carla_dfeature = cat(2,carla_dfeature,feature_box(carla_d_arr)); 
end