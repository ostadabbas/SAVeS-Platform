% this script visualize raw lidar mat file

lidar_path = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\nu-morning\lidar_raw\";
lid_disp_ct = 634;
hold on;legend;
xlabel("x");ylabel("y");zlabel("z");
for i=534:25:lid_disp_ct
    vel = load(strcat(lidar_path,int2str(i),'.mat')).vel1;
    scatter3(vel(1,:),vel(2,:),vel(3,:),'.')
end