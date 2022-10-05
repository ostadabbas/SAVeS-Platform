vel_count = 3922;
vel_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\lidar_raw\";
img_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\carlav2.2-t05\cam0\";
vel_save_loc = "D:\LocalProjects\lm-vid2vid\proc_bags\valid_bags\carlav2.2-t10\depth_gt\";
% for i=1:vel_count
%     v1 = load(strcat(vel_loc,string(i),".mat")).vel1;
%     the_lidar = carla_lidar_to_cam(v1,90,1224,1024);
%     scatter3(the_lidar(1,:),the_lidar(2,:),the_lidar(3,:))
% end

% N = 100;
% data = randn(N,3) * 40;
% 
% h = scatter3(data(:,1),data(:,2),data(:,3));
% for ii = 1:500
%    data = data + randn(N,3);
%    set(h,'XData',data(:,1),'YData',data(:,2),'ZData',data(:,3));
%    drawnow
%    pause(1/5)
% end
offest = 0;
% v1 = load(strcat(vel_loc,string(1+offest),".mat")).vel1;
% scatter3(v1(1,:),v1(2,:),v1(3,:));
% the_lidar = carla_lidar_to_cam(v1,90,800,600);
% h = scatter3(the_lidar(1,:),the_lidar(2,:),the_lidar(3,:));
% 
for ii = 1:vel_count
    v1 = load(strcat(vel_loc,string(ii+offest),".mat")).vel1;
%     p1 = imread(strcat(img_loc,string(ii),".jpg"));
    the_lidar = carla_lidar_to_cam_v2(v1,90,800,600);
    save(strcat(vel_save_loc,sprintf('%06d',ii-1),'.mat'),"the_lidar",'-mat');
% %     figure; % add this line before imshow()
% %     imshow(p1);
% %     hold on
% %     scatter(the_lidar(1,:),the_lidar(2,:),3,the_lidar(3,:),'fill');
% %     hold off;
% %    h = scatter3(the_lidar(1,:),the_lidar(2,:),the_lidar(3,:));
% %    set(h,'XData',the_lidar(1,:),'YData',the_lidar(2,:),'ZData',the_lidar(3,:));
% %    drawnow
end