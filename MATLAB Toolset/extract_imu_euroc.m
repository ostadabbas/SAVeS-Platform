% this scripts extracts imu data from carla to EuRoC format

new_carla_bag = rosbag("D:\LocalProjects\lm-vid2vid\carla-loopv1.bag");
imu_info_temp = select(new_carla_bag,"Topic", "/carla/ego_vehicle/imu");
imu_info = readMessages(imu_info_temp,'DataFormat','struct');
imu_length = length(imu_info);
linear_acc = zeros(imu_length,3);
ang_vel = zeros(imu_length,3);
timestamp = strings(imu_length,1);
for i=1:imu_length
    linear_acc(i,1) = imu_info{i}.LinearAcceleration.Z;
    linear_acc(i,2) = -imu_info{i}.LinearAcceleration.Y;
    linear_acc(i,3) = imu_info{i}.LinearAcceleration.X;
    ang_vel(i,1) = imu_info{i}.AngularVelocity.Z;
    ang_vel(i,2) = -imu_info{i}.AngularVelocity.Y;
    ang_vel(i,3) = imu_info{i}.AngularVelocity.X;
    timestamp(i) = strcat(int2str(imu_info{i}.Header.Stamp.Sec),sprintf("%09d",imu_info{i}.Header.Stamp.Nsec));
end

dest_loc = ".\generated\";
fileID = fopen(strcat(dest_loc,'carla_imu.csv'),'w');
formatSpec = '%s,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f\n';
header = ["#timestamp [ns]","w_RS_S_x [rad s^-1]","w_RS_S_y [rad s^-1]","w_RS_S_z [rad s^-1]","a_RS_S_x [m s^-2]","a_RS_S_y [m s^-2]","a_RS_S_z [m s^-2]"
];
fprintf(fileID,'%s,%s,%s,%s,%s,%s,%s\n',header(1),header(2),header(3),header(4),header(5),header(6),header(7));
for i=1:length(imu_info)
    fprintf(fileID,formatSpec,...
        timestamp(i),...
        ang_vel(i,1),ang_vel(i,2),ang_vel(3),...
        linear_acc(i,1),linear_acc(i,2),linear_acc(i,3));
end
fclose(fileID);