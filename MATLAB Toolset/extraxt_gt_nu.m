% This script fuses imu and gps data from NUance databag and output into
% kitti ground truth file format (as ground truth for odemenery, 3x3 rotation matrix + 3 translation)

% nu_bag = rosbag("D:\LocalProjects\lm-vid2vid\raw_bags\morning_stereo_rgb_ir_lidar_gps.bag");
% imu_temp_info = select(nu_bag,"Topic", "/imu/imu");
% imu_info = readMessages(imu_temp_info,'DataFormat','struct');
% extract rotation quat and timestamp
imu_length = length(imu_info);
imu_quat = zeros(imu_length,4);
imu_times = zeros(imu_length,2);
imu_accel = zeros(imu_length,3);
imu_gyro = zeros(imu_length,3);
for i=1:imu_length
    imu_quat(i,2) = imu_info{i}.Orientation.X;
    imu_quat(i,3) = imu_info{i}.Orientation.Y;
    imu_quat(i,4) = imu_info{i}.Orientation.Z;
    imu_quat(i,1) = imu_info{i}.Orientation.W;
    imu_times(i,1) = imu_info{i}.Header.Stamp.Sec;
    imu_times(i,2) = imu_info{i}.Header.Stamp.Nsec;
    imu_accel(i,1) = imu_info{i}.LinearAcceleration.X;
    imu_accel(i,2) = imu_info{i}.LinearAcceleration.Y;
    imu_accel(i,3) = imu_info{i}.LinearAcceleration.Z+9.8;
    imu_gyro(i,1) = imu_info{i}.AngularVelocity.X;
    imu_gyro(i,2) = imu_info{i}.AngularVelocity.Y;
    imu_gyro(i,3) = imu_info{i}.AngularVelocity.Z+0.02;
end
% obtain gps data
% gps_temp_info = select(nu_bag,"Topic","/vehicle/gps/fix");
% gps_info = readMessages(gps_temp_info,'DataFormat','struct');
gps_length = length(gps_info);
gps_xyz = zeros(gps_length,3);
gps_time = zeros(gps_length,2);

for i=1:gps_length
    gps_xyz(i,1) = gps_info{i}.Latitude;
    gps_xyz(i,2) = gps_info{i}.Longitude;
    gps_xyz(i,3) = gps_info{i}.Altitude;
    gps_time(i,1) = gps_info{i}.Header.Stamp.Sec;
    gps_time(i,2) = gps_info{i}.Header.Stamp.Nsec;
end

imuFs = 100;
gpsFs = 1;
numsamples = 600;
localOrigin = [42.3488, -71.0857, 6.0];
% localOrigin = [0,0,0];
estPosition = zeros(numsamples,3);
estOrientation = quaternion.zeros(numsamples,1);

gndFusion = insfilterNonholonomic('ReferenceFrame', 'ENU', ...
    'IMUSampleRate', imuFs, ...
    'ReferenceLocation', localOrigin, ...
    'DecimationFactor', 2);
idx = 0;
initAtt = quaternion([imu_info{1}.Orientation.W,imu_info{1}.Orientation.X,imu_info{1}.Orientation.Y,imu_info{1}.Orientation.Z]);

gndFusion.State(1:4) = compact(initAtt).';
gndFusion.State(5:7) = [0,0,0];
gndFusion.State(8:10) = [0,0,0];
gndFusion.State(11:13) = [0,0,0];
gndFusion.State(14:16) = [8.9,0,0];
gndFusion.ZeroVelocityConstraintNoise = 1e-2;
% Process noises
gndFusion.GyroscopeNoise = 4e-6;
gndFusion.GyroscopeBiasNoise = 4e-14;
gndFusion.AccelerometerNoise = 4.8e-2;
gndFusion.AccelerometerBiasNoise = 4e-14;

% extract image time
% img_temp_info = select(nu_bag,"Topic", "/camera_array/cam0/image_raw");
% img_info = readMessages(img_temp_info,'DataFormat','struct');
img_time = zeros(length(img_info),2);
for i=1:length(img_info)
    img_time(i,1) = img_info{i}.Header.Stamp.Sec;
    img_time(i,2) = img_info{i}.Header.Stamp.Nsec;
end

% Initial error covariance
gndFusion.StateCovariance = 1e-9*ones(16);
no_time_match = 0;

for sampleIdx = 1:597
    to_check = imu_times(:,1) == gps_time(sampleIdx,1);
    if sum(to_check) == 0
        continue
    end
    idx = find(to_check==1,1);
    for i=1:sum(to_check)
        predict(gndFusion,imu_accel(idx,:),imu_gyro(idx,:));
        [estPosition(idx,:), estOrientation(idx,:)] = pose(gndFusion);
        if imu_times(idx,1) ~= gps_time(sampleIdx,1)
            no_time_match = no_time_match + 1;
        end
        idx = idx + 1;
    end
    fusegps(gndFusion,gps_xyz(sampleIdx,:),reshape(gps_info{sampleIdx}.PositionCovariance,3,3));
end
% figure;
% scatter3(estPosition(:,1),estPosition(:,2),estPosition(:,3));
% figure;
% scatter3(gps_xyz(:,1),gps_xyz(:,2),gps_xyz(:,3));

% output the trajectory and camera rotation to kitti file format
output_arr = zeros(length(img_info),3);
for i=1:length(img_info)
    similar_s = find(imu_times(:,1)==img_time(i,1) & abs(estPosition(:,1)-0.0)>=1e-5);
    if isempty(similar_s)
        % try to find the nearest possible non 0 value
        [ix_, min_idx_ix] = min(abs(imu_times(:,1)-img_time(i,1)));
        while abs(estPosition(min_idx_ix,1)-0.0)<=1e-5
            min_idx_ix = min_idx_ix + 1;
        end
        output_arr(i,1:3) = estPosition(min_idx_ix,:);
        output_arr(i,4) = min_idx_ix;
        continue
    end
    selected = imu_times(similar_s,2);
    [the_min, min_idx] = min(abs(selected-img_time(i,1)));
    output_arr(i,1:3) = estPosition(similar_s(min_idx),:);
    output_arr(i,4) = similar_s(min_idx);
end

% convert quat to rotation matrix
new_rotm = quat2rotm(estOrientation(output_arr(:,4)));

dest_loc = ".\generated\";
fileID = fopen(strcat(dest_loc,'gt_nu.txt'),'w');
formatSpec = '%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n';
for i=1:length(img_info)
    fprintf(fileID,formatSpec,...
        new_rotm(1,1,i),new_rotm(1,2,i),new_rotm(1,3,i),output_arr(i,1),...
        new_rotm(2,1,i),new_rotm(2,2,i),new_rotm(2,3,i),output_arr(i,2),...
        new_rotm(3,1,i),new_rotm(3,2,i),new_rotm(3,3,i),output_arr(i,3));
end
fclose(fileID);