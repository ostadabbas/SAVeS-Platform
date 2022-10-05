function pt_array = extract_xyzi(frame_data,pt_step,iloc)
%extract lidar data
    lol = reshape(frame_data.Data,pt_step,[]);
    u8x = lol(1:4,:);f32x = typecast(reshape(u8x,1,[]),'single');
    u8y = lol(5:8,:);f32y = typecast(reshape(u8y,1,[]),'single');
    u8z = lol(9:12,:);f32z = typecast(reshape(u8z,1,[]),'single');
    u8intense = lol(iloc+1:iloc+4,:);f32in = typecast(reshape(u8intense,1,[]),'single');
    demo_lidar_readable = zeros(4,length(f32x));
    demo_lidar_readable(1,:)=f32x;demo_lidar_readable(2,:)=f32y;demo_lidar_readable(3,:)=f32z;demo_lidar_readable(4,:)=f32in;
    pt_array = demo_lidar_readable;
end